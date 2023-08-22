import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class JoystickService {
  theta:number = 0
  x_left:number  = 0
  y_left:number  = 0
  x_right:number  = 0
  y_right:number  = 0
  radian:number  = 0
  rightDecRPM: number = 0;
  leftDecRPM: number = 0;
  pwr_sin: number = 0;
  pwr_cos: number = 0;
  prevXValue: number = 0;

  constructor() { }

  // get the left hand side thumdstick value
  getLeftCoordinate(gamepad: any){
    // set a dead zone, to eliminate bouncing when user do not control the thumbstick
    const stickDeadZone = 0.05;

    // get the left hand side thumstick x and y axis value
    const x_axis_left = gamepad.axes[0]
    const y_axis_left = -(gamepad.axes[1])

    // console.log(x_axis_left)
    // console.log(y_axis_left)

    // if the x axis value is over or less than the dead zone,
    // which mean user is controlling the thumbstick and move over the dead zone
    if( (x_axis_left < -stickDeadZone || x_axis_left > stickDeadZone) ||
      (y_axis_left < -stickDeadZone || y_axis_left > stickDeadZone)){
        // conver the value from -1 and 1 to -100 and 100
        this.x_left = x_axis_left*100
        this.y_left = y_axis_left*100
    }else{
      // if the value within the dead zone, set a default value
      this.x_left = -111
      this.y_left = -111
    }
  }

  // Calculation the theta / degree value, to calculate the motor power value later
  calThetaDegree(){
    // console.log(this.x_left)
    // console.log(this.y_left)
    // console.log("------------------")
    if((this.x_left>=0)&&(this.y_left>=0)){
      this.theta = (Math.atan(this.y_left/this.x_left))/Math.PI*180;
    }else if((this.x_left<0)&&(this.y_left>=0)){
      this.theta = 180+(Math.atan(this.y_left/this.x_left))/Math.PI*180;
    }else if((this.x_left<0)&&(this.y_left<0)){
      this.theta = 180+(Math.atan(this.y_left/this.x_left))/Math.PI*180;
    }else{
      this.theta = 360+(Math.atan(this.y_left/this.x_left))/Math.PI*180;
    }
  }

  // Calculation the radian of the cos and sin, to calculate the motor power value later
  calCosSinRadian(){
    if(this.theta<45){
      this.radian = Math.cos(this.theta*Math.PI/180);  
    }else if(this.theta<=135){
      this.radian = Math.sin(this.theta*Math.PI/180);  
    }else if(this.theta<=225){
      this.radian = Math.abs(Math.cos(this.theta*Math.PI/180));  
    }else if(this.theta<=315){
      this.radian = Math.abs(Math.sin(this.theta*Math.PI/180));  
    }else{
      this.radian = Math.abs(Math.cos(this.theta*Math.PI/180));  
    }
  }

  calRomoPwr(gamepad: any){
    // get the left hand side thumdstick value
    this.getLeftCoordinate(gamepad)

    // if that is not default value
    if (this.x_left != -111 && this.y_left != -111){
      let pwr_array = [0,0,0,0]
      // Calculation the theta / degree value
      this.calThetaDegree()
      // Calculation teh radian of the cos and sin
      this.calCosSinRadian()

      // if the top-right button do not pressing 
      if(!gamepad.buttons[6]["pressed"]){
        // then calculate the hypotenuse 
        const hypot = Math.hypot(this.y_left, this.x_left);
        // and throught the hypotenuse and radian of the sin cos, 
        // to get the length of the thumbstick user moving
        const radial = hypot * this.radian;
        // console.log(this.radian)

        // Because each of the small wheels inside the mecanum wheels has a 45-degree incline.
        // so we try to rotate it become two 0 degree and two 90 degree 
        // and calculate the radian of the ratated wheel sin and cos
        const sin = Math.sin((this.theta-45)*Math.PI/180);
        const cos = Math.cos((this.theta-45)*Math.PI/180);
        // calculate the max value
        const max = Math.max(Math.abs(sin), Math.abs(cos));

        // to scale up the pwr of motor in some direction
        this.pwr_sin = Math.round(sin*radial*1/max); // limit the max value from 3 to 1
        this.pwr_cos = Math.round(cos*radial*1/max); // limit the max value from 3 to 1

        pwr_array = [this.pwr_cos, this.pwr_sin, this.pwr_sin, this.pwr_cos];
      }

      // if the top-right button is pressing
      if (gamepad.buttons[6]["pressed"]){
        // which mean user decide using normal mode not 360 direction mode to move
        // so, we can just skip the x axix and justify how many length that user push up
        this.pwr_cos = Math.round(this.y_left*1); // limit the max value from 3 to 1
        this.pwr_sin = Math.round(this.y_left*1); // limit the max value from 3 to 1

        // when using the normal mode, the user able throught the right thumdstick to control the device move left or right
        // there is a mapping to convert the value of head moving angle to motor power value
        pwr_array = [this.pwr_cos - this.leftDecRPM <=0 ? 0: this.pwr_cos - this.leftDecRPM, 
                    this.pwr_sin - this.rightDecRPM <=0 ? 0: this.pwr_sin - this.rightDecRPM,
                    this.pwr_sin - this.leftDecRPM <=0 ? 0: this.pwr_sin - this.leftDecRPM,
                    this.pwr_cos - this.rightDecRPM <=0 ? 0: this.pwr_cos - this.rightDecRPM]
      }
      return pwr_array
    }
    return null
  }

  // get the right hand side thumdstick value
  getRightCoordinate(gamepad:any){
    // set a dead zone, to eliminate bouncing when user do not control the thumbstick
    const stickDeadZone = 0.05;
    // get the right hand side thumstick x and y axis value
    const x_axis_right = gamepad.axes[2]
    const y_axis_right = -(gamepad.axes[3])

    // if the x axis value is over or less than the dead zone,
    if( (x_axis_right < -stickDeadZone || x_axis_right > stickDeadZone) ||
      (y_axis_right < -stickDeadZone || y_axis_right > stickDeadZone)){

        // Because the circle top-right is (0.707, 0.707) instead of (1, 1)
        // So to mapping the value, we given a boundery which 0.707 for each of side lenght (a square inside the circle)
        this.x_right = x_axis_right
        this.y_right = y_axis_right

        // once the valuse is over 0.707, or less than -0.707, variable will replace the value to +-0.707
        if (x_axis_right > 0.707){
          this.x_right = 0.707
        }  
        
        if( y_axis_right > 0.707){
          this.y_right = 0.707
        }
        
        if(x_axis_right < -0.707){
          this.x_right = -0.707
        }
        
        if(y_axis_right < -0.707){
          this.y_right = -0.707
        }

    }else{
      // if the value within the dead zone, set a default value
      this.x_right = -111
      this.y_right = -111
    }
  }


  calRomoHead(gamepad:any){
    // get the right hand side thumdstick value
    this.getRightCoordinate(gamepad)

    // if that is not default value
    if(this.x_right != -111 && this.y_right != -111){
      // about the view direction
      let message = "";
      // we mapping the value from -0.707 and 0.707 to 0 and 180 degree
      let head_x = Math.floor(this.mapping(this.x_right, 0.707, -0.707, 180, 0))
      const head_y = Math.floor(this.mapping(this.y_right, -0.707, 0.707, 0, 180))

      // set a center point
      const centerAngle = 90
      // and expand it around 10 degree,
      const centerAngleRight = centerAngle + 10
      const centerAngleLeft = centerAngle - 10

      // if the top-right button is pressing 
      if (gamepad.buttons[6]["pressed"]){
        
        // so if over 100 degree, means user move the right hand side thumdstick to right
        if (head_x >= centerAngleRight) {
          // console.log("move right")
          this.leftDecRPM  = 0 
          // mapping the value from 100 and 180 to 20 and 300
          this.rightDecRPM = Math.floor(this.mapping(head_x, centerAngleRight, 180, 20, Math.max(this.pwr_cos, this.pwr_sin)*2))
        }// so if less than 80 degree, means user move the right hand side thumdstick to left
        else if (head_x <= centerAngleLeft){
          // console.log("move left")
          this.rightDecRPM = 0
          // mapping the value from 0 and 80 to 300 and 20
          // what the sequence is opposite, because we will use the result value to minuts the above motor power
          // so when user move the thumdstick to the end of left, then the power need to minuts 300 value to become zero
          this.leftDecRPM = Math.floor(this.mapping(head_x, 0, centerAngleLeft, Math.max(this.pwr_cos, this.pwr_sin)*2, 20))
          
        }else {
          this.leftDecRPM  = 0
          this.rightDecRPM = 0
        }
      }

      if(head_x === 90 && head_y === 90){
        message = "Center";
      }else if(head_x > 90 && head_y === 90){
        message = "Left";
      }else if(head_x < 90 && head_y === 90){
        message = "Right";
      }else if(head_x === 90 && head_y < 90){
        message = "Down";
      }else if(head_x === 90 && head_y > 90){
        message = "Up";
      }else if(head_x > 90 && head_y < 90){
        message = "Down Left";
      }else if(head_x < 90 && head_y < 90){
        message = "Down Right";
      }else if(head_x > 90 && head_y > 90){
        message = "Up Left";
      }else if(head_x < 90 && head_y > 90){
        message = "Up Right";
      }
      
      return {"head_x": head_x, "head_y": head_y, "message": message}
    }
    return null
  }

  mapping(oldVal: number, oldMin: number, oldMax: number, newMin: number, newMax: number) {
    return (oldVal - oldMin) / (oldMax - oldMin) * (newMax - newMin) + newMin;
  }
}
