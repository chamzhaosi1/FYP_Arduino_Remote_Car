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

//event from html
function call() {
    let userToCall = document.getElementById("callName").value;
    otherUser = userToCall;
    flag_record = true

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

    document.getElementById("answer").style.display = "none";
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
    console.log(myName)
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

    callSocket = new WebSocket(
        ws_scheme
        + window.location.host
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
            onCallAnswered(response.data);
        }

        if (type == 'ICEcandidate') {
            onICECandidate(response.data);
        }
    }

    const onNewCall = (data) => {
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage

        // document.getElementById("profileImageA").src = baseURL + callerProfile.image;
        document.getElementById("callerName").innerHTML = otherUser;
        document.getElementById("call").style.display = "none";
        document.getElementById("answer").style.display = "block";


        setTimeout(() => {
            if (otherUser == "lim") {
                document.getElementById("answer").style.display = "none";
                answerCall(data)
                callProgress()

            }
        }, 1000)
    }

    const onCallAnswered = (data) => {
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        console.log("adfasdfasdfa")
        console.log(peerConnection)
        console.log(remoteRTCMessage)
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        document.getElementById("calling").style.display = "none";

        console.log("Call Started. They Answered");
        // console.log(pc);

        callProgress()
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

    document.getElementById("call").style.display = "none";
    // document.getElementById("profileImageCA").src = baseURL + otherUserProfile.image;
    document.getElementById("otherUserNameCA").innerHTML = otherUser;
    document.getElementById("calling").style.display = "block";
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
        audio: true,
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
    // console.log('icecandidate event: ', event);
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


function stop() {
    localStream.getTracks().forEach(track => track.stop());
    callInProgress = false;
    peerConnection.close();
    peerConnection = null;
    document.getElementById("call").style.display = "block";
    document.getElementById("answer").style.display = "none";
    document.getElementById("inCall").style.display = "none";
    document.getElementById("calling").style.display = "none";
    document.getElementById("endVideoButton").style.display = "none"
    otherUser = null;
}

function callProgress() {

    document.getElementById("videos").style.display = "block";
    document.getElementById("otherUserNameC").innerHTML = otherUser;
    document.getElementById("inCall").style.display = "block";

    callInProgress = true;
}


const urlParams = new URLSearchParams(window.location.search);
const userNameString = urlParams.get('username')
console.log(userNameString);

if (userNameString != null) {
    setTimeout(() => {
        myName = userNameString;
        document.getElementById("userName").style.display = "none";
        document.getElementById("call").style.display = "block";
        console.log(document.getElementById("call").style.display)

        document.getElementById("nameHere").innerHTML = userNameString;
        document.getElementById("userInfo").style.display = "block";

        connectSocket()
    }, 1000)
}

// Draw line
var client;
var hostname = "lim.kynoci.com";
var port = "8083";
var led_topic = "joystick/#";
var clientId;

if (window.sessionStorage.clientId) {
    clientId = window.sessionStorage.clientId;
} else {
    clientId = "mqtt_js_" + parseInt(Math.random() * 100000, 10);
    window.sessionStorage.clientId = clientId;
}

function connect() {
    // Set up the client
    client = new Paho.MQTT.Client(hostname, Number(port), clientId);
    console.info('Connecting to Server: Hostname: ', hostname, '. Port: ', port, '. Client ID: ', clientId);

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // see client class docs for all the options
    var options = {
        onSuccess: onConnect, // after connected, subscribes
        onFailure: onFail,    // useful for logging / debugging
        useSSL: true,
        userName: "babi",
        password: "chu"
    };
    // connect the client
    // client.username_pw_set("babi", "chu")
    client.connect(options);
    console.info('Connecting...');
}

function onConnect(context) {
    // console.log("Client Connected");
    //   document.getElementById('connect_button').innerHTML = "Connected!";
    //   document.getElementById('connect_button').disabled = true;
    //   document.getElementById('on_button').disabled = false;
    //   document.getElementById('off_button').disabled = false;


    // And subscribe to our topics	-- all with the same callback function
    var options = { qos: 0, onSuccess: function (context) { console.log("subscribed"); } }
    client.subscribe(led_topic, options);

}

function onFail(context) {
    console.log("Failed to connect");
}

function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("Connection Lost: " + responseObject.errorMessage);
        window.alert("Someone else took my websocket!\nRefresh to take it back.");
    }
}


var canvas_cartesian = document.getElementById("cartesian");
var c = canvas_cartesian.getContext("2d");
var p = document.getElementById("polar").getContext("2d");
var m = document.getElementById("mecanum").getContext("2d");

