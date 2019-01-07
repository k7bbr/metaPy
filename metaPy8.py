#Copyright (C)2013, Brandon Rasmussen, K7BBR

import serial
import time
import requests

'''-----------------USER CONFIGURATION-----------------'''
port = "/dev/ttyUSB0" #enter scanner USB/serial port in quotes here
baudrate = 57600 #enter scanner baudrate here (BCT8 max rate is 57600)
icecastUser = "source" #enter icecast username in quotes here (For RR feed use "source")
icecastPass = "hackme" #enter icecast password in quotes here
icecastServerAddress = "192.168.1.100:8000" #enter icecast server IP Address (and port if necessary) here
icecastMountpoint = "mymountpoint" #enter icecast mountpoint in quotes here - don't add leading '/'
'''-----------------END USER CONFIGURATION---------------'''
'''----------UNNECESSARY TO MODIFY SCRIPT BELOW----------'''

urlBase = "http://" + icecastServerAddress + "/admin/metadata?mount=/" + icecastMountpoint + "&mode=updinfo&song="
serTimeout = float(.005) # serial timeout here (.005 is probably sufficient)
test = "LCD FRQ" #'''test string to send to Uniden Scanner to get current status
	     #for BCT8 will be RF to get frequency, or LCD FRQ to read icon status
	     #for BC125AT use CIN'''
FREQold = 0 #initialize FREQ old test variable
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
    parsed = pserBuffer[5:13]
    #print parsed
    #stringtest = parsed[1:3]
    global FREQold, FREQ, metadata
    #if stringtest == "FRQ":
        #length = len(parsed) 
    if (parsed.find('.') != -1): #check list length so we don't get exception
        FREQ = parsed
        #print FREQ
        #SYSNAME = parsed[5]
        #TG = parsed[7]

        if (FREQ != FREQold) and (FREQ != ''): #check if group change or scanner not receiving
            metadata = FREQ
            #print metadata
        else:
            metadata = ''

def updateData(pMetadata):
    global FREQ, FREQold
    if pMetadata != '':
	print pMetadata
        FREQold = FREQ
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
            
while True: #infinite loop
    getData()

    receiveData()
               
    parseData(serBuffer)

    updateData(metadata)
		
    time.sleep(.1) #pause
