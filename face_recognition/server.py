import argparse, asyncio, json, logging, os, ssl, uuid, base64, cv2, face_recognition, time, random
from cvzone.PoseModule import PoseDetector
import numpy as np
from PIL import Image
from aiohttp import web
from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from mqtt import MQTT_Class

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform, userName, mac_address):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

        ## for save the image purpose
        self.userName = userName

        ## for save the mac_address
        self.mac_address = mac_address

        ## because not every frame to face recognization, so we need save the previous face location
        self.previousFaceRecNameLoc = [{"name": None, "faceLoc": None}]

        ## to save the authorized image when user using camera function
        self.saveAuthorizedPath = "static/authorizedImg"

        ## get the dataset/authorized img file location
        self.getAuthorizedPath = (
            "/home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized"
        )

        ## get the dataset/intruder img file location
        self.getIntruderPath = (
            "/home/engineer/romo_v2/romo_web/backend/romo_back/media/intrusion"
        )

        ## save the unauthorized picture
        self.saveUnauthorizedPath = "static/unauthorizedImg"

        ## to keep dataset folder name
        self.classNames = []

        ## to keep image position front, down ...
        self.pictName = []

        ## to keep dataset image
        self.images = []

        ## to save intruder name, to check whether already send one current intruder image to back for this time
        self.saveIntrImageName = []
        self.recordExistIntrCount = []

        ## to keep dataset image encode for recognizing purpose
        self.encodeListKnown = []

        ## check whether face detected
        self.isFaceDetected = False

        ## check whether users want to capture thier face
        self.isFaceCapture = False

        self.isExistIntrFaceDetected = False

        ## count intruder face
        self.intruderCount = []

        ## count intruder alert
        self.intruderAlertCount = 0

        ## to get the image and its name
        self.loadAuthImgDataSet()
        self.loadIntrImgDataSet()

        print(self.pictName)

        ## to get a list of the image encode for face recoginzing purpose
        self.findEncodings(self.images)
        print("Encoding Complete")

        print(self.pictName)

        ## to incread the drawing the box
        self.x_offset = 15
        self.y_offset = 20

        ## to count the frame
        self.count = 0

        ## to name the image
        self.label = ""

        ## to clear the auth and intr folder before live streaming starting
        self.clearAuthImageDir()
        self.clearIntrImageDir()

        ## initial the mqtt class
        self.mqtt = MQTT_Class()

        self.pose_detector = PoseDetector()

        self.bboxInfo_array = []

    async def recv(self):
        # print("asf")
        frame = await self.track.recv()

        img = frame.to_ndarray(format="bgr24")

        ## only the first, and every 10th frame do the face detection and recognization process
        if self.count == 0 or self.count % 10 == 0:
            self.previousFaceRecNameLoc = []
            self.bboxInfo_array = []
            ## pass each of frame to do the face process
            self.faceRecognized(img)

            if self.transform != "face_detection":
                self.poseDetection(img)

        ## if the frame no face detect then the previous name and location need to clear
        elif not self.isFaceDetected:
            if len(self.previousFaceRecNameLoc) > 0:
                for eachFaceRecNameLoc in self.previousFaceRecNameLoc:
                    eachFaceRecNameLoc["name"] = None
                    eachFaceRecNameLoc["faceLoc"] = None

        ## becuase above only pass first and every 10th frame to do face process, so other frame need use previous name and locatio value to do labling
        elif (
            len(self.previousFaceRecNameLoc) > 0
            and self.previousFaceRecNameLoc[0]["faceLoc"] is not None
        ):
            for eachFaceRecNameLoc in self.previousFaceRecNameLoc:
                self.boxForFaceDetect(
                    img,
                    eachFaceRecNameLoc["name"],
                    eachFaceRecNameLoc["faceLoc"],
                    isSkipFrame=True,
                )

        ## this is to count the frame number
        self.count = self.count + 1

        if self.transform == "face_detection":
            ## to let user focus on inside circle only
            ## this function must be below / before the frame use to capture
            img = self.blurWithCenterClear(img)
        else:
            self.drawPoseBox(img)

        ## rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame

    ## this function is to find the person and get the location and width, high value
    def poseDetection(self, img):
        ## this dependency is to detect / recognis the human pose
        ## but we use it just to find a person who is far away with our device
        img = self.pose_detector.findPose(img, draw=False)
        lmList, bboxInfo = self.pose_detector.findPosition(img, bboxWithHands=False)

        if bboxInfo:
            self.bboxInfo_array.append(bboxInfo)

    ## base on the loaction record, we draw a box and a circle about the person
    def drawPoseBox(self, img):
        if len(self.bboxInfo_array) > 0:
            bbox = self.bboxInfo_array[0]["bbox"]
            center = self.bboxInfo_array[0]["center"]

            cv2.rectangle(img, bbox, (255, 100, 255), 2)
            cv2.circle(img, center, 2, (255, 0, 0), cv2.FILLED)

    ##  face detect and compare with the date set
    def faceRecognized(self, img):
        ## temperary copy the img to do further process (face detection and recognization)
        tmp_img = img.copy()

        ## scale down the image to improve the process speed
        imgS = cv2.resize(tmp_img, (0, 0), None, 0.5, 0.5)  # scale down 2 time smaller

        ## using the scale down image the do face detection
        facesCurFrame = face_recognition.face_locations(
            imgS, number_of_times_to_upsample=2, model="cnn"
        )

        ## if the face detected
        if facesCurFrame:
            ## set the face is detected
            self.isFaceDetected = True
            crop_image_list = []

            ## crop the only the face
            if len(facesCurFrame) > 0:
                for eachFacesCurFrame in facesCurFrame:
                    crop_image_list.append(self.faceCropped(imgS, eachFacesCurFrame))

            # print("crop_image_list: ", len(crop_image_list))
            ## convert Python array to NumPy array
            if len(crop_image_list) > 0:
                for index, each_crop_image in enumerate(crop_image_list):
                    crop_image = np.array(each_crop_image)

                    if self.transform == "face_detection":
                        if self.isFaceCapture:
                            self.captureUnknownImg(crop_image, self.label, -1)

                        self.boxForFaceDetect(img, "", facesCurFrame[index])
                        self.previousFaceRecNameLoc[index]["faceLoc"] = facesCurFrame[
                            index
                        ]

                    else:
                        ## find face location from the crop_image
                        # newFacesCurFrame = face_recognition.face_locations(
                        #     crop_image, number_of_times_to_upsample=1, model="cnn"
                        # )
                        newFacesCurFrame = face_recognition.face_locations(crop_image)
                        if self.isFaceDetected:
                            ## if database has presave authorized image
                            if len(self.encodeListKnown) > 0:
                                ## face encodings the crope image
                                encodesCurFrame = face_recognition.face_encodings(
                                    crop_image,
                                    known_face_locations=newFacesCurFrame,
                                    num_jitters=3,
                                    model="large",
                                )

                                if len(encodesCurFrame) > 0:
                                    ## compare the unknow face with the dateset faces throught the encode
                                    for encodeFace in encodesCurFrame:
                                        matches = face_recognition.compare_faces(
                                            self.encodeListKnown,
                                            encodeFace,
                                            tolerance=0.3,
                                        )  ## return boolean
                                        faceDis = face_recognition.face_distance(
                                            self.encodeListKnown, encodeFace
                                        )  ## return float
                                        matchIndex = np.argmin(
                                            faceDis
                                        )  ## get the minimum value from the list
                                        print("matchIndex: ", matchIndex)
                                        print("matches: ", matches)

                                        ## match the draw the box and label the name
                                        if matches[matchIndex]:
                                            name = self.classNames[matchIndex].upper()
                                            self.boxForFaceDetect(
                                                imgS, name, facesCurFrame[index]
                                            )
                                            # self.intruderCount = []

                                            ## if the name of image exist intruder, then
                                            if name.lower().startswith("intruder"):
                                                self.intruderAlertCount = (
                                                    self.intruderAlertCount + 1
                                                )
                                                self.foundExistIntr(
                                                    crop_image, name.lower()
                                                )

                                        else:
                                            ## if the face is not recogninzed, then
                                            ## recode the count of the unauthorized face
                                            if len(self.intruderCount) < index + 1:
                                                self.intruderCount.append(1)
                                            else:
                                                self.intruderCount[index] = (
                                                    self.intruderCount[index] + 1
                                                )

                                            self.intruderAlertCount = (
                                                self.intruderAlertCount + 1
                                            )
                                            self.boxForFaceDetect(
                                                imgS,
                                                "New Intruder Found",
                                                facesCurFrame[index],
                                            )

                                            print(self.intruderCount)
                                            print(index)

                                            ## if detected more than 5 time
                                            if self.intruderCount[index] > 5:
                                                self.captureUnknownImg(
                                                    crop_image, "Intruder", index
                                                )
                                else:
                                    ## to prevent the list out of range, when the lenght of the encodesCurFrame is 0
                                    if len(self.intruderCount) < index + 1:
                                        self.intruderCount.append(0)

                            ## if don have the presave image, then directly to intruder
                            else:
                                if len(self.intruderCount) < index + 1:
                                    self.intruderCount.append(1)
                                else:
                                    self.intruderCount[index] = (
                                        self.intruderCount[index] + 1
                                    )

                                self.intruderAlertCount = self.intruderAlertCount + 1
                                self.boxForFaceDetect(
                                    imgS, "New Intruder Found", facesCurFrame[index]
                                )

                                ## if detected more than 5 time
                                if self.intruderCount[index] > 5:
                                    self.captureUnknownImg(
                                        crop_image, "Intruder", index
                                    )

        else:
            self.isFaceDetected = False
            self.intruderCount = []
            self.intruderAlertCount = 0

    ## if detected 5 time exiting intruder, then capture the face
    def foundExistIntr(self, crop_image, intrName):
        for i, element in enumerate(self.saveIntrImageName):
            if element == intrName.lower():
                self.recordExistIntrCount[i] = self.recordExistIntrCount[i] + 1

                if self.recordExistIntrCount[i] > 5:
                    self.isExistIntrFaceDetected = True
                    self.captureUnknownImg(crop_image, intrName, -1)
                    self.recordExistIntrCount[i] = 0

    ## save the img to the data set
    def captureUnknownImg(self, unknownImage, imgName, index):
        # Convert the NumPy array to a PIL image object
        # image = Image.fromarray(unknownImage)

        # Compute the hash value of the image
        # hash_value = imagehash.average_hash(image)

        ## if the label name is not include "intruder", then
        if not ("intruder" in imgName.lower()):
            self.createFolder(self.saveAuthorizedPath, self.userName)
            cv2.imwrite(
                f"{self.saveAuthorizedPath}/{self.userName}/{imgName}.jpg", unknownImage
            )

        ## if new intruder face detected, then
        elif not self.isExistIntrFaceDetected:
            ## generate a random number
            newImgName = "-".join(["intruder", str(self.generate_random_number())])

            ## create a folder to keep the image
            self.createFolder(self.saveUnauthorizedPath, self.userName)
            cv2.imwrite(
                f"{self.saveUnauthorizedPath}/{self.userName}/{newImgName}.jpg",
                unknownImage,
            )
            ## get it's path
            newIntruderImg = os.path.join(
                self.saveUnauthorizedPath,
                self.userName,
                ("".join([newImgName, ".jpg"])),
            )
            print("New Intruder Image: ", newIntruderImg)

            ## append it into the known face list
            self.classNames.append(newImgName)
            self.saveIntrImageName.append(newImgName)
            self.recordExistIntrCount.append(0)
            self.pictName.append("".join([newImgName, ".jpg"]))

            ## get the encode of the it
            self.findEncodings(
                [cv2.imread(newIntruderImg)], addOn=len(self.classNames) - 1
            )

            ## topic to mqtt to public / notice frontend there a intruter found
            if self.mac_address != "":
                path = "/".join(["romo", self.mac_address, "ROMO_intrusion_found"])

            message_data = {"warning": "Intruder Found", "image_name": newImgName}
            print("Send Intruder Found: ", newImgName)
            self.mqtt.public_message(path, message_data)

        ## if a old intruder face is detected
        elif self.isExistIntrFaceDetected:
            ## create a folder and save the image
            self.createFolder(self.saveUnauthorizedPath, self.userName)
            cv2.imwrite(
                f"{self.saveUnauthorizedPath}/{self.userName}/{imgName}.jpg",
                unknownImage,
            )

            ## mqtt topic, to inform frontend a exist intruder is found
            if self.mac_address != "":
                path = "/".join(
                    ["romo", self.mac_address, "ROMO_exist_intrusion_found"]
                )

            message_data = {"warning": "Exist Intruder Found", "image_name": imgName}

            self.mqtt.public_message(path, message_data)
            self.isExistIntrFaceDetected = False

        if index != -1:
            ## reset the count
            self.intruderCount[index] = 0

        self.isFaceCapture = False

    ## create folder
    def createFolder(self, mainPath, subPath):
        folder_path = os.path.join(mainPath, subPath)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
            print("Folder created successfully. : ", folder_path)
        else:
            print("Folder already exists.: ", folder_path)

    ## blur other part of the circle
    def blurWithCenterClear(self, img):
        ## to reduce some value of the hight
        offset = 20
        height, width, _ = img.shape
        center = (width // 2, height // 2)
        radius = (height // 2) - offset

        ## blur the image
        blurred_img = cv2.GaussianBlur(img, (51, 51), 0)

        ## create a whole black image with a circle
        mask = np.zeros((height, width, 3), dtype=np.uint8)
        mask = cv2.circle(mask, center, radius, (255, 255, 0), -1)

        ## this np.where is to campare each of the array element and when it is not circle element then should be img element else blurred_img
        out = np.where(mask == np.array([255, 255, 0]), img, blurred_img)

        ## draw the circle again
        cv2.circle(out, center, radius, (37, 88, 110), 3)

        return out

    ## get the auth image and the person name
    def loadAuthImgDataSet(self):
        ## load all authorized folder
        # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized
        mainDirList = os.listdir(self.getAuthorizedPath)

        # ROMO user = [cham, lim, tan, jacky, ...]
        for folder in mainDirList:
            # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized/cham
            userFolder = os.path.join(self.getAuthorizedPath, folder)
            personFolderList = os.listdir(userFolder)

            # ROMO user's authorized folder = [cham_zhao_si, mother, father, ...]
            for personFolder in personFolderList:
                # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized/cham/cham_zhao_si
                personFolderPath = os.path.join(userFolder, personFolder)
                pictList = os.listdir(personFolderPath)

                # authorized img in folder = [cham_zhao_si-81, cham_zhao_si-82, ...]
                for pic in pictList:
                    # print(os.path.join(personFolderPath, pic))

                    # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized/cham/cham_zhao_si/cham_zhao_si-81.jpg
                    curImg = cv2.imread(os.path.join(personFolderPath, pic))

                    ## append the image
                    self.images.append(curImg)

                    ## append the folder name (cham_zhao_si, mother, father, ...)
                    self.classNames.append(personFolder)

                    ## append the picture name (cham_zhao_si-81, cham_zhao_si-82, ...)
                    self.pictName.append(pic)

    ## get the intr image and the person name
    def loadIntrImgDataSet(self):
        ## load all intruder folder
        # /home/engineer/romo_v2/romo_web/backend/romo_back/media/intruder
        mainDirList = os.listdir(self.getIntruderPath)

        # ROMO user = [cham, lim, tan, jacky, ...]
        for folder in mainDirList:
            # /home/engineer/romo_v2/romo_web/backend/romo_back/media/intruder/cham
            userFolder = os.path.join(self.getIntruderPath, folder)
            intruderLabelList = os.listdir(userFolder)

            # ROMO user's intruder folder = [intruder-81, intruder-82, intruder-83, ...]
            for intruderLabelFolder in intruderLabelList:
                # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized/cham/intruder-81
                personFolderPath = os.path.join(userFolder, intruderLabelFolder)
                intrPictList = os.listdir(personFolderPath)

                self.saveIntrImageName.append(intruderLabelFolder)
                self.recordExistIntrCount.append(0)

                # authorized img in folder = [intruder-81, intruder-82, ...]
                for intrPic in intrPictList:
                    # print(intrPic)

                    # /home/engineer/romo_v2/romo_web/backend/romo_back/media/authorized/cham/intruder-81.jpg
                    curImg = cv2.imread(os.path.join(personFolderPath, intrPic))

                    ## append the image
                    self.images.append(curImg)

                    ## append the folder name (intruder-81,intruder-82, intruder-83, ...)
                    self.classNames.append(intruderLabelFolder)

                    ## append the picture name (intruder-81,intruder-82, intruder-83, ...)
                    self.pictName.append(intruderLabelFolder)

        # print(self.saveIntrImageName)

    ## find the dataset encodings
    def findEncodings(self, images, addOn=0):
        for index, img in enumerate(images):
            ## change the color from Blue, Green, Red to Red, Green, Blue
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            try:
                ## encode each of the dataset image
                encode = face_recognition.face_encodings(img)[0]
                self.encodeListKnown.append(encode)

            except:
                ## if the dateset have a img which no any face, then deleted the img
                # os.remove(f"{self.authorizedPath}/{self.classNames[index]}.jpg")
                print(
                    f"{self.getAuthorizedPath}/{self.classNames[index+addOn]}/{self.pictName[index+addOn]} got image not face detect!"
                )
                ## once the image is not face detect, then need to remove element from the image, className and pictName array
                self.images.pop(index)
                self.classNames.pop(index)
                self.pictName.pop(index)

    # def clearAllArrayElement(self):
    #     self.encodeListKnown = []
    #     self.images = []
    #     self.classNames = []
    #     self.pictName = []

    ## draw the box and natation with name (images's name)
    def boxForFaceDetect(self, img, name, faceLoc, isSkipFrame=False):
        ## for other frames which without do the face process
        # self.previousFaceRecNameLoc["name"] = name
        # self.previousFaceRecNameLoc["faceLoc"] = faceLoc
        if not isSkipFrame:
            self.previousFaceRecNameLoc.append({"name": name, "faceLoc": faceLoc})

        ## because the face location is top, right, bottom, left
        y1, x2, y2, x1 = faceLoc

        ## because the frame is resize at begining so now resize back
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2

        if not ("intruder" in name.lower()):
            boxColor = (78, 159, 61)  ## red
            frontColor = (255, 255, 255)  ## white
            fillColor = (30, 81, 40)
        else:
            boxColor = (71, 77, 201)  ## green
            frontColor = (255, 255, 255)  ## white
            fillColor = (31, 37, 156)

        ## draw a rectangle / box
        cv2.rectangle(
            img,
            (x1 + (self.x_offset), y1 - self.y_offset),
            (x2 + (self.x_offset), y2 + self.y_offset),
            boxColor,
            2,
        )

        ## only face recognition mode put the name of person and
        if self.transform == "face_recognition":
            ## draw a filled rectangle / box
            cv2.rectangle(
                img,
                (x1 + (self.x_offset), y2 + (self.y_offset * 2 + 10)),
                (x2 + (self.x_offset), y2 + self.y_offset),
                fillColor,
                cv2.FILLED,
            )

            front_scale = float(((x2 + (self.x_offset)) - (x1 + (self.x_offset))) / 250)

            ## write the its name into the filled box
            cv2.putText(
                img,
                name,
                (x1 + (self.x_offset), y2 + (self.y_offset * 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                front_scale,
                frontColor,
                2,
            )

            ## once detected the intruder face more then 5 time, a notice will be mqtt publc to notice the frontend alert play
            if (
                self.intruderAlertCount >= 5
                and self.intruderAlertCount % 5 == 0
                and self.mac_address != ""
            ):
                path = "/".join(["romo", self.mac_address, "ROMO_intrusion_alert"])

                alert_message = {"warning": "Intruder Alert"}

                self.mqtt.public_message(path, alert_message)
                self.intruderAlertCount = 0

    ## crop the face only keep the circle part
    def faceCropped(self, img, location):
        ## face location top, right, bottom, left
        y1, x2, y2, x1 = location

        cropped_image = img[
            (y1 if y1 - self.y_offset * 2 < 0 else y1 - self.y_offset * 2) : y2
            + self.y_offset * 2,
            (x1 if x1 - self.x_offset * 2 < 0 else x1 - self.x_offset * 2) : x2
            + self.x_offset * 2,
        ]

        ## return cropped image
        return cropped_image

    # To prevent same name image crash
    def generate_random_number(self):
        # Generate 4 bytes of truly random data
        random_bytes = os.urandom(2)
        random_int = int.from_bytes(random_bytes, byteorder="big")
        current_time = int(time.time())  # Get the current time as a Unix timestamp
        random.seed(current_time)  # Set the random seed based on the current time
        random_number = random.randint(
            1, 100
        )  # Generate a random number between 1 and 100
        return random_number + random_int

    ## make sure every time run the server the folder is empty, so the image retrieve by user/frontend is the lastest one
    def clearAuthImageDir(self):
        try:
            # static/authorizedImg/cham
            mainAuthPath = os.path.join(self.saveAuthorizedPath, self.userName)
            mainAuthDirList = os.listdir(mainAuthPath)

            # authorised image in device user's folder = [lim-01, lim-02]
            if len(mainAuthDirList) > 0:
                # iterate each of the image and remove them
                for file in mainAuthDirList:
                    image_path = os.path.join(mainAuthPath, file)
                    os.remove(image_path)

        except FileNotFoundError:
            print("Not File Found")

    ## make sure every time run the server the folder is empty, so the image retrieve by user/frontend is the lastest one
    def clearIntrImageDir(self):
        try:
            # static/unuthorizedImg/cham
            mainIntrPath = os.path.join(self.saveUnauthorizedPath, self.userName)
            mainIntrDirList = os.listdir(mainIntrPath)

            # authorised image in device user's folder = [lim-01, lim-02]
            if len(mainIntrDirList) > 0:
                # iterate each of the image and remove them
                for file in mainIntrDirList:
                    image_path = os.path.join(mainIntrPath, file)
                    os.remove(image_path)

        except FileNotFoundError:
            print("Not File Found")

    def captureImage(self, label):
        self.isFaceCapture = True
        self.label = label

    def resetCaptureFlag(self):
        self.isFaceCapture = False


local_video: any


async def activeCapture(request):
    global local_video
    params = await request.json()
    print(params)
    ## Set the capture flag is true to able user snapshot the their face image
    local_video.captureImage(params["label"])

    response = web.Response(text="successfully", content_type="text/plain")
    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    return response


async def retrieveCaptureImg(request):
    params = await request.json()
    try:
        mainPath = "static/authorizedImg/"
        userName = params["userName"]

        # static/authorizedImg/cham
        mainDir = os.path.join(mainPath, userName)
        mainDirList = os.listdir(mainDir)

        # authorised image in device user's folder = [lim-01]
        if len(mainDirList) > 0:
            # get first image from the array, Remark: This is becuase the array must only a single image
            image_filename = mainDirList[0]

            # static/authorizedImg/cham/lim-01.jpg
            image_path = os.path.join(mainDir, image_filename)

            # read the image byte
            with open(image_path, "rb") as file:
                image_data = file.read()

            # remove the image from the folder
            os.remove(image_path)
            print("Image has been removed: ", image_path)

        response = web.Response(body=image_data, content_type="image/jpeg")

    except UnboundLocalError:
        local_video.resetCaptureFlag()
        response = web.Response(text="some thing wrong", content_type="text/plain")

    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    return response


async def retrieveIntruderImg(request):
    params = await request.json()
    try:
        mainPath = "static/unauthorizedImg/"
        userName = params["userName"]
        intrLabel = params["intrLabel"]
        imageArray = []

        # static/unauthorizedImg/cham
        mainDir = os.path.join(mainPath, userName)

        # unauthorized image in device user's folder = [intruder-89, intruder-90, ...]
        ## Remark: This will has the multiple image, because it may detect multiple intruders' face in a frame
        mainDirList = os.listdir(mainDir)
        if len(mainDirList) > 0:
            # iterate each of the image
            for image_filename in mainDirList:
                if image_filename.startswith(intrLabel):
                    # static/unauthorizedImg/cham/intruder-89.jpg
                    image_path = os.path.join(mainDir, image_filename)

                    # read the image byte
                    with open(image_path, "rb") as file:
                        image_data = file.read()
                        image_base64 = base64.b64encode(image_data).decode("utf-8")
                        imageArray.append(image_base64)

                    # remove the image from the folder
                    os.remove(image_path)
                    print("Image has been removed: ", image_path)

        response = web.Response(
            text=json.dumps(imageArray), content_type="application/json"
        )

    except UnboundLocalError:
        local_video.resetCaptureFlag()
        response = web.Response(text="some thing wrong", content_type="text/plain")

    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    return response


async def handle_options(request):
    response = web.Response()
    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# async def index(request):
#     content = open(os.path.join(ROOT, "index.html"), "r").read()
#     return web.Response(content_type="text/html", text=content)


# async def javascript(request):
#     content = open(os.path.join(ROOT, "client.js"), "r").read()
#     return web.Response(content_type="application/javascript", text=content)


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

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
        elif track.kind == "video":
            global local_video
            local_video = VideoTransformTrack(
                track,
                transform=params["video_transform"],
                userName=params["userName"],
                mac_address=params["mac_address"],
            )
            pc.addTrack(local_video)

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            # await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    response = web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

    response.headers["Access-Control-Allow-Origin"] = "https://romo.kynoci.com:4200"
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

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(args.cert_file, args.key_file)

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    # app.router.add_get("/", index)
    # app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    app.router.add_post("/capture", activeCapture)
    app.router.add_post("/retrieveCapture", retrieveCaptureImg)
    app.router.add_post("/retrieveIntruder", retrieveIntruderImg)
    app.router.add_route("OPTIONS", "/capture", handle_options)
    app.router.add_route("OPTIONS", "/retrieveCapture", handle_options)
    app.router.add_route("OPTIONS", "/retrieveIntruder", handle_options)

    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
