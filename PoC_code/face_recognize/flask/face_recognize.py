import cv2, sys, os, threading, face_recognition, random, string, datetime, queue
from time import sleep
import numpy as np
from collections import deque 
from utils import InputCamera, OutputCamera
from flask import Flask
from multiprocessing import Process
from subprocess import call

app = Flask(__name__)

class MotionOpenCV:
    
    def __init__(self):
        # self.VID_WIDTH = 1280
        # self.VID_HEIGHT = 720
        self.VID_WIDTH = 800
        self.VID_HEIGHT = 448
        # self.VID_WIDTH = 640
        # self.VID_HEIGHT = 480
        self.VIDEO_IN = "/dev/video0"
        self.VIDEO_OUT = "/dev/video6"
        self.VID_BRIGHTNESS = 120
        ## multiple * 5 (only accept)
        self.FOCUS = 5 

        self.isFaceDetected = False

        ## because not every frame to face recognization, so we need save the previous face location 
        self.previousFaceRecNameLoc = {
            "name" : None,
            "faceLoc" : None
        }

        ## get the dataset/img file location
        self.path = 'static/unknowImg'

        ## to keep dataset image name
        self.calssNames = []

        ## to keep dataset image encode for recognizing purpose
        self.encodeListKnown = []

        ## to know wheter the snapshot btn is trigger or not
        self.isClickedSnapshot = False

        ## to know wheter a unknow face detect or not
        self.isUnknowFaceDetected = False

        ## becuase not each frame will do face process, so if the unknown face frame is detect 12 frame which will pass to do face process then will snapshot the face
        self.ready_count = 3
        ## how many frame to take snapshot
        self.SNAPSHOT_FRAME = 12

        ## snapshot hint
        self.status = None

        ## after the class is created, then the freame / facerecognized will be multithread run, 
        ## however after the thread runing, value of the variable change will old, because both same variale name will be point to different address
        ## so, need to use the deque, which like a list, to get real-time changing value.
        self.udQueue = deque()
        self.shQueue = deque()
        self.nameSpeack = deque()

        ## the face recognize process need to run in background, so that frontend call backend not need to wait return
        t =  threading.Thread(target=self.getVideoStream)
        t.daemon = True
        t.start()     


    def getVideoStream(self):
        # open and configure input camera
        input = InputCamera(self.VIDEO_IN, (self.VID_WIDTH, self.VID_HEIGHT), self.VID_BRIGHTNESS, self.FOCUS)

        # get frame rate per second
        frameRate = int(input.getFrameRate())
        print(frameRate)

        # open output device
        output = OutputCamera(self.VIDEO_OUT, (self.VID_WIDTH, self.VID_HEIGHT), self.VID_BRIGHTNESS)

        ## to get the image and its name
        images, self.calssNames = self.loadImgDataSet()

        ## to get a list of the image encode for face recoginzing purpose
        self.encodeListKnown = self.findEncodings(images)
        print('Encoding Complete')

        count  = 0
        while True:
            img = input.get()

            ## to let user focus on inside circle only 
            img = self.blurWithCenterClear(img)
            
            ## only the first, middle, and last frame do the face detection and recognization process
            if count == (frameRate - frameRate) or count == int(frameRate/2) or count == frameRate-1:
                ## pass each of frame to do the face process
                self.faceRecognized(img, self.encodeListKnown)

            ## if the frame no face detect then the previous name and location need to clear
            elif not self.isFaceDetected:
                self.previousFaceRecNameLoc["name"] = None
                self.previousFaceRecNameLoc["faceLoc"] = None

            ## becuase above only pass first, middel and last frame to do face process, so other frame need use previous name and locatio value to do labling
            elif self.previousFaceRecNameLoc["name"] is not None:
                self.boxForFaceDetect(img, self.previousFaceRecNameLoc["name"], self.previousFaceRecNameLoc["faceLoc"])

            ## this is to count the frame number    
            count = count + 1
            
            ## once the count number equal to fps then loop again
            if count == frameRate - 1:
                count = 0

            ## after each of the frame complete the face progess then output to virtual webcam
            output.write(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # if 0xFF == ord('q'):
            #     break


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


    ## draw the box and natation with name (images's name)
    def boxForFaceDetect(self, img, name, faceLoc):
        h, w, _ = img.shape
        offset = w - (w//2 + ((h//2)-20))

        ## for other frames which without do the face process
        self.previousFaceRecNameLoc["name"] = name
        self.previousFaceRecNameLoc["faceLoc"] = faceLoc

        ## because the face location is top, right, bottom, left
        y1,x2,y2,x1 = faceLoc

        ## because the frame is resize at begining so now resize back 
        y1,x2,y2,x1 = y1*2,x2*2,y2*2,x1*2

        ## draw a rectangle / box
        cv2.rectangle(img, (x1+offset, y1), (x2+offset, y2+20), (0,255,0),2)

        ## draw a filled rectangle / box
        cv2.rectangle(img,(x1+offset, y2+35), (x2+offset, y2-10), (0,255,0), cv2.FILLED)

        ## write the its name into the filled box
        cv2.putText(img, name, (x1+6+offset, y2+26), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        ## when the snapshot btn is triger then a "Ready -- 1,2,3" will labeling at the bottom
        if self.status == "Ready -- ":
            cv2.putText(img, (self.status + str(self.ready_count // 3)), (x1+6+offset, y2+30+100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        
        ## calculate the area of the face / box
        recArea = (x2 - x1) * (y2 - y1)

        ## wtite down the total area 
        cv2.putText(img, ("Area: " + str(recArea)), (x1+6+offset, y2+30+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        return recArea


    ##  face detect and compare with the date set
    def faceRecognized(self, img, tempEncodeListKnown):
        ## copy a img before draw the box and label
        tmpImg = img.copy() 

        ## because only the circle part will be do to the face recoginze, so need to crop the image
        crop_image = self.faceCropped(img)

        ## reduce the size of the image
        imgS = cv2.resize(crop_image,(0,0), None, 0.5, 0.5)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        ## to know the face location (top, right, bottom, left)
        # facesCurFrame = face_recognition.face_locations(imgS, number_of_times_to_upsample=2)
        facesCurFrame = face_recognition.face_locations(imgS)

        ## if has the face location, then equal a face detected
        if facesCurFrame:
            self.isFaceDetected = True
        else:
            self.isFaceDetected = False


        if self.isFaceDetected:
            ## to do the unknown face encod
            # encodesCurFrame = face_recognition.face_encodings(imgS, known_face_locations=facesCurFrame, num_jitters=3)
            encodesCurFrame = face_recognition.face_encodings(imgS, known_face_locations=facesCurFrame)

            ## compare the unknow face with the dateset faces throught the encode
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(tempEncodeListKnown, encodeFace, tolerance=0.4) ## return boolean
                faceDis = face_recognition.face_distance(tempEncodeListKnown, encodeFace) ## return float
                matchIndex = np.argmin(faceDis) ## get the minimum value from the list

                ## match the draw the box and label the name
                if matches[matchIndex]:
                    name = self.calssNames[matchIndex].upper()
                    self.boxForFaceDetect(img, name, faceLoc)
                    # print(name)
                    
                    ## once recognize a face then espesk greeting with the person's name
                    ## multi process in order to avoid need to wait it complete
                    p = Process(target=self.greetingSpeak, args=(name, matchIndex))
                    p.start()
                    self.nameSpeack[matchIndex]=True
                    # print(self.nameSpeack[matchIndex])

                else:
                    ## if it is a unknonw face then draw a bow with lable unknown
                    area = self.boxForFaceDetect(img, "unknown", faceLoc)
                        
                    ## once the are of the face is closer with the webcam enough then frontend snapshot btn can be trigger
                    if area > 30000:
                        self.isUnknowFaceDetected = True
                        # print(hex(id(self.udQueue)))

                        # print("while: ", len(self.udQueue))
                        ## let the frontend know a unknown face is detect
                        ## if true then the snapshot btn can be trigger
                        if len(self.udQueue) < 0:
                            self.udQueue.append(self.isUnknowFaceDetected)
                        else:
                            self.udQueue.clear()
                            self.udQueue.append(self.isUnknowFaceDetected)

                        ## if the sanpshot btn is trigger then ready to capture the face
                        if len(self.shQueue) > 0 and self.shQueue[0]:
                            self.ready_count += 1
                            self.status = "Ready -- "
                            
                            ## once the count or frame is enought the capture the face
                            if self.ready_count == self.SNAPSHOT_FRAME:

                                ## save the img and pass a name
                                self.captureUnknownImg(tmpImg, self.shQueue[1])

                                ## after snapshot a picture then sleep 2 second for file saving
                                ## if not the pitcure will disapper after a few second
                                sleep(2)

                                ## once the face is saved, then dateset need to reload
                                images, self.calssNames = self.loadImgDataSet()
                                self.encodeListKnown = self.findEncodings(images)
                                print('Encoding again complete')
                                
                                ## clear the snapshot btn value
                                self.shQueue.clear()

                                ## the ready count for capture is loop again
                                self.ready_count = 3
                                self.status = None
                    else:
                       self.udQueue.clear()
                       self.ready_count = 3
                       self.status = None 
        else:
            self.udQueue.clear()

    ## espeak the greeting and the person's name once detect a known face
    def greetingSpeak(self, name, matchIndex):
        ## if the face haven't be especk then do the especk process
        if not self.nameSpeack[matchIndex]:
            cmd_beg = 'espeak '
            cmd_end = ' 2>/dev/null'
            greeting = ' How are you '
            afterReplaceName = name.replace("_", " ")
            call([cmd_beg+ "' " + greeting + afterReplaceName + "' " +cmd_end], shell=True)


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
                os.remove(f'{self.path}/{self.calssNames[index]}.jpg')

            finally:
                index += 1

        return encodeList


    ## get the image and the person name
    def loadImgDataSet(self):
        images = []
        calssNames = []
        self.nameSpeack.clear()
        myList = os.listdir(self.path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            images.append(curImg)
            calssNames.append(os.path.splitext(cl)[0])
            self.nameSpeack.append(False)
        return images, calssNames


    ## crop the face only keep the circle part
    def faceCropped(self, img):
        offset = 20
        height, width, _ = img.shape
        center = (width//2, height//2)
        radius = (height//2)-offset
        cropped_image = img[:, (center[0] - radius) : (center[0] + radius)]

        return cropped_image

 
    ## frontend will invoke this method and to known whether a unknonw face detected or not
    def getIsUnknowFaceDetected(self):
        # print(hex(id(self.udQueue)))
        # print("below :", len(self.udQueue))
        if len(self.udQueue) > 0:
            return self.udQueue[0]
        else:
            return False


    ## frontend will invoke this method to let backend known whether the snapshot 
    def snapshotUnknownFace(self, newImgName):
        self.isClickedSnapshot = True
        if len(self.shQueue) != 0:
            self.shQueue.clear()
            self.shQueue.append(self.isClickedSnapshot)
            self.shQueue.append(newImgName)
            # print(self.shQueue[0])
            # print(self.shQueue[1])
        else:
            self.shQueue.append(self.isClickedSnapshot)
            self.shQueue.append(newImgName)


# if __name__ == "__main__":
#     # faceCropped()
#     sys.exit(MotionOpenCV())