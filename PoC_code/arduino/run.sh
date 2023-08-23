# a01_blink
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega a01_blink
arduino-cli upload -p /dev/ttyACM1 --fqbn arduino:avr:mega a01_blink
picocom -b 9600 -r -l /dev/ttyACM1
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a02_servo
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a02_servo
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a02_servo
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a03_servo_16_channel
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a03_servo_16_channel
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a03_servo_16_channel
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a04_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a04_motor
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a04_motor
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a05_motor_ind_dec
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a05_motor_ind_dec
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a05_motor_ind_dec
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a06_motor_encoder
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a06_motor_encoder
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a06_motor_encoder
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a07_motor_pid
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a07_motor_pid
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a07_motor_pid
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a08_motor_double_int_pid
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a08_motor_double_int_pid
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a08_motor_double_int_pid
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a10_motor_pid_speed
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a10_motor_pid_speed
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a10_motor_pid_speed
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a11_motor_srpr
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a11_motor_srpr
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a11_motor_srpr
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b01_enc_single_int_rasing
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b01_enc_single_int_rasing
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b01_enc_single_int_rasing
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b02_enc_double_int_rasing
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b02_enc_double_int_rasing
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b02_enc_double_int_rasing
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b03_enc_double_int_change
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b03_enc_double_int_change
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b03_enc_double_int_change
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b04_read_serial_input
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b04_read_serial_input
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b04_read_serial_input
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b05_value_goto_pos
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b05_value_goto_pos
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b05_value_goto_pos
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b06_value_goto_pos_com
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b06_value_goto_pos_com
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b06_value_goto_pos_com
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b07_value_time_int
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b07_value_time_int
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b07_value_time_int
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b08_get_cphs_rpm
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b08_get_cphs_rpm
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b08_get_cphs_rpm
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b09_dynmic_pwm_diy
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b09_dynmic_pwm_diy
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b09_dynmic_pwm_diy
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b10_dynmic_pwm_map
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b10_dynmic_pwm_map
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b10_dynmic_pwm_map
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# b11_dynmic_pwm_without_pid
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno b11_dynmic_pwm_without_pid
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno b11_dynmic_pwm_without_pid
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# c01_youtube_pid_position
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno c01_youtube_pid_position
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno c01_youtube_pid_position
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# c02_youtube_pid_speed
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno c02_youtube_pid_speed
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno c02_youtube_pid_speed
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

###############################################################################
############################## Mega Board #####################################
###############################################################################

# d01_mega_motor_single_int_rasing
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d01_mega_motor_single_int_rasing
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d01_mega_motor_single_int_rasing
picocom -b 9600 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d02_mega_enc_double_int_chage
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d02_mega_enc_double_int_chage
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d02_mega_enc_double_int_chage
picocom -b 9600 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d03_mega_motor_ind_dec
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d03_mega_motor_ind_dec
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d03_mega_motor_ind_dec
picocom -b 9600 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d04_mega_pid_filter_frequency
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d04_mega_pid_filter_frequency
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d04_mega_pid_filter_frequency
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d05_mega_left_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d05_mega_left_motor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d05_mega_left_motor
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d06_mega_right_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d06_mega_right_motor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d06_mega_right_motor
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d07_mega_both_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d07_mega_both_motor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d07_mega_both_motor
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d08_mega_function_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d08_mega_function_motor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d08_mega_function_motor
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d09_mega_extra_int_pin
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d09_mega_extra_int_pin
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d09_mega_extra_int_pin
picocom -b 9600 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d10_mega_both_motor_extra_int
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d10_mega_both_motor_extra_int
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d10_mega_both_motor_extra_int
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d11_mega_four_motor_front_right
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d11_mega_four_motor_front_right
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d11_mega_four_motor_front_right
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d12_mega_four_motor_front_left
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d12_mega_four_motor_front_left
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d12_mega_four_motor_front_left
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d13_mega_four_motor_back_right
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d13_mega_four_motor_back_right
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d13_mega_four_motor_back_right
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d14_mega_four_motor_back_left
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d14_mega_four_motor_back_left
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d14_mega_four_motor_back_left
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d15_mega_four_motor_combine
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d15_mega_four_motor_combine
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d15_mega_four_motor_combine
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d16_mega_omni_wheel_direction
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d16_mega_omni_wheel_direction
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d16_mega_omni_wheel_direction
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d16_mega_omni_wheel_direction
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d16_mega_omni_wheel_direction
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d16_mega_omni_wheel_direction
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d17_mega_serial_four_num
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d17_mega_serial_four_num
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d17_mega_serial_four_num
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d18_mega_read_serial_from_python
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d18_mega_read_serial_from_python
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d18_mega_read_serial_from_python
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

###############################################################################
########################### Servo Motot #######################################
###############################################################################
# a01_blink
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a01_blink
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a01_blink
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a12_servo_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a12_servo_motor
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a12_servo_motor
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a13_servo_motor_dny
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a13_servo_motor_dny
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a13_servo_motor_dny
picocom -b 115200 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a14_both_servo_motor
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a14_both_servo_motor
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a14_both_servo_motor
picocom -b 9600 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# a15_both_servo_motor_dny
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:uno a15_both_servo_motor_dny
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno a15_both_servo_motor_dny
picocom -b 115200 -r -l /dev/ttyUSB0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

###############################################################################
############################## Mega Board (Motor + Servo) #####################
###############################################################################

# d19_mega_servo_motor_dny
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d19_mega_servo_motor_dny
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d19_mega_servo_motor_dny
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"

# d20_mega_servo_inc_dec
cd /home/engineer/romo_v2/arduino
arduino-cli compile --fqbn arduino:avr:mega d20_mega_servo_inc_dec
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega d20_mega_servo_inc_dec
picocom -b 115200 -r -l /dev/ttyACM0
# To stop picocom monitoring Ctrl + "a" and Ctrl + "x"