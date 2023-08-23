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

#define ENCA_R 2 // YELLOW
#define ENCB_R 3 // GREEN
#define PWM_R 6
#define IN2_R 26 // BLACK
#define IN1_R 28 // WHITE

#define ENCA_L 19 // GREEN
#define ENCB_L 18 // YELLOW
#define PWM_L 5
#define IN2_L 24 // BLACK
#define IN1_L 22 // WHITE

// volatile int pos_i = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
// long prevT = 0;
// float eprev = 0;
// float eintegral = 0;
// int prevPos = 0;

// globals
long prevT_R = 0;
int posPrev_R = 0;
// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i_R = 0;
volatile float velocity_i_R = 0;
volatile long prevT_i_R = 0;

float v1Filt_R = 0;
float v1Prev_R = 0;
float vx_R[] = {0,0,0};
float vy_R[] = {0,0,0};

long prevT_L = 0;
int posPrev_L = 0;
// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i_L = 0;
volatile float velocity_i_L = 0;
volatile long prevT_i_L = 0;

float v1Filt_L = 0;
float v1Prev_L = 0;
float vx_L[] = {0,0,0};
float vy_L[] = {0,0,0};

int k = 0;
// float v2Filt = 0;
// float v2Prev = 0;

float eintegral_R = 0;
float eintegral_L = 0;

// float printSec = 0.01; 
// int secTimes = 10; // if 0.5 printSec = 2, 0.1 printSec = 10
int target = 0;

String valInString = "";
char inChar;

