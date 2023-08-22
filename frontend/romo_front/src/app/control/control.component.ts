import { Component, OnInit, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UsersService } from '../services/users.service';
import { Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { MqttWebsocketService } from '../services/mqtt.service';
import { Romoview2dService } from '../services/romoview2d.service';
import { LiveStreamingService } from '../services/live-streaming.service';
import { FaceRecognizationService } from '../services/face-recognization.service';
import { KeyboardMouseService } from '../services/keyboard-mouse.service';
import { JoystickService } from '../services/joystick.service';
import { Subscription, zipAll } from 'rxjs';
import { IMqttMessage } from "ngx-mqtt";
import { IntrusionService } from '../services/intrusion.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-control',
  templateUrl: './control.component.html',
  styleUrls: ['./control.component.css']
})
export class ControlComponent implements OnInit {
  name: string = ""
  deviceOwnerName?: string
  deviceMacAddress?: string
  deviceControlType?: string
  FaceRecognitionMode: any;
  CarryTray: any;
  rpmValues: number = 50 // save the rmp speed
  rotationAngle: number = 0;
  rightDecRPM: number = 0;
  leftDecRPM: number = 0;
  mecanum?: CanvasRenderingContext2D;
  localVideo: any;
  remoteVideo: any;
  remoteVideoFace: any;
  isRemoteVideoFaceConnect: Boolean = false;
  subscription!: Subscription;
  alert_sound: string = "../../assets/security-alarm.mp3";
  controlType : string = "";
  viewMessage : string = "Center";
  FPSType: string = "Live Streaming FPS: ";
  new_img_info?= new FormData();
  imageDataArray: any[] = [];
  imgScrArray: any[] = [];
  alertAudio?: HTMLAudioElement;
  isPlaying: boolean = false;
  temp_intr_img_array: any[] = [];
  keep_showing_intr_face_array: string[] = [];
  isLoadingShow: Boolean = false;
  remoteVideoLoadedCount: number = 0;
  isRemoteVideoLoaded: boolean = false;
  isKeyboardMouseCtrl: boolean = true;
  isAGreenPressing : boolean = false;
  isTopRightPressing : boolean = false;
  is360DModeStarted : boolean = true;
  jsExitButtonCount : number = 0;
  isJSExitBtnPressing : boolean = false;
  isPauseAlertBtnPressing : boolean = false;
  isRefreshBtnPressing : boolean = false;
  hookValue : number = 0;
  lastFrameTime = performance.now();
  frameCountMessage = 0;
  getFPSInterval:any

  constructor(private loginService: UsersService,
    private route: ActivatedRoute,
    private router: Router,
    private mqtt: MqttWebsocketService,
    private elementRef: ElementRef,
    private romo2d: Romoview2dService,
    private livestreaming: LiveStreamingService,
    private faceRecognization: FaceRecognizationService,
    private keyboardMouseService: KeyboardMouseService,
    private joystickService: JoystickService,
    private readonly eventMqtt: MqttWebsocketService,
    private intrusionService: IntrusionService,
    private location: Location) {
    this.FaceRecognitionMode = new FormGroup({
      FRMcheckbox: new FormControl(''),
    })
    this.CarryTray = new FormGroup({
      CarryTraycheckbox: new FormControl(''),
    })
  }

  ngOnInit() {
    // get observable object
    this.loginService.getAutheToken('user').subscribe({
      next: (response: any) => {
        console.log(response)
        let first_name: string = response.body['user_info']['first_name'];
        let last_name: string = response.body['user_info']['last_name'];
        this.name = (first_name + " " + last_name);
        this.deviceOwnerName = response.body['user_info']['username'];

        this.route.paramMap.subscribe(param => {
          this.deviceMacAddress = param.get('mac_address')?.toString()
          this.deviceControlType = param.get('control_type')?.toString()
        })

        // Call keyboard and mouser or joystick controller 
        if (this.deviceControlType === "keyboard_mouse") {
          this.controlType = "Keyboard Mouse"

        } else {
          this.controlType = "Joystick"
          this.isKeyboardMouseCtrl = false
          window.addEventListener('gamepadconnected', this.handleGamepadConnected);
          window.addEventListener('gamepaddisconnected', this.handleGamepadDisconnected);
          requestAnimationFrame(() => this.checkGamepadState());
        }

        // Get the element by its ID and get canvas context 2d
        this.mecanum = this.elementRef.nativeElement.querySelector('#mecanum').getContext('2d');
        this.romo2d.redraw(this.mecanum)

        // Start conneting live streaming websocket
        this.localVideo = this.elementRef.nativeElement.querySelector('#localVideo')
        this.remoteVideo = this.elementRef.nativeElement.querySelector('#remoteVideo')
        this.remoteVideoFace = this.elementRef.nativeElement.querySelector('#remoteVideoFace')
        this.livestreaming.connectWebSocket(this.deviceOwnerName!, this.deviceMacAddress!, this.localVideo, this.remoteVideo, "owner")

        // Start conneting intrusion websocket
        this.mqttSubcIntr();
      },
      error: (error) => {
        this.router.navigate(['/login'])
      }
    })
  }

