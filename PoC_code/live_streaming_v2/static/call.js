'use strict';

const baseURL = "/"

let localVideo = document.querySelector('#localVideo');
let remoteVideo = document.querySelector('#remoteVideo');

let otherUser;
let remoteRTCMessage;

let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;
let flag_record = false

let callInProgress = false;
let userToCall = "None"

//event from html
function call() {
    console.log(userToCall)
    // replase ":" to "_", because this ":" special character is not allow 
    if(userToCall != "None"){
        userToCall = userToCall.replace(/:/g, "_");
        otherUser = userToCall;
    }
    // flag_record = true;

    beReady()
        .then(bool => {
            processCall(userToCall)
        })
}

//event from html
function answer() {
    //do the event firing

    beReady()
        .then(bool => {
            processAccept();
        })

    // document.getElementById("answer").style.display = "none";
}

let pcConfig = {
    "iceServers":
        [
            {
                urls: "turn:103.111.75.247:3478",
                username: "test",
                credential: "test123",
            }
            // {
            //     urls: "stun:openrelay.metered.ca:80",
            // },
            // { url: 'stun:stun.l.google.com:19302' },
            // {
            //     urls: "turn:openrelay.metered.ca:80",
            //     username: "openrelayproject",
            //     credential: "openrelayproject",
            // },
            // {
            //     urls: "turn:openrelay.metered.ca:443",
            //     username: "openrelayproject",
            //     credential: "openrelayproject",
            // },
            // {
            //     urls: "turn:openrelay.metered.ca:443?transport=tcp",
            //     username: "openrelayproject",
            //     credential: "openrelayproject",
            // },
            //   {url:'stun:stun01.sipphone.com'},
            // {url:'stun:stun.ekiga.net'},
            // {url:'stun:stun.fwdnet.net'},
            // {url:'stun:stun.ideasip.com'},
            // {url:'stun:stun.iptel.org'},
            // {url:'stun:stun.rixtelecom.se'},
            // {url:'stun:stun.schlund.de'},
            // {url:'stun:stun.l.google.com:19302'},
            // {url:'stun:stun1.l.google.com:19302'},
            // {url:'stun:stun2.l.google.com:19302'},
            // {url:'stun:stun3.l.google.com:19302'},
            // {url:'stun:stun4.l.google.com:19302'},
            // {url:'stun:stunserver.org'},
            // {url:'stun:stun.softjoys.com'},
            // {url:'stun:stun.voiparound.com'},
            // {url:'stun:stun.voipbuster.com'},
            // {url:'stun:stun.voipstunt.com'},
            // {url:'stun:stun.voxgratia.org'},
            // {url:'stun:stun.xten.com'},
            // {
            //     url: 'turn:numb.viagenie.ca',
            //     credential: 'muazkh',
            //     username: 'webrtc@live.com'
            // },
            // {
            //     url: 'turn:192.158.29.39:3478?transport=udp',
            //     credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
            //     username: '28224511:1379330808'
            // },
            // {
            //     url: 'turn:192.158.29.39:3478?transport=tcp',
            //     credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
            //     username: '28224511:1379330808'
            // }
        ]
};

// Set up audio and video regardless of what devices are present.
let sdpConstraints = {
    offerToReceiveAudio: true,
    offerToReceiveVideo: true
};

/////////////////////////////////////////////



let socket;
let callSocket;
function connectSocket() {
    // console.log(myName)
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

    callSocket = new WebSocket(
        ws_scheme
        + "romo.kynoci.com:8000"
        + '/ws/call/'
    );

    callSocket.onopen = event => {
        //let's send myName to the socket
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: myName
            }
        }));
    }

    callSocket.onmessage = (e) => {
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if (type == 'connection') {
            console.log(response.data.message)
        }

        if (type == 'call_received') {
            // console.log(response);
            onNewCall(response.data)
        }

        if (type == 'call_answered') {
            console.log(response);
            onCallAnswered(response.data);
        }

        if (type == 'ICEcandidate') {
            onICECandidate(response.data);
        }

        if (type == 'end_session') {
            console.log("end session")
            reloadPage();
        }
    }

    const onNewCall = (data) => {
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage

        // console.log(otherUser);

        // document.getElementById("profileImageA").src = baseURL + callerProfile.image;
        // document.getElementById("callerName").innerHTML = otherUser;
        // document.getElementById("call").style.display = "none";
        // document.getElementById("answer").style.display = "block";
        // console.log("12312312312312");

        if (otherUser == "cham") {
            // console.log("dsffsdf");
            // document.getElementById("answer").style.display = "none";
            // answerCall(data)
            // callProgress()
            document.getElementById("remoteVideoDiv").style.display = "block";
            answer();
        }
    }

    const onCallAnswered = (data) => {
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        // console.log("adfasdfasdfa")
        // console.log(peerConnection)
        // console.log(remoteRTCMessage)
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        // document.getElementById("calling").style.display = "none";

        console.log("Call Started. They Answered");
        // console.log(pc);

        callProgress()
        document.getElementById("deviceTable").style.display = "none";
    }

    const onICECandidate = (data) => {
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

    console.log(userToCall)
    if(userToCall != "None"){
        call();
    }
}

