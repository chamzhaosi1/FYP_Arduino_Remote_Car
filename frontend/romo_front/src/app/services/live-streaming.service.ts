import { Injectable } from '@angular/core';
import { environment as env} from 'src/environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class LiveStreamingService {

  callSocket?: WebSocket 
  deviceOwnerName?: string
  deviceMacAddress?: string
  otherUser?: string;
  localVideo: any;
  remoteVideo: any;
  userToCall?: any;
  localStream: any;
  remoteStream: any;
  peerConnection: any;
  remoteRTCMessage: any;
  iceCandidatesFromCaller:any = [];
  role: string = "";
  fpsRounded: number = 0;
  getFPSInterval:any

  constructor() { }

  connectWebSocket(deviceOwnerName: string,
    deviceMacAddress: string, 
    localVideo:any, 
    remoteVideo:any,
    role:string,
   ){
    this.deviceOwnerName = deviceOwnerName
    this.deviceMacAddress = deviceMacAddress
    this.localVideo = localVideo
    this.remoteVideo = remoteVideo
    this.role = role;
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

    // if (this.callSocket === undefined){
    this.callSocket = new WebSocket(
      ws_scheme
      + env.websocket.host
      + env.websocket.path
    );
    // }

    this.callSocket.onopen = event => {
      //let's send myName to the socket
      this.callSocket?.send(JSON.stringify({
          type: 'login',
          data: {
              name: this.role === "owner" ? this.deviceOwnerName : this.deviceMacAddress?.replace(/:/g, "_")
          }
      }));

      if (this.role === "owner"){
        this.userToCall = this.role === "owner" ? this.deviceMacAddress?.replace(/:/g, "_") : this.deviceOwnerName;
        this.refreshWebSocket()
      }

      if (this.role === "romo"){
        this.call()
      }
    }

    this.callSocket.onmessage = (e) => {
      let response = JSON.parse(e.data);


      let type = response.type;

        if (type == 'connection') {
            // console.log(response.data.message)
        }

        if (type == 'call_received') {
            // console.log(response);
            this.onNewCall(response.data)
        }

        if (type == 'call_answered') {
            // console.log(response);
            this.onCallAnswered(response.data);
        }

        if (type == 'ICEcandidate') {
            this.onICECandidate(response.data);
        }

        if (type == 'end_session' || type == 'refresh_session') {
            // console.log("end session")
            this.reloadPage();
        }
    }
  }
  
  call(){
    if (this.deviceMacAddress != "" && this.deviceOwnerName !=""){
      // if the role is owner then user to call will be mac address else owner
      // because is romo call user
      this.userToCall = this.role === "owner" ? this.deviceMacAddress?.replace(/:/g, "_") : this.deviceOwnerName;
    }

    this.otherUser = this.deviceOwnerName

    this.beReady()
        .then(bool => {
            this.processCall(this.userToCall!)
        })
  }

  answer(){
    this.beReady()
    .then(bool => {
        this.processAccept();
    })
  }

  beReady(){
    return navigator.mediaDevices.getUserMedia({
      audio: false,
      video: true,

    }).then(stream => {

      this.localStream = stream;
      this.localVideo.srcObject = stream;

      return this.createConnectionAndAddStream()
    })
    .catch(function (e) {
        alert('getUserMedia() error: ' + e.name);
    });
  }

  processCall(userName:string){
    console.log("processCall")
    this.peerConnection.createOffer((sessionDescription:any) => {
      this.peerConnection.setLocalDescription(sessionDescription);
      this.sendCall({
          name:  userName,
          rtcMessage: sessionDescription
      })
    }, (error:any) => {
        console.log("Error");
    });
  }

  processAccept(){
    this.peerConnection.setRemoteDescription(new RTCSessionDescription(this.remoteRTCMessage));
    this.peerConnection.createAnswer((sessionDescription:any) => {
      this.peerConnection.setLocalDescription(sessionDescription);

        if (this.iceCandidatesFromCaller.length > 0) {
            //I am having issues with call not being processed in real world (internet, not local)
            //so I will push iceCandidates I received after the call arrived, push it and, once we accept
            //add it as ice candidate
            //if the offer rtc message contains all thes ICE candidates we can ingore this.
            for (let i = 0; i < this.iceCandidatesFromCaller.length; i++) {
                //
                let candidate = this.iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                  this.peerConnection.addIceCandidate(candidate).then((done:any) => {
                        console.log(done);
                    }).catch((error:any) => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            this.iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        this.answerCall({
            caller: this.otherUser,
            rtcMessage: sessionDescription
        })

    }, (error:any) => {
        console.log("Error");
    })
  }

  onNewCall(data:any){
    this.otherUser = data.caller;
    this.remoteRTCMessage = data.rtcMessage

    if (this.deviceMacAddress != "" && this.deviceOwnerName !=""){
      if (this.otherUser === this.deviceOwnerName || this.otherUser === this.deviceMacAddress?.replace(/:/g, "_")){
        this.answer()
      }
    }
  }

  onCallAnswered(data:any){
    this.remoteRTCMessage = data.rtcMessage
    this.peerConnection.setRemoteDescription(new RTCSessionDescription(this.remoteRTCMessage));
    console.log("Call Started. They Answered");
    // console.log(pc);

    // this.callProgress()
  }

  onICECandidate(data:any){
    // console.log(data);
    console.log("GOT ICE candidate");

    let message = data.rtcMessage

    let candidate = new RTCIceCandidate({
        sdpMLineIndex: message.label,
        candidate: message.candidate
    });

    if (this.peerConnection) {
        console.log("ICE candidate Added");
        this.peerConnection.addIceCandidate(candidate);
    } else {
        console.log("ICE candidate Pushed");
        this.iceCandidatesFromCaller.push(candidate);
    }
  }

  reloadPage(){
    location.reload();
  }

  createConnectionAndAddStream(){
    this.createPeerConnection();
    this.peerConnection.addStream(this.localStream);
    return true;
  }

  createPeerConnection(){
    try {
      this.peerConnection = new RTCPeerConnection(env.pcConfig);
      // this.peerConnection = new RTCPeerConnection();
      // console.log(this.peerConnection)
      // peerConnection = new RTCPeerConnection();
      // this.peerConnection.onicecandidate = this.handleIceCandidate;
      this.peerConnection.addEventListener("icecandidate", (e:any) => this.handleIceCandidate(e))
      this.peerConnection.addEventListener("addstream", (e:any) => this.handleRemoteStreamAdded(e))
      this.peerConnection.addEventListener("removestream", (e:any) => this.handleRemoteStreamRemoved(e));
      // this.peerConnection.onaddstream = this.handleRemoteStreamAdded;
      // this.peerConnection.onremovestream = this.handleRemoteStreamRemoved;
      console.log('Created RTCPeerConnnection');
      return;

    } catch (e:any) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
  }

  sendICEcandidate(data:any) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    this.callSocket?.send(JSON.stringify({
        type: 'ICEcandidate',
        data
    }));
  }

  handleIceCandidate(event:any){
    // console.log('icecandidate event: ', event);
    if (event.candidate) {
      console.log("Local ICE candidate");
      // console.log(event.candidate.candidate);

      // this.sendICEcandidate({
      //     user: this.otherUser,
      //     rtcMessage: {
      //         label: event.candidate.sdpMLineIndex,
      //         id: event.candidate.sdpMid,
      //         candidate: event.candidate.candidate
      //     }
      // })

      let data = {
        user: this.otherUser,
          rtcMessage: {
              label: event.candidate.sdpMLineIndex,
              id: event.candidate.sdpMid,
              candidate: event.candidate.candidate
          }
      }

      // console.log(this.otherUser)

      this.callSocket?.send(JSON.stringify({
        type: 'ICEcandidate',
        data
      }));

      console.log("Send ICE candidate");

    } else {
      console.log('End of candidates.');
      this.countFPS();
    }
  }

  handleRemoteStreamAdded(event:any){
    console.log('Remote stream added.');
    // console.log(event)
    this.remoteStream = event.stream;
    // console.log(this.remoteStream)
    this.remoteVideo.srcObject = this.remoteStream;
  }

  handleRemoteStreamRemoved(event:any){
    console.log('Remote stream removed. Event: ', event);
    this.remoteVideo.srcObject = null;
    this.localVideo.srcObject = null;
  }

  sendCall(data:any) {
    //to send a call
    console.log("Send Call");

    // socket.emit("call", data);
    this.callSocket?.send(JSON.stringify({
        type: 'call',
        data
    })); 
    
      
  }

  answerCall(data:any){
    this.callSocket?.send(JSON.stringify({
      type: 'answer_call',
      data
    }));
    // this.callProgress();
  }

  closeWebSocket(){
    // stop/close the both video stream
    this.localStream.getTracks().forEach((track:any) => track.stop())
    this.remoteStream.getTracks().forEach((track:any) => track.stop())
    console.log("Close Peer Connection")
    this.peerConnection.close()

    // stop/disconnect the websocket
    this.callSocket?.send(JSON.stringify({
      type: 'stopSession',
      data: {
        "client" : this.userToCall
      }
    }));    
    console.log("Close WebSocket")
    this.callSocket?.close()

    // clear the FPS count 
    clearInterval(this.getFPSInterval)
  }

  refreshWebSocket(){
    this.callSocket?.send(JSON.stringify({
      type: 'refreshSession',
      data: {
        "client" : this.userToCall
      }
    }));
  }

  countFPS(){
    let previousFramesReceived = 0;
    let previousTimestamp = 0;

    this.getFPSInterval = setInterval(async () => {
        const stats = await this.peerConnection.getStats();
        let framesReceived = 0;
        let timestamp = 0;
        stats.forEach((report:any) => {
          if (report.type === 'inbound-rtp' && report.mediaType === 'video') {
              framesReceived = report.framesReceived; // total number of full frames that have been received on this RTP stream.
              timestamp = report.timestamp;
          }
        });
        const fps = (framesReceived - previousFramesReceived) / ((timestamp - previousTimestamp) / 1000);
        this.fpsRounded = Math.round(fps);
        // console.log(`Incoming FPS: ${fpsRounded}`);
        previousFramesReceived = framesReceived;
        previousTimestamp = timestamp;
    }, 1000);
  }

  getFPSValue(){
    return this.fpsRounded;
  }
}
