import cv2 as cv #pip install opencv-contrib-python
import mediapipe as mp #pip install mediapipe
import time
import numpy as np
import math
from timeit import default_timer as timer
import mouse #pip install mouse
import pynput #pip install pynput
from pynput.keyboard import Key, Controller
keyboard = Controller()

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# minVol = volume.GetVolumeRange()[0]
# maxVol = volume.GetVolumeRange()[1]

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH,640) 
cap.set(cv.CAP_PROP_FRAME_HEIGHT,480)

HandsMediaPipe = mp.solutions.hands
hands = HandsMediaPipe.Hands()
DrawMediaPipe = mp.solutions.drawing_utils

def checkList(list):
  
    element = list[0]
    chk = True

    for item in list:
        if element != item:
            chk = False
            break
              
    if (chk == True): return True
    else: return False 

if not cap.isOpened():
    print("Cannot open camera")
    exit()

timerFlag = False
startVolFlag = False
startTime = 0
endTime = 0
timeTaken = 0
exitList = [0] * 20
fingerID = [4,8,12,16,20]
previousState = [0,1,0,1,0]

while True:
    
    ret, frame = cap.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(image)
    
    if results.multi_hand_landmarks:
        for eachHandLandmarks in results.multi_hand_landmarks:
            LandmarkList = []
            xList = []
            yList = []
            
            for id, landmarks in enumerate(eachHandLandmarks.landmark):
                height, weight, channel = image.shape
                PixelX, PixelY = int(landmarks.x * weight), int(landmarks.y * height)

                LandmarkList.append([id, PixelX, PixelY])
                xList.append(PixelX)
                yList.append(PixelY)

                # if id == 4:
                #     cv.circle(frame, (PixelX, PixelY), 15, (255,0,255), cv.FILLED)
                #     print(id, PixelX, PixelY)
            DrawMediaPipe.draw_landmarks(frame, eachHandLandmarks, HandsMediaPipe.HAND_CONNECTIONS)

            if len(LandmarkList) != 0:
                    # print(LandmarkList)
                    fingers = []

                    if (LandmarkList[fingerID[0]-1][1] < LandmarkList[fingerID[0]][1]):
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    for id in range(1,5):
                        if (LandmarkList[fingerID[id]][2] < LandmarkList[fingerID[id]-2][2]):
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    print(fingers)

                    if previousState == [1,1,1,1,1] and fingers == [0,0,0,0,0]:
                        # print('k')
                        keyboard.press('k') #Play/Pause
                        # keyboard.release('k')

                    if previousState == [0,0,0,0,0] and fingers == [0,1,0,0,0]:
                        # print('f')
                        keyboard.press('f') #Full screen
                        # keyboard.release('f')
                    
                    if previousState == [0,0,0,0,0] and fingers == [0,0,0,0,1]:
                        print('c')
                        keyboard.press('c') #Subtitle
                        # keyboard.release('c')

                    previousState = fingers

            x1, y1 = LandmarkList[4][1], LandmarkList[4][2]
            x2, y2 = LandmarkList[8][1], LandmarkList[8][2]
            CenterX, CenterY = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x1 - x2, y1 - y2)
            # print(length)
            xMin, yMin = min(xList), min(yList)
            xMax, yMax = max(xList), max(yList)
            area = (xMax - xMin) * (yMax - yMin) // 100
            # print(area)
            # boundingBox = [xMin, yMin, xMax, yMax]
            # # print(boundingBox)
            cv.rectangle(frame, (xMin-20, yMin-20), (xMax+20, yMax+20), (0, 255, 0), 2)

            if timerFlag == False:
                if 250 < area < 800 and length < 50:
                    startTime = timer()
                    print("Timer started")
                    timerFlag = True

            if timerFlag == True:
                if not (length < 50):
                    endTime = timer()
                    print("Timer ended")
                    timerFlag = False
                    timeTaken = endTime - startTime
                    print("Time taken: ", timeTaken)

            # print(startVolFlag)
            if timeTaken > 3:
                startVolFlag = True
                # print("Volume started")

            if startVolFlag == True:
                # print("Start drawing")
                cv.circle(frame, (x1, y1), 11, (153,153,255), cv.FILLED)
                cv.circle(frame, (x2, y2), 11, (153,153,255), cv.FILLED)
                cv.line(frame, (x1, y1), (x2, y2), (153,153,255), 3)
                cv.circle(frame, (CenterX, CenterY), 11, (153,153,255), cv.FILLED)

                vol = 5 * round(np.interp(length, [10, 250], [0, 100])/5)
                # print(int(length),vol)
                for i in range(18, -1, -1):
                    exitList[i + 1] = exitList[i]
                exitList[0] = vol/100
                # print(exitList)

                if checkList(exitList):
                    startVolFlag = False
                    endTime = 0
                    startTime = 0
                    timeTaken = 0
                volume.SetMasterVolumeLevelScalar(vol/100, None)

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

