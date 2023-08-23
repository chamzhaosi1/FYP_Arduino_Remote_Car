// This alternate version of the code does not require
// atomic.h. Instead, interrupts() and noInterrupts() 
// are used. Please use this code if your 
// platform does not support ATOMIC_BLOCK.

// CONCLUSION
// B01 (DOUBLE - RASING (1 TIME )) -- 330 COUNT = 360 DEGREE
// B02 (DOUBLE - RASING / FAILING (2 TIME )) -- 660 COUNT = 360 DEGREE
// B03 /B05  (DOUBLE - CHANGE (4 TIME )) -- 1320 COUNT = 360 DEGREE

#include <SPI.h>
#include <SD.h>
#include <TimerOne.h>

#define ENCA 2 // GREEN
#define ENCB 3 // YELLOW
#define PWM 5
#define IN2 8 // BLACK
#define IN1 4 // WHITE

volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
long prevT = 0;
float eprev = 0;
float eintegral = 0;
int prevPos = 0;

float printSec = 0.01; 
// int secTimes = 10; // if 0.5 printSec = 2, 0.1 printSec = 10
int target = 0;

String valInString = "";
char inChar;

void setup() {
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);

	// unsigned long int timeInterval = (printSec * 1000000);
  // Timer1.initialize(timeInterval); // 0.5 microseconds = 0.5 second
  // Timer1.attachInterrupt(serialPrint);

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

    // set target position
    // target = 1200;
    // int target = 250*sin(prevT/1e6);

    // PID constants
    float kp = 1;
    float kd = 0.16;
    float ki = 0.0;

    // time difference
    long currT = micros();
    float deltaT = ((float) (currT - prevT))/( 1.0e6 );
    prevT = currT;

    // Read the position
    int pos = 0; 
    noInterrupts(); // disable interrupts temporarily while reading
    pos = posi;
    interrupts(); // turn interrupts back on
    
    // error
    int e = pos - target;

    // derivative
    float dedt = (e-eprev)/(deltaT);

    // integral
    eintegral = eintegral + e*deltaT;

    // control signal
    float u = kp*e + kd*dedt + ki*eintegral;

    // motor power
    float pwr = fabs(u);
    if( pwr > 255 ){
        pwr = 255;
    }

    // motor direction
    int dir = 1;
    if(u<0){
        dir = -1;
    }

    // signal the motor
    setMotor(dir,pwr,PWM,IN1,IN2);

    // store previous error
    eprev = e;    

		Serial.print(target);
		Serial.print(",");
		Serial.print(posi);
		Serial.println();
}

void serialPrint(){
	// Serial.print(" - ");
	// Serial.print(target);
	// Serial.print(",");
	// Serial.print(posi);
	// Serial.println();
}


void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == -1){
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