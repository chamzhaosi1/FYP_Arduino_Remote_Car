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
#include <Servo.h>
#include <PinChangeInterrupt.h>

Servo x_servo;
Servo y_servo;
Servo h_servo;

#define X 8
#define Y 9
#define H 12

// FR = FRONT RIGHT
// FL = FRONT LEFT
// BR = BACK RIGHT
// BL = BACK LEFT

#define FR 0
#define FL 1
#define BR 2
#define BL 3

// FRONT RIGHT
#define ENCA_FR 18 // GREEN 
#define ENCB_FR 19 // YELLOW
#define PWM_FR 4
#define IN2_FR 22 
#define IN1_FR 24 

// FRONT LEFT
#define ENCA_FL 11 // GREEN
#define ENCB_FL 10 // YELLOW
#define PWM_FL 5
#define IN2_FL 28
#define IN1_FL 26 

// BACK RIGHT
#define ENCA_BR 20 // GREEN
#define ENCB_BR 21 // YELLOW
#define PWM_BR 6
#define IN2_BR 30
#define IN1_BR 32 

// BACK LEFT
#define ENCA_BL 3 // GREEN
#define ENCB_BL 2 // YELLOW
#define PWM_BL 7
#define IN2_BL 36
#define IN1_BL 34 

// globals
long prevT[] = {0,0,0,0};
long posPrev[] = {0,0,0,0};

// Use the "volatile" directive for variables
// used in an interrupt
volatile long pos_i[] = {0,0,0,0};

float eintegral[] = {0,0,0,0};
float vt[] = {0,0,0,0};
float vFilt[] = {0,0,0,0};
float vx[][3] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0}};
float vy[][3] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0}};

bool FR_abs = false;
bool FL_abs = false;
bool BR_abs = false;
bool BL_abs = false;
bool temp_stop[] = {false, false, false, false};
bool working[] = {false, false, false, false};

int dir[4];
float u[] = {0,0,0,0};
double deltaT[] = {0,0,0,0};
float velocity[] = {0,0,0,0};
int pwr[] = {0,0,0,0};
long pos[] = {0,0,0,0};
int prev_dir[] = {0,0,0,0};
int prev_rmp[] = {0,0,0,0};
int temp_dir[] = {0,0,0,0};
int count[] = {0,0,0,0};
int StringCount = 0;
bool isHeadControl = false;
bool isHookControl = false;

// for count loop, every three time will be print out the value
int k = 0;

int target = 0;

String valInString = "";
String strValues[4];

void setup() {
  Serial.begin(115200);
  // Serial.begin(9600);

	x_servo.attach(X);
	y_servo.attach(Y);
	h_servo.attach(H);

	pinMode(ENCA_FR,INPUT);
  pinMode(ENCB_FR,INPUT);
	pinMode(ENCA_FL,INPUT);
  pinMode(ENCB_FL,INPUT);
	pinMode(ENCA_BR,INPUT);
  pinMode(ENCB_BR,INPUT);
  pinMode(ENCA_BL,INPUT);
  pinMode(ENCB_BL,INPUT);
	
	pinMode(PWM_FR,OUTPUT);
  pinMode(IN1_FR,OUTPUT);
  pinMode(IN2_FR,OUTPUT);
	pinMode(PWM_FL,OUTPUT);
  pinMode(IN1_FL,OUTPUT);
  pinMode(IN2_FL,OUTPUT);
	pinMode(PWM_BR,OUTPUT);
  pinMode(IN1_BR,OUTPUT);
  pinMode(IN2_BR,OUTPUT);
  pinMode(PWM_BL,OUTPUT);
  pinMode(IN1_BL,OUTPUT);
  pinMode(IN2_BL,OUTPUT);
  
	attachInterrupt(digitalPinToInterrupt(ENCA_FR),readEncoderAFR_wrapper, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_FR),readEncoderBFR_wrapper, CHANGE);
	// attachPinChangeInterrupt => Extra intterupt pin (software way)
	attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(ENCA_FL), readEncoderAFL_wrapper, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(ENCB_FL), readEncoderBFL_wrapper, CHANGE);
	attachInterrupt(digitalPinToInterrupt(ENCA_BR),readEncoderABR_wrapper, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_BR),readEncoderBBR_wrapper, CHANGE);
	attachInterrupt(digitalPinToInterrupt(ENCA_BL),readEncoderABL_wrapper, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB_BL),readEncoderBBL_wrapper, CHANGE);
	

  while (!Serial) {
    // wait for serial port to connect
  }
}