  // whem the page is going to destroy, then release all resouce
  ngOnDestroy(): void {
    if(this.isRemoteVideoFaceConnect){
      this.faceRecognization.stop()
    }

    if(this.isRemoteVideoLoaded){
      this.livestreaming.closeWebSocket()
    }

    window.removeEventListener('gamepadconnected', this.handleGamepadConnected);
    window.removeEventListener('gamepaddisconnected', this.handleGamepadDisconnected);
    clearInterval(this.getFPSInterval);

    // pause the alert audio
    this.pauseAlertAudio()
  }

  // JOYSTICK CONTROLLER
  handleGamepadConnected(event: Event) {
    const gamepad = (event as GamepadEvent).gamepad;
    console.log(`Gamepad connected: ${gamepad.id}`);
  }

  handleGamepadDisconnected(event: Event) {
    const gamepad = (event as GamepadEvent).gamepad;
    console.log(`Gamepad disconnected: ${gamepad.id}`);
  }

  checkGamepadState() {
    const gamepads = navigator.getGamepads();

    if (gamepads[0] !== null && this.isRemoteVideoLoaded) {
      // Calculate Mecanum
      // if the left hand side thumdstick is pushing
      let pwr_value = this.joystickService.calRomoPwr(gamepads[0])
      
      // and then count the motor power and return value not equal null, 
      if(pwr_value != null){
        this.romo2d.redraw(this.mecanum)
        this.romo2d.mecanum_dir(this.mecanum, 49.5, 50, 45, pwr_value![0]);
        this.romo2d.mecanum_dir(this.mecanum, 150.5, 50, -45, pwr_value![1]);
        this.romo2d.mecanum_dir(this.mecanum, 49.5, 150, -45, pwr_value![2]);
        this.romo2d.mecanum_dir(this.mecanum, 150.5, 150, 45, pwr_value![3]);
        // to let the fronted UI meter rpm rotate
        this.rotationAngle = Math.round(Math.max(Math.abs(pwr_value![0]), Math.abs(pwr_value![1])))
        // mqtt the motor power value
        this.motorControl([pwr_value![0], pwr_value![1], pwr_value![2], pwr_value![3]])
      
      }else{
        // if equal null then set default value for everything
        this.romo2d.redraw(this.mecanum)
        this.rotationAngle = 0
        this.motorControl([0, 0, 0, 0])
      }

      // Calculate Romo head 
      // if the right hand side thumdstick is pushing
      let head_value = this.joystickService.calRomoHead(gamepads[0])

      // and then count the angle of head and return value not equal null,
      if(head_value != null){
        this.viewMessage =  head_value["message"]
        this.headControlAngle(head_value["head_x"], head_value["head_y"])
      }

      // if the top left button is pressed, then chg the notice message on screen
      if(gamepads[0].buttons[6]["pressed"]){
        this.is360DModeStarted = false
      }else{
        this.is360DModeStarted = true
      }

      // it the top right button is pressed, then turn the hook 30 or 85 degree
      if(gamepads[0].buttons[7]["pressed"]){

        if(!this.isTopRightPressing){
          this.isTopRightPressing = true
          let preValue = this.CarryTray.get("CarryTraycheckbox").value
        
          // 30 mean close / attached the hook, 85 mean release the hook
          if (preValue != "ON") {
            this.hookValue = 30;
          }else{
            this.hookValue = 85;
          }
          this.hookControl();
  
          this.CarryTray.setValue({
            CarryTraycheckbox: preValue === 'ON' ? '' : 'ON'
          })
          
        }
      }else{
        this.isTopRightPressing = false;
      }

      // if the green A button is pressed 
      if(gamepads[0]!.buttons[0].value > 0){
        // if the button status is pressing and the remote video is loaded,
        // then user can enable the FRM 
        if (!this.isAGreenPressing && this.isRemoteVideoLoaded){
          this.isAGreenPressing = true
          let preValue = this.FaceRecognitionMode.get("FRMcheckbox").value
          // set the FRM _ON or _OFF
          this.FaceRecognitionMode.setValue({
            FRMcheckbox: preValue === 'ON' ? '' : 'ON'
          })

          if (preValue != "ON") {
            console.log("FRM NO")
            this.startFaceRecognizationMode()
            clearInterval(this.getFPSInterval);
          } else {
            // set default value
            this.isLoadingShow = false
            this.isRemoteVideoFaceConnect = false
            this.faceRecognization.stop()
          }
        }
      }else{
        this.isAGreenPressing = false
      }

      // if press the red B button then pause alert sound 
      if(gamepads[0]!.buttons[1].value > 0){
        if (!this.isPauseAlertBtnPressing  && this.isPlaying){
          this.isPauseAlertBtnPressing = true
          this.pauseAlertAudio()
        }
      }else{
        this.isPauseAlertBtnPressing = false
      }

      // if press the blue x button 2 time then exit to the home page
      if(gamepads[0]!.buttons[2].value > 0){
        if (!this.isJSExitBtnPressing){
          this.isJSExitBtnPressing = true
          this.jsExitButtonCount = this.jsExitButtonCount + 1

          setTimeout(() => {
            // after 3 seconds, set the time back to 0
            this.jsExitButtonCount = 0
          }, 3000);
          
          if(this.jsExitButtonCount == 2){
            // close the livestreaming
            if(this.isRemoteVideoFaceConnect){
              this.faceRecognization.stop()
            }

            if(this.isRemoteVideoLoaded){
              this.livestreaming.closeWebSocket()
            }

            // clear the interval
            clearInterval(this.getFPSInterval);

            // pause the alert audio
            this.pauseAlertAudio()
            // redirect to dashboard page
            this.router.navigate(['/'])
          }
        }
      }else{
        this.isJSExitBtnPressing = false
      }

      // if press yellow Y button then refresh the page
      if(gamepads[0]!.buttons[3].value > 0){
        if(!this.isRefreshBtnPressing){
          this.location.go(this.location.path());
          window.location.reload();
        }
      }else{
        this.isRefreshBtnPressing = false
      }
    }
    requestAnimationFrame(() => this.checkGamepadState());
  }

