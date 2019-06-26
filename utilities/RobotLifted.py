#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from sys import stderr

import threading
import time
import constants


# --------------------------------------------------------------------------------
#  Has the robot been lifted off the table?
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  mode         - ROBOT_LIFTED_USE_TOUCH_SENSOR or ROBOT_LIFTED_USE_COLOUR_SENSOR.
#
#  Returns:
#  
#  boolean      - True if the robot has been lifted off the table.
#               - False if the robot is still on the table.
#
# --------------------------------------------------------------------------------

def isRobotLifted(debug, mode):

    lifted = False

    if mode == constants.ROBOT_LIFTED_USE_COLOUR_SENSOR:

        cl = ColorSensor() 
        lifted = cl.raw[0] < constants.LIFTED_MINIMUM_THRESHOLD and cl.raw[1] < constants.LIFTED_MINIMUM_THRESHOLD and cl.raw[2] < constants.LIFTED_MINIMUM_THRESHOLD

    if mode == constants.ROBOT_LIFTED_USE_TOUCH_SENSOR:

        ts = TouchSensor()
        lifted = ts.is_pressed

    if debug and lifted:
        print("Robot lifted.", file = stderr)

    return lifted