// Reference: https://github.com/NicoHood/PinChangeInterrupt/#pinchangeinterrupt-table

#include <PinChangeInterrupt.h>
 
#define PIN1 10 
#define PIN2 11 // the pin we are interested in
volatile int burp=0;    // a counter to see how many times the pin has changed
 
void setup() {
  Serial.begin(9600);
  Serial.print("PinChangeInt test on pin ");
  Serial.print(PIN1);
  Serial.print(PIN2);
  Serial.println();

  pinMode(PIN1, INPUT);     //set the pin to input
  pinMode(PIN2, INPUT);     //set the pin to input

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN1), burpcount, RISING);
  }
 
void loop() {

	Serial.print("burpcount: ");
	Serial.println(burp);

}
 
void burpcount()
{
  burp++;
}