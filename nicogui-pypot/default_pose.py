import time
import time
import os
import signal
import PySimpleGUI as sg
import cv2
import numpy as np
#from beeply.notes import beeps
from nicomotion.Motion import Motion
from nicocameras import NicoCameras, image_shift_xy
from nicodummy import DummyRobot
import serial

def quit():
    os._exit(0)

# exit on ctrl-c
def signal_handler(signal, frame):
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
try:
    robot = Motion(motorConfig=motorConfig)
except:
    robot = DummyRobot()
    print('motors are not operational')

defaultSpeed = 0.04*0.5

safe = { # standard position
                'l_shoulder_z':0.0,
                'l_shoulder_y':0.0,
                'l_arm_x':0.0,
                'l_elbow_y':89.0,
                'l_wrist_z':0.0,
                'l_wrist_x':-56.0,
                'l_thumb_z':-57.0,
                'l_thumb_x':-180.0,
                'l_indexfinger_x':-180.0,
                'l_middlefingers_x':-180.0,
                'r_shoulder_z':0.0,
                'r_shoulder_y':0.0,
                'r_arm_x':0.0,
                'r_elbow_y':89.0,
                'r_wrist_z':0.0,
                'r_wrist_x':-56.0,
                'r_thumb_z':-57.0,
                'r_thumb_x':-180.0,
                'r_indexfinger_x':-180.0,
                'r_middlefingers_x':-180.0,
                'head_z':0.0,
                'head_y':0.0
            }
for k in safe.keys():
    robot.setAngle(k,safe[k],defaultSpeed)