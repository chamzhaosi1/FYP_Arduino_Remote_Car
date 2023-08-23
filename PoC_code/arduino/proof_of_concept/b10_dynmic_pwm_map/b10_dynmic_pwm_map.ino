// CONCLUSION
// B01 (DOUBLE - RASING (1 TIME )) -- 330 COUNT = 360 DEGREE
// B02 (DOUBLE - RASING / FAILING (2 TIME )) -- 660 COUNT = 360 DEGREE
// B03 /B05  (DOUBLE - CHANGE (4 TIME )) -- 1320 COUNT = 360 DEGREE

#include <SPI.h>
#include <SD.h>
#include <TimerOne.h>

#define ENCA 2 // GREEN
#define ENCB 3 // YELLOW
#define PWM 5 // 
#define IN2 8 // BLACK
#define IN1 4 // WHITE
// #define PWMVAL 75*2
// #define PWMVAL 255

volatile int posi = 0;
int cur_posi = 0;
int target = 0;
int dir = 1;
int pwmVal = 0;
float printSec = 0.1; 
int secTimes = 10; // if 0.5 printSec = 2, 0.1 printSec = 10

int prevC;

String valInString = "";
char inChar;

void setup() {
    Serial.begin(9600);
    pinMode(ENCA,INPUT);
    pinMode(ENCB,INPUT);

	unsigned long int timeInterval = (printSec * 1000000);
    Timer1.initialize(timeInterval); // 0.5 microseconds = 0.5 second
    Timer1.attachInterrupt(serialPrint);

    attachInterrupt(digitalPinToInterrupt(ENCA),readEncoderA, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENCB),readEncoderB, CHANGE);
    
    pinMode(PWM,OUTPUT);
    pinMode(IN1,OUTPUT);
    pinMode(IN2,OUTPUT);
    
    // Serial.println("target pos");

    while (!Serial) {
        // wait for serial port to connect
    }
}

void loop() {
	while (Serial.available() > 0) {

        int inputChar = Serial.read();
        if(isDigit(inputChar)){
            valInString += (char)inputChar;
            // Serial.println(valInString);

        }else if(isAlpha(inputChar)) {
            valInString = "";
            inChar = (char)inputChar;

        }else if ((char)inputChar == '\r') {
            // Serial.println(valInString);
            if(valInString != ""){
                // Serial.println(valInString.toInt());
                target = (valInString.toInt());
                valInString = "";
            }else{
                Serial.println(inChar);

                if(inChar == 'R' || inChar == 'r'){
                    target = 0;
                }

                if(inChar == 'O' || inChar == 'o'){
                    target = 0;
                    posi = 0;
                }
            }
        } 
    }
    
    // When hitting the target stop to rotate
    if(target > posi){
        dir=1;
    }
    
    if(target < posi){
        dir=-1;
    }
    setMotor(dir, pwmVal, PWM, IN1, IN2);
	delay(1);
}

