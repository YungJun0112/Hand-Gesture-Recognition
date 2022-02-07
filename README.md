## Hand-Gesture-Recognition

### Introduction

Implementing image processing to recognize hand gesture to carry out functions such as Play/Pause, Zoom In/Out, Enable/Disable Subtitle &amp; Control the PC volume

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

#### Control Audio
![Index Thumb Touch](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Index%20Thumb%20Touch.PNG)
![Control Audio](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Control%20Audio.PNG)

Hold your index finger and thumb together for at least 3 seconds, then slowly move them apart
If you see a line formed between your fingers, you are now able to control your computer audio
The longer the length of the line, the louder the computer audio volume
If you wish to set the volume, just remain the distance between your fingers unchanged for several seconds
The line will disappear and the new computer audio volume is set
