#!/usr/bin/python3
import sys
import socket
import pickle
import re
import hashlib
from cryptography.fernet import Fernet
import WastonAPI
import ServerKeys
from ServerKeys import * # or ServerKeys
from NAPPS_Wolfram_API import *
import WastonAPI

from ctypes import *

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
    """
    Check all the user input error
    """
    if (len(commands) != 5): 
        print("Invalid Command Arguments")
        return True

    if (commands[1] != "-sp"):
        print("Missing -sp")
        return True

    if (commands[3] != "-z"):
        print("Missing -z")
        return True

    return False

#****************** Main Function *****************

commands = sys.argv
if error(commands): sys.exit()

WolframAPI = Wolfram_API()
WolframAPI.init(WOLFRAM_API_KEY)

host = ""
port = int(commands[2])
size = int(commands[4])
backlog = 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

while 1:
    client, address = s.accept()
    recvData = pickle.loads(client.recv(size))
    package = Data(recvData) 
    if package.isGoodData():
        #do some magic

        WastonAPI.TextToSpeechToRead(package.getMSG(), ServerKeys.WastonAPI, ServerKeys.WastonUrL)

        WolframAPI.sendQuestion(package.getMSG())
        ans = WolframAPI.returnAns()

        answer = Data()
        answer.setData(ans)

        client.send(answer.picklePayload())

        print ("data", package.getMSG())
    else:
        s.send(b"Interrupted Message")
        
    client.close()