void serialPrint(){
	
	int cphs = (posi - prevC);
	float rpm = cphs / ((float)1320/(secTimes * (float)60));
	// float rpm = cphs / 0.45;

	int diff = abs(target - posi);

	if(diff < 10){
		pwmVal = 0;
	}else if(diff < 50){
		pwmVal = map(diff, 51, 100, 75, 80);
	}else if(diff < 500){
		pwmVal = map(diff, 100, 500, 80, 85);
	}else if(diff < 850){
		pwmVal = map(diff, 500, 850, 85, 180);
	}else if(diff < 1320){
		pwmVal = map(diff, 850, 1320, 180, 225);
	}

	// if(diff < 10){
	// 	pwmVal = 0;
	// }else if(diff < 50){
	// 	pwmVal = map(diff, 51, 100, 75, 80);
	// }else if(diff < 100){
	// 	pwmVal = map(diff, 101, 150, 80, 85);
	// }else if(diff < 150){
	// 	pwmVal = map(diff, 151, 200, 85, 90);
	// }else if(diff < 200){
	// 	pwmVal = map(diff, 201, 250, 90, 95);
	// }else if(diff < 250){
	// 	pwmVal = map(diff, 251, 300, 95, 100);
	// }else if(diff < 300){
	// 	pwmVal = map(diff, 301, 350, 100, 105);
	// }else if(diff < 350){
	// 	pwmVal = map(diff, 351, 400, 105, 110);
	// }else if(diff < 400){
	// 	pwmVal = map(diff, 401, 450, 110, 115);
	// }else if(diff < 450){
	// 	pwmVal = map(diff, 451, 500, 115, 120);
	// }else if(diff < 500){
	// 	pwmVal = map(diff, 501, 550, 120, 125);
	// }else if(diff < 550){
	// 	pwmVal = map(diff, 551, 600, 125, 130);
	// }else if(diff < 600){
	// 	pwmVal = map(diff, 601, 650, 130, 135);
	// }else if(diff < 650){
	// 	pwmVal = map(diff, 651, 700, 135, 140);
	// }else if(diff < 700){
	// 	pwmVal = map(diff, 701, 750, 145, 150);
	// }else if(diff < 750){
	// 	pwmVal = map(diff, 751, 800, 150, 155);
	// }else if(diff < 800){
	// 	pwmVal = map(diff, 801, 850, 160, 165);
	// }else if(diff < 850){
	// 	pwmVal = map(diff, 851, 900, 165, 170);
	// }else if(diff < 900){
	// 	pwmVal = map(diff, 901, 950, 170, 175);
	// }else if(diff < 950){
	// 	pwmVal = map(diff, 951, 1000, 175, 180);
	// }else if(diff < 1000){
	// 	pwmVal = map(diff, 1001, 1050, 180, 185);
	// }else if(diff < 1050){
	// 	pwmVal = map(diff, 1051, 1100, 185, 190);
	// }else if(diff < 1100){
	// 	pwmVal = map(diff, 1101, 1150, 190, 195);
	// }else if(diff < 1150){
	// 	pwmVal = map(diff, 1151, 1200, 195, 200);
	// }else if(diff < 1200){
	// 	pwmVal = map(diff, 1201, 1250, 200, 205);
	// }else if(diff < 1250){
	// 	pwmVal = map(diff, 1251, 1300, 205, 210);
	// }else if(diff < 1300){
	// 	pwmVal = map(diff, 1301, 1320, 210, 215);
	// }else if(diff < 1320){
	// 	pwmVal = map(diff, 1321, 1000000, 215, 225);
	// }

	// if(diff < 50){
	// 	pwmVal = 0;
	// }else if(diff < 100){
	// 	pwmVal = 75;
	// }else if(diff < 200){
	// 	pwmVal = 111;
	// }else if(diff < 300){
	// 	pwmVal = 147;
	// }else if(diff < 500){
	// 	pwmVal = 165;
	// }else if(diff < 600){
	// 	pwmVal = 183;
	// }else if(diff < 700){
	// 	pwmVal = 201;
	// }else if(diff < 800){
	// 	pwmVal = 219;
	// }else if(diff < 900){
	// 	pwmVal = 237;
	// }else{
	// 	pwmVal = 255;
	// }



  Serial.print(" - ");
  Serial.print(target);
  Serial.print(" , ");
  Serial.print(posi);
  Serial.print(" , ");
  Serial.print(dir);
  Serial.print(" , ");
  Serial.print(cphs);
  Serial.print(" , ");
  Serial.print((int)rpm);
  Serial.print(" , ");
  Serial.print(diff);
  Serial.print(" , ");
  Serial.println(pwmVal);

	prevC = posi;
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == -1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == 1){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
  }
}

void readEncoderA(){
	int a = digitalRead(ENCA);
  int b = digitalRead(ENCB);

  if(a == 0){
    if(b == 0){
			posi++;
		}else{
			posi--;
		}
  }
  else{
    if(b == 0){
			posi--;
		}else{
			posi++;
		}
  }
}

void readEncoderB(){
  int a = digitalRead(ENCA);
	int b = digitalRead(ENCB);

  if(b == 0){
    if(a == 0){
			posi--;
		}else{
			posi++;
		}
  }
  else{
    if(a == 0){
			posi++;
		}else{
			posi--;
		}
  }
}