#!/usr/bin/python3
import sys
import socket
import pickle
import re
import hashlib
from cryptography.fernet import Fernet
import cv2
import time
import sys
import numpy
import pyzbar.pyzbar as pyzbar
import WastonAPI
import ClientKeys

#***** This finction is to supress all the warning from pyaudio******
#source: https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time

from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


#*********************** Data Class **********************
class Data:
    """
    Data class is a data structure that contains string MD5 message,
    byte symmetric key, and byte encrypted message. 
    """
    def __init__(self, other = None):
        if (other == None):
            self.default_constructor()
        else:
            self.parameterize_constructor(other)
    
    def default_constructor(self):
        #generate a symmetric key from fernet
        self.sKey = Fernet.generate_key()
        self.encryptedMSG = b""
        self.md5MSG = ""
    
    def parameterize_constructor(self, other):
        """
        Input argument is a tuple that contains : symetric key, encrypted
        message, and md5 message
        """
        self.sKey = other[0]
        self.encryptedMSG = other[1]
        self.md5MSG = other[2]

    def setData(self, item):
        """
        this function will take in a string msg then use the symmetric key to 
        encrypt the msg.  Then, it will generate MD5 msg and store it inside "data" data type
        """
         #create a tool using symmetric key to encrypt msg using symmetric key
        tool = Fernet(self.sKey)
        #encrypt the message, the argument has to be byte
        self.encryptedMSG = tool.encrypt(item.encode())
        #https://docs.python.org/3/library/hashlib.html
        hashMSG = hashlib.md5()
        # hash the encrypt message. the argument has to be byte
        hashMSG.update(self.encryptedMSG)
        self.md5MSG = hashMSG.hexdigest()

    def isGoodData(self):
        """
        This function will check if the recieve data from the other side is good.
        The checking method is to use MD5 to hash the encrypted message then
        compare the result with given MD5 message. If both of them match,
        the data is secure
        """
        serverMD5 = hashlib.md5()
        serverMD5.update(self.encryptedMSG)
        return self.md5MSG == serverMD5.hexdigest()

    def getMSG(self):
        """
        return the decryped message (actual readable message)
        """
        tool = Fernet(self.sKey)
        decrytedMSG = tool.decrypt(self.encryptedMSG)
        return decrytedMSG.decode()

    def getPayload(self):
        return (self.sKey, self.encryptedMSG, self.md5MSG)

    def picklePayload(self):
        """
        pick the payload before sending data
        """
        return pickle.dumps(self.getPayload())

#***********************Error Checking**********************
def error(commands):
    if (len(commands) != 7): 
        print("Invalid Command Arguments")
        return True

    if (commands[1] != "-sip"):
        print("Missing sip")
        return True

    if (commands[3] != "-sp"):
        print("Missing -sip")
        return True

    if (commands[5] != "-z"):
        print("Missing -z")
        return True

    return False

#****************** Main Function *****************

commands = sys.argv
if error(commands): sys.exit()

host = commands[2]
port = int(commands[4])
size = int(commands[6])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open the socket: " + str(message))
    sys.exit(1)

#create camera object
camera = cv2.VideoCapture(0)

while 1:
    
    running, image = camera.read()
    cv2.imshow("Capture", image)
    key = cv2.waitKey(1)
    message= pyzbar.decode(image)
    if (key == ord('x')) : break

    if len(message) > 0:
        #turn off the camera immediately to
        #prevent take the same picture twice
        camera.release()

        question = message[0][0].decode()
        question = question.strip('\'') 

        package = Data()
        package.setData(question)

        s.send(package.picklePayload())

        recvData = pickle.loads(s.recv(size))
        recvPackage = Data(recvData) 
        

        check = recvPackage.getMSG()
        WastonAPI.TextToSpeechToRead(recvPackage.getMSG(), ClientKeys.WastonAPI, ClientKeys.WastonUrL)   
        print("Recieve: ", recvPackage.getMSG())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        #turn the camera back on as soon as client recieve the answer
        camera = cv2.VideoCapture(0)

s.close()
camera.release()
cv2.destroyAllWindows()

