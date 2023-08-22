# d18_mega_read_serial_from_python
cd /home/engineer/romo_v2/romo_web/arduino
arduino-cli compile --fqbn arduino:avr:mega d18_mega_read_serial_from_python
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d18_mega_read_serial_from_python
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"
