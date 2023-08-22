export const environment = {
  production: true,
	hmr: false,
	http: {
		// apiUrl: 'https://localhost:8000/api/',
		// apiUrl: 'https://192.168.0.138:8000/api/', 
		apiUrl: 'https://romo.kynoci.com:8000/api/', 
	},
	mqtt: {
		server: 'w33.kynoci.com',
		protocol: "wss",
		port: 15676,
		username: 'newera',
   	password: 'newera2023',
		path: '/ws'
	},
	websocket: {
		host: "romo.kynoci.com:8000",
		path: '/ws/call/'
	},
  face: {
    host: "https://romo.kynoci.com:8081",
		live_path: '/offer',
    capture_path: '/capture',
    retrieveCap_path: '/retrieveCapture',
    retrieveInt_path: '/retrieveIntruder'
  },
	pcConfig: {
		"iceServers":
      [
        // {"urls": "stun:stun.jap.bloggernepal.com:5349"},
        // {"urls": "stun:stun.l.google.com:19302"},
        // {
        //   "urls": "turn:103.111.75.247:3478",
        //   "username": "test",
        //   "credential": "test123"
        // },
        // {
        //   "urls": "turn:turn.jap.bloggernepal.com:5349",
        //   "username": "guest",
        //   "credential": "somepassword"
      	// },
        // {
        //   urls: "stun:openrelay.metered.ca:80",
        // },
        // { urls: 'stun:stun.l.google.com:19302' },
        // {
        //   urls: "turn:openrelay.metered.ca:80",
        //   username: "openrelayproject",
        //   credential: "openrelayproject",
        // },
        // {
        //   urls: "turn:openrelay.metered.ca:443",
        //   username: "openrelayproject",
        //   credential: "openrelayproject",
        // },
        // {
        //   urls: "turn:openrelay.metered.ca:443?transport=tcp",
        //   username: "openrelayproject",
        //   credential: "openrelayproject",
        // },
        // {url:'stun:stun01.sipphone.com'},
        // {url:'stun:stun.ekiga.net'},
        // {url:'stun:stun.fwdnet.net'},
        // {url:'stun:stun.ideasip.com'},
        // {url:'stun:stun.iptel.org'},
        // {url:'stun:stun.rixtelecom.se'},?\
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
	}
};