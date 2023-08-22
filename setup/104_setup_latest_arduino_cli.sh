###############################################################################
### Arduino-CLI Program
###############################################################################

### Step 1 : Install Arduino-CLI
# REFER : https://arduino.github.io/arduino-cli/installation/
apt -y install curl wget
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh
arduino-cli version

### Step 2 : Prepare Board Library
arduino-cli core update-index
arduino-cli core install arduino:samd
arduino-cli core install arduino:avr
arduino-cli core upgrade
arduino-cli core list

## list arduino board
watch -n 1 arduino-cli board list
arduino-cli board list
arduino-cli board listall

lsusb

###############################################################################
### Enable Serial Debug and Remote Sync
###############################################################################

### Serial Debuging
# Install
apt -y install picocom
# Enter Serial Com
picocom -b 9600 -r -l /dev/ttyACM0
# Quit Serial Com
# To exit picocom, use CNTL-A followed by CNTL-X.

###############################################################################
### Other Libraries
###############################################################################

### Install Related Library
arduino-cli lib update-index
# arduino-cli lib install ArduinoBLE WiFiNINA ArduinoMQTTclient ArduinoJSON \
# FlashStorage ArduinoHttpClient SD

## search available library
# arduino-cli lib search <library_name>
arduino-cli lib search servo

arduino-cli lib examples Servo
arduino-cli lib install Servo

arduino-cli lib examples Wire
arduino-cli lib install Wire

arduino-cli lib install TimerOne
arduino-cli lib install SD
arduino-cli lib install Servo
arduino-cli lib install --git-url https://github.com/NicoHood/PinChangeInterrupt.git
# arduino-cli lib install --git-url https://github.com/GreyGnome/PinChangeInt.git

## If want to install lib from git, we need give the premission for unsafe installment

# Show config
arduino-cli config dump
export ARDUINO_LIBRARY_ENABLE_UNSAFE_INSTALL=true

arduino-cli lib examples Adafruit_PWMServoDriver
# arduino-cli lib install Adafruit_PWMServoDriver
arduino-cli lib install --git-url https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library.git


###############################################################################
### Detect Hardware
###############################################################################

apt -y install hwinfo

### Senario 1.A : Plug in Arduino MKR WiFI 1010 as NORMAL start up mode
hwinfo | grep Arduino 
#   Model: "Arduino SA Arduino MKR WiFi 1010"
#   Vendor: usb 0x2341 "Arduino SA"
#   Device: usb 0x8054 "Arduino MKR WiFi 1010"

### Senario 1.B : Plug in Arduino MKR WiFI 1010 as BOOTOADER start up mode
hwinfo | grep Arduino
#   Model: "Arduino SA Arduino MKR WiFi 1010"
#   Vendor: usb 0x2341 "Arduino SA"
#   Device: usb 0x0054 "Arduino MKR WiFi 1010"

###############################################################################
### Timestamp for PICOCOM
###############################################################################
apt -y install screen moreutils
picocom -b 9600 -r -l /dev/ttyACM0 | ts

###############################################################################
### Plot graph
###############################################################################
pip install plotly
# apt -y install gnuplot
# arduino-cli lib install SD

# arduino-cli core list
# nano <core_library_path>/platform.local.txt
# compiler.cpp.flags=-c -g -Os -Wall -Wextra -std=gnu++11 {build.extra_flags} -fno-exceptions -fpermissive -fno-threadsafe-statics -Wno-error=narrowing -lc