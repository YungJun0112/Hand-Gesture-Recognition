# Author: Yong Yung Jun (TARUC)
# Date: 6 Febuary 2022
# Description : This python script can be used to recognize hand gesture and carry out functions such as
#               Play/Pause, Minimize/Maximize screen, On/Off Subtitle, Activate Virtual Mouse

# Requirements
# pip install pynput
# pip install opencv-contrib-python
# pip install mediapipe
# pip install mouse
# pip install pyautogui

# Import necessary libraries
from pynput.keyboard import Controller
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import cv2 as cv
import mediapipe as mp
import numpy as np
import math
from timeit import default_timer as timer
import mouse
import pyautogui

# Get the width and height of the computer screen
widthScreen, heightScreen = pyautogui.size()

# Initialisation of the keyboard and speakers function
keyboard = Controller()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Initialisation of the mediapipe function, which is used for tracking the hand gesture
HandsMediaPipe = mp.solutions.hands
hands = HandsMediaPipe.Hands()
DrawMediaPipe = mp.solutions.drawing_utils

# Setting the camera to use default computer camera and set the width and height of the outputframe
widthCam, heightCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, widthCam)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, heightCam)


def checkList(list):
    # This is a function to check whether all the items in the list are having the same value
    # This function is used in the speaker function to measure hong long the hand has been stayed in the particular gesture
    element = list[0]
    check = True

    for item in list:
        if element != item:
            check = False
            break

    if (check == True):
        return True
    else:
        return False


# If the camera cannot be open, this will be executed
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Initializing the necessary variables
timerFlag = False
startVolFlag = False
startTime, endTime = 0, 0
currentLocX, currentLocY = 0, 0
previousLocX, previousLocY = 0, 0
frameResize = 100  # This is the size use to adjust the bounding box for Virtual Mouse
smoothing = 5
timeTaken = 0
exitList = [0] * 20
fingerID = [4, 8, 12, 16, 20]  # These are all the fingertips landmarks
previousState = [0, 1, 0, 1, 0]

