#!/usr/bin/env python3
#from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor
import ev3dev2.sensor.lego 
import ev3dev2.led 

from sys import stderr

import threading
import time
import os
import json
import constants

def delayForXSeconds(debug, stop, delayLength):

    if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
        print("Start delayForXSeconds({}), thread {}".format(delayLength, threading.current_thread().ident), file=stderr)

    start_time = time.time()

    while time.time() < start_time + delayLength:

        if stop():
            if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
                print("Kill delayForXSeconds({}), thread {}.".format(delayLength, threading.current_thread().ident), file=stderr)
            break

    if not stop():
        if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
            print("End delayForXSeconds({}), thread {}.".format(delayLength, threading.current_thread().ident), file=stderr)

