import { Injectable } from '@angular/core';
import { environment as env} from 'src/environments/environment.prod';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FaceRecognizationService {
    pc : any;
    remoteLocalVideo:any;
    remoteLocalStream:any;
    remoteFaceVideo:any;
    sender:any;
    videoType: string = "";
    userName: string = "";
    mac_address: string = "";
    isLoadingShow : Boolean = false;
    fpsRounded: number = 0;
    getFPSInterval:any

    constructor(private http : HttpClient) { } 

    createPeerConnection() {
        // console.log(remoteLocalVideo)
        this.pc = new RTCPeerConnection(env.pcConfig);
        
        // connect audio / video
        this.pc.addEventListener('track', (evt:any) => {
            if (evt.track.kind == 'video'){
                if(this.remoteFaceVideo === ""){
                    this.remoteLocalVideo.srcObject = evt.streams[0];
                }else{
                    this.remoteFaceVideo.srcObject = evt.streams[0];
                }
            }
        });

        this.pc.onicecandidate = this.handleIceCandidate;
    }

    handleIceCandidate(event:any) {
        if (event.candidate) {
            console.log("Local ICE candidate");
        } else {
            console.log('End of candidates.');
        }
    }

    negotiate() {
        return this.pc.createOffer().then((offer:any) => {
            this.pc.setLocalDescription(offer);
            return this.pc
        }).then(() => {
            // wait for ICE gathering to complete
            return new Promise<void>((resolve) => {
                if (this.pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    const checkState = () => {
                        if (this.pc.iceGatheringState === 'complete') {
                            console.log("iceGatheringState is complete")
                            this.pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }
                    this.pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(() => {
            console.log("After iceGatheringState")
            var offer = this.pc.localDescription;

            let data = JSON.stringify({
                        sdp: offer.sdp,
                        type: offer.type,
                        video_transform: this.videoType,
                        userName : this.userName,
                        mac_address : this.mac_address
                    })
            
            console.log("FRM ws call")
            return this.http.post(env.face.host+env.face.live_path, data).subscribe({
                next : (answer:any) => {
                    this.isLoadingShow = false
                    this.countFPS()
                    return this.pc.setRemoteDescription(answer);
                },
                error : (error:any) => {
                    alert(error);
                }
            })
        });
    }

    start(remoteLocalVideo:any, remoteFaceVideo:any, videoType:string, userName:string, mac_address?:string) {

        this.videoType = videoType
        this.remoteLocalVideo = remoteLocalVideo
        this.userName = userName
        this.mac_address = mac_address as string
        this.remoteFaceVideo = remoteFaceVideo
    
        
        this.createPeerConnection();

        var constraints = {
            audio: false,
            video: true
        };

        if (constraints.audio || constraints.video) {
            if (this.videoType === "face_recognition"){
                this.remoteLocalStream = this.remoteLocalVideo.captureStream()
                this.remoteLocalStream.getTracks().forEach((track:any) => {
                    this.sender = this.pc.addTrack(track, this.remoteLocalStream);
                    return this.negotiate();
                });
            }else{
                navigator.mediaDevices.getUserMedia(constraints).then((stream:any) => {
                    this.remoteLocalStream = stream
                    this.remoteLocalStream.getTracks().forEach((track:any) => {
                        this.sender = this.pc.addTrack(track, stream);
                    });
                    return this.negotiate();
                })
            }
        } else {
            this.negotiate();
        }
    }

    stop(){
        setTimeout(() => {
            console.log("Close FRM")
            // close local audio / video
            this.remoteLocalStream.getTracks().forEach((track:any) => track.stop())
            this.pc.removeStream(this.remoteLocalStream)
            this.pc.removeTrack(this.sender);
            // close peer connection
            this.pc.close();
            // clear the FPS count 
            clearInterval(this.getFPSInterval)
        }, 500);
    }

    snapshot(label:any){
        return this.http.post(env.face.host+env.face.capture_path, label, {responseType: 'text'})
    }

    retrieveCap(userName: any){
        return this.http.post(env.face.host+env.face.retrieveCap_path, userName, {responseType: 'blob'})
    }

    retrieveInt(userName: any){
        return this.http.post(env.face.host+env.face.retrieveInt_path, userName)
    }

    countFPS(){
        let previousFramesReceived = 0;
        let previousTimestamp = 0;
    
        this.getFPSInterval = setInterval(async () => {
            const stats = await this.pc.getStats();
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
            // console.log(`Incoming FPS: ${this.fpsRounded}`);
            previousFramesReceived = framesReceived;
            previousTimestamp = timestamp;
        }, 1000);
    }

    getFPSValue(){
        return this.fpsRounded;
    }
}
