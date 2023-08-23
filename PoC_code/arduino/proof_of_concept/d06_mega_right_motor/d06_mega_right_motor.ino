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
#include <util/atomic.h>

#define ENCA 2 // GREEN
#define ENCB 3 // YELLOW
#define PWM 6
#define IN2 26 // BLACK
#define IN1 28 // WHITE

// volatile int pos_i = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
// long prevT = 0;
// float eprev = 0;
// float eintegral = 0;
// int prevPos = 0;

// globals
long prevT = 0;
int posPrev = 0;
// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i = 0;
volatile float velocity_i = 0;
volatile long prevT_i = 0;

float v1Filt = 0;
float v1Prev = 0;
float vx[] = {0,0,0};
float vy[] = {0,0,0};
int k = 0;
// float v2Filt = 0;
// float v2Prev = 0;

float eintegral = 0;

// float printSec = 0.01; 
// int secTimes = 10; // if 0.5 printSec = 2, 0.1 printSec = 10
int target = 0;

String valInString = "";
char inChar;

void setup() {
  Serial.begin(115200);
  // Serial.begin(9600);
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
									pos_i = 0;
							}
					}
			} 
	}


	// int pwr = 100/3.0*micros()/1.0e6;
	// int dir = 1;
	// setMotor(dir, pwr, PWM, IN1, IN2);

	// set target position
	// target = 1200;
	// int target = 250*sin(prevT/1e6);

    // read the position in an atomic block
  // to avoid potential misreads
  int pos = 0;
  float velocity2 = 0;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    pos = pos_i;
    // velocity2 = velocity_i;
  }

	// Compute velocity with method 1
  long currT = micros();
  float deltaT = ((float) (currT-prevT))/1.0e6;
  float velocity1 = (pos - posPrev)/deltaT;
  posPrev = pos;
  prevT = currT;

	// Convert count/s to RPM
  // float v1 = velocity1/1320*60.0; // 180 = (1 motor shaft rotation / 6) x (1 output shaft rotation / 30)
  vx[0] = velocity1/1320*60.0;
  // float v2 = velocity2/1320*60.0;

  // float v1 = 333;
  // float v2 = 333;

  // Low-pass filter (25 Hz cutoff)
  //  v1Filt = 0.854*v1Filt + 0.0728*v1 + 0.0728*v1Prev;
  // Low-pass filter (30 Hz cutoff)
  // v1Filt = 0.5218*v1Filt + 0.2390*v1 + 0.2390*v1Prev;
  // v1Prev = v1;
  // v2Filt = 0.854*v2Filt + 0.0728*v2 + 0.0728*v2Prev;
  // v2Prev = v2;

  // Compute the filtered signal
  // (second order Butterworth example)
  float vb[] = {0.007777, 0.01555399, 0.007777};
  float va[] = {1.73550016, -0.76660814};

  vy[0] = va[0]*vy[1] + va[1]*vy[2] +
               vb[0]*vx[0] + vb[1]*vx[1] + vb[2]*vx[2];

  v1Filt = vy[0];

	// Serial.print(v1);
	// Serial.print(",");
	// Serial.print(v1Filt);
	// Serial.println("");
	// delay(1);

	// Set a target
	// float vt = 100*(sin(currT/1e6)>0);
	// float vt = 100;
	float vt = target;

	// Compute the control signal u
	float kp = 2; // if the distance of the current and target is bigger, than add kp to increase the voltage
	float ki = 5; 
	float e = vt-v1Filt;
	eintegral = eintegral + e*deltaT;
	
	float u = kp*e + ki*eintegral;

	//Set the motor speed and direction
	int dir = 1;
	if (u<0){
		dir = -1;
	}
	int pwr = (int) fabs(u);
	if(pwr > 255){
		pwr = 255;
	}
	setMotor(dir,pwr,PWM,IN1,IN2);

  delay(1); // Wait 1ms
  for(int i = 1; i >= 0; i--){
    vx[i+1] = vx[i]; // store xi
    vy[i+1] = vy[i]; // store yi
  }

  if(k % 3 ==0){
    Serial.print(target);
    Serial.print(",");
    // Serial.print(v1);
    Serial.print(vx[0]);
    Serial.print(",");
    Serial.print(v1Filt);
    Serial.print(",");
    // Serial.print(v1t);
    // Serial.print(",");
    Serial.print(dir);
    Serial.println();
  }

  k = k+1;
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
			pos_i++;
		}else{
			pos_i--;
		}
  }
  else{
    if(b == 0){
			pos_i--;
		}else{
			pos_i++;
		}
  }
}

void readEncoderB(){
  int a = digitalRead(ENCA);
	int b = digitalRead(ENCB);

  if(b == 0){
    if(a == 0){
			pos_i--;
		}else{
			pos_i++;
		}
  }
  else{
    if(a == 0){
			pos_i++;
		}else{
			pos_i--;
		}
  }
}