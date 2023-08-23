var remoteVideoSecond = document.getElementById('remoteVideo');
var video_internal = document.getElementById("video_internal");
var remoteRTCMessage_internal = null;
var callSocket_internal = null;


// remoteVideoSecond.addEventListener('playing', ()=>{
//     console.log("playing")
// })

// remoteVideoSecond.addEventListener('play', ()=>{
//     console.log("play")
// })

remoteVideoSecond.addEventListener('loadedmetadata', () => {
    // document.getElementById("media_internal").style.display = "block";
    // video_internal.srcObject = remoteVideoSecond.captureStream();
    // video_internal.play();
    console.log(flag_record)
    if (flag_record) {
        start()
    }
})

// let pcConfig_internal = {
//     "iceServers":
//     [
//         {
//           urls: "stun:openrelay.metered.ca:80",
//         },
//         {
//           urls: "turn:openrelay.metered.ca:80",
//           username: "openrelayproject",
//           credential: "openrelayproject",
//         },
//         {
//           urls: "turn:openrelay.metered.ca:443",
//           username: "openrelayproject",
//           credential: "openrelayproject",
//         },
//         {
//           urls: "turn:openrelay.metered.ca:443?transport=tcp",
//           username: "openrelayproject",
//           credential: "openrelayproject",
//         },
//       ]
// };

function createInternalPeerConnection() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    
    config.iceServers = [
        {
        urls: "stun:openrelay.metered.ca:80",
      },
      {url:'stun:stun.l.google.com:19302'},
      {
        urls: "turn:openrelay.metered.ca:80",
        username: "openrelayproject",
        credential: "openrelayproject",
      },
      {
        urls: "turn:openrelay.metered.ca:443",
        username: "openrelayproject",
        credential: "openrelayproject",
      },
      {
        urls: "turn:openrelay.metered.ca:443?transport=tcp",
        username: "openrelayproject",
        credential: "openrelayproject",
      },
    //   {url:'stun:stun01.sipphone.com'},
    //   {url:'stun:stun.ekiga.net'},
    //   {url:'stun:stun.fwdnet.net'},
    //   {url:'stun:stun.ideasip.com'},
    //   {url:'stun:stun.iptel.org'},
    //   {url:'stun:stun.rixtelecom.se'},
    //   {url:'stun:stun.schlund.de'},
    //   {url:'stun:stun.l.google.com:19302'},
    //   {url:'stun:stun1.l.google.com:19302'},
    //   {url:'stun:stun2.l.google.com:19302'},
    //   {url:'stun:stun3.l.google.com:19302'},
    //   {url:'stun:stun4.l.google.com:19302'},
    //   {url:'stun:stunserver.org'},
    //   {url:'stun:stun.softjoys.com'},
    //   {url:'stun:stun.voiparound.com'},
    //   {url:'stun:stun.voipbuster.com'},
    //   {url:'stun:stun.voipstunt.com'},
    //   {url:'stun:stun.voxgratia.org'},
    //   {url:'stun:stun.xten.com'},
    //   {
    //       url: 'turn:numb.viagenie.ca',
    //       credential: 'muazkh',
    //       username: 'webrtc@live.com'
    //   },
    //   {
    //       url: 'turn:192.158.29.39:3478?transport=udp',
    //       credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
    //       username: '28224511:1379330808'
    //   },
    //   {
    //       url: 'turn:192.158.29.39:3478?transport=tcp',
    //       credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
    //       username: '28224511:1379330808'
    //   }
];
    
    pc = new RTCPeerConnection({
        sdpSemantics: 'unified-plan', //newer implementation of WebRTC
        iceServers: [{urls: 'stun:stun.l.google.com:19302'}],
        iceCandidatePoolSize: 2
    });
    console.log(pc)

    // connect audio / video
    pc.addEventListener('track', function (evt) {
        if (evt.track.kind == 'video') {
            document.getElementById('video_internal').srcObject = evt.streams[0];
        }
        else
            document.getElementById('audio_internal').srcObject = evt.streams[0];
    });

    pc.addEventListener('iceconnectionstatechange', function (evt) {
        console.log(pc)
    })

    


    // pc.addEventListener('icegatheringstatechange', function(evt){
    //     console.log("addEventListener")
    //     console.log(pc)
    //     console.log(pc.canTrickleIceCandidates)
    //     // if(pc.canTrickleIceCandidates){
    //        creatAnwser()
    //     // }
    // })

    

    return pc;
}

function sendICEcandidate_internal(data) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    callSocket.send(JSON.stringify({
        type: 'ICEcandidate_internal',
        data
    }));
}