void loop() {
	while (Serial.available() > 0) {
		// ASCII refer: https://www.google.com/search?q=ascii+table&rlz=1C1CHBF_enMY1021MY1021&source=lnms&tbm=isch&sa=X&ved=2ahUKEwihlpGX6t_9AhUdR2wGHXJzDl0Q_AUoAXoECAEQAw&biw=1920&bih=937&dpr=1#imgrc=G8psQ_-P2ipTLM
		int inputChar = Serial.read();
		// Serial.println(inputChar);
		// Serial.println(inputChar == 32);
		if(isDigit(inputChar)){
				// Serial.println((char)inputChar);
				valInString += (char)inputChar;
				// Serial.println(valInString);

		}else if(inputChar == 44 || inputChar == 45){
			valInString += (char)inputChar;

		}else if (inputChar == 32) {
			if(valInString != ""){
				// Serial.println(valInString.length());
				while (valInString.length() > 0){
					int index = valInString.indexOf(',');
					if (index == -1){// if no found ","
						if (StringCount < 1){
							isHookControl = true;

						}else if (StringCount < 2){
							isHeadControl = true;
						}
						
						strValues[StringCount++] = valInString;
						StringCount = 0;
						break;

					}else{
						strValues[StringCount++] = valInString.substring(0, index);
						valInString = valInString.substring(index+1);
					}
				}

				valInString = "";

				if(isHookControl){
					h_servo.write(strValues[0].toInt());
					isHookControl = false;

				}else if(isHeadControl){
					x_servo.write(strValues[0].toInt());
					y_servo.write(strValues[1].toInt());
					isHeadControl = false;
					
				}else{
					int FR_rpm = strValues[FR].toInt();
					int FL_rpm = strValues[FL].toInt();
					int BR_rpm = strValues[BR].toInt();
					int BL_rpm = strValues[BL].toInt();
					
					vt[FR] = abs(FR_rpm);
					if(vt[FR] != 0){
						FR_abs = FR_rpm < 0 ? true : false;
						working[FR] = true;
					}else{
						working[FR] = false;
					}

					vt[FL] = abs(FL_rpm);
					if(vt[FL] != 0){
						FL_abs = FL_rpm < 0 ? true : false;
						working[FL] = true;
					}else{
						working[FL] = false;
					}

					vt[BR] = abs(BR_rpm);
					if(vt[BR] != 0){
						BR_abs = BR_rpm < 0 ? true : false;
						working[BR] = true;
					}else{
						working[BR] = false;
					}

					vt[BL] = abs(BL_rpm);
					if(vt[BL] != 0){
						BL_abs = BL_rpm < 0 ? true : false;
						working[BL] = true;
					}else{
						working[BL] = false;
					}
				}
			}
		}
	}

	// read the position in an atomic block
	// to avoid potential misreads
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
		pos[FR] = FR_abs == true ? abs(pos_i[FR]) : pos_i[FR];
		pos[FL] = FL_abs == true ? abs(pos_i[FL]) : pos_i[FL];
		pos[BR] = BR_abs == true ? abs(pos_i[BR]) : pos_i[BR];
		pos[BL] = BL_abs == true ? abs(pos_i[BL]) : pos_i[BL];
		// pos[FR] = pos_i[FR];
		// pos[FL] = pos_i[FL];
		// pos[BR] = pos_i[BR];
		// pos[BL] = pos_i[BL];
	}

	//Invoke compute velocity function
	computeVelocity(FR, deltaT, velocity, pos);
	computeVelocity(FL, deltaT, velocity, pos);
	computeVelocity(BR, deltaT, velocity, pos);
	computeVelocity(BL, deltaT, velocity, pos);

	//Invoke convert count/s to RPM
	convertToRPM(FR, velocity);
	convertToRPM(FL, velocity);
	convertToRPM(BR, velocity);
	convertToRPM(BL, velocity);

	// Compute the filtered signal
	// (second order Butterworth example)
	computeFilteredSignal(FR);
	computeFilteredSignal(FL);
	computeFilteredSignal(BR);
	computeFilteredSignal(BL);

	// Set a target
	// float vt = 100*(sin(currT/1e6)>0);
	// float vt = 100;
	// float vt = target;
	// float vt = 50 // fixed rpm / speed

	// vt[FR] = target;
	// vt[FL] = target;
	// vt[BR] = target;
	// vt[BL] = target;

	// Compute the control signal u
	computeControlSignalU(FR, vt[FR], u, deltaT);
	computeControlSignalU(FL, vt[FL], u, deltaT);
	computeControlSignalU(BR, vt[BR], u, deltaT);
	computeControlSignalU(BL, vt[BL], u, deltaT);


	//Set the motor speed and direction
	if(!temp_stop[FR] && working[FR]){
		dir[FR] = FR_abs == true ? -1 : 1;
	}else{
		dir[FR] = 0;
	}

	if(!temp_stop[FL] && working[FL]){
		dir[FL] = FL_abs == true ? -1 : 1;
	}

	if(!temp_stop[BR] && working[BR]){
		dir[BR] = BR_abs == true ? -1 : 1;
	}

	if(!temp_stop[BL] && working[BL]){
		dir[BL] = BL_abs == true ? -1 : 1;
	}


	// the below two function is to settel when the rmp from hight to low with change dir
	// becaue when change dir with low rpm the encoder will keep rotating previous dir (with not discover with wood)
	// so, we need temperary stop it and waiting vFilt is below than expected rpm (50 times) 
	// because if only one time checking it whether less than it will not so accurate, 
	// i just write down as bigger as i testing
	stopTemp(FR);
	stopTemp(FL);
	stopTemp(BR);
	stopTemp(BL);

	resumeFromstopTemp(FR);
	resumeFromstopTemp(FL);
	resumeFromstopTemp(BR);
	resumeFromstopTemp(BL);

	setMotorSpeedDireaction(FR, u, dir, pwr);
	setMotorSpeedDireaction(FL, u, dir, pwr);
	setMotorSpeedDireaction(BR, u, dir, pwr);
	setMotorSpeedDireaction(BL, u, dir, pwr);

	prev_dir[FR] = dir[FR];
	prev_dir[FL] = dir[FL];
	prev_dir[BR] = dir[BR];
	prev_dir[BL] = dir[BL];

	prev_rmp[FR] = vt[FR];
	prev_rmp[FL] = vt[FL];
	prev_rmp[BR] = vt[BR];
	prev_rmp[BL] = vt[BL];

	// motor start
	setMotor(dir[FR], pwr[FR], PWM_FR, IN1_FR, IN2_FR);
	setMotor(dir[FL], pwr[FL], PWM_FL, IN1_FL, IN2_FL);
	setMotor(dir[BR], pwr[BR], PWM_BR, IN1_BR, IN2_BR);
	setMotor(dir[BL], pwr[BL], PWM_BL, IN1_BL, IN2_BL);

	delay(1); // Wait 1ms
	stortVPrevValue(FR);
	stortVPrevValue(FL);
	stortVPrevValue(BR);
	stortVPrevValue(BL);

	// every TEN time loops, will print out the value
	// if(k % 10 == 0){
	//   serialPrint(vt, dir);
	// }

	k = k+1;

}
void serialPrint(float* target, int* dir){
  Serial.print(target[FR]);
	Serial.print(", ");
	Serial.print(vx[FR][0]); //2
	Serial.print(", ");
	Serial.print(vFilt[FR]);
	Serial.print(", ");
	Serial.print(dir[FR]); //4
	Serial.print(", ");
	Serial.print(pos_i[FR]);
	Serial.print(", ");
	Serial.print(u[FR]); //6
	Serial.print("    ");

	Serial.print(target[FL]);
	Serial.print(",");
	Serial.print(vx[FL][0]);
	Serial.print(",");
	Serial.print(vFilt[FL]);
	Serial.print(",");
	Serial.print(dir[FL]);
	Serial.print(",");
	Serial.print(pos_i[FL]);
	Serial.print("    ");

	Serial.print(target[BR]);
	Serial.print(",");
	Serial.print(vx[BR][0]);
	Serial.print(",");
	Serial.print(vFilt[BR]);
	Serial.print(",");
	Serial.print(dir[BR]);
	Serial.print(",");
	Serial.print(pos_i[BR]);
	Serial.print("    ");

	Serial.print(target[BL]);
	Serial.print(",");
	Serial.print(vx[BL][0]);
	Serial.print(",");
	Serial.print(vFilt[BL]);
	Serial.print(",");
	Serial.print(dir[BL]);
	Serial.print(",");
	Serial.print(pos_i[BL]);
	Serial.println("");
}

