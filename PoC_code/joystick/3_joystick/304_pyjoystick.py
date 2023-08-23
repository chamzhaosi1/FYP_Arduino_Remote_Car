print("Number of joysticks: 111")

import pygame
print("Number of joysticks: 222")
pygame.init()

num_joysticks = pygame.joystick.get_count()
print("Number of joysticks: {}".format(num_joysticks))

joystick = pygame.joystick.Joystick(0)
joystick.init()


while True:
    pygame.event.get()
    # Get the input values for the Xbox gamepad axes
    axis_x = round(joystick.get_axis(0)*100)

    tmp = (joystick.get_axis(1)-0.0305)*100
    if(tmp>=0):
        tmp=tmp*100/97
    else:
        tmp=tmp*100/103

    axis_y = -round(tmp)
    # Get the input values for the Xbox gamepad buttons
    # button_a = joystick.get_button(0)
    # button_b = joystick.get_button(1)
    # button_x = joystick.get_button(2)
    # button_y = joystick.get_button(3)
    # Print the input values
    # print("X-axis: {}, Y-axis: {}, A: {}, B: {}, X: {}, Y: {}".format(
    #     axis_x, axis_y, button_a, button_b, button_x, button_y))
    # Print the input values
    print("X-axis: {}, Y-axis: {}".format(axis_x, axis_y))