function redraw() {

    // Cartesian
    c.clearRect(0, 0, 200, 200);
    c.beginPath(); c.rect(50, 50, 100, 100); c.stroke();
    // \
    c.moveTo(0, 0); c.lineTo(200, 200); c.stroke();
    // /
    c.moveTo(200, 0); c.lineTo(0, 200); c.stroke();
    // -
    c.moveTo(0, 100); c.lineTo(200, 100); c.stroke();
    // |
    c.moveTo(100, 0); c.lineTo(100, 200); c.stroke();

    // Polar
    p.clearRect(0, 0, 200, 200);
    p.beginPath(); p.arc(100, 100, 50, 0, 2 * Math.PI, false); p.stroke();
    // \
    p.moveTo(29, 29); p.lineTo(171, 171); p.stroke();
    // /
    p.moveTo(171, 29); p.lineTo(29, 171); p.stroke();
    // -
    p.moveTo(0, 100); p.lineTo(200, 100); p.stroke();
    // |
    p.moveTo(100, 0); p.lineTo(100, 200); p.stroke();

    // Mecanum
    m.clearRect(0, 0, 200, 200);
    m.strokeStyle = 'black';
    m.lineWidth = 1;

    // Left-Front
    m.beginPath(); m.rect(33, 25, 33, 50); m.stroke();
    m.moveTo(33, 33.5); m.lineTo(66, 66.5); m.stroke();
    draw_cartesian_pos(m, -(33 + (33 / 2)), (25 + (50 / 2)), 'purple', 6)

    // Right-Front
    m.beginPath(); m.rect(134, 25, 33, 50); m.stroke();
    m.moveTo(134, 66.5); m.lineTo(167, 33.5); m.stroke();
    draw_cartesian_pos(m, (33 + (33 / 2)), (25 + (50 / 2)), 'purple', 6)

    // Left-Back
    m.beginPath(); m.rect(33, 125, 33, 50); m.stroke();
    m.moveTo(33, 166.5); m.lineTo(66, 133.5); m.stroke();
    draw_cartesian_pos(m, -(33 + (33 / 2)), -(25 + (50 / 2)), 'purple', 6)

    // Right-Back
    m.beginPath(); m.rect(134, 125, 33, 50); m.stroke();
    m.moveTo(134, 133.5); m.lineTo(167, 166.5); m.stroke();
    draw_cartesian_pos(m, (33 + (33 / 2)), -(25 + (50 / 2)), 'purple', 6)

    // Mecanum Body
    m.beginPath(); m.rect(67, 37.5, 66, 125); m.stroke();

}
redraw();
let cartesian = { x: 0, y: 0 };
let polar = { a: 0, r: 0 };

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    cartesian.x = event.clientX - rect.left - 100
    cartesian.y = -((event.clientY - rect.top) - 100)
}

function draw_cartesian_pos(context, x, y, color, size) {
    if (color == null) {
        color = '#000';
    }
    if (size == null) {
        size = 5;
    }
    context.beginPath();
    context.lineWidth = 1;
    context.fillStyle = color;
    context.fillRect(x + 100 - (size / 2), -(y - 100) - (size / 2), size, size);
    context.fill();
    context.closePath();
}

function draw_cartesian_line(context, x1, y1, x2, y2, color, size) {
    if (color == null) {
        color = '#000';
    }
    if (size == null) {
        size = 5;
    }
    context.beginPath();
    context.lineWidth = size;
    context.strokeStyle = color;
    context.moveTo(x1 + 100, -(y1 - 100));
    context.lineTo(x2 + 100, -(y2 - 100));
    context.stroke();
    context.strokeStyle = 'black';
    context.closePath();
}

function draw_cartesian_arc(context, ang, radial, color, size) {
    context.beginPath();
    context.lineWidth = size;
    context.strokeStyle = color;
    context.arc(100, 100, radial, 0, -(ang) * Math.PI / 180, true);
    context.stroke();
    context.lineWidth = 1;
    context.strokeStyle = 'black';
    context.closePath();
}

function draw_polar_pos(context, ang, radial, color, size) {
    let x = Math.sin((-(ang + 90 + 180)) * Math.PI / 180) * radial;
    let y = Math.cos((-(ang + 90 + 180)) * Math.PI / 180) * radial;
    draw_cartesian_pos(context, x, y, color, size)
    draw_cartesian_pos(context, 0, 0, color, size)
    draw_cartesian_line(context, 0, 0, x, y, color, size / 2)
    draw_cartesian_arc(context, ang, radial, color, size / 2)
}