# An infinite while loop to keep on capturing video via the camera until 'q' button is pressed
while True:
    # Start the camera, convert the color to RGB, and activate mediapipe to track the hand gesture using the image captured
    ret, frame = cap.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(image)

    # If hand is detected, each hand can carry out the below functions
    if results.multi_hand_landmarks:
        for eachHandLandmarks in results.multi_hand_landmarks:
            # These lists are used to store the hand landmarks
            LandmarkList = []
            xList = []
            yList = []

            for id, landmarks in enumerate(eachHandLandmarks.landmark):
                # Find out the exact pixel for the hand landmarks
                height, weight, channel = image.shape
                PixelX, PixelY = int(
                    landmarks.x * weight), int(landmarks.y * height)

                LandmarkList.append([id, PixelX, PixelY])
                xList.append(PixelX)
                yList.append(PixelY)

            # Draw out the handlanmarks on the frame
            DrawMediaPipe.draw_landmarks(
                frame, eachHandLandmarks, HandsMediaPipe.HAND_CONNECTIONS)

            # If there are hand detected, execute the code below
            if len(LandmarkList) != 0:
                # Draw a bounding box over the hand
                xMin, yMin = min(xList), min(yList)
                xMax, yMax = max(xList), max(yList)
                area = (xMax - xMin) * (yMax - yMin) // 100
                cv.rectangle(frame, (xMin-20, yMin-20),
                             (xMax+20, yMax+20), (0, 255, 0), 2)

                fingers = []
                # Obtain the landmarks for index finger and middle finger
                xIndex, yIndex = LandmarkList[8][1:]
                xMiddle, yMiddle = LandmarkList[12][1:]

                # Find out which finger is up, if it is up, output 1, else, output 0
                # This is specially for the thumb which we use x-value to find its position to determine whether it is up or not
                if (LandmarkList[fingerID[0]-1][1] < LandmarkList[fingerID[0]][1]):
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    # If the y-value of the landmarks below the finger tips is lower than the landmarks for the finger tips then it is consider up
                    if (LandmarkList[fingerID[id]][2] < LandmarkList[fingerID[id]-2][2]):
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # If/else statement to determine whether certain conditions are met to carry out certain functions
                # These are the hotkeys that can used to control Youtube media player
                # If the fingers changed from showing palm closing to a fist, 'k' button is press to act as Play/Pause button
                if previousState == [1, 1, 1, 1, 1] and fingers == [0, 0, 0, 0, 0]:
                    keyboard.press('k')  # Play/Pause

                # If the fingers changed from a fist to show ring finger, 'f' button is press to act as Maximize/Minimize Full Screen button
                if previousState == [0, 0, 0, 0, 0] and fingers == [0, 0, 0, 1, 0]:
                    keyboard.press('f')  # Full screen

                # If the fingers changed from a fist to show pinky finger, 'c' button is press to act as On/Off subtitle button
                if previousState == [0, 0, 0, 0, 0] and fingers == [0, 0, 0, 0, 1]:
                    keyboard.press('c')  # Subtitle

                # If the index finger or the index & middle fingers are up, Virtual Mouse function activated
                if fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]:
                    # Find the interpolation between the screen the the Virtual Mouse frame
                    xInterp = np.interp(
                        xIndex, (frameResize, widthCam-frameResize), (0, widthScreen))
                    yInterp = np.interp(
                        yIndex, (frameResize, heightCam-frameResize), (0, heightScreen))

                    # The interpolation value is then undergo smoothing process to prevent flickering effect
                    currentLocX = previousLocX + \
                        (xInterp - previousLocX)/smoothing
                    currentLocY = previousLocY + \
                        (yInterp - previousLocY)/smoothing

                    # A filled circle is drawn on the index finger tips if virtual mouse function is activated
                    cv.circle(frame, (xIndex, yIndex), 15,
                              (255, 0, 255), cv.FILLED)
                    # A rectangle is drawn to act as the bounding box for the finger to move around to act as the computer mouse
                    cv.rectangle(frame, (100, 100),
                                 (widthCam-100, heightCam-100), (255, 0, 255), 2)
                    mouse.move(widthScreen - currentLocX, currentLocY)
                    previousLocX, previousLocY = currentLocX, currentLocY

                # If the index fingers and middle finger touches each other, initiate a left mouse click
                if fingers == [0, 1, 1, 0, 0]:
                    length = math.hypot(xIndex - xMiddle, yIndex - yMiddle)
                    if length < 33:
                        mouse.click('left')

                previousState = fingers

            # Control audio function
            # Find the landmarks for thumb
            xThumb, yThumb = LandmarkList[4][1], LandmarkList[4][2]
            CenterX, CenterY = (xThumb + xIndex) // 2, (yThumb + yIndex) // 2
            length = math.hypot(xThumb - xIndex, yThumb - yIndex)

            # Start the timer if it is not started yet and if the thumb and index fingers are pressed against each other
            if timerFlag == False:
                if 250 < area < 800 and length < 20:
                    startTime = timer()
                    print("Timer started")
                    timerFlag = True

            # If the thumb and index fingers are released, calculated the time taken 
            if timerFlag == True:
                if not (length < 50):
                    endTime = timer()
                    print("Timer ended")
                    timerFlag = False
                    timeTaken = endTime - startTime
                    print("Time taken: ", timeTaken)
            # If it exceeds a certain time period, control autio function activated
            if timeTaken > 3:
                startVolFlag = True

            if startVolFlag == True:
                # if control autio function activated, draw a line between thumb and index fingers to notify the user
                # that they are now controling the computer audio base on the difference in length between the index finger and thumb
                cv.circle(frame, (xThumb, yThumb), 11,
                          (153, 153, 255), cv.FILLED)
                cv.circle(frame, (xIndex, yIndex), 11,
                          (153, 153, 255), cv.FILLED)
                cv.line(frame, (xThumb, yThumb),
                        (xIndex, yIndex), (153, 153, 255), 3)
                cv.circle(frame, (CenterX, CenterY), 11,
                          (153, 153, 255), cv.FILLED)

                # Find the interpolation value and smooth it 
                vol = 5 * round(np.interp(length, [10, 250], [0, 100])/smoothing)
                # Input the interpolation value into the exitList, and move all the values in the list one step back
                for i in range(18, -1, -1):
                    exitList[i + 1] = exitList[i]
                exitList[0] = vol/100

                # If all the values in the exitList are the same, which indicates the user has remain the hand gesture for a period of time
                # This indicates that the user would like to set the audio volume to the current volume
                # hence change the startVolFlag to false to break out from this function
                if checkList(exitList):
                    startVolFlag = False
                    endTime = 0
                    startTime = 0
                    timeTaken = 0
                # set the computer audio based on the interpolation value obtained from the distance between index finger and thumb
                volume.SetMasterVolumeLevelScalar(vol/100, None)

    # If cannot retrieve frame from the computer camera, execute this and exit
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Output the frame and if 'q' button is pressed, exit
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# release the camera and destroy the window created
cap.release()
cv.destroyAllWindows()
