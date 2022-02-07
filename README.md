## Hand-Gesture-Recognition

Author: Yong Yung Jun (TARUC)
Date: 6 Febuary 2022

### Introduction

This python script can be used to recognize hand gesture and carry out functions such as Play/Pause, Minimize/Maximize screen, <br />
On/Off Subtitle, Activate Virtual Mouse, Previous/Next video, Speech to Text Recognition

=================================

### Requirements

* pip install pynput
* pip install opencv-contrib-python
* pip install mediapipe
* pip install mouse
* pip install pyautogui
* pip install SpeechRecognition pydub
* https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio <- Download pyaudio wheel from this link, cd to the directory and pip install it

### Functions
Before showing the hand gesture to run the functions, always remember to click on the Youtube browser to ensure to commands are sent to that particular browser 

#### Control Audio
![Index Thumb Touch](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Index%20Thumb%20Touch.PNG)
![Control Audio](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Control%20Audio.PNG)

Hold your index finger and thumb together for at least 3 seconds, then slowly move them apart <br />
If you see a line formed between your fingers, you are now able to control your computer audio <br />
The longer the length of the line, the louder the computer audio volume <br />
If you wish to set the volume, just remain the distance between your fingers unchanged for several seconds <br />
The line will disappear and the new computer audio volume is set <br />

#### Virtual Mouse
![Index Middle Up](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Index%20Middle%20Up.PNG)

Raise up your index finger and middle finger and virtual mouse will be activated <br />
The computer cursor will follow the movement of your middle finger tips <br />
If you wish to initiate a mouse click, kindly tap your middle finger and index finger <br />

