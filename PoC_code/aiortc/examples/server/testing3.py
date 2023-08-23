import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import numpy as np

# import websocket

# import webbrowser
# import rel
import time

# from Screenshot import Screenshot_clipping

import cv2, face_recognition
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
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

        ## because not every frame to face recognization, so we need save the previous face location
        self.previousFaceRecNameLoc = {"name": None, "faceLoc": None}

        ## get the dataset/img file location
        self.path = "static/unknowImg"

        ## to keep dataset image name
        self.calssNames = []

        ## to keep dataset image encode for recognizing purpose
        self.encodeListKnown = []

        self.isFaceDetected = False

        ## to get the image and its name
        # images, self.calssNames = self.loadImgDataSet()

        ## to get a list of the image encode for face recoginzing purpose
        # self.encodeListKnown = self.findEncodings(images)
        # print("Encoding Complete")

        self.count = 0
        # self.haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.model_path = 'pose_landmarker_lite.task'

    async def recv(self):
        # print("asf")
        frame = await self.track.recv()

        if self.transform == "face_detection":
          object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
          img = frame.to_ndarray(format="bgr24")
          tmp_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
          gray_image = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
          cv2.imwrite("testing.jpg", gray_image)
          # print(type(img))
          height, width, _ = img.shape
          # print(height, width)

          # Extract Region of interest
          # roi = img[340:720 ,500:800]

          # Object Detection
          mask = object_detector.apply(gray_image)
          cv2.imwrite("testing1.jpg", mask)
          contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
          
          for cnt in contours:
            #Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 100:
              cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)

              

          # tmp_img = img.copy()
          # print('Original Dimensions : ', tmp_img.shape) # number of rows, columns (number of pixels), and channels
          # tmp_img = cv2.resize(tmp_img, (0, 0), None, 0.25, 0.25) # scale down 4 time smaller
          # print('Resized Dimensions : ', tmp_img.shape)
          # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

          ## only the first, middle, and last frame do the face detection and recognization process
          # if self.count == 0 or self.count % 3 == 0:
          #     ## pass each of frame to do the face process
          #     self.faceRecognized(img, self.encodeListKnown)

          # ## if the frame no face detect then the previous name and location need to clear
          # elif not self.isFaceDetected:
          #     self.previousFaceRecNameLoc["name"] = None
          #     self.previousFaceRecNameLoc["faceLoc"] = None

          # ## becuase above only pass first, middel and last frame to do face process, so other frame need use previous name and locatio value to do labling
          # elif self.previousFaceRecNameLoc["name"] is not None:
          #     self.boxForFaceDetect(
          #         img,
          #         self.previousFaceRecNameLoc["name"],
          #         self.previousFaceRecNameLoc["faceLoc"],
          #     )

          # ## this is to count the frame number
          # self.count = self.count + 1

          # ## once the count number equal to fps then loop again
          # if self.count == frameRate - 1:
          #     self.count = 0

          # rebuild a VideoFrame, preserving timing information
          # img = cv2.resize(img,(0,0), None, 4, 4)
          new_frame = VideoFrame.from_ndarray(img, format="bgr24")
          new_frame.pts = frame.pts
          new_frame.time_base = frame.time_base
          return new_frame
        else:
          return frame

    ##  face detect and compare with the date set
    def faceRecognized(self, img, tempEncodeListKnown):
        tmp_img = img.copy()

        ## because only the circle part will be do to the face recoginze, so need to crop the image
        # crop_image = self.faceCropped(img)

        # cv2.imwrite("testing.jpg", crop_image)

        imgS = cv2.resize(tmp_img, (0, 0), None, 0.5, 0.5)  # scale down 4 time smaller



        facesCurFrame = face_recognition.face_locations(
            imgS, number_of_times_to_upsample=1, model="cnn"
        )

        if facesCurFrame:
            crop_image = self.faceCropped(imgS, facesCurFrame[0])

            if len(crop_image) > 0:
                # Convert Python array to NumPy array
                crop_image = np.array(crop_image)
                newFacesCurFrame = face_recognition.face_locations(
                    crop_image, number_of_times_to_upsample=1, model="cnn"
                )
                # print(newFacesCurFrame)

                ## if has the face location, then equal a face detected
                if len(newFacesCurFrame) >= 0:
                    # print(facesCurFrame[0])
                    self.isFaceDetected = True
                    # crop_image = self.faceCropped(imgS, facesCurFrame[0])
                    # newFacesCurFrame = face_recognition.face_locations(crop_image, number_of_times_to_upsample=1, model='cnn')
                    # print(newFacesCurFrame)

                if self.isFaceDetected:

                    encodesCurFrame = face_recognition.face_encodings(
                        crop_image,
                        known_face_locations=newFacesCurFrame,
                        num_jitters=1,
                        model="small",
                    )

                    ## compare the unknow face with the dateset faces throught the encode
                    for encodeFace, faceLoc in zip(encodesCurFrame, newFacesCurFrame):
                        matches = face_recognition.compare_faces(
                            self.encodeListKnown, encodeFace, tolerance=0.45
                        )  ## return boolean
                        faceDis = face_recognition.face_distance(
                            self.encodeListKnown, encodeFace
                        )  ## return float
                        matchIndex = np.argmin(
                            faceDis
                        )  ## get the minimum value from the list

                        ## match the draw the box and label the name
                        if matches[matchIndex]:
                            name = self.calssNames[matchIndex].upper()
                            self.boxForFaceDetect(imgS, name, facesCurFrame[0])
                        else:
                            self.boxForFaceDetect(imgS, "unknown", facesCurFrame[0])
        else:
            self.isFaceDetected = False

    ## get the image and the person name
    def loadImgDataSet(self):
        images = []
        calssNames = []

        mainDirList = os.listdir(self.path)
        for folder in mainDirList:
            userFolder = os.path.join(self.path, folder)
            if os.path.isdir(userFolder):
                pictList = os.listdir(userFolder)
                for pic in pictList:
                    curImg = cv2.imread(os.path.join(userFolder, pic))
                    images.append(curImg)
                    calssNames.append(folder)

        return images, calssNames

    # refer https://www.geeksforgeeks.org/python-multiple-face-recognition-using-dlib/

    ## find the dataset encodings
    def findEncodings(self, images):
        encodeList = []
        index = 0
        for img in images:
            ## change the color from Blue, Green, Red to Red, Green, Blue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            try:
                ## encode each of the dataset image
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)

            except:
                ## if the dateset have a img which no any face, then deleted the img
                os.remove(f"{self.path}/{self.calssNames[index]}.jpg")

            finally:
                index += 1

        return encodeList

    ## draw the box and natation with name (images's name)
    def boxForFaceDetect(self, img, name, faceLoc):
        # h, w, _ = img.shape
        # offset = w - (w//2 + ((h//2)-20))

        x_offset = 15
        y_offset = 20

        ## for other frames which without do the face process
        self.previousFaceRecNameLoc["name"] = name
        self.previousFaceRecNameLoc["faceLoc"] = faceLoc

        ## because the face location is top, right, bottom, left
        y1, x2, y2, x1 = faceLoc

        ## because the frame is resize at begining so now resize back
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2

        ## draw a rectangle / box
        # cv2.rectangle(img, (x1+offset, y1), (x2+offset, y2+20), (0,255,0),2)
        cv2.rectangle(
            img,
            (x1 + (x_offset), y1 - y_offset),
            (x2 + (x_offset), y2 + y_offset),
            (0, 255, 255),
            2,
        )

        ## draw a filled rectangle / box
        cv2.rectangle(
            img,
            (x1 + (x_offset), y2 + (y_offset * 2 + 10)),
            (x2 + (x_offset), y2 + y_offset),
            (0, 255, 0),
            cv2.FILLED,
        )

        front_scale = float(((x2 + (x_offset)) - (x1 + (x_offset))) / 250)
        # print(front_scale)

        ## write the its name into the filled box
        cv2.putText(
            img,
            name,
            (x1 + (x_offset), y2 + (y_offset * 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            front_scale,
            (255, 255, 255),
            2,
        )

        # print(x1 + (x_offset*6), x2 + (x_offset*7))

    ## crop the face only keep the circle part
    def faceCropped(self, img, location):
        # offset = 20
        # height, width, _ = img.shape
        # center = (width//2, height//2)
        # radius = (height//2)-offset

        x_offset = 15
        y_offset = 20

        ## because the face location is top, right, bottom, left
        y1, x2, y2, x1 = location
        # y1,x2,y2,x1 = y1*2,x2*2,y2*2,x1*2
        # print(x1-10)
        # print(location)

        # img[y_start:y_end , x_start : x_end]
        cropped_image = img[
            (y1 if y1 - y_offset * 2 < 0 else y1 - y_offset * 2) : y2 + y_offset * 2,
            (x1 if x1 - x_offset * 2 < 0 else x1 - x_offset * 2) : x2 + x_offset * 2,
        ]
        # print(cropped_image)

        # cv2.imwrite("testing.jpg", cropped_image)
        # cropped_image = img[:, (x1 + (x_offset*6), y2+(y_offset*2+10)) : (x2 + (x_offset*7), y2+y_offset)]
        return cropped_image


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # prepare local media
    # player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
    # if args.write_audio:
    #     recorder = MediaRecorder(args.write_audio)
    # else:
    #     recorder = MediaBlackhole()

    # @pc.on("datachannel")
    # def on_datachannel(channel):
    #     @channel.on("message")
    #     def on_message(message):
    #         if isinstance(message, str) and message.startswith("ping"):
    #             channel.send("pong" + message[4:])

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            pass
            # pc.addTrack(player.audio)
            # recorder.addTrack(track)
        elif track.kind == "video":
            local_video = VideoTransformTrack(
                track, transform=params["video_transform"]
            )
            pc.addTrack(local_video)

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            # await recorder.stop()

    # @pc.on("iceconnectionstatechange")
    # def on_iceconnectionstatechange():
    #     print(pc.iceConnectionState)
    #     print("###############")

    # handle offer
    await pc.setRemoteDescription(offer)
    # await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print(pc.localDescription)
    print(pc.iceConnectionState)

    response = web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )
    print("sdfgsdfgsdfg")
    print(response.text)
    return response


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
        "--port", type=int, default=4200, help="Port for HTTP server (default: 8080)"
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
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