void resumeFromstopTemp(int motorIndex){
	if(temp_stop[motorIndex]){
		if(vFilt[motorIndex] <= vt[motorIndex]){
			count[motorIndex]++;
		}

		if (count[motorIndex] == 70){
			temp_stop[motorIndex] = false;
			setInitValue(motorIndex);
			count[motorIndex] = 0;
		}
	}
}

void stopTemp(int motorIndex){
		if (prev_rmp[motorIndex] != vt[motorIndex]){
		temp_dir[motorIndex] = dir[motorIndex];
		dir[motorIndex] = 0;
		temp_stop[motorIndex] = true;
	}
}

void setInitValue(int motorIndex){
	// delay(5000);
  prevT[motorIndex] = micros();
	// prevT[motorIndex] = 0;
  // deltaT[motorIndex] = 0;
	// velocity[motorIndex] = 0;
                                                                       
	pos[motorIndex] = 0;
	pos_i[motorIndex] = 0;
	posPrev[motorIndex] = 0;
                                                                       
  vx[motorIndex][0] = 0;
	vx[motorIndex][1] = 0;
	vx[motorIndex][2] = 0;
	vy[motorIndex][0] = 0;
	vy[motorIndex][1] = 0;
	vy[motorIndex][2] = 0;
  // vFilt[motorIndex] = 0;
                                                                       
  eintegral[motorIndex] = 0;
                                                                       
	// pwr[motorIndex] = 0;
	u[motorIndex] = 0;
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
		// Serial.println("change direction");
		// dir[motorIndex] = 1;
		dir[motorIndex] = -dir[motorIndex];
		// Serial.println(dir[motorIndex]);
	}

	pwr[motorIndex] = (int) fabs(u[motorIndex]);
	if(pwr[motorIndex] > 255){
		pwr[motorIndex] = 255;
	}
}

