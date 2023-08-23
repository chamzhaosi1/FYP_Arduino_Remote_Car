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

int prevC;

String valInString = "";
char inChar;

void setup() {
    Serial.begin(9600);
    pinMode(ENCA,INPUT);
    pinMode(ENCB,INPUT);

    Timer1.initialize(500000); // 0.5 microseconds = 0.5 second
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

}

void serialPrint(){
	
	int cphs = (posi - prevC);
	int rpm = cphs / 11;

	int diff = abs(target - posi);

	if(diff < 50){
		pwmVal = 0;
	}else if(diff < 100){
		pwmVal = 75;
	}else if(diff < 200){
		pwmVal = 111;
	}else if(diff < 300){
		pwmVal = 147;
	}else if(diff < 500){
		pwmVal = 165;
	}else if(diff < 600){
		pwmVal = 183;
	}else if(diff < 700){
		pwmVal = 201;
	}else if(diff < 800){
		pwmVal = 219;
	}else if(diff < 900){
		pwmVal = 237;
	}else{
		pwmVal = 255;
	}

  Serial.print(" - ");
  Serial.print(target);
  Serial.print(" , ");
  Serial.print(posi);
  Serial.print(" , ");
  Serial.print(dir);
	Serial.print(" , ");
  Serial.print(cphs);
	Serial.print(" , ");
  Serial.print(rpm);
	Serial.print(" , ");
  Serial.println(diff);

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