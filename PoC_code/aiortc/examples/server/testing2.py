import os, cv2

path = 'static/unknowImg'
images = []
calssNames = []
# self.nameSpeack.clear()
mainDirList = os.listdir(path)
for folder in mainDirList:
    userFolder = os.path.join(path, folder)
    if os.path.isdir(userFolder):
        calssNames.append(folder)
        pictList = os.listdir(userFolder)
        for pic in pictList:
            curImg = cv2.imread(os.path.join(userFolder, pic))
            images.append(curImg)

print(calssNames)