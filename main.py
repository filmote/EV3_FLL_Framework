#!/usr/bin/env python3

import threading
import time
import os
import constants
import xml.etree.ElementTree as ET

from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import MoveTank, LargeMotor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep
from sys import stderr

from utilities import RobotLifted
from functions.DriveForXRotations import driveForXRotations
from functions.DelayForXSeconds import delayForXSeconds
from functions.ReturnWhenObjectWithinXcm import returnWhenObjectWithinXcm
from functions.WaitUntilKeyPress import waitUntilKeyPress


# --------------------------------------------------------------------------------
#  Launch an individual step.
#
#  Launches an individual step as a new thread. The details of the 'process' node 
#  are queried to determine what step to launch and what parameters are passed.
#  
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  stop         - Should the process be stopped?
#  action       - JSON process node.  
#
#  Returns:
#  
#  thread       - Reference to the newly created thread. 
#
# --------------------------------------------------------------------------------

def launchStep(debug, stop, action):

    if (action.get('action') == 'launchInParallel'):

        thread = threading.Thread(target = launchSteps, args = (debug, stop, action, True))
        thread.start()
        return thread

    # --------------------------------------------------------------------------------

    if (action.get('action') == 'launchInSerial'):

        thread = threading.Thread(target = launchSteps, args = (debug, stop, action, False))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action.get('action') == 'waitUntilKeyPress'):

        # Create action ..

        thread = threading.Thread(target = waitUntilKeyPress, args = (debug, stop))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action.get('action') == 'driveForXRotations'):

        # Get all other parameters ..

        rotations = float(action.get('rotations'))
        speed = float(action.get('speed'))

        # Create action ..

        thread = threading.Thread(target = driveForXRotations, args = (debug, stop, rotations, speed))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action.get('action') == 'delayForXSeconds'):

        # Get all other parameters ..

        delay = float(action.get('length'))

        # Create action ..

        thread = threading.Thread(target = delayForXSeconds, args = (debug, stop, delay))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action.get('action') == 'returnWhenObjectWithinXcm'):

        # Get all other parameters ..

        distance = float(action.get('distance'))

        # Create action ..

        thread = threading.Thread(target = returnWhenObjectWithinXcm, args = (debug, stop, distance))
        thread.start()
        return thread


# --------------------------------------------------------------------------------
#  Launch an set of related steps.
#
#  Launches a set of related steps as individual threads hosted inside a single 
#  thread.  Where actions are nominated to run in parallel, the process continues
#  until all actions are completed.  Where actions are nominated to run serially
#  they are started one after the other.
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  stop         - Should the process be stopped?
#  actions      - JSON action node or nodes.  
#  inParallel   - Where more than one action is specified, should we launch
#                 the actions in parallel or serial?  Default is in parallel.
#
#  Returns:
#  
#  thread       - Reference to the newly created thread. 
#
# --------------------------------------------------------------------------------
    
def launchSteps(debug, stop, actions, inParallel = True):

    threadPool = []
    stepCount = 0

    # Launch the process(es) for this step.  If the step contains sub-steps, then
    # we handle these differently to a single step ..

    if len(actions):
#        print("multiple {}".format(actions.get('action')), file=stderr)
        
        if inParallel:
            for process in actions:
                newThread = launchStep(debug, stop, process)
                threadPool.append(newThread)

        if not inParallel:
            newThread = launchStep(debug, stop, actions[stepCount])
            stepCount = stepCount + 1
            threadPool.append(newThread)
        

    # The step is a single action ..

    if not len(actions):
#        print("single {}".format(actions.get('action')), file=stderr)

        newThread = launchStep(debug, stop, actions)
        threadPool.append(newThread)


    allThreadsCompleted = False


    # Query the threads repeatedly to see if any have completed ..

    while not allThreadsCompleted:

        # Loop through the threads and remove finished ones from the thread pool ..

        for thread in threadPool:
            if not thread.isAlive():
                threadPool.remove(thread)


        # If there are no more active threads then check to see if we are done ..

        if not threadPool:


            # If we were running multiple steps in serial and we still have more to go then load the next one ..

            if inParallel == False and stepCount < len(actions):
                newThread = launchStep(debug, stop, actions[stepCount])
                threadPool.append(newThread)
                stepCount = stepCount + 1


            # Otherwise we have completed all of the work for this step and we are done ..

            else:
                allThreadsCompleted = True

        sleep (0.1) # Give the CPU a rest



# --------------------------------------------------------------------------------
#  Main routine.
# --------------------------------------------------------------------------------

def main():

    colourSensorAttachments = ColorSensor(constants.INPUT_COLOUR_SENSOR_ATTACHMENTS)

    leds = Leds()
    leds.all_off()


    # Set up debugging level ..

    # debug = constants.DEBUG_NONE 
    debug = constants.DEBUG | constants.DEBUG_THREAD_LIFECYCLE

    if debug:
        print('Waiting for an accessory ..', file=stderr)


    # Load JSON and strip out comments ..

    programsXML = ET.parse('data/programs.xml')
    programs = programsXML.getroot()

    
    while True:

        rgb = colourSensorAttachments.raw

        for program in programs:

            rProgram = int(program.get('r'))
            gProgram = int(program.get('g'))
            bProgram = int(program.get('b'))

            print(rgb, file=stderr)
            if abs(rgb[0] - rProgram) < constants.COLOUR_TOLERANCE and abs(rgb[1] - gProgram) < constants.COLOUR_TOLERANCE and abs(rgb[2] - bProgram) < constants.COLOUR_TOLERANCE:

                if debug:
                    print("Run {}".format(program.get('name')), file = stderr)


                # Load progam into memory ..

                dataXML = ET.parse('data/' + program.get('fileName'))
                steps = dataXML.getroot()

                threadPool = []
                stop_threads = False

                for step in steps:

                    inParallel = False if step.get('action') == 'launchInSerial' else True
                    thread = threading.Thread(target = launchSteps, args = (debug, lambda: stop_threads, step, inParallel))
                    threadPool.append(thread)
                    thread.start()

                    allThreadsCompleted = False

                    while not allThreadsCompleted:

                        if RobotLifted.isRobotLifted(debug, constants.ROBOT_LIFTED_USE_TOUCH_SENSOR):
                            stop_threads = True

                        for thread in threadPool:
                            if not thread.isAlive():
                                threadPool.remove(thread)

                        if not threadPool:
                            allThreadsCompleted = True


                        # If the robot has been lifted then exist the 'while' loop ..

                        if stop_threads:
                            break

                        sleep(0.1) # Give the CPU a rest


                    # If the robot has been lifted then exit the 'while' loop ..

                    if stop_threads:
                        break
               

    if debug:
        print('Finished.', file = stderr)
    
main()