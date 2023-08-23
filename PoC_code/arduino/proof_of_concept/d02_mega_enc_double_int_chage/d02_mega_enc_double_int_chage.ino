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

#define ENCA 2 // GREEN
#define ENCB 3 // YELLOW
#define PWM 6
#define IN2 26 // BLACK
#define IN1 28 // WHITE

volatile int posi = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder_R, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB),readEncoder_R, CHANGE);
  
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  // Serial.println("target pos");

  while (!Serial) {
    // wait for serial port to connect
  }
}

void loop() {
	Serial.print("Count Position: ");
	Serial.println(posi);
}

void readEncoder_R(){
  int a_R = digitalRead(ENCA);
  int b_R = digitalRead(ENCB);

  if (a_R == 0){
    posi += (b_R == 0) ? 1 : -1;
  }
  else {
    posi += (b_R == 0) ? -1 : 1;
  }
}

// void readEncoderA(){
// 	int a = digitalRead(ENCA);
//   int b = digitalRead(ENCB);

//   if(a == 0){
//     if(b == 0){
// 			posi++;
// 		}else{
// 			posi--;
// 		}
//   }
//   else{
//     if(b == 0){
// 			posi--;
// 		}else{
// 			posi++;
// 		}
//   }
// }

// void readEncoderB(){
//   int a = digitalRead(ENCA);
// 	int b = digitalRead(ENCB);

//   if(b == 0){
//     if(a == 0){
// 			posi--;
// 		}else{
// 			posi++;
// 		}
//   }
//   else{
//     if(a == 0){
// 			posi++;
// 		}else{
// 			posi--;
// 		}
//   }
// }