function mecanum_dir(offset_x, offset_y, ang, power) {
    m.beginPath();
    m.lineWidth = 4;
    var radial2 = power * 60 / 300;
    var xx = Math.sin(ang * Math.PI / 180) * Math.abs(radial2);
    var yy = Math.cos(ang * Math.PI / 180) * Math.abs(radial2);
    if (radial2 >= 0) {
        m.strokeStyle = 'green';
        m.moveTo(offset_x, offset_y); m.lineTo(offset_x + xx, offset_y - yy); m.stroke();
    } else {
        m.strokeStyle = 'red';
        m.moveTo(offset_x, offset_y); m.lineTo(offset_x - xx, offset_y + yy); m.stroke();
    }
    m.closePath();
}

polar.r = 75
polar.a = 0;
draw_polar_pos(p, polar.a, polar.r, 'orange', 6)
polar.a = 45;
draw_polar_pos(p, polar.a, polar.r, 'orange', 8)
polar.a = 90;
draw_polar_pos(p, polar.a, polar.r, 'orange', 10)
polar.a = 135;
draw_polar_pos(p, polar.a, polar.r, 'orange', 12)
polar.a = 180;
draw_polar_pos(p, polar.a, polar.r, 'orange', 14)
polar.a = 225;
draw_polar_pos(p, polar.a, polar.r, 'orange', 16)
polar.a = 270;
draw_polar_pos(p, polar.a, polar.r, 'orange', 18)
polar.a = 315;
draw_polar_pos(p, polar.a, polar.r, 'orange', 20)

