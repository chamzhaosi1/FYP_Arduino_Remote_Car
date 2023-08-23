#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 8
#define IN1 4
 
int pos = 0;
int pwmVal = 0;
int in2_type = 1;
int in1_type = 0;
int pos_count = 1;
 
void setup() {
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
}
 
void loop() {
	for (pwmVal; pwmVal<255; pwmVal+=15){
		analogWrite(PWM,pwmVal);
		digitalWrite(IN2,in2_type);
		digitalWrite(IN1,in1_type);
		Serial.print("Increment: ");
		Serial.println(pwmVal);
        Serial.print("Encoder: ");
		Serial.println(pos);
        Serial.println();
		delay(500);
	}

	for (pwmVal; pwmVal>0; pwmVal-=15){
		analogWrite(PWM,pwmVal);
		digitalWrite(IN2,in2_type);
		digitalWrite(IN1,in1_type);
		Serial.print("Decrement: ");
		Serial.println(pwmVal);
        Serial.print("Encoder: ");
		Serial.println(pos);
        Serial.println();
		delay(500);
	}

	pos_count++;
	Serial.print("Pos Count: ");
	Serial.println(pos_count);
    Serial.println();

	if(pos_count % 2 == 0){
		in2_type = 0;
		in1_type = 1;
	}else{
		in2_type = 1;
		in1_type = 0;
	}

	Serial.print("Input type: ");
	Serial.println(in2_type);
    Serial.print("Input type: ");
	Serial.println(in1_type);
}
 
void readEncoder(){
  int b = digitalRead(ENCB);
//   Serial.print("b");
//   Serial.println(b);

  if(b > 0){
    pos++;
  }
  else{
    pos--;
  }
}