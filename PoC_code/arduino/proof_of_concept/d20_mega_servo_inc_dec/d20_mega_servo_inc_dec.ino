#include <Servo.h> 

Servo servoGreen; // servo object representing the MG 996R servo
Servo servoBlue; // servo object representing the MG 996R servo

int degree;
String valInString = "";
char inChar;

Servo servo; // servo object representing the MG 996R servo

void setup() {
  Serial.begin(115200);
  servoGreen.attach(12); // servo is wired to Arduino on digital pin 5
  servoBlue.attach(13); // servo is wired to Arduino on digital pin 6

  while (!Serial) {
    // wait for serial port to connect
  }
}

void loop() {
  for (int i = 0; i<180; i++){
  Serial.print("Servo Green Turn ");
  Serial.print(i);
  Serial.println(" Degree");
  servoGreen.write(i); // move MG996R's shaft to angle 180°
  delay(500);
  }
  
  // Serial.print("Servo Blue Turn ");
  // Serial.print(degree);
  // Serial.println(" Degree");
  // servoBlue.write(degree); // move MG996R's shaft to angle 180°

}