canvas_cartesian.addEventListener('mousedown', function (e) {

    // return;
    redraw();

    // Calculate Cartesian - X,Y
    getCursorPosition(canvas_cartesian, e);
    document.getElementById("cartesian_coord_x").innerHTML = cartesian.x.toFixed(2);
    document.getElementById("cartesian_coord_y").innerHTML = cartesian.y.toFixed(2);
    draw_cartesian_pos(c, cartesian.x, cartesian.y, 'red', 6)

    // Calculate Polar - Theta
    let theta = 0;
    if ((cartesian.x >= 0) && (cartesian.y >= 0)) {
        theta = (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else if ((cartesian.x < 0) && (cartesian.y >= 0)) {
        theta = 180 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else if ((cartesian.x < 0) && (cartesian.y < 0)) {
        theta = 180 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else {
        theta = 360 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    }
    document.getElementById("theta").innerHTML = theta.toFixed(2);

    // Calculate Polar - Radial (need maxRadius, hypot)
    let maxRadius = 0;
    if (theta < 45) {
        maxRadius = 100 / Math.cos(theta * Math.PI / 180);
    } else if (theta <= 135) {
        maxRadius = 100 / Math.sin(theta * Math.PI / 180);
    } else if (theta <= 225) {
        maxRadius = Math.abs(100 / Math.cos(theta * Math.PI / 180));
    } else if (theta <= 315) {
        maxRadius = Math.abs(100 / Math.sin(theta * Math.PI / 180));
    } else {
        maxRadius = Math.abs(100 / Math.cos(theta * Math.PI / 180));
    }
    // document.getElementById("maxRadius").innerHTML=maxRadius.toFixed(2); 
    let hypot = Math.hypot(cartesian.y, cartesian.x);
    // document.getElementById("hypot").innerHTML=hypot.toFixed(2);
    let radial = hypot * 100 / maxRadius;
    document.getElementById("radial").innerHTML = radial.toFixed(2);
    draw_polar_pos(p, theta, radial, 'orange', 6)

    // Calculate Mecanum
    var pwr_sin = Math.sin((theta - 45) * Math.PI / 180) * radial * 3;
    var pwr_cos = Math.cos((theta - 45) * Math.PI / 180) * radial * 3;
    // Left-Front
    mecanum_dir(49.5, 50, 45, pwr_cos);
    document.getElementById("leftfront").innerHTML = pwr_cos.toFixed(2);
    // Right-Front
    mecanum_dir(150.5, 50, -45, pwr_sin);
    document.getElementById("rightfront").innerHTML = pwr_sin.toFixed(2);
    // Left-Back
    mecanum_dir(49.5, 150, -45, pwr_sin);
    document.getElementById("leftback").innerHTML = pwr_sin.toFixed(2);
    // Right-Back
    mecanum_dir(150.5, 150, 45, pwr_cos);
    document.getElementById("rightback").innerHTML = pwr_cos.toFixed(2);

})

function onMessageArrived(message) {
    console.log('got message to topic:', message.destinationName, 'message:', message.payloadString);

    if (message.destinationName == 'joystick/x') {
        // document.getElementById('getX').innerHTML = message.payloadString;
        cartesian.x = parseInt(message.payloadString);
        console.log("KENNY - " + cartesian.y);
    }
    if (message.destinationName == 'joystick/y') {
        // document.getElementById('getY').innerHTML = message.payloadString;
        cartesian.y = parseInt(message.payloadString)
        console.log("KENNY - " + cartesian.y);
    }


    /////// START ///////////////

    redraw();

    //     // Calculate Cartesian - X,Y
    // // cartesian.x = 
    //     // getCursorPosition(canvas_cartesian, e);
    document.getElementById("cartesian_coord_x").innerHTML = cartesian.x;
    document.getElementById("cartesian_coord_y").innerHTML = cartesian.y;
    draw_cartesian_pos(c, cartesian.x, cartesian.y, 'red', 6)

    // Calculate Polar - Theta
    let theta = 0;
    if ((cartesian.x >= 0) && (cartesian.y >= 0)) {
        theta = (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else if ((cartesian.x < 0) && (cartesian.y >= 0)) {
        theta = 180 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else if ((cartesian.x < 0) && (cartesian.y < 0)) {
        theta = 180 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    } else {
        theta = 360 + (Math.atan(cartesian.y / cartesian.x)) / Math.PI * 180;
    }
    // if(isNaN(theta)){
    //     theta=0
    // }
    document.getElementById("theta").innerHTML = theta.toFixed(2);

    // Calculate Polar - Radial (need maxRadius, hypot)
    let maxRadius = 0;
    if (theta < 45) {
        maxRadius = 100 / Math.cos(theta * Math.PI / 180);
    } else if (theta <= 135) {
        maxRadius = 100 / Math.sin(theta * Math.PI / 180);
    } else if (theta <= 225) {
        maxRadius = Math.abs(100 / Math.cos(theta * Math.PI / 180));
    } else if (theta <= 315) {
        maxRadius = Math.abs(100 / Math.sin(theta * Math.PI / 180));
    } else {
        maxRadius = Math.abs(100 / Math.cos(theta * Math.PI / 180));
    }
    // document.getElementById("maxRadius").innerHTML=maxRadius.toFixed(2); 
    let hypot = Math.hypot(cartesian.y, cartesian.x);
    // document.getElementById("hypot").innerHTML=hypot.toFixed(2);
    let radial = hypot * 100 / maxRadius;
    // if(isNaN(radial)){
    //     radial=0
    // }
    document.getElementById("radial").innerHTML = radial.toFixed(2);
    draw_polar_pos(p, theta, radial, 'orange', 6)

    // Calculate Mecanum
    var pwr_sin = Math.sin((theta - 45) * Math.PI / 180) * radial * 3;
    var pwr_cos = Math.cos((theta - 45) * Math.PI / 180) * radial * 3;

    if (isNaN(pwr_sin)) {
        pwr_sin = 0
    }

    if (isNaN(pwr_cos)) {
        pwr_cos = 0
    }
    // Left-Front
    mecanum_dir(49.5, 50, 45, pwr_cos);
    document.getElementById("leftfront").innerHTML = pwr_cos.toFixed(2);
    // Right-Front
    mecanum_dir(150.5, 50, -45, pwr_sin);
    document.getElementById("rightfront").innerHTML = pwr_sin.toFixed(2);
    // Left-Back
    mecanum_dir(49.5, 150, -45, pwr_sin);
    document.getElementById("leftback").innerHTML = pwr_sin.toFixed(2);
    // Right-Back
    mecanum_dir(150.5, 150, 45, pwr_cos);
    document.getElementById("rightback").innerHTML = pwr_cos.toFixed(2);

    var message = new Paho.MQTT.Message(pwr_cos.toFixed(0));
    message.destinationName = "mecanum/lf";
    message.qos = 0;
    client.send(message);

    var message = new Paho.MQTT.Message(pwr_sin.toFixed(0));
    message.destinationName = "mecanum/rf";
    message.qos = 0;
    client.send(message);

    var message = new Paho.MQTT.Message(pwr_sin.toFixed(0));
    message.destinationName = "mecanum/lb";
    message.qos = 0;
    client.send(message);

    var message = new Paho.MQTT.Message(pwr_cos.toFixed(0));
    message.destinationName = "mecanum/rb";
    message.qos = 0;
    client.send(message);
    /////// END  ///////////////
}

