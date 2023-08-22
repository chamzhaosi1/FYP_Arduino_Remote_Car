# ROMO
## A small full-stack FYI project

### Frontend with Angular
To-do list
1. [x] Wireframe with [figma] (https://www.figma.com/file/VqNmqyV41fqQaViNZa2ufl/ROMO?node-id=0-1&t=rSr9cvNKY1FtBjDs-0)
2. [x] Login page
    * Date: 18/4/2023
        - Able to pass the username and password to backend
        - Able to get repsonse http status code
        - Able based on the status code showing the error message or redirect to anothor page
        - Able based on the cookies login to the user dashboard
3. [x] Registration page
    * Date: 19/4/2023
        - Able to pass the username, first/last name, email, and password to backend
        - Checking whether the password and confirm password is same
        - If successfully register an account, then directly access to the dashboar page based on the token given
        - If unsuccessfully, then an error (may be username or email already exists) will be informed to the user
        - NOTICE: user's password need to be hashed before store in database, and this kind error won't be info developer, until login admin portal (Invalid password format or unknown hashing algorithm.)
4. [x] Dashboard page
    - [x] Logout
        * Date: 19/4/2023
            - Just noticed, if the http client pass three argument, it will return HTTPResponse data type, and only this kind of data type just can uptate the cookies.
            - HTTPONLY flag is secure, to prevent the xSS or CORS attack
            - After pressing the logout button, cookies will be deleted/updated by the backend, and will redirect to the dashboard and if not found the cookies, login pass will be showing 
    - [x] Control Tool Form
        - [x] Keyboard & Mouse Controller
            * Date: 20/5/2023
                - User able to using keyboard and mourse to control dir, moving and view of the device
                - User able to use thier keyboard by pressing w, a, d, x, q, e, z, c (8 directions) and (shirt + w) will able to turn right or left based on the mouse moving.
                - Keyboard and mouse trigger value will be publish to a specific topic mqtt, to let raspberry pi get the value and pyserial to the arduino.
            - [x] Stop Live streaming
                * Date: 31/5/2023
                - After the user quickly press two time escape button, the connection and stream will be stoped and disconnected, and return to the dashboard page.
            - [x] Date: 06/7/2023
                - User able to pressing the "1" and "2" to start and attach or stop and release the face recognition mode and carry tray representatively.
                - User able to pressing the "p" to pause the aleart sound.
        - [x] Joystick Controller
            * Date: 06/7/2023 
                - User able to control the moving by left thumbstick and view by right thumstick.
                - User able to start or stop face recognition by pressing "A" button, refresh the page by pressing "Y" buttton, pause alert sound by pressing "B" button and exit the page by pressing "X" button.
                - User able to press top left button with both thumbstick to start normal moving mode.
                - User able to press top right button to release and attach the carry tray.
    - [x] Device Registration Form (with Label)
        * Date: 21/4/2023
            - User able to register ROMO device with mac address and label name.
            - After add a device, below devices list will be updated.
            - User also able to delete any row device, and list will be update automatically.
            - If user do not has any device, a message will be given.
    - [x] Device Connetion
        * Date: 31/5/2023
            - Once raspberry pi get ping, then will public a status to mqtt topic and frontend will subscribe the topic and based on the status enable the connect button.
5. [x] Image Authorized page
    - [x] Upload authorized person
        * Date: 22/4/2023
            - User able to upload, get and delete the image from the frontend ui.
            - To send an image to the backend, we need apply FormDate object. This is because the Angular will convert the data to json formater, but the FormData object can be carried the file and imgae type to backend.
            - We can apply formcontrol's function - reset() to reset touched and value.
    - [x] Snapshot authorized person
        * Date: 11/6/2023
            - User able to snapshot their authorized person face with connect to the face detection server, to make sure the image has person' face. 
            - User need to enter the authorized person name to send it with image to the backend to save in the database
            - User id and date time will be auto retrieve and generate
    - [x] List the authorized person image by group
        * Date: 11/6/2023
            - Once loading this page, backend will response a list of the image with their detail information. And based on the person name group the same person face and showing the faces
            - User able to delete each of the face 
6. [x] Control page
    - [x] Real-time WebRTC
        - [x] Date: 22/5/2034
            - Add the ssl certificate and private key when runing the server
                ("start": "ng serve --host 0.0.0.0 --port 4200 --ssl --ssl-cert /etc/nginx/ssl/kynoci.com-sub-cert.pem  --ssl-key /etc/nginx/ssl/kynoci.com-sub-privkey.pem")
    - [x] Calculate Cartesian Coordinate to Polar Coordinate = Wheel Speed
        - [x] Date: 06/7/2023
            - Based on the math sin and cos, we can get the value of the hypothesis
            - Based on the hypot, we can know how long is user pushed, and mapping the value to the speed of the rotate
            - Because the mecanum wheel the slop 45 degree, so before mapping or convert to the speed, we need deduce 45 degree
            - After calculation the value, we mqtt publish the value 
    - [x] 2D romo view
        - [x] Date: 20/5/2023 For keyboard, mourse and joystick  controller
    - [x] RPM animation (optional)
        - [x] Date: 20/5/2023 For keyboard, mourse and joystick controller
    - [x] Face recognization
        - [x] Face detection
            * Date: 31/5/2023
                - Once the remote video load the stream, the remote video frame will send to the face recognization backend and start face detectiona and draw a box and label unknow with the face, and then return the frame to frontend.
        - [x] Face recognization
            * Date: 11/6/2023
                - User able to decide whether want to start the face recognization mode by pressing button "1"
                - Once pressing "1" button, the connection need to take around 1 minute 
                - Once a person face is recognized, a green box and name will be showed, but if the face is unreconized, the face will be snapshoted and the picture will be showed at the right bottom and alert sound will be played
                - Bottom picutre will be showed 2 different unauthorized faces only, and the alert sound can press "p" button to pause.
7. [x] Intrusion page
    - [x] List of intruder
        * Date: 11/6/2023
            - Once a unrecognized face is detected and snapshoted, picture and intruder label will be send to the backend to save into the database
            - Once this page is loaded, all of the intruder images will be retrieve and show the detail include, which romo device found and found date time.
            - User able to decide and convert the intruder to authorized by enter their person name. 
            - User able to delete the intruder if there is some error happend
8. [x] Control Manual (optional)
    - [x] Manual - Keybaord and joystick
        * Date: 06/07/2023
            - Show each of the button and guide how to control the ROMO device for both controller.
 

### Backend with Django
To-do list
1. [x] [Database design] (https://app.diagrams.net/)
2. [x] Login user authentication and token
    * Date: 18/4/2023
        - Able login with the django auth user model 
        - Able generate/encode the JWT (Json Web Token) and set as the cookies
        - Able decode the JWT and get the user id and query the user model
        - Able based on the condition return different http status code
        - Able based on the JWT response user info
    * Date: 19/4/2023
        - After login successfully, then user info (username, email, fistname and last name) will be response to the frontend
3. [x] Registration page
    * Date: 19/4/2023
        - Able to receive new user info and insert to the database
        - Able raise an error if username or email is exists
        - Able to set cookies when successfully register an account
4. [x] Logout 
    * Date: 19/4/2023
        - Able to delete the cookies (to be honest, it like update the cookies to be emtpy string)
5. [x] API for device GET(read), POST(create), Delete(delete)
    * Date: 24/4/2023
        - Based on the cookies, get user id and find the device that had been register by user
        - Receive a new romo info (mac address and label), it will be insert to the database
        - Based on received mac_address to delete the romo device from database
6. [x] API for upload authorized image GET(read), POST(create), DELETE(delete),
    * Date: 22/4/2023
        - User able to send a image and it's name to backend, backend will store the image to the media folder and save it path and label name to the database
        - I change the code structure about get one or multiple image after query the database. Neverless one, multiple or empty row of the data, backend will return an array. So the error of "DoesNotExist" may not be raise
        - In order to return a image and some extra data (id and name label) to the frontend, i apply the base64 to encode the image from binary to text, and send it like json with extra data message to the frontend
        - When user deleting a image, both database and folder's image will be deleted.
7. [x] Control page
    - [x] Runing server with ssl certificate
        * Date: 22/5/2023
        - Frontend able to access https://localhost:8000 by running the below command
            (daphne -e ssl:8000:privateKey=/etc/nginx/ssl/kynoci.com-sub-privkey.pem:certKey=/etc/nginx/ssl/kynoci.com-sub-cert.pem romo_back.asgi:application)
    - [x] [WebRTC] (#real-time-webrtc)
        * Date: 31/5/2023
        - Frontend will through the backend (Djando channel) exchange the ice information to both peer, and turn or stun server confirm the both peer able to communication by themselve then live streaming wil be started.
    - [x] [Face-Recognization] (#real-time-face-recognization-with-aiortc-backend)
        * Date: 11/6/2023
        - Whatever authorized face or intruder face is captured or detected, all of them will be save into the database
8. [x] API for save intruder image GET(read), POST(create), PUT(update, convert), DELETE(delete)
    * Date: 11/6/2023
        - Once the intruder face is captured, frontend will send the the image and intruder label to backend and save to the database
        - If later the intruder face is captured again, we will update it as a latest one, however, the previous image won't be deleted but each intruder will only keep most three latest only
        - This is because, when face recognized backend encode more each intruder face, when face recognized can be more accurate and reliable.
        - However, the database will only has a single row data for each intruder. 
        - This is becuase the frontend will only show one each of the intruder face and the lastest date time
        - When delete a intruder detail, all of the image inside the folder will be deleted as well.

### Raspberry Pi
1. [x] WIFI Onbording - Let user connect to wifi
    * Date: 24/4/2023
    - [x] Setup wifi server
    - [x] Setup wifi client
    * Date: 07/5/2023
    - [x] Combine both
        - Using python flask run as web server and to let user choose ssid and type password of it
        - User able the to use phone or laptop that can connect wifi, and connect with "romo_wifi" (pss:newera2023)
        - This wifi access point will not be using, but user can open a browser and type "http://rapsberrypi:5000"
        to let raspberry pi and connect wifi that has choosen by them
        - Wifi ssid and password will be recored. 
2. [x] Subscribe the mecanum direction and rotation per data
    - [x] Keyboard and mouse
        * Date: 21/5/2023
        - Raspberry pi able to subscribe the mecanum dir and rpm data and transmit them to the arduino.
3. [x] Open a headless browser and access a frontend page
    * Date: 31/5/2023
    - Once the raspberry pi can get ping, a multi thread will run a node file to access the frontend server https://romo.kynoci.com:4200/login_romo/e4:5f:01:42:52:3e, then this page will based on the mac address given connect and login to the backend server https://romo.kynoci.com:8000/ws/call/, and try to call the device owner, and public mqtt about the device is ready.

### Hardware with Arduino
To-do list
* Comming soon 

### Real-time WebRTC
1. [x] Create RTCPeerConnection
    * Date: 31/5/2023 
    - Retrieve both peer local and remote ice information by turn or stun server and exchange them by backend django channel. If both data infomation able to pair then live streaming will be started
2. [x] Stop Connection
    * Date: 31/5/2023
    - After the user quickly press two time escape button, the connection and stream will be stoped and disconnected, and return to the dashboard page

### Real-time face recognization with aiortc backend
1. [x] Run with SSL certificate 
    * Date: 31/5/2023
    - Run the server like (python server.py --cert-file /etc/nginx/ssl/kynoci.com-sub-cert.pem --key-file /etc/nginx/ssl/kynoci.com-sub-privkey.pem)
2. [x] Connect Websocket with aiortc
    * Date: 31/5/2023
    - Once the client side remote video stream is loaded, then frontend will start collect the ice information and send to this backend, if the ip/device able to connect, frontend stream will be receive.
3. [x] Face Detection
    * Date: 31/5/2023 
    - Once each of the fream is received, face detection will be started
    - User able to take their authorized face when the face is detected.
4. [x] Face Recognization
    * Date: 11/6/2023
    - Once the face is recognized, a green box and person name will be showed on the frame, but if the face is unauthorized, then a red box and "New Intruder Found" will be attached and capture the face and save it to a folder
    - Once intrusion is happend, three different mqtt will be trigger, which are "New Intruder Found", "Intruder alert", and "Exist Intruder Found".
        - "New Intruder Found": when a new unauthorized face detected, we need let frontend to know and retrieve the capture image 
        - "Intruder alert" : when a new or exist unauthorized face detected, we need let frontend to know a intrusion happend, please play the alert sound
        - "Exist Intruder Found": when an exist unauthorized face detected, we need let frontend to know and retrieve the latest image and update to the backend database
        