function handleIceCandidateInternal(event) {
    // // console.log('icecandidate event: ', event);
    // if (event.candidate) {
    //     console.log("Local ICE candidate");
    //     // console.log(event.candidate.candidate);

        if(pc.iceConnectionState  == 'checking'){
            sendICEcandidate_internal({
                type: "peericecandidate",
                rtcMessage: {
                    label: event.candidate.sdpMLineIndex,
                    id: event.candidate.sdpMid,
                    candidate: event.candidate.candidate
                }
            })
        }
    // } else {
    //     console.log('End of candidates.');
    // }
}



function negotiate() {
    return pc.createOffer().then(function (offer) {
        return pc.setLocalDescription(offer);
    }).then(function () {
        // wait for ICE gathering to complete
        return new Promise(function (resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        console.log("iceGatheringState is complete")
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function () {
        var offer = pc.localDescription;
        console.log(offer)

        callSocket_internal.send(JSON.stringify({
            type: 'peer_offer_internal',
            data : {
                rtcdata: {
                    rtcMessage: offer
                }
            }
        }));
        
        // connectSocket()

        
        // pc.addEventListener("iceconnectionstatechange", ()=> {
        //     console.log('####################')
        //     console.log(pc.iceConnectionState)
        //     if(pc.iceConnectionState  == 'checking'){
        //         console.log('####################')
        //         console.log(pc.iceConnectionState)
        //         pc.createOffer().then(function(offer){
        //             pc.setLocalDescription(offer);
        //             sendICEcandidate_internal({
        //                 type: "sendIceCandidateAgain",
        //                 rtcMessage: {
        //                     candidate: offer
        //                 }
        //             })
        //         })
        //     }
        // })

        
        

        // return fetch('/offer/system/', {
        //     body: JSON.stringify({
        //         sdp: offer.sdp,
        //         type: offer.type
        //     }),
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     method: 'POST'
        // });
        // }).then(function(response) {
        //     return response.json();
        // }).then(function(answer) {
        //     return pc.setRemoteDescription(answer);
        // }).catch(function(e) {
        //     alert(e);
    });
}

function creatAnwser(){
    if(pc.canTrickleIceCandidates){
        pc.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage_internal))
        console.log(pc)
        console.log(pc.canTrickleIceCandidates)
    }
}

function start() {
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

    callSocket_internal = new WebSocket(
        ws_scheme
        + window.location.host
        + '/ws/call/'
    );

    myName1 = "system"

    callSocket_internal.onopen = event => {
        //let's send myName to the socket
        callSocket_internal.send(JSON.stringify({
            type: 'login',
            data: {
                name: myName1,
            }
        }));
    }

    callSocket_internal.onmessage = (e) => {
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if (type == 'connection') {
            console.log(response.data.message, " internal ")
        }

        if (type == 'RemoteAnwser') {
            // onICECandidate(response.data);

            remoteRTCMessage_internal = response.data
            // console.log(remoteRTCMessage_internal)
            // console.log(pc.canTrickleIceCandidates)

            pc.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage_internal))
            console.log(pc)
            console.log(pc.canTrickleIceCandidates)
        }

        if (type == 'ICEcandidate'){
            onICECandidate(response.data)
        }

        const onICECandidate = (data) =>{
            // console.log(data);
            console.log("GOT ICE candidate");
    
            let message = data.rtcMessage
    
            let candidate = new RTCIceCandidate({
                sdpMLineIndex: message.label,
                candidate: message.candidate
            });
    
            if (peerConnection) {
                console.log("ICE candidate Added");
                peerConnection.addIceCandidate(candidate);
            } else {
                console.log("ICE candidate Pushed");
                iceCandidatesFromCaller.push(candidate);
            }
    
        }
    }

    pc = createInternalPeerConnection();

    var constraints = {
        audio: false,
        video: true
    };

    constraints.video = {
        width: 640,
        height: 480
    };


    if (constraints.audio || constraints.video) {
        if (constraints.video) {
            document.getElementById('media_internal').style.display = 'block';
        }

        // navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        //     stream.getTracks().forEach(function(track) {
        //         pc.addTrack(track, stream);
        //     });
        //     return negotiate();
        // }, function(err) {
        //     alert('Could not acquire media: ' + err);
        // });

        remoteVideoSecond.captureStream().getTracks().forEach(function (track) {
            pc.addTrack(track, remoteVideoSecond.captureStream())
        })
        video_internal.play();
        return negotiate();

        // navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        //     stream.getTracks().forEach(function(track) {
        //         pc.addTrack(track, stream);
        //     });
        //     return negotiate();
        // }, function(err) {
        //     alert('Could not acquire media: ' + err);
        // });
    } else {
        negotiate();
    }
}