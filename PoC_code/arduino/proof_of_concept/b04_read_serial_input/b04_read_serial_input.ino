void setup() {
    Serial.begin(9600);
    
}

// Serial.parseInt()
// Serial.parseFloat()
// Serial.readString()
// Serial.read()

String valInString = "";
char inChar;

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
                Serial.println(valInString.toInt());
                valInString = "";
            }else{
                Serial.println(inChar);
            }
        } 
    }    
}