  // KEYBOARD AND MOUSE CONTROLLER
  handleKeyDown(event: KeyboardEvent) {
    if (this.isKeyboardMouseCtrl && this.isRemoteVideoLoaded) {
      let keydownResult = this.keyboardMouseService.handleKeyDown(event)
      console.log(typeof keydownResult)
      console.log(keydownResult)
      // != boolean == number[]
      if (typeof keydownResult === "object") {
        if (event.key === "W"){
          this.is360DModeStarted = false
        }

        // Calculate Mecanum
        this.romo2d.redraw(this.mecanum)
        this.romo2d.mecanum_dir(this.mecanum, 49.5, 50, 45, (keydownResult as number[])[0]);
        this.romo2d.mecanum_dir(this.mecanum, 150.5, 50, -45, (keydownResult as number[])[1]);
        this.romo2d.mecanum_dir(this.mecanum, 49.5, 150, -45, (keydownResult as number[])[2]);
        this.romo2d.mecanum_dir(this.mecanum, 150.5, 150, 45, (keydownResult as number[])[3]);

        // mqtt the each of the motor rpm and direction
        this.motorControl(keydownResult as number[])

        // this.calEachMotors()
        if (!((keydownResult as number[]).every((element:number) => element === 0))){
          this.rotationAngle = this.rpmValues
        }

      } else if (typeof keydownResult === "boolean") {
        // when return boolean type data, means exit
        // close the livestreaming
        if(this.isRemoteVideoFaceConnect){
          this.faceRecognization.stop()
        }

        if(this.isRemoteVideoLoaded){
          this.livestreaming.closeWebSocket()
        }

        // clear the interval
        clearInterval(this.getFPSInterval);

        // pause the alert audio
        this.pauseAlertAudio()
        // redirect to dashboard page
        this.router.navigate(['/'])

      } else if (keydownResult === "FRM") {

        // if the remote video is loaded, then user can enable the FRM 
        if (this.isRemoteVideoLoaded) {
          let preValue = this.FaceRecognitionMode.get("FRMcheckbox").value
          // set the FRM _ON or _OFF
          this.FaceRecognitionMode.setValue({
            FRMcheckbox: preValue === 'ON' ? '' : 'ON'
          })

          if (preValue != "ON") {
            console.log("NO")
            this.startFaceRecognizationMode()
            clearInterval(this.getFPSInterval)
          } else {
            this.isLoadingShow = false
            this.isRemoteVideoFaceConnect = false
            this.faceRecognization.stop()
            clearInterval(this.getFPSInterval)
            this.displayLiveFPSValue();
            this.FPSType = "Live Streaming FPS: "
          }
        }

      } else if (keydownResult === "TRAY") {
        let preValue = this.CarryTray.get("CarryTraycheckbox").value
        
        // 30 mean close / attached the hook, 85 mean release the hook
        if (preValue != "ON") {
          this.hookValue = 30;
        }else{
          this.hookValue = 85;
        }
        this.hookControl();

        this.CarryTray.setValue({
          CarryTraycheckbox: preValue === 'ON' ? '' : 'ON'
        })

      } else if (keydownResult === "pause" && this.isPlaying) {
        this.pauseAlertAudio()
      }
    }

  }

