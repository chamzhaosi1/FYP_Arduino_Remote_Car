import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import numpy as np
import imagehash
from PIL import Image
from collections import deque 

# import websocket

# import webbrowser
# import rel
import time, threading

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

    def __init__(self, track, transform, userName):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

        self.userName = userName

        ## because not every frame to face recognization, so we need save the previous face location
        self.previousFaceRecNameLoc = None

        ## get the dataset/img file location
        self.authorizedPath = "static/authorizedImg"

        ## save the unauthorized picture
        # self.unauthorizedPath = "static/unauthorizedImg"

        ## to keep dataset folder name
        # self.calssNames = []

        ## to keep dataset image encode for recognizing purpose
        # self.encodeListKnown = []

        ## to keep image position front, down ...
        # self.pictName = []
        
        ## check whether face detected
        self.isFaceDetected = False
        self.isFaceCapture = False
        self.shQueue = deque()
        
        ## count intruder face
        # self.intruderCount = 0

        ## to get the image and its name
        # images, self.calssNames, self.pictName = self.loadImgDataSet()

        # self.test = False

        ## to get a list of the image encode for face recoginzing purpose
        # self.findEncodings(images)
        # print("Encoding Complete")

        ## to incread the drawing the box
        self.x_offset = 15
        self.y_offset = 20

        ## to count the frame
        self.count = 0

        ## to name the image
        self.label = ""
    
        ## to clear the folder before live streaming starting
        self.clearImageDir()

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "face_detection":
            return self.face_detection_mode(frame)
        else:
            return frame

    def face_detection_mode(self, frame):
        img = frame.to_ndarray(format="bgr24")

        ## to let user focus on inside circle only 
        img = self.blurWithCenterClear(img)

        ## only the first, and every 10th frame do the face detection and recognization process
        if self.count == 0 or self.count % 10 == 0:
            ## pass each of frame to do the face process
            self.faceDetected(img)
        
        ## if the frame no face detect then the previous name and location need to clear
        elif not self.isFaceDetected:
            self.previousFaceRecNameLoc = None

        ## becuase above only pass first, middel and last frame to do face process, so other frame need use previous name and locatio value to do labling
        else:
            self.boxForFaceDetect(img, "", self.previousFaceRecNameLoc)

            
        ## this is to count the frame number
        self.count = self.count + 1

        ## rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame

    ##  face detect and compare with the date set
    def faceDetected(self, img):
        ## temperary copy the img to do further process (face detection and recognization)
        tmp_img = img.copy()

        ## scale down the image to improve the process speed
        imgS = cv2.resize(tmp_img, (0, 0), None, 0.5, 0.5)  # scale down 2 time smaller

        ## using the scale down image the do face detection
        facesCurFrame = face_recognition.face_locations(imgS)

        ## if the face detected
        if facesCurFrame:
            ## set the face is detected
            self.isFaceDetected = True

            ## crop the only the face 
            crop_image = self.faceCropped(imgS, facesCurFrame[0])

            ## convert Python array to NumPy array
            crop_image = np.array(crop_image)

            print(self.isFaceCapture)
            if self.isFaceCapture:
                self.captureUnknownImg(crop_image, self.label)

            self.boxForFaceDetect(img, "", facesCurFrame[0])
            self.previousFaceRecNameLoc = facesCurFrame[0]
            
        #     ## find face location from the crop_image 
        #     newFacesCurFrame = face_recognition.face_locations(
        #         crop_image, number_of_times_to_upsample=1, model="cnn"
        #     )
            
        #     ## set the face is detected
        #     self.isFaceDetected = True

        #     if self.isFaceDetected:
        #         ## face encodings the crope image 
        #         encodesCurFrame = face_recognition.face_encodings(
        #             crop_image,
        #             known_face_locations=newFacesCurFrame,
        #             num_jitters=2,
        #             model="large",
        #         )

        #         ## compare the unknow face with the dateset faces throught the encode
        #         for encodeFace in encodesCurFrame:
        #             matches = face_recognition.compare_faces(
        #                 self.encodeListKnown, encodeFace, tolerance=0.45
        #             )  ## return boolean
        #             faceDis = face_recognition.face_distance(
        #                 self.encodeListKnown, encodeFace
        #             )  ## return float
        #             matchIndex = np.argmin(
        #                 faceDis
        #             )  ## get the minimum value from the list

        #             ## match the draw the box and label the name
        #             if matches[matchIndex]:
        #                 name = self.calssNames[matchIndex].upper()
        #                 self.boxForFaceDetect(imgS, name, facesCurFrame[0])
        #                 self.intruderCount = 0
        #             else:
        #                 self.boxForFaceDetect(imgS, "Intruder found", facesCurFrame[0])
        #                 self.intruderCount = self.intruderCount + 1

        #                 ## if detected more than 10 time 
                        
        #                 if self.intruderCount > 10:
        #                     self.captureUnknownImg(crop_image, "intruder")
        else:
            self.isFaceDetected = False

    ## save the img to the data set
    def captureUnknownImg(self, unknownImage, imgName):
        # Convert the NumPy array to a PIL image object
        image = Image.fromarray(unknownImage)

        # Compute the hash value of the image
        hash_value = imagehash.average_hash(image)

        imgName = "-".join([imgName, str(hash_value)])

        print(f'{self.authorizedPath}/{self.userName}/{imgName}.jpg')

        folder_path = os.path.join(self.authorizedPath, self.userName)
        # Check if the folder already exists
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
            print("Folder created successfully.")
        else:
            print("Folder already exists.")

        cv2.imwrite(f'{folder_path}/{imgName}.jpg', unknownImage)
        
        ## reset the count
        self.isFaceCapture = False

    ## blur other part of the circle
    def blurWithCenterClear(self, img):
        ## to reduce some value of the hight
        offset = 20
        height, width, _ = img.shape
        center = (width//2, height//2)
        radius = (height//2)-offset

        ## blur the image
        blurred_img = cv2.GaussianBlur(img, (51, 51), 0)

        ## create a whole black image with a circle
        mask = np.zeros((height, width, 3), dtype=np.uint8)
        mask = cv2.circle(mask, center, radius, (255,255,0), -1)

        ## this np.where is to campare each of the array element and when it is not circle element then should be img element else blurred_img 
        out = np.where(mask==np.array([255, 255, 0]), img, blurred_img)

        ## draw the circle again
        cv2.circle(out, center, radius, (37, 88, 110), 3)
        return out

    # ## get the image and the person name
    # def loadImgDataSet(self):
    #     images = []
    #     calssNames = []
    #     pictName= []

    #     ## load all folder
    #     mainDirList = os.listdir(self.authorizedPath)
    #     for folder in mainDirList:
    #         userFolder = os.path.join(self.authorizedPath, folder)
    #         if os.path.isdir(userFolder):
    #             ## load the image in each of the folder
    #             pictList = os.listdir(userFolder)
    #             print(userFolder)
    #             for pic in pictList:
    #                 print(pic)
    #                 curImg = cv2.imread(os.path.join(userFolder, pic))
    #                 ## append the image 
    #                 images.append(curImg)
    #                 ## append the folder name
    #                 calssNames.append(folder)
    #                 ## append the picture name
    #                 pictName.append(pic)

    #     return images, calssNames, pictName

    # ## find the dataset encodings
    # def findEncodings(self, images):
    #     index = 0
    #     for img in images:
    #         ## change the color from Blue, Green, Red to Red, Green, Blue
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #         try:
    #             ## encode each of the dataset image
    #             encode = face_recognition.face_encodings(img)[0]
    #             self.encodeListKnown.append(encode)

    #         except:
    #             ## if the dateset have a img which no any face, then deleted the img
    #             # os.remove(f"{self.authorizedPath}/{self.calssNames[index]}.jpg")
    #             print(f"{self.authorizedPath}/{self.calssNames[index]}/{self.pictName[index]} got image not face detect!")

    #         finally:
    #             index += 1


    ## draw the box and natation with name (images's name)
    def boxForFaceDetect(self, img, name, faceLoc):
        ## for other frames which without do the face process
        # self.previousFaceRecNameLoc["name"] = name
        # self.previousFaceRecNameLoc["faceLoc"] = faceLoc

        ## because the face location is top, right, bottom, left
        y1, x2, y2, x1 = faceLoc

        ## because the frame is resize at begining so now resize back
        y1, x2, y2, x1 = y1 * 2 , x2 * 2, y2 * 2, x1 * 2

        if name != "Intruder found":
            boxColor = (78, 159, 61)
            frontColor = (255, 255, 255)
            fillColor = (30, 81, 40)
        else:
            boxColor = (71, 77, 201)
            frontColor = (255, 255, 255)
            fillColor = (31, 37, 156)

        ## draw a rectangle / box
        cv2.rectangle(
            img,
            (x1 + (self.x_offset), y1 - self.y_offset),
            (x2 + (self.x_offset), y2 + self.y_offset),
            boxColor,
            2,
        )

        # ## draw a filled rectangle / box
        # cv2.rectangle(
        #     img,
        #     (x1 + (self.x_offset), y2 + (self.y_offset * 2 + 10)),
        #     (x2 + (self.x_offset), y2 + self.y_offset),
        #     fillColor,
        #     cv2.FILLED,
        # )

        # front_scale = float(((x2 + (self.x_offset)) - (x1 + (self.x_offset))) / 250)

        ## write the its name into the filled box
        # cv2.putText(
        #     img,
        #     name,
        #     (x1 + (self.x_offset), y2 + (self.y_offset * 2)),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     front_scale,
        #     frontColor,
        #     2,
        # )

    ## crop the face only keep the circle part
    def faceCropped(self, img, location):
        ## face location top, right, bottom, left
        y1, x2, y2, x1 = location

        cropped_image = img[
            (y1 if y1 - self.y_offset * 2 < 0 else y1 - self.y_offset * 2) : y2 + self.y_offset * 2,
            (x1 if x1 - self.x_offset * 2 < 0 else x1 - self.x_offset * 2) : x2 + self.x_offset * 2,
        ]
        
        ## return cropped image
        return cropped_image
    
    def clearImageDir(self):
        mainPath = "static/unauthorizedImg/"
        endwith = ".jpg"
        image_path = None

        mainDirList = os.listdir(mainPath)
        print(len(mainDirList))
        if len(mainDirList) > 0:
            for file in mainDirList:
                image_path = os.path.join(mainPath, file)
                os.remove(image_path)
    
    def captureImage(self, label):
        self.isFaceCapture = True
        self.label = label

    def resetCaptureFlag(self):
        self.isFaceCapture = False

local_video : any

async def activeCapture(request):
    global local_video
    params = await request.json()
    print(params)
    local_video.captureImage(params['label'])

    response = web.Response(text="successfully", content_type='text/plain')
    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    return response

async def retrieveCaptureImg(request):
    params = await request.json()
    try:
        mainPath = "static/authorizedImg/"
        endwith = ".jpg"
        userName = params['userName']

        mainDir = os.path.join(mainPath, userName)
        mainDirList = os.listdir(mainDir)
        print(len(mainDirList))
        if len(mainDirList) > 0:
            image_filename = mainDirList[0]
            print(image_filename)
            if image_filename.endswith(endwith):
                print(os.path.join(mainDir, image_filename))
                image_path = os.path.join(mainDir, image_filename)
                with open(image_path, 'rb') as file:
                    image_data = file.read()
                    os.remove(image_path)
        
        response = web.Response(body=image_data, content_type='image/jpeg')

    except UnboundLocalError :
        local_video.resetCaptureFlag()
        response = web.Response(text="some thing wrong", content_type='text/plain')


    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    return response


async def handle_options(request):
    response = web.Response()
    response.headers['Access-Control-Allow-Origin'] = 'https://romo.kynoci.com:4200'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

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
            global local_video
            local_video = VideoTransformTrack(
                track, transform=params["video_transform"],
                userName = params["userName"]
            )
            pc.addTrack(local_video)

            # # Create thread objects
            # thread1 = VideoThread(track, params["video_transform"], pc)
            # # Start the threads
            # thread1.start()    

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
    # print(pc.localDescription)
    # print(pc.iceConnectionState)

    response = web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    # print("sdfgsdfgsdfg")
    # print(response.text)
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
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/retrieve",retrieveCaptureImg)
    app.router.add_post("/offer", offer)
    app.router.add_post("/capture", activeCapture)
    app.router.add_route('OPTIONS', '/capture', handle_options)
    app.router.add_route('OPTIONS', '/retrieve', handle_options)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
