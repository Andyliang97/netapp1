# NAPPS_ASSN_1

![alt text](http://i.imgur.com/okD6ewD.png)

<br/>  

# Relevant client and server initialization info:
TODO  
Client Rpi
• Reads QR code and decodes question
• Builds question payload
• Sends question payload to server Rpi via socket interface
• Receives and parses answer payload
• Sends answer text to IBM Watson via API call
• Receives speech voice file from IBM Watson
• Speaks out answer
• Displays answer on monitor

Server Rpi
• Receives question payload from bridge Rpi
• Parses question payload
• Sends question text to IBM Watson via API call
• Receives speech voice file from IBM Watson
• Speaks out question
• Sends question to WolframAlpha engine via API call
• Receives answer from WolframAlpha engine
• Builds answer payload
• Sends answer payload to client Rpi via socket interface

Instruction: run the server first by following command:
    python3 -sp "port number" -z "size of package"
Then run the client by following command:
    python3 -sip "server IP address" -sp "port number" -z "size of package"

The software could scan multiple time. Each time there is a valid QR code,
the client camera will wait until it recives the answer then run again.

# Extra libraries used (python 3.5.4):
wolframalpha  (pip install wolframalpha)   
watson_developer_cloud  (pip install --upgrade watson-developer-cloud)  
import json 
import pyaudio
(sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools 
sudo apt-get install python-pyaudio python3-pyaudio
)
import wave  
import sys  
import socket  
import pickle  
import re  
import hashlib  
import cryptography
import cv2  
import time  
import sys  
import numpy  
import pyzbar
(sudo apt-get install libzbar0
pip install pyzbar
pip3 install pyzbar
pip install pyzbar[scripts])

# Anything else that might need clarification during validation:
TODO  
Try with differet hardwares and operating system beside raspi and ubuntu# netapp1
