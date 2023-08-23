/*
MIT License
Copyright 2021 Michael Schoeffler (https://www.mschoeffler.com)
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
/*
* Example source code of an Arduino tutorial on how to control an MG 996R servo motor. 
*/

#include <Servo.h> 

int degree;
String valInString = "";
char inChar;

Servo servo; // servo object representing the MG 996R servo

void setup() {
  servo.attach(3); // servo is wired to Arduino on digital pin 3
  Serial.begin(115200);

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

			}else if ((char)inputChar == '\r') {
					// Serial.println(valInString);
					if(valInString != ""){
							// Serial.println(valInString.toInt());
							degree = (valInString.toInt());
							valInString = "";

              Serial.print("Turn ");
              Serial.print(degree);
	            Serial.println(" Degree");

              servo.write(degree); // move MG996R's shaft to angle 180°
					}
			} 
	}
}