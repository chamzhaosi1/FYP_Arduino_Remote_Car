# call/consumers.py
import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import time
from . import opencv

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


# ROOT = os.path.dirname(__file__)

# logger = logging.getLogger("pc")
# pcs = set()



class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'peer_offer_internal':
            async def test2():
                self.datasystemrtc = await opencv.offer(text_data_json['data']['rtcdata']["rtcMessage"])
                

            asyncio.run(test2())
            
            
            caller = "system"
            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'remoteAnwser',
                    'data': {
                        "sdp" : self.datasystemrtc.sdp,
                        "type" : self.datasystemrtc.type
                    }
                }
            )
        # if eventType == "sendIceCandidateAgain":
        #    opencv.addRemoteIceCandidateAgain(text_data_json['data']["rtcMessage"]["candidate"]) 

        if eventType == "ICEcandidate_internal":
            pass
            # print("ICEcandidate_internal")
            # opencv.offer(text_data_json['data']['rtcMessage'])


        if eventType == 'login':
            name = text_data_json['data']['name']
            print(name)

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )

        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name)
            # print(text_data_json)


            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name
            
            caller = text_data_json['data']['caller']
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':

            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

    def call_received(self, event):
        # print(event)
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))

    def remoteAnwser(self, event):
        print("remoteAnwser")
        self.send(text_data=json.dumps({
            'type': 'RemoteAnwser',
            'data': event['data']
        }))


    # def offer(request):
    #     print("1234")
    #     params = request.json()
    #     offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    #     pc = RTCPeerConnection()
    #     pc_id = "PeerConnection(%s)" % uuid.uuid4()
    #     pcs.add(pc)

    #     def log_info(msg, *args):
    #         logger.info(pc_id + " " + msg, *args)

    #     log_info("Created for %s", request.remote)

    #     # prepare local media
    #     player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
    #     if args.write_audio:
    #         recorder = MediaRecorder(args.write_audio)
    #     else:
    #         recorder = MediaBlackhole()

    #     @pc.on("datachannel")
    #     def on_datachannel(channel):
    #         @channel.on("message")
    #         def on_message(message):
    #             if isinstance(message, str) and message.startswith("ping"):
    #                 channel.send("pong" + message[4:])

    #     @pc.on("iceconnectionstatechange")
    #     async def on_iceconnectionstatechange():
    #         log_info("ICE connection state is %s", pc.iceConnectionState)
    #         if pc.iceConnectionState == "failed":
    #             await pc.close()
    #             pcs.discard(pc)

    #     @pc.on("track")
    #     def on_track(track):
    #         log_info("Track %s received", track.kind)

    #         if track.kind == "audio":
    #             pc.addTrack(player.audio)
    #             recorder.addTrack(track)
    #         elif track.kind == "video":
    #             local_video = opencv.VideoTransformTrack(
    #                 track, transform=params["video_transform"]
    #             )
    #             pc.addTrack(local_video)

    #         @track.on("ended")
    #         async def on_ended():
    #             log_info("Track %s ended", track.kind)
    #             await recorder.stop()

    #     # handle offer
    #     pc.setRemoteDescription(offer)
    #     recorder.start()

    #     # send answer
    #     answer =  pc.createAnswer()
    #     pc.setLocalDescription(answer)

    #     return web.Response(
    #         content_type="application/json",
    #         text=json.dumps(
    #             {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    #         ),
    #     )


    # async def on_shutdown(app):
    #     # close peer connections
    #     coros = [pc.close() for pc in pcs]
    #     await asyncio.gather(*coros)
    #     pcs.clear()
    
    

    