## Hand-Gesture-Recognition

Author: Yong Yung Jun (TARUC) <br />
Date: 6 Febuary 2022

### Introduction

This python script can be used to recognize hand gesture and carry out functions such as Play/Pause, Minimize/Maximize screen, 
On/Off Subtitle, Activate Virtual Mouse, Previous/Next video, Speech to Text Recognition, Control Audio Volume

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

#### Play/Pause Video
![Palm](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/palm.PNG)
![Fist](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/fist.PNG)

First, show your palm with all fingers up <br />
Then quickly close your palm into a fist <br />
If it is not working, try a few more times and close your palm faster <br />

#### Maximise/Minimise Video Screen
![Fist](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/fist.PNG)
![Ring Up](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Ring%20Up.PNG)

First, show your fist with all fingers closed <br />
Then raise your ring finger <br />

#### Switch On/Off Video Subtitle
![Fist](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/fist.PNG)
![Pinky Up](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Pinky%20Up.PNG)

First, show your fist with all fingers closed <br />
Then raise your pinky finger <br />

#### Virtual Mouse
![Index Middle Up](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Index%20Middle%20Up.PNG)

Raise up your index finger and middle finger and virtual mouse will be activated <br />
The computer cursor will follow the movement of your middle finger tips <br />
If you wish to initiate a mouse click, kindly tap your middle finger and index finger <br />

#### Previous/Next Video
![Thumb Down](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/thumb%20down.PNG)
![Palm](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/palm.PNG)

Close your thumb and other fingers remains up, this will activate the function <br />
Move your hand to the left for some distance if you would like to proceed to the next video <br />
Move your hand to the right for some distance if you would like to proceed to the previous video <br />
Then, open up your thumb to show your palm, the Youtube video shall act accordingly <br />

#### Speech-to-Text Recognition
![Thumb Pinky Up](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Thumb%20Pinky%20Up.PNG)

Thumb and pinky finger up and others remain down, this will activate this function <br />
The frame showing your hand will pause while the program listen to you <br />
Speak in english and the program will analyse it and search it in the Youtube Search Bar <br />

#### Control Audio
![Index Thumb Touch](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Index%20Thumb%20Touch.PNG)
![Control Audio](https://github.com/AlexJun0112/Hand-Gesture-Recognition/blob/main/raw/Control%20Audio.PNG)

Hold your index finger and thumb together for at least 3 seconds, then slowly move them apart <br />
If you see a line formed between your fingers, you are now able to control your computer audio <br />
The longer the length of the line, the louder the computer audio volume <br />
If you wish to set the volume, just remain the distance between your fingers unchanged for several seconds <br />
The line will disappear and the new computer audio volume is set <br />