void computeControlSignalU(int motorIndex, int vt, float* u, double* deltaT){
	float kp = 5; // if the distance of the current and target is bigger, than add kp to increase the voltage
	float ki = 10; 
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

void computeVelocity(int motorIndex, double* deltaT, float* velocity, long int* pos){
	long currT = micros(); // current time
  	deltaT[motorIndex] = ((double) (currT-prevT[motorIndex]))/1.0e6;
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

void readEncoderAFR_wrapper(){
	readEncoderA(FR, ENCA_FR, ENCB_FR);
}

void readEncoderBFR_wrapper(){
	readEncoderB(FR, ENCA_FR, ENCB_FR);
}

void readEncoderAFL_wrapper(){
	readEncoderA(FL, ENCA_FL, ENCB_FL);
}

void readEncoderBFL_wrapper(){
	readEncoderB(FL, ENCA_FL, ENCB_FL);
}

void readEncoderABR_wrapper(){
	readEncoderA(BR, ENCA_BR, ENCB_BR);
}

void readEncoderBBR_wrapper(){
	readEncoderB(BR, ENCA_BR, ENCB_BR);
}

void readEncoderABL_wrapper(){
	readEncoderA(BL, ENCA_BL, ENCB_BL);
}

void readEncoderBBL_wrapper(){
	readEncoderB(BL, ENCA_BL, ENCB_BL);
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

