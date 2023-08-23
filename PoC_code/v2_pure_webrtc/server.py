import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
from pathlib import Path
# import websocket

# import webbrowser
# import rel
import time
# from Screenshot import Screenshot_clipping

# import cv2, face_recognition
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription


ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()


# class VideoTransformTrack(MediaStreamTrack):
#     """
#     A video stream track that transforms frames from an another track.
#     """

#     kind = "video"

#     def __init__(self, track, transform):
#         super().__init__()  # don't forget this!
#         self.track = track
#         self.transform = transform


#     async def recv(self):
#         # print("asf")
#         frame = await self.track.recv()

#         if self.transform == "cartoon":
#             img = frame.to_ndarray(format="bgr24")

#             # prepare color
#             img_color = cv2.pyrDown(cv2.pyrDown(img))
#             for _ in range(6):
#                 img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
#             img_color = cv2.pyrUp(cv2.pyrUp(img_color))

#             # prepare edges
#             img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#             img_edges = cv2.adaptiveThreshold(
#                 cv2.medianBlur(img_edges, 7),
#                 255,
#                 cv2.ADAPTIVE_THRESH_MEAN_C,
#                 cv2.THRESH_BINARY,
#                 9,
#                 2,
#             )
#             img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

#             # combine color and edges
#             img = cv2.bitwise_and(img_color, img_edges)

#             # rebuild a VideoFrame, preserving timing information
#             new_frame = VideoFrame.from_ndarray(img, format="bgr24")
#             new_frame.pts = frame.pts
#             new_frame.time_base = frame.time_base
#             return new_frame
#         elif self.transform == "edges":
#             print("edges")
#             # perform edge detection
#             img = frame.to_ndarray(format="bgr24")
#             img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

#             # rebuild a VideoFrame, preserving timing information
#             new_frame = VideoFrame.from_ndarray(img, format="bgr24")
#             new_frame.pts = frame.pts
#             new_frame.time_base = frame.time_base
#             return new_frame
#         elif self.transform == "rotate":
#             # rotate image
#             img = frame.to_ndarray(format="bgr24")
#             rows, cols, _ = img.shape
#             M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
#             img = cv2.warpAffine(img, M, (cols, rows))

#             # rebuild a VideoFrame, preserving timing information
#             new_frame = VideoFrame.from_ndarray(img, format="bgr24")
#             new_frame.pts = frame.pts
#             new_frame.time_base = frame.time_base
#             return new_frame
#         elif self.transform == "face_detection":
#             img = frame.to_ndarray(format="bgr24")

#             tmp_img = img.copy()
#             tmp_img = cv2.resize(tmp_img,(0,0), None, 0.25, 0.25)
#             # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#             facesCurFrame = face_recognition.face_locations(tmp_img)
#             if facesCurFrame:
#                 print(facesCurFrame)
#                 # print(cv2.cv.CV_CAP_PROP_FPS)
#                 # print(cv2.CAP_PROP_FPS)
#                 # print(cv2.CV_CAP_PROP_FRAME_WIDTH)
#                 # print(cv2.CV_CAP_PROP_FRAME_HEIGHT)
#                 x_offset = 15
#                 y_offset = 20

#                 ## because the face location is top, right, bottom, left
#                 y1,x2,y2,x1 = facesCurFrame[0]
#                 ## because the frame is resize at begining so now resize back 
#                 y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
#                 ## draw a rectangle / box
#                 # cv2.rectangle(img, (x1+50, y1+50), (x2, y2), (255,0,0),2)
#                 # cv2.rectangle(img, (20, 20), (40, 40), (255,255,0),2)
#                 # cv2.rectangle(img, (0, 0), (10, 10), (255,255,255),2)
#                 cv2.rectangle(img, (x1-x_offset, y1-y_offset), (x2+x_offset, y2+y_offset), (0,255,255),2)
#                 ## draw a filled rectangle / box
#                 # cv2.rectangle(img,(x1, y2-40), (x2, y2), (0,255,0), cv2.FILLED)
#                 ## write the its name into the filled box
#                 cv2.putText(img, "unknown", (x1, y2+y_offset+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

#             # rebuild a VideoFrame, preserving timing information
#             # img = cv2.resize(img,(0,0), None, 4, 4)
#             new_frame = VideoFrame.from_ndarray(img, format="bgr24")
#             new_frame.pts = frame.pts
#             new_frame.time_base = frame.time_base
#             return new_frame

        
#         else:
#             return frame


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def client_javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

    
async def main_javascript(request):
    content = open(os.path.join(ROOT, "main.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def call_css(request):
    content = open(os.path.join(ROOT, "call.css"), "r").read()
    return web.Response(content_type="application/css", text=content)

async def pikachu_png(request):
    data = Path("char-pikachu.png").read_bytes()
    return web.Response(body=data, content_type="image/png")
    # content = open(os.path.join(ROOT, "char-pikachu.png"), "rb").read()
    # return web.Response(content_type="image/png", text=content)

# async def offer(request):
#     params = await request.json()
#     offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

#     pc = RTCPeerConnection()
#     pc_id = "PeerConnection(%s)" % uuid.uuid4()
#     pcs.add(pc)

#     def log_info(msg, *args):
#         logger.info(pc_id + " " + msg, *args)

#     log_info("Created for %s", request.remote)

#     # prepare local media
#     # player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
#     # if args.write_audio:
#     #     recorder = MediaRecorder(args.write_audio)
#     # else:
#     #     recorder = MediaBlackhole()

#     # @pc.on("datachannel")
#     # def on_datachannel(channel):
#     #     @channel.on("message")
#     #     def on_message(message):
#     #         if isinstance(message, str) and message.startswith("ping"):
#     #             channel.send("pong" + message[4:])

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
#             pass
#             # pc.addTrack(player.audio)
#             # recorder.addTrack(track)
#         elif track.kind == "video":
#             local_video = VideoTransformTrack(
#                 track, transform=params["video_transform"]
#             )
#             pc.addTrack(local_video)

#         @track.on("ended")
#         async def on_ended():
#             log_info("Track %s ended", track.kind)
#             # await recorder.stop()

#     # @pc.on("iceconnectionstatechange")
#     # def on_iceconnectionstatechange():
#     #     print(pc.iceConnectionState)
#     #     print("###############")


#     # handle offer
#     await pc.setRemoteDescription(offer)
#     # await recorder.start()

#     # send answer
#     answer = await pc.createAnswer()
#     await pc.setLocalDescription(answer)
#     print(pc.localDescription)
#     print(pc.remoteDescription)

#     return web.Response(
#         content_type="application/json",
#         text=json.dumps(
#             {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
#         ),
#     )

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8081, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--write-audio", help="Write received audio to a file")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    print(args.cert_file)

    # if args.cert_file:
    #     ssl_context = ssl.SSLContext()
    #     ssl_context.load_cert_chain(args.cert_file, args.key_file)
    # else:
    #     ssl_context = None

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(args.cert_file, args.key_file)

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/client.js", client_javascript)
    app.router.add_get("/main.js", main_javascript)
    app.router.add_get("/call.css", call_css)
    app.router.add_get("/char-pikachu.png", pikachu_png)
    # app.router.add_post("/offer", offer)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