void setup() {
  Serial.begin(115200);
  // Serial.begin(9600);
  pinMode(ENCA_R,INPUT);
  pinMode(ENCB_R,INPUT);
  pinMode(ENCA_L,INPUT);
  pinMode(ENCB_L,INPUT);

	// unsigned long int timeInterval = (printSec * 1000000);
  // Timer1.initialize(timeInterval); // 0.5 microseconds = 0.5 second
  // Timer1.attachInterrupt(serialPrint);

  attachInterrupt(digitalPinToInterrupt(ENCA_R),readEncoderA_R, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_R),readEncoderB_R, CHANGE);
	attachInterrupt(digitalPinToInterrupt(ENCA_L),readEncoderA_L, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_L),readEncoderB_L, CHANGE);
  
  pinMode(PWM_R,OUTPUT);
  pinMode(IN1_R,OUTPUT);
  pinMode(IN2_R,OUTPUT);
	pinMode(PWM_L,OUTPUT);
  pinMode(IN1_L,OUTPUT);
  pinMode(IN2_L,OUTPUT);
  
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
									pos_i_R = 0;
									pos_i_L = 0;
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
  int pos_R = 0;
	int pos_L = 0;
  // float velocity2 = 0;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    pos_R = pos_i_R;
		pos_L = pos_i_L;
    // velocity2 = velocity_i;
  }

	// Compute velocity with method 1
  long currT_R = micros();
  float deltaT_R = ((float) (currT_R-prevT_R))/1.0e6;
  float velocity1_R = (pos_R - posPrev_R)/deltaT_R;
  posPrev_R = pos_R;
  prevT_R = currT_R;

	long currT_L = micros();
  float deltaT_L = ((float) (currT_L-prevT_L))/1.0e6;
  float velocity1_L = (pos_L - posPrev_L)/deltaT_L;
  posPrev_L = pos_L;
  prevT_L = currT_L;

	// Convert count/s to RPM
  // float v1 = velocity1/1320*60.0; // 180 = (1 motor shaft rotation / 6) x (1 output shaft rotation / 30)
  vx_R[0] = velocity1_R/1320*60.0;
	vx_L[0] = velocity1_L/1320*60.0;
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
  float vb_R[] = {0.007777, 0.01555399, 0.007777};
  float va_R[] = {1.73550016, -0.76660814};

  vy_R[0] = va_R[0]*vy_R[1] + va_R[1]*vy_R[2] +
               vb_R[0]*vx_R[0] + vb_R[1]*vx_R[1] + vb_R[2]*vx_R[2];

  v1Filt_R = vy_R[0];

	float vb_L[] = {0.007777, 0.01555399, 0.007777};
  float va_L[] = {1.73550016, -0.76660814};

  vy_L[0] = va_L[0]*vy_L[1] + va_L[1]*vy_L[2] +
               vb_L[0]*vx_L[0] + vb_L[1]*vx_L[1] + vb_L[2]*vx_L[2];

  v1Filt_L = vy_L[0];

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
	float kp = 5; // if the distance of the current and target is bigger, than add kp to increase the voltage
	float ki = 30; 
	float e_R = vt-v1Filt_R;
	eintegral_R = eintegral_R + e_R*deltaT_R;
	
	float u_R = kp*e_R + ki*eintegral_R;

	float e_L = vt-v1Filt_L;
	eintegral_L = eintegral_L + e_L*deltaT_L;
	
	float u_L = kp*e_L + ki*eintegral_L;

	//Set the motor speed and direction
	int dir_R = 1;
	int dir_L = 1;

	if (u_R<0){
		dir_R = -1;
	}

	if (u_L<0){
		dir_L = -1;
	}

	int pwr_R = (int) fabs(u_R);
	if(pwr_R > 255){
		pwr_R = 255;
	}

	int pwr_L = (int) fabs(u_L);
	if(pwr_L > 255){
		pwr_L = 255;
	}

	setMotor(dir_R,pwr_R,PWM_R,IN1_R,IN2_R);
	setMotor(dir_L,pwr_L,PWM_L,IN1_L,IN2_L);

  delay(1); // Wait 1ms
  for(int i = 1; i >= 0; i--){
    vx_R[i+1] = vx_R[i]; // store xi
    vy_R[i+1] = vy_R[i]; // store yi

		vx_L[i+1] = vx_L[i]; // store xi
    vy_L[i+1] = vy_L[i]; // store yi
  }

  if(k % 3 ==0){
    Serial.print(target);
    Serial.print(",");
    // Serial.print(v1);
    Serial.print(vx_R[0]);
    Serial.print(",");
    Serial.print(v1Filt_R);
    Serial.print(",");
    // Serial.print(v1t);
    // Serial.print(",");
    Serial.print(dir_R);
    Serial.print("      ");

		Serial.print(target);
    Serial.print(",");
    // Serial.print(v1);
    Serial.print(vx_L[0]);
    Serial.print(",");
    Serial.print(v1Filt_L);
    Serial.print(",");
    // Serial.print(v1t);
    // Serial.print(",");
    Serial.print(dir_L);
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

void readEncoderA_R(){
	int a_R = digitalRead(ENCA_R);
  int b_R = digitalRead(ENCB_R);

  if(a_R == 0){
    if(b_R == 0){
			pos_i_R++;
		}else{
			pos_i_R--;
		}
  }
  else{
    if(b_R == 0){
			pos_i_R--;
		}else{
			pos_i_R++;
		}
  }
}

void readEncoderB_R(){
  int a_R = digitalRead(ENCA_R);
	int b_R = digitalRead(ENCB_R);

  if(b_R == 0){
    if(a_R == 0){
			pos_i_R--;
		}else{
			pos_i_R++;
		}
  }
  else{
    if(a_R == 0){
			pos_i_R++;
		}else{
			pos_i_R--;
		}
  }
}

void readEncoderA_L(){
	int a_L = digitalRead(ENCA_L);
  int b_L = digitalRead(ENCB_L);

  if(a_L == 0){
    if(b_L == 0){
			pos_i_L++;
		}else{
			pos_i_L--;
		}
  }
  else{
    if(b_L == 0){
			pos_i_L--;
		}else{
			pos_i_L++;
		}
  }
}

void readEncoderB_L(){
  int a_L = digitalRead(ENCA_L);
	int b_L = digitalRead(ENCB_L);

  if(b_L == 0){
    if(a_L == 0){
			pos_i_L--;
		}else{
			pos_i_L++;
		}
  }
  else{
    if(a_L == 0){
			pos_i_L++;
		}else{
			pos_i_L--;
		}
  }
}