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
#include <util/atomic.h>
#include <PinChangeInterrupt.h>
// #include <PinChangeInt.h>

// FR = FRONT RIGHT
// FL = FRONT LEFT
// BR = BACK RIGHT
// BL = BACK LEFT

#define FR 0
#define FL 1
#define BR 2
#define BL 3

// FRONT RIGHT
// #define ENCA_FR 18 // GREEN
// #define ENCB_FR 19 // YELLOW
// #define PWM_FR 4
// #define IN2_FR 22 
// #define IN1_FR 24 

// FRONT LEFT
#define ENCA_FL 11 // GREEN
#define ENCB_FL 10 // YELLOW
#define PWM_FL 5
#define IN2_FL 28
#define IN1_FL 26 

// globals
long prevT[] = {0,0,0,0};
int posPrev[] = {0,0,0,0};
int pos[] = {0,0,0,0};

// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i[] = {0,0,0,0};
volatile float velocity_i[] = {0,0,0,0};
volatile long prevT_i[] = {0,0,0,0};

float eintegral[] = {0,0,0,0};
float vFilt[] = {0,0,0,0};
float vPrev[] = {0,0,0,0};
float vx[][3] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0}};
float vy[][3] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0}};

// for count loop, every three time will be print out the value
int k = 0;

int target = 0;

String valInString = "";
char inChar;

void setup() {
  Serial.begin(115200);
  // Serial.begin(9600);
  pinMode(ENCA_FL,INPUT);
  pinMode(ENCB_FL,INPUT);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(ENCA_FL), readEncoderAFL_wrapper, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(ENCB_FL), readEncoderBFL_wrapper, CHANGE);
//   attachPCINT(digitalPinToPCINT(ENCA_FL), readEncoderAFL_wrapper, CHANGE);
//   attachPCINT(digitalPinToPCINT(ENCB_FL), readEncoderBFL_wrapper, CHANGE);

  pinMode(PWM_FL,OUTPUT);
  pinMode(IN1_FL,OUTPUT);
  pinMode(IN2_FL,OUTPUT);

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
									pos_i[FL] = 0;
							}
					}
			} 
	}

  // read the position in an atomic block
  // to avoid potential misreads
  
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    pos[FL] = pos_i[FL];
  }

	//Invoke compute velocity function
	float deltaT[] = {0,0,0,0};
	float velocity[] = {0,0,0,0};
	computeVelocity(FL, deltaT, velocity, pos);

	//Invoke convert count/s to RPM
	convertToRPM(FL, velocity);

  // Compute the filtered signal
  // (second order Butterworth example)
	computeFilteredSignal(FL);

	// Set a target
	// float vt = 100*(sin(currT/1e6)>0);
	// float vt = 100;
	float vt = target;

	// Compute the control signal u
	float u[] = {0,0,0,0};
	computeControlSignalU(FL, vt, u, deltaT);

	//Set the motor speed and direction
	int dir[] = {1,1,1,1};
	int pwr[] = {0,0,0,0};
	setMotorSpeedDireaction(FL, u, dir, pwr);

	// motor start
	setMotor(dir[FL], pwr[FL], PWM_FL, IN1_FL, IN2_FL);

  delay(1); // Wait 1ms
  stortVPrevValue(FL);


	// every three time loops, will print out the value
  if(k % 3 ==0){
    serialPrint(vt, dir);
  }

  k = k+1;
}

void serialPrint(int target, int* dir){
	Serial.print(target);
	Serial.print(",");
	Serial.print(vx[FL][0]);
	Serial.print(",");
	Serial.print(vFilt[FL]);
	Serial.print(",");
	Serial.print(dir[FL]);
	Serial.print(",");
	Serial.print(posPrev[FL]);
	Serial.print(",");
	Serial.print(pos[FL]);
	Serial.println("");
}

void stortVPrevValue(int motorIndex){
	for(int i = 1; i >= 0; i--){
    vx[motorIndex][i+1] = vx[motorIndex][i]; // store xi
    vy[motorIndex][i+1] = vy[motorIndex][i]; // store yi
  }
}

void setMotorSpeedDireaction(int motorIndex, float* u, int* dir, int* pwr){
	// Serial.println(motorIndex);
	// Serial.println(u[motorIndex]);
	if (u[motorIndex]<0){
		dir[motorIndex] = -1;
	}

	pwr[motorIndex] = (int) fabs(u[motorIndex]);
	if(pwr[motorIndex] > 255){
		pwr[motorIndex] = 255;
	}
}

void computeControlSignalU(int motorIndex, int vt, float* u, float* deltaT){
	float kp = 5; // if the distance of the current and target is bigger, than add kp to increase the voltage
	float ki = 30; 
	float e = vt-vFilt[motorIndex];
	eintegral[motorIndex] = eintegral[motorIndex] + e*deltaT[motorIndex];
	
	u[motorIndex] = kp*e + ki*eintegral[motorIndex];
}

void computeFilteredSignal(int motorIndex){
	float vb[] = {0.007777, 0.01555399, 0.007777};
  float va[] = {1.73550016, -0.76660814};

	vy[motorIndex][0] = va[0]*vy[motorIndex][1] + va[1]*vy[motorIndex][2] +
            	vb[0]*vx[motorIndex][0] + vb[1]*vx[motorIndex][1] + vb[2]*vx[motorIndex][2];

  vFilt[motorIndex] = vy[motorIndex][0];
}

void convertToRPM(int motorIndex, float* velocity){
	vx[motorIndex][0] = velocity[motorIndex]/1320*60.0;
}

void computeVelocity(int motorIndex, float* deltaT, float* velocity, int* pos){
	long currT = micros();
  deltaT[motorIndex] = ((float) (currT-prevT[motorIndex]))/1.0e6;
  velocity[motorIndex] = (pos[motorIndex] - posPrev[motorIndex])/deltaT[motorIndex];
	posPrev[motorIndex] = pos[motorIndex];
	prevT[motorIndex] = currT;
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

void readEncoderAFL_wrapper(){
	readEncoderA(FL, ENCA_FL, ENCB_FL);
}

void readEncoderBFL_wrapper(){
	readEncoderB(FL, ENCA_FL, ENCB_FL);
}

void readEncoderA(int motorIndex, int ENCA, int ENCB){
	int a = digitalRead(ENCA);
  int b = digitalRead(ENCB);

  if(a == 0){
    if(b == 0){
			pos_i[motorIndex]++;
		}else{
			pos_i[motorIndex]--;
		}
  }
  else{
    if(b == 0){
			pos_i[motorIndex]--;
		}else{
			pos_i[motorIndex]++;
		}
  }
}

void readEncoderB(int motorIndex, int ENCA, int ENCB){
  int a = digitalRead(ENCA);
	int b = digitalRead(ENCB);

  if(b == 0){
    if(a == 0){
			pos_i[motorIndex]--;
		}else{
			pos_i[motorIndex]++;
		}
  }
  else{
    if(a == 0){
			pos_i[motorIndex]++;
		}else{
			pos_i[motorIndex]--;
		}
  }
}