  // any key is released the value will be counted again
  handleKeyUp(event: KeyboardEvent) {
    if (this.isKeyboardMouseCtrl && this.isRemoteVideoLoaded) {
      // set rmp to 0
      // this rpmValues and rotationAngle are for the rpm meter
      this.rpmValues = 50;
      this.rotationAngle = 0;

      // public the initial value to the mqtt
      if(event.key != "1" && event.key != "2"){
        this.motorControl(this.keyboardMouseService.handleKeyUp(event))
      }

      // redraw the mecanum dir notation
      this.romo2d.redraw(this.mecanum)

      this.is360DModeStarted = true
    }
  }

  handleMouseMove(event: MouseEvent) {
    if (this.isKeyboardMouseCtrl && this.isRemoteVideoLoaded) {
      let result_array = this.keyboardMouseService.handleMouseMove(event)
      // console.log(result_array)

      // get the right and left reduce rpm from return
      this.rightDecRPM = result_array["rightDecRPM"]
      this.leftDecRPM = result_array["leftDecRPM"]
      this.viewMessage =  result_array["message"]
      this.headControlAngle(result_array["angleX"], result_array["angleY"])
    }
  }

  headControlAngle(angleX: number, angleY: number) {
    // mqtt to a topic
    let subtopic = this.deviceMacAddress + "/ROMO_head_control"
    this.mqtt.publish(subtopic, JSON.stringify({
      "angle_x": angleX,
      "angle_y": angleY
    })).subscribe()
  }

  RPMScroll(event: WheelEvent) {
    if (this.isKeyboardMouseCtrl) {
      this.rpmValues = this.keyboardMouseService.RPMScroll(event)
      this.rotationAngle = this.rpmValues
    }
  }

  motorControl(motorArray: number[]) {
    let subtopic = this.deviceMacAddress + "/ROMO_motor_control"
    this.mqtt.publish(subtopic, JSON.stringify({
      "lf": motorArray[0],
      "rf": motorArray[1],
      "lb": motorArray[2],
      "rb": motorArray[3],
    })).subscribe()
  }

  hookControl(){
    let subtopic = this.deviceMacAddress + "/ROMO_hook_control"
    this.mqtt.publish(subtopic, JSON.stringify({
      "hook_value" : this.hookValue,
    })).subscribe()
  }

  startFaceRecognizationMode() {
    // to make sure after second time face recognization is ready, then dont connect again
    if (!this.isRemoteVideoFaceConnect) {
      this.isLoadingShow = true
      this.faceRecognization.start(this.remoteVideo, this.remoteVideoFace, "face_recognition", this.deviceOwnerName!, this.deviceMacAddress!);
    }
  }

  onLoadedVideoMetadata(event: any) {
    this.isRemoteVideoLoaded = true
    this.displayLiveFPSValue();
    this.FPSType = "Live Streaming FPS: "
  }

  onLoadedFaceVideoMetadata(event: any) {
    this.isLoadingShow = false
    this.isRemoteVideoFaceConnect = true
    this.displayFaceFPSValue();
    this.FPSType = "Face Mode Live Streaming FPS: "
  }

