from flask import Flask, render_template, request, send_file, json
from multiprocessing import Process
import os, shutil, time
from face_recognize import MotionOpenCV

app = Flask(__name__)
motion = None

@app.route('/')
def index():
    global motion
    motion = MotionOpenCV() 
    return render_template("index.html")


@app.route('/delete_img', methods=['POST'])
def delete_img():
    deleteImgName = request.form["deleteImgName"]
    # print(deleteImgName)
    try:
        path = "static/unknowImg/"
        # print(path + oldImgName)
        os.remove(path + deleteImgName)   

        assetsPath = "assets/"
        os.remove(assetsPath + deleteImgName)
    except:
        pass

    return render_template("index.html")
        


@app.route('/unknown_face_detect', methods=['GET'])
def getUnknownFaceDetected(): 
    return json.dumps(motion.getIsUnknowFaceDetected())

   

@app.route('/snapshot_unknown_face_detect', methods=['POST'])
def snapshot_unknown_face_detect():
    newImgName = (request.form['inputNewName']).replace(" ", "_")
    motion.snapshotUnknownFace(newImgName)
    return "snapshot successfully"


if __name__ == '__main__':   
   app.run(host='0.0.0.0', port=5000, debug=True)  

   

###############################################################################
####################### Function not use just for remark ######################
###############################################################################


# def getStaticPitcure():
#     imageList = os.listdir('static/unknowImg')
#     imageList = ['unknowImg/' + image for image in imageList]
#     return imageList


# def copyImgToStatic():
#     sourcePath = "assets/"
#     distPath = "static/unknowImg"
#     for p in os.listdir(sourcePath):
#         if os.path.splitext(p)[0].startswith("unknown"):
#             shutil.copy((sourcePath + "/" +p), distPath)
#             time.sleep(1.5)


# @app.route('/update_img_name', methods=['POST'])
# def update_img_name():
#     newImgName = (request.form["inputNewName"]).replace(" ", "_")
#     oldImgName = request.form["oldName"]
    
#     updateImgName(newImgName, oldImgName)

#     return render_template("index.html" )


# def updateImgName(newImgName, oldImgName):
#     print(newImgName)
#     print(oldImgName)
#     try:
#         assetsPath = "assets/"
#         fileExtension = ".jpg"
#         os.rename(path + oldImgName , path + newImgName + fileExtension)
        
#         path = "static/unknowImg/"
#         os.remove(assetsPath + oldImgName)

#         motion.afterUnknonwRenameEncd()
#     except:
#         pass


# def runMotionOpenCV():
#    subprocess.Popen("python face_recognize.py", shell=True)

# def getUnknownImg():
#    dicfile = "assets/"
#    for p in os.listdir(dicfile):
#       if os.path.splitext(p)[0].startswith("unknown"):
#             # copyImgToStatic()
#             return True, p

#    # print(unknownFileName)
#    return False, ""


# def delectFromAssest():
#     dicfile = "assets/"
#     for p in os.listdir(dicfile):
#       if os.path.splitext(p)[0].startswith("unknown"):
#         try:
#             print(p)
#             # print(path + oldImgName)
#             os.remove(dicfile +p)
#         except:
#             pass