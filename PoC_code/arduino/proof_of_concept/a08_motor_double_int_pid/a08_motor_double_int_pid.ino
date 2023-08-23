// This alternate version of the code does not require
// atomic.h. Instead, interrupts() and noInterrupts() 
// are used. Please use this code if your 
// platform does not support ATOMIC_BLOCK.

#include <SPI.h>
#include <SD.h>

#define ENCA 2 // GREEN
#define ENCB 3 // YELLOW
#define PWM 5
#define IN2 8
#define IN1 4

volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
long prevT = 0;
float eprev = 0;
float eintegral = 0;
int prevPos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder1, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCB),readEncoder2, FALLING);
  
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  // Serial.println("target pos");

  while (!Serial) {
    // wait for serial port to connect
  }
}

void loop() {
    // set target position
    int target = 1200;
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
    Serial.print(" ");
    Serial.print(pos);
    Serial.println();
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

void readEncoder1(){
  int b = digitalRead(ENCB);
  if(b > 0){
    posi++;
  }
  else{
    posi--;
  }
}

void readEncoder2(){
  int a = digitalRead(ENCA);
  if(a > 0){
    posi++;
  }
  else{
    posi--;
  }
}