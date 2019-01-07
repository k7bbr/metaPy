#Copyright (C)2013, Brandon Rasmussen, K7BBR

import serial
import time
import requests

'''-----------------USER CONFIGURATION-----------------'''
port = "/dev/ttyUSB0" #enter scanner USB/serial port in quotes here
baudrate = 115200 #enter scanner baudrate here
icecastUser = "username" #enter icecast username in quotes here 
icecastPass = "hackkme" #enter icecast password in quotes here
icecastServerAddress = "192.168.1.100:8000" #enter icecast server IP Address (and port if necessary) here
icecastMountpoint = "mymountpoint" #enter icecast mountpoint in quotes here - don't add leading '/'
delay = 0 #enter the time in seconds of desired update delay time to match audio feed
'''-----------------END USER CONFIGURATION---------------'''
'''----------UNNECESSARY TO MODIFY SCRIPT BELOW----------'''

urlBase = "http://" + icecastServerAddress + "/admin/metadata?mount=/" + icecastMountpoint + "&mode=updinfo&song="
serTimeout = float(.005) # serial timeout here (.005 is probably sufficient)
test = "GLG" #'''test string to send to Uniden Scanner to get current status
	     #for BCT8 will be RF to get frequency, or LCD FRQ to read icon status
	     #for BC125AT use CIN'''
TGIDold = 0 #initialize TGID old test variable
metadata = ''

serialFromScanner = serial.Serial(port, baudrate, timeout=serTimeout) #initialize serial connection
serialFromScanner.flushInput() #flush serial input

def getData():
    global serBuffer, nextChar
    serBuffer = '' #clear the serBuffer
    nextChar = '' #reset the nextChar marker
    serialFromScanner.write(test +'\r\n') #send initial request to scanner

def receiveData():
    if (serialFromScanner.inWaiting() > 0): #check to see if there's serial data waiting
        global nextChar, serBuffer
        while nextChar != '\r': #continue filling serBuffer until carriage return
            nextChar = serialFromScanner.read(1) #read one character
            serBuffer += nextChar

def parseData(pserBuffer):
    parsed = pserBuffer.split(",")
    stringtest = parsed[0]
    global TGIDold, TGID, metadata
    if stringtest == "GLG":
        length = len(parsed) 
        if (length >= 10): #check list length so we don't get exception 10 for BCT15, 13 for BC886XT	
            TGID = parsed[1]
            SYSNAME = parsed[5]
            GROUP = parsed[6]
            TG = parsed[7]
	if (TGID.find('.') != -1): #check to see if a trunked or conventional system and get FREQuency
	    FREQ = TGID.lstrip('0') #remove leading 0 if present
            if (FREQ[-1] == '0'):#remove trailing 0 if present
                FREQ = FREQ[:-1] 
	else:
	    FREQ = 0
        if (TGID != TGIDold) and (TGID != ''): #check if group change or scanner not receiving
	    if (FREQ == 0): #for a trunked system
                metadata = ((SYSNAME) + " " + (TGID) + " " + (TG))
	    else: #for a conventional system
		metadata = ((FREQ) + " " + (SYSNAME) + " " + (GROUP) + " " + (TG)) #User can delete/rearrange items to update
       	else:
            metadata = ''

def updateData(pMetadata):
    global TGID, TGIDold
    if pMetadata != '':
	print pMetadata
        TGIDold = TGID
	metadataFormatted = metadata.replace(" ","+") #add "+" instead of " " for icecast2
	requestToSend = (urlBase) +(metadataFormatted)
	r = requests.get((requestToSend), auth=(icecastUser,icecastPass))
	status = r.status_code
	nowGMT = time.gmtime()
	timestamp = time.asctime(nowGMT)
	print (timestamp)
	
	if status == 200:
	    print "Icecast Update OK"
	else:
	    print "Icecast Update Error", status

time.sleep(delay) #implement user-defined delay to match audio stream
            
while True: #infinite loop
    getData()

    receiveData()
               
    parseData(serBuffer)

    updateData(metadata)
		
    time.sleep(.1) #pause
