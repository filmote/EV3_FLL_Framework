from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D


# Debug constants

DEBUG_NONE                                  = 0

DEBUG                                       = (1 << 1)
DEBUG_THREAD_LIFECYCLE                      = (1 << 2)

DEBUG_MOVEMENT_ROTATION_STARTING_POSITION   = (1 << 10)
DEBUG_MOVEMENT_ROTATION_CURRENT_POSITION    = (1 << 11)
DEBUG_MOVEMENT_ROTATION_FINAL_POSITION      = (1 << 12)
DEBUG_MOVEMENT_ROTATION_ALL                 = DEBUG_MOVEMENT_ROTATION_STARTING_POSITION | DEBUG_MOVEMENT_ROTATION_CURRENT_POSITION | DEBUG_MOVEMENT_ROTATION_FINAL_POSITION


# Infrared constants

IR_PROMIXITY_TO_CM_RATIO                    = 1.2


# Colour sensor

COLOUR_TOLERANCE                            = 20
LIFTED_MINIMUM_THRESHOLD                    = 10


# Robot

ROBOT_LIFTED_USE_TOUCH_SENSOR               = 0
ROBOT_LIFTED_USE_COLOUR_SENSOR              = 1

OUTPUT_LARGE_MOTOR_LEFT                     = OUTPUT_B
OUTPUT_LARGE_MOTOR_RIGHT                    = OUTPUT_C

INPUT_TOUCH_SENSOR                          = INPUT_1
INPUT_GYRO                                  = INPUT_2
INPUT_COLOUR_SENSOR_MAT                     = INPUT_3
INPUT_COLOUR_SENSOR_ATTACHMENTS             = INPUT_3
INPUT_INFRARED_SENSOR                       = INPUT_4
