// #define ENCA 2
#define PWM 3
#define IN2 2
#define IN1 4 

int pos = 0;

void setup() {
  Serial.begin(9600);
//   pinMode(ENCA,INPUT);
//   attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
}

void loop() {
  setMotor(1, PWMVAL, PWM, IN1, IN2);
  delay(5000);
//   Serial.println(pos);
  setMotor(-1, PWMVAL, PWM, IN1, IN2);
  delay(5000);
//   Serial.println(pos);
//   setMotor(0, 255, PWM, IN1, IN2);
//   delay(200);
//   Serial.println(pos);
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

// void readEncoder(){
//   int b = digitalRead(ENCA);
//   if(b > 0){
//     pos++;
//   }
//   else{
//     pos--;
//   }
// }