import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import time
from multiprocessing import Process
import websocket

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCIceServer, RTCConfiguration, RTCIceCandidate
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform


    async def recv(self):
        # print("asf")
        frame = await self.track.recv()

        if self.transform == "cartoon":
            img = frame.to_ndarray(format="bgr24")

            # prepare color
            img_color = cv2.pyrDown(cv2.pyrDown(img))
            for _ in range(6):
                img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
            img_color = cv2.pyrUp(cv2.pyrUp(img_color))

            # prepare edges
            img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img_edges = cv2.adaptiveThreshold(
                cv2.medianBlur(img_edges, 7),
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                2,
            )
            img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

            # combine color and edges
            img = cv2.bitwise_and(img_color, img_edges)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "edges":
            print("edges")
            # perform edge detection
            img = frame.to_ndarray(format="bgr24")
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "rotate":
            # rotate image
            img = frame.to_ndarray(format="bgr24")
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
            img = cv2.warpAffine(img, M, (cols, rows))

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        else:
            return frame


async def offer(data):

    # print("qwddas")
    # def on_open(ws):
    #     #let's send myName to the socket
    #     ws.send(json.dumps({
    #         type: 'login',
    #         data: {
    #             "name": "system1"
    #         }
    #     }))

    # websocket.enableTrace(True)
    # ws = websocket.WebSocketApp("wss://romo.kynoci.com:8000/ws/call",
    #                           on_open=on_open,)
  
    # print(data)
    offer = RTCSessionDescription(sdp=data['sdp'], type=data['type'])

    # ice_server = RTCIceServer(urls="stun:stun.l.google.com:19302")
    # pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[ice_server]))

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    
    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("iceconnectionstatechange")
        print("iceconnectionstatechange")
        print("iceconnectionstatechange")
        print("iceconnectionstatechange")
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)
        # if pc.iceConnectionState == "checking":
        #     print("added ice candidate")
        #     pc.addIceCandidate(event['candidate'])

    # def addRemoteIceCandidate(event):
    #     if pc.iceConnectionState == "checking":
    #         print("added ice candidate")
    #         pc.addIceCandidate(event['candidate'])

    # if(data['type'] == 'peericecandidate'):
    #     addRemoteIceCandidate(data)
    

    # @pc.on("iceconnectionstatechange")
    # def on_iceconnectionstatechange():
    #     print(f"ICE connection state is {pc.iceConnectionState}")
    #     if pc.iceConnectionState == "failed":
    #         pc.close()
    #     if pc.iceConnectionState == "checking":
    #         candidates = pc.remoteDescription.sdp.split("\r\n")
    #         for candidate in candidates:
    #             if "a=candidate:" in candidate:
    #                 print("added ice candidate")
    #                 candidate = candidate.replace("a=candidate:", "")
    #                 splitted_data = candidate.split(" ")
    #                 remote_ice_candidate = RTCIceCandidate(
    #                     foundation=splitted_data[0],
    #                     component=splitted_data[1],
    #                     protocol=splitted_data[2],
    #                     priority=int(splitted_data[3]),
    #                     ip=splitted_data[4],
    #                     port=int(splitted_data[5]),
    #                     type=splitted_data[7],
    #                     sdpMid=0,
    #                     sdpMLineIndex=0,
    #                 )
    #                 pc.addIceCandidate(remote_ice_candidate)

    # @pc.on("iceconnectionstatechange")
    # async def on_iceconnectionstatechange():
    #     print("iceconnectionstatechange")
    #     print(pc.iceConnectionState)

    @pc.on("icegatheringstatechange")
    async def on_icegatheringstatechange():
        print(pc.iceGatheringState)
        # if (pc.iceGatheringState == "complete"):
        #     # # handle offer
        #     await pc.setRemoteDescription(offer)
        #     # # await recorder.start()

        #     # # send answer
        #     answer =  await pc.createAnswer()
        #     await pc.setLocalDescription(answer)

        #     print("before return")
        #     return pc.localDescription


        # print(pc.iceGatheringState)
        # print(pc.signalingState)
        # print(pc.remoteDescription)
        # print(pc.localDescription)
        # print(pc.iceConnectionState)
        # print("above")
        # print(pc)


    # def f(name):
    #     while True:
    #         # print(pc.iceGatheringState)
    #         # print(pc.signalingState)
    #         # print(pc.remoteDescription)
    #         print(name)
    #         print(pc.localDescription)
    #         print(pc.iceConnectionState)
    #         time.sleep(5)

    # p1 = Process(target=f, args=('P1',))
    # p1.start()


    @pc.on("track")
    def on_track(track):
        print("track")
        log_info("Track %s received", track.kind)
        
        # print(pc.iceGatheringState)
        # print(pc.signalingState)

        if track.kind == "audio":
            # pc.addTrack(player.audio)
            # recorder.addTrack(track)
            pass
        elif track.kind == "video":
            local_video = VideoTransformTrack(
                track, "edges"
            )
            pc.addTrack(local_video)

        @track.on("ended")
        def on_ended():
            log_info("Track %s ended", track.kind)
            pass
            # await recorder.stop()

    # @pc.on("icecandidate")
    # def on_icecandidate():
    #     print("icecandidate")
    #     print(pc.getLocalCandidates())
    #     print(pc.getRemoteCandidates())
    #     print("###############")

    # # handle offer
    print(pc.signalingState)
    print("setRemoteDescription")
    await pc.setRemoteDescription(offer)
    print(pc.signalingState)
    # # await recorder.start()

    # # send answer
    print("before createAnswer")
    answer =  await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print("after createAnswer")


    while True:
        print(pc.signalingState)
        print("setRemoteDescription")
        await pc.setRemoteDescription(offer)
        print(pc.signalingState)
        time.sleep(3)

    # # # handle offer
    # print("setRemoteDescription")
    # await pc.setRemoteDescription(offer)
    # # # await recorder.start()


    # print(pc.connectionState)
    # print(pc.localDescription)
    # offer = pc.localDescription
    

    # data_system = {
    #     "sdp": offer.sdp,
    #     "type" : offer.type
    # }

    # print(data_system["user"])
    # print(data_system["rtcdata"])

    # print(pc.localDescription)
    # print(pc.iceConnectionState)

    # p2 = Process(target=f, args=('P2',))
    # p2.start()

    # print("below")
    # print(pc)

    # print("before return")
    return pc.localDescription

    # return web.Response(
    #     content_type="application/json",
    #     text=json.dumps(
    #         {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    #     ),
    # )

# async def addRemoteIceCandidateAgain(offer):
#     global pc
#     await pc.setRemoteDescription(offer)

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