  // covert the image to desired data type
  convertBase64ToBlob(base64String: string): Blob {
    const byteCharacters = atob(base64String);
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512);

      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    const blob = new Blob(byteArrays, { type: 'image/jpeg' });
    return blob;
  }

  // keep the image like a file data type, same as user upload a image
  blobToFile(blob: Blob, fileName: string): File {
    const fileOptions: FilePropertyBag = { type: blob.type };
    return new File([blob], fileName, fileOptions);
  }

  // send the new intruder image, and it info to the backend
  sendImageToBackend(data: any, intrImgLabel: string): void {
    this.new_img_info = new FormData()
    const blob = this.convertBase64ToBlob(data)
    const image_file = this.blobToFile(blob, "intruder.jpg")
    // console.log(image_file)

    this.new_img_info?.append("intruder_img", image_file)
    this.new_img_info?.append("intruder_label_id", intrImgLabel)
    this.new_img_info?.append("mac_address", this.deviceMacAddress!)
    this.intrusionService.uploadIntrImg("upl_intr_img", this.new_img_info).subscribe({
      next: (response: any) => {
        console.log(response)
      }
    })
  }

  // there will only display two different intrurder id on the frontend,
  // so if the image is are inside the list, the new intruder image will be updated
  updateImageToBackend(data: any, intrImgLabel: string): void {
    this.new_img_info = new FormData()
    const blob = this.convertBase64ToBlob(data)
    const image_file = this.blobToFile(blob, "intruder.jpg")
    // console.log(image_file)

    this.new_img_info?.append("intruder_img", image_file)
    this.new_img_info?.append("intruder_label_id", intrImgLabel)
    this.intrusionService.updateIntrImg("upt_intr_img", this.new_img_info).subscribe({
      next: (response: any) => {
        console.log(response)
      }
    })
  }

  retrieveInt(intrImgLabel: string, isExistIntrFace: Boolean) {
    this.faceRecognization.retrieveInt({ 'userName': this.deviceOwnerName, 'intrLabel': intrImgLabel}).subscribe({
      next: (response: any) => {
        // console.log(response)
        this.imageDataArray = response; // Assuming the response is an array of image data

        if (!isExistIntrFace) {
          this.imageDataArray.forEach((element) => {
            this.temp_intr_img_array.push(element)
            this.keep_showing_intr_face_array.push(intrImgLabel)
            this.sendImageToBackend(element, intrImgLabel)
          })

          this.showIntruderImage()
        } else {
          // if the intr img is no showing, then showing it     
          if (!this.keep_showing_intr_face_array.includes(intrImgLabel)) {
            this.imageDataArray.forEach((element) => {
              this.temp_intr_img_array.push(element)
              this.keep_showing_intr_face_array.push(intrImgLabel)
              this.updateImageToBackend(element, intrImgLabel)
            })
            this.showIntruderImage()
          }
        }
      }
    })
  }

  showIntruderImage(): void {
    if (this.temp_intr_img_array.length > 2) {
      this.temp_intr_img_array = this.temp_intr_img_array.slice(-2);
      this.keep_showing_intr_face_array = this.keep_showing_intr_face_array.slice(-2);
    }

    this.imgScrArray.splice(0);

    this.temp_intr_img_array.forEach((element: any) => {
      let imgScr = 'data:image/jpeg;base64,' + element;
      this.imgScrArray.push(imgScr)
    })
  }

  playAlertAudio() {
    this.alertAudio = new Audio(this.alert_sound);
    this.alertAudio.addEventListener('ended', () => {
      this.alertAudio!.currentTime = 0; // Reset the audio to the beginning
      this.alertAudio!.play(); // Restart the audio playback
    });

    this.alertAudio.play()
    this.isPlaying = true;
  }

  pauseAlertAudio() {
    if (this.isPlaying) {
      this.alertAudio!.pause();
      this.isPlaying = false;
    }
  }

  mqttSubcIntr() {
    let intFaceSubtopic = this.deviceMacAddress + "/ROMO_intrusion_found";
    this.subscription = this.eventMqtt.subscribe(intFaceSubtopic).subscribe((data: IMqttMessage) => {
      let item = JSON.parse(data.payload.toString());
      console.log(item['warning'])
      if (item['warning'] === "Intruder Found") {
        this.retrieveInt(item['image_name'], false)
      }
    })

    let alertAudioSubtopic = this.deviceMacAddress + "/ROMO_intrusion_alert";
    this.subscription = this.eventMqtt.subscribe(alertAudioSubtopic).subscribe((data: IMqttMessage) => {
      let item = JSON.parse(data.payload.toString());
      console.log(item['warning'])
      if (item['warning'] === "Intruder Alert" && !this.isPlaying) {
        this.playAlertAudio()
      }
    })

    let existIntrSubtopic = this.deviceMacAddress + "/ROMO_exist_intrusion_found";
    this.subscription = this.eventMqtt.subscribe(existIntrSubtopic).subscribe((data: IMqttMessage) => {
      let item = JSON.parse(data.payload.toString());
      console.log(item['warning'])
      if (item['warning'] === "Exist Intruder Found") {
        this.retrieveInt(item['image_name'], true)
      }
    })
  }

  displayLiveFPSValue(){
    this.getFPSInterval = setInterval(()=>{this.frameCountMessage = this.livestreaming.getFPSValue()},1000)
  }

  displayFaceFPSValue(){
    this.getFPSInterval = setInterval(()=>{this.frameCountMessage = this.faceRecognization.getFPSValue()},1000)
  }
}