/**
 * 
 * @param {Object} data 
 * @param {number} data.name - the name of the user to call
 * @param {Object} data.rtcMessage - the rtc create offer object
 */
function sendCall(data) {
    //to send a call
    console.log("Send Call");

    // socket.emit("call", data);
    callSocket.send(JSON.stringify({
        type: 'call',
        data
    }));

    // document.getElementById("call").style.display = "none";
    // document.getElementById("profileImageCA").src = baseURL + otherUserProfile.image;
    // document.getElementById("otherUserNameCA").innerHTML = otherUser;
    // document.getElementById("calling").style.display = "block";
}



/**
 * 
 * @param {Object} data 
 * @param {number} data.caller - the caller name
 * @param {Object} data.rtcMessage - answer rtc sessionDescription object
 */
function answerCall(data) {
    //to answer a call
    // socket.emit("answerCall", data);
    callSocket.send(JSON.stringify({
        type: 'answer_call',
        data
    }));
    callProgress();
}

/**
 * 
 * @param {Object} data 
 * @param {number} data.user - the other user //either callee or caller 
 * @param {Object} data.rtcMessage - iceCandidate data 
 */
function sendICEcandidate(data) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    callSocket.send(JSON.stringify({
        type: 'ICEcandidate',
        data
    }));
}

function beReady() {
    return navigator.mediaDevices.getUserMedia({
        // audio: true,
        video: true,
    })
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;

            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}

function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: userName,
            rtcMessage: sessionDescription
        })
    }, (error) => {
        console.log("Error");
    });
}

function processAccept() {
    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    peerConnection.createAnswer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);

        if (iceCandidatesFromCaller.length > 0) {
            //I am having issues with call not being processed in real world (internet, not local)
            //so I will push iceCandidates I received after the call arrived, push it and, once we accept
            //add it as ice candidate
            //if the offer rtc message contains all thes ICE candidates we can ingore this.
            for (let i = 0; i < iceCandidatesFromCaller.length; i++) {
                //
                let candidate = iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                    peerConnection.addIceCandidate(candidate).then(done => {
                        console.log(done);
                    }).catch(error => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        answerCall({
            caller: otherUser,
            rtcMessage: sessionDescription
        })

    }, (error) => {
        console.log("Error");
    })
}

/////////////////////////////////////////////////////////

function createPeerConnection() {
    try {
        peerConnection = new RTCPeerConnection(pcConfig);
        console.log(peerConnection)
        // peerConnection = new RTCPeerConnection();
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.addEventListener("addstream", (e) => handleRemoteStreamAdded(e))
        peerConnection.onremovestream = handleRemoteStreamRemoved;
        console.log('Created RTCPeerConnnection');
        return;

    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleIceCandidate(event) {
    console.log('icecandidate event: ', event);
    if (event.candidate) {
        console.log("Local ICE candidate");
        // console.log(event.candidate.candidate);

        sendICEcandidate({
            user: otherUser,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    remoteVideo.srcObject = remoteStream;
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
    remoteVideo.srcObject = null;
    localVideo.srcObject = null;
}

window.onbeforeunload = function () {
    if (callInProgress) {
        stop();
    }
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  

async function reloadPage(){
    location.reload();
    // await sleep(3000);
}


async function stop() {
    // console.log(otherUser)
    callSocket.send(JSON.stringify({
        type: 'stopSession',
        data: {
            client : otherUser,
        }
    }));
    
    // console.log(document.getElementById(".loader").style.display)
    document.getElementById("loader").style.display = "block";
    await sleep(3000);
    location.reload();
    document.getElementById("loader").style.display = "none";

    
    // localStream.getTracks().forEach(track => track.stop());
    // callInProgress = false;
    // peerConnection.close();
    // peerConnection = null;
    // document.getElementById("deviceTable").style.display = "block";
    // document.getElementById("call").style.display = "block";
    // document.getElementById("answer").style.display = "none";
    // document.getElementById("inCall").style.display = "none";
    // document.getElementById("calling").style.display = "none";
    // document.getElementById("endVideoButton").style.display = "none"
    // otherUser = null;
}

function callProgress() {

    document.getElementById("videos").style.display = "block";
    document.getElementById("remoteVideoDiv").style.display = "block";
    document.getElementById("buttonStop").style.display = "block";
    // document.getElementById("otherUserNameC").innerHTML = otherUser;
    // document.getElementById("inCall").style.display = "block";

    callInProgress = true;
}

// for raspberry pi auto registre an account
const urlParams = new URLSearchParams(window.location.search);
let userNameString = urlParams.get('username')
console.log(userNameString);

if (userNameString != null) {
    userNameString = userNameString.replace(/:/g, "_");
    myName = userNameString;

    document.getElementById("deviceTable").style.display = "none";
    connectSocket();
    userToCall = "cham"
    console.log("call")
    call()
}


