import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class KeyboardMouseService {

  exit2time: number = 0;
  FaceRecognitionMode: any;
  directionValues: number = -1 // save the direction
  rpmValues: number = 50 // save the initial rmp speed
  motorArray: number[] = [0,0,0,0] // Left-Front, Right-Front, Left-Back, Right-Back // for save direction and rmp
  rotationAngle: number = 0;
  rightDecRPM: number = 0;
  leftDecRPM: number = 0;
  prevXValue: number = 0;

  constructor() { }

  handleKeyDown(event: KeyboardEvent): Boolean | number[] | string {
    // this.isExit = false
    let keyValue = event.key
    console.log(keyValue)

    switch (keyValue) {
      case "1":
        return "FRM"

      case "2":
        return "TRAY"
        
      case "Escape":
        this.exit2time++;
        
        if (this.exit2time === 2) {
          // // close the livestreaming
          // this.livestreaming.closeWebSocket()
          // // redirect to dashboard page
          // this.router.navigate(['/'])

          // this.isExit = true
          return true
        }

        setTimeout(() => {
          // after 3 seconds, set the time back to 0
          this.exit2time = 0
        }, 3000);
        return ""

      case "p":
      case "P":
        return "pause"
      
      // W (shirt + w) = forward but based on the head chg direction
      case "W":
        // console.log("forward but based on the head chg direction")
        this.directionValues = 0 
        break

      // w = forward only
      case "w":
        // console.log("forward")
        this.directionValues = 1
        break

      // a or A = left vertically move
      case "a":
      case "A":
        // console.log("left")
        this.directionValues = 2
        break

      // d or D = right vertically move
      case "d":
      case "D":
        // console.log("right")
        this.directionValues = 3 
        break
      
      // x or X = backward only
      case "x":
      case "X":
        // console.log("back")
        this.directionValues = 4 
        break

      // q or Q = North-West moving
      case "q":
      case "Q":
        // console.log("North-West")
        this.directionValues = 5
        break 

      // e or E = North-East moving
      case "e":
      case "E":
        // console.log("North-East")
        this.directionValues = 6 
        break 

      // z or Z = South-West moving
      case "z":
      case "Z":
        // console.log("South-West")
        this.directionValues = 7 
        break 

      // c or C = South-East moving
      case "c":
      case "C":
        // console.log("South-East")
        this.directionValues = 8 
        break 

      default:
        console.log("Wrong control key")
        // if press wrong than return a initail value
        return [0,0,0,0]
    }

    this.rotationAngle = this.rpmValues
    return this.calEachMotors()
  }

  // any key is released the value will be counted again
  handleKeyUp(event: KeyboardEvent) : number[] {
    // set rmp to 0
    // this rpmValues and rotationAngle are for the mecanum wheeel draw
    this.rpmValues = 50;
    this.rotationAngle = 0;
    this.rightDecRPM = 0;
    this.leftDecRPM = 0;

    // this is return initial motor rpm
    return [0,0,0,0]
  }

  calEachMotors(): number[] {
    const direction = this.directionValues 
    // const rpm = this.rpmValues;
    const rpm = this.rpmValues;

    switch (direction){
      case 0:
        this.motorArray = [
            (rpm - this.leftDecRPM <= 0 ? 0 : rpm - this.leftDecRPM),
           (rpm - this.rightDecRPM <= 0 ? 0 : rpm - this.rightDecRPM), 
           (rpm - this.leftDecRPM <= 0 ? 0 : rpm - this.leftDecRPM), 
           (rpm  - this.rightDecRPM <= 0 ? 0 : rpm - this.rightDecRPM)
          ]
        break;
      case 1:
        this.motorArray = [rpm, rpm, rpm, rpm]
        break;

      case 2:
        this.motorArray = [-rpm, rpm, rpm, -rpm]
        break;

      case 3:
        this.motorArray = [rpm, -rpm, -rpm, rpm]
        break;

      case 4:
        this.motorArray = [-rpm, -rpm, -rpm, -rpm]
        break;

      case 5:
        this.motorArray = [0, rpm, rpm, 0]
        break;

      case 6:
        this.motorArray = [rpm, 0, 0, rpm]
        break;

      case 7:
        this.motorArray = [-rpm, 0, 0, -rpm]
        break;

      case 8:
        this.motorArray = [0, -rpm, -rpm, 0]
        break;
    }

    return this.motorArray
  }

  handleMouseMove(event: MouseEvent){
    // get window width and height
    let windW = window.innerWidth
    let windH = window.innerHeight

    // get window center
    let centerW = Math.floor(windW/2)
    let centerH = Math.floor(windH/2)

    //let center has 100 px buffer
    let centerRight = centerW + 5
    let centerLeft = centerW + 5

    // get the x and y position of the mouse
    let mouseX = event.clientX
    let mouseY = event.clientY

    if (mouseX > centerRight) {
      // console.log("move right")
      this.leftDecRPM  = 0 
      this.rightDecRPM = Math.floor(this.mapping(mouseX, centerRight, windW, 20, this.rpmValues*2)) // multiple 2 because the angle wil be also time 2
    }else if (mouseX < centerLeft){
      // console.log("move left")
      this.rightDecRPM = 0
      this.leftDecRPM = Math.floor(this.mapping((centerLeft - mouseX), 0, centerLeft, 20, this.rpmValues*2)) // multiple 2 because the angle wil be also time 2
    }else {
      this.leftDecRPM  = 0
      this.rightDecRPM = 0
    }

    // mapping the value to the angle 
    let angleX = Math.floor(this.mapping(mouseX, windW, 0, 180, 0))
    let angleY = Math.floor(this.mapping(mouseY, windH, 0, 0, 180))

    // calibarate and angle when user move the view point from left edge of screen to center in left section 
    let isCalibarated = false;
    // if the user curson in left section
    if (mouseX < centerLeft){
      if (this.prevXValue === 0){
        // record the prevXValue, because the error not will be happend when user move the cursor from left edge of screen to center 
        this.prevXValue = mouseX 
      }

      // if the pre value is lower than current, which mean user is doing so
      if (this.prevXValue < mouseX){
        angleX += 18

        // record the status, to show the view point direction message
        isCalibarated = true;

      }else if (this.prevXValue > mouseX) {
        this.prevXValue = 0
      }
    }

    let message = "";
    if(angleX === 90 && angleY === 90){
      message = "Center";
    }else if(angleX < 90 && angleY === 90){
      message = "Left";
    }else if(angleX > 90 && angleY === 90){
      message = "Right";
    }else if(angleX === 90 && angleY < 90){
      message = "Down";
    }else if(angleX === 90 && angleY > 90){
      message = "Up";
    }else if(angleX < 90 && angleY < 90){
      message = "Down Left";
    }else if(angleX > 90 && angleY < 90){
      message = "Down Right";
    }else if(angleX < 90 && angleY > 90){
      message = "Up Left";
    }else if(angleX > 90 && angleY > 90){
      message = "Up Right";
    }

    // if the angle is callibarated, then minus the calibarate value and show the actual message
    if (isCalibarated){
      if((angleX - 18) < 90 && angleY === 90){
          message = "Left";
      }else if((angleX - 18) < 90 && angleY < 90){
          message = "Down Left";
      }else if((angleX - 18) < 90 && angleY > 90){
          message = "Up Left";
      }
    }
    
    return {"rightDecRPM": this.rightDecRPM, "leftDecRPM": this.leftDecRPM, "angleX": angleX, "angleY": angleY, "message": message}
  }

  RPMScroll(event: WheelEvent): number {
    this.rpmValues -= event.deltaY/20;

    if (this.rpmValues >= 100 ){ // limit the max value from 300 to 100
      this.rpmValues = 100 // limit the max value from 300 to 100
    }else if(this.rpmValues <= 0){
      this.rpmValues = 0
    }

    return this.rpmValues
  }

  mapping(oldVal: number, oldMin: number, oldMax: number, newMin: number, newMax: number) {
    return (oldVal - oldMin) / (oldMax - oldMin) * (newMax - newMin) + newMin;
  }
}
