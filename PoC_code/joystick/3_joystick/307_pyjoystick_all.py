import pygame
import time

import os
import sys
os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()

num_joysticks = pygame.joystick.get_count()
print("Number of joysticks: {}".format(num_joysticks))

joystick = pygame.joystick.Joystick(0)
joystick.init()

# total=0
# counter=0
# total=total+right_stick_y
# counter=counter+1
# print("1. avarage : {}".format(total/counter))

while True:
    pygame.event.get()

    # print("###########################################")

    # 1 - Right Stick
    tmp = (joystick.get_axis(3)-0.016428450907557464)*100
    if(tmp>=0):
        tmp=tmp*100/98.35410315143174
    else:
        tmp=tmp*100/101.64284509075574
    right_stick_x = round(tmp)
    #
    tmp = (joystick.get_axis(4)-0.01843069041576502)*100
    if(tmp>=0):
        tmp=tmp*100/98.15387920061099
    else:
        tmp=tmp*100/101.8430690415765
    right_stick_y = -round(tmp)   
    #
    right_stick_button=joystick.get_button(10)
    # print(" 1. right_stick_x : {}, right_stick_y: {}, right_stick_button:{}".format(right_stick_x, right_stick_y, right_stick_button))
    
    # 2 - Directional Pad (D-Pad)
    d_pad_left=joystick.get_button(11)
    d_pad_right=joystick.get_button(12)
    d_pad_up=joystick.get_button(13)
    d_pad_down=joystick.get_button(14)
    # print(" 2. d_pad_left: {}, d_pad_right: {}, d_pad_up:{}, d_pad_down:{}".format(d_pad_left, d_pad_right, d_pad_up, d_pad_down))

    # 3 - Left Stick
    left_stick_x = round(joystick.get_axis(0)*100)
    tmp = (joystick.get_axis(1)-0.0305)*100
    if(tmp>=0):
        tmp=tmp*100/97
    else:
        tmp=tmp*100/103
    left_stick_y = -round(tmp)
    left_stick_button = joystick.get_button(9)
    # print(" 3. left_stick_x  : {}, left_stick_y: {}, left_stick_button:{}".format(left_stick_x, left_stick_y, left_stick_button))

    # 4 - Back Button
    back_button=joystick.get_button(6)
    # print(" 4. back_button: {}".format(back_button))

    # 5 - Left Bumper
    left_bumper=joystick.get_button(4)
    # print(" 5. left_bumper: {}".format(left_bumper))

    # 6 - Left Trigger
    left_trigger = (joystick.get_axis(2)+1)*100/1.999969482421875
    # print(" 6. left_trigger: {}".format(round(left_trigger)))

    # 7 - Guide Button
    guide_button=joystick.get_button(8)
    # print(" 7. guide_button: {}".format(guide_button))

    # 8 - Start Button
    start_button=joystick.get_button(7)
    # print(" 8. start_button: {}".format(start_button))

    # 9 - Right Trigger
    right_trigger = (joystick.get_axis(5)+1)*100/1.999969482421875
    # print(" 9. right_trigger: {}".format(round(right_trigger)))

    # 10 - Right Bumper
    right_bumper=joystick.get_button(5)
    # print("10. right_bumper: {}".format(right_bumper))
 
    # A - A Button (Green)
    a_button=joystick.get_button(0)
    # print(" A. a_button: {}".format(a_button))
 
    # B - B Button (Red)
    b_button=joystick.get_button(1)
    # print(" B. b_button: {}".format(b_button))

    # X - X Button (Blue)
    x_button=joystick.get_button(2)
    # print(" X. x_button: {}".format(x_button))

    # Y - Y Button (Yellow)
    y_button=joystick.get_button(3)
    # print(" Y. y_button: {}".format(y_button))


    # print(" ")
    # print("# # #   V e r s i o n   1   # # #")
    # print(" left (bumper: {}, trigger: {}) - (trigger: {}, bumper: {}) right".format(left_bumper,round(left_trigger),round(right_trigger),right_bumper))
    # print(" button (back: {}, guide: {}, start: {})".format(back_button,guide_button,start_button))
    # print(" left_stick (x: {}, y: {}, button:{})".format(left_stick_x, left_stick_y, left_stick_button))
    # print(" d_pad (left: {}, right: {}, up:{}, down:{})".format(d_pad_left, d_pad_right, d_pad_up, d_pad_down))
    # print(" right_stick (x : {}, y: {}, button:{})".format(right_stick_x, right_stick_y, right_stick_button))
    # print(" button (a: {}, b: {}, x: {}, y: {})".format(a_button,b_button,x_button,y_button))

    os.system('clear')
    # print(" ")
    print("# # #   V e r s i o n   2   # # #")
    print(" ")
    print("left (trigger:{}, bumper:{})                          (bumper:{}, trigger:{}) right".format(str(round(left_trigger)).rjust(3, ' '),left_bumper,right_bumper,str(round(right_trigger)).rjust(3, ' ')))
    print(" ")
    print("                            (back:{}, guide:{}, start:{})".format(back_button,guide_button,start_button))
    print(" ")
    print("left_stick (x:{}, y:{}, button:{})                   (a:{}, b:{}, x:{}, y:{}) button".format(str(left_stick_x).rjust(4, ' '), str(left_stick_y).rjust(4, ' '), left_stick_button,a_button,b_button,x_button,y_button))    
    print(" ")
    print("  d_pad (left:{}, up:{}, down:{}, right:{})    (x:{}, y:{}, button:{}) right_stick ".format(d_pad_left, d_pad_up, d_pad_down, d_pad_right, str(right_stick_x).rjust(4, ' '), str(right_stick_y).rjust(4, ' '), right_stick_button))
    # print("###########################################")
    # print("get_button_0: {}".format(joystick.get_button(0)))
    # print("get_button_1: {}".format(joystick.get_button(1)))
    # print("get_button_2: {}".format(joystick.get_button(2)))
    # print("get_button_3: {}".format(joystick.get_button(3)))
    # print("get_button_4: {}".format(joystick.get_button(4)))
    # print("get_button_5: {}".format(joystick.get_button(5)))
    # print("get_button_6: {}".format(joystick.get_button(6)))
    # print("get_button_7: {}".format(joystick.get_button(7)))
    # print("get_button_8: {}".format(joystick.get_button(8)))
    # print("get_button_9: {}".format(joystick.get_button(9)))
    # print("get_button_10: {}".format(joystick.get_button(10)))
    # print("get_button_11: {}".format(joystick.get_button(11)))
    # print("get_button_12: {}".format(joystick.get_button(12)))
    # print("get_button_13: {}".format(joystick.get_button(13)))
    # print("get_button_14: {}".format(joystick.get_button(14)))

    # print("###########################################")
    # print("get_axis_0: {}".format(joystick.get_axis(0)))
    # print("get_axis_1: {}".format(joystick.get_axis(1)))
    # print("get_axis_2: {}".format(joystick.get_axis(2)))
    # print("get_axis_3: {}".format(joystick.get_axis(3)))
    # print("get_axis_4: {}".format(joystick.get_axis(4)))
    # print("get_axis_5: {}".format(joystick.get_axis(5)))

    time.sleep(0.1)