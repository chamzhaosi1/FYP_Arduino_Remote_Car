// CONCLUSION
// B01 (DOUBLE - RASING (1 TIME )) -- 330 COUNT = 360 DEGREE
// B02 (DOUBLE - RASING / FAILING (2 TIME )) -- 660 COUNT = 360 DEGREE
// B03 /B05  (DOUBLE - CHANGE (4 TIME )) -- 1320 COUNT = 360 DEGREE

#include <SPI.h>
#include <SD.h>
#include <TimerOne.h>

// #define ENCA 2 // GREEN
// #define ENCB 3 // YELLOW
// #define PWM 5 // 
// #define IN2 8 // BLACK
// #define IN1 4 // WHITE
// #define PWMVAL 75*2
// #define PWMVAL 255

const int motorPin1 = 4;  // Motor driver pin 1
const int motorPin2 = 8;  // Motor driver pin 2
const int encoderPinA = 2;  // Encoder signal A pin
const int encoderPinB = 3;  // Encoder signal B pin
const float Kp = 1;  // Proportional gain

volatile int encoderCount = 0;  // Encoder pulse count
volatile int lastEncoderCount = 0; // Last encoder count
volatile unsigned long lastTime = 0;  // Last time the encoder count was updated
float currentSpeed = 0.0;  // Current motor speed
float targetSpeed = 100.0; // Desired speed in rotations per second
float printSec = 0.1; 
float speedError;
float voltage;

void setup() {
  Serial.begin(9600);
  unsigned long int timeInterval = (printSec * 1000000);
  Timer1.initialize(timeInterval); // 0.5 microseconds = 0.5 second
  Timer1.attachInterrupt(serialPrint);

  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoderCount, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB), updateEncoderCount, CHANGE);
}

void loop() {
  // Update motor speed measurement every 100ms
  unsigned long currentTime = millis();
  if (currentTime - lastTime >= 100) {
    currentSpeed = (float)(encoderCount - lastEncoderCount) / 20.0;  // Convert encoder pulses to rotations per second
    lastEncoderCount = encoderCount;
    lastTime = currentTime;
  }
  
  // Adjust motor voltage based on speed error
  speedError = targetSpeed - currentSpeed;
  voltage = Kp * speedError;
  if (voltage > 0) {
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
    analogWrite(motorPin2, min(voltage, 255)); // Set max voltage to 255
  } else {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
    analogWrite(motorPin1, min(-voltage, 255)); // Set max voltage to 255
  }
}

void updateEncoderCount() {
  // Update encoder pulse count
  int encoderA = digitalRead(encoderPinA);
  int encoderB = digitalRead(encoderPinB);
  if (encoderA == encoderB) {
    encoderCount++;
  } else {
    encoderCount--;
  }
}

void serialPrint(){
    Serial.print(" - ");
    Serial.print(targetSpeed);
    Serial.print(" , ");
    Serial.print(currentSpeed);
    Serial.print(" , ");
    Serial.println(speedError);
}
