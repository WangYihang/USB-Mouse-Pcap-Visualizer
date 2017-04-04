#!/usr/bin/env python

import sys
import os

DataFileName = "usb.dat"
data = []

screenWidth = 1024
screenHeight = 800

mousePositionX = screenWidth / 2
mousePositionY = screenHeight / 2

def main():
    global mousePositionX
    global mousePositionY
    # check argv
    if len(sys.argv) != 3:
        print "Usage : "
        print "        python UsbMiceHacker.py data.pcap out.png"
        print "Tips : "
        print "        To use this python script , you must install the PIL first."
        print "        You can use `sudo pip install pillow` to install it"
        print "Author : "
        print "        WangYihang <wangyihanger@gmail.com>"
        print "        If you have any questions , please contact me by email."
        print "        Thank you for using."
        exit(1)

    # get argv
    pcapFilePath = sys.argv[1]
    outputImagePath = sys.argv[2]
    
    # get data of pcap
    os.system("tshark -r %s -T fields -e usb.capdata > %s" % (pcapFilePath, DataFileName))

    # read data
    with open(DataFileName, "r") as f:
        for line in f:
            data.append(line[0:-1])
    

    # handle move
    for i in data:
	Bytes = i.split(":")
	if Bytes[0] == "01":
	    print "[+] Left butten."
	elif Bytes[0] == "02":
	    print "[+] Right Butten." 
	elif Bytes[0] == "00":
	    print "[+] Moving."
	else:
	    print "[-] Known operate."
	offsetX = int(Bytes[2], 16)
	offsetY = int(Bytes[4], 16)
        if offsetX > 0x7F:
	    offsetX -= 0xFF
        if offsetY > 0x7F:
	   offsetY -= 0xFF
	mousePositionX += offsetX
	mousePositionY += offsetY
	print "[+] (%d, %d)" % (mousePositionX, mousePositionY)

    # handle click

    # handle left drag

    # handle right drag
   
    # TODO handle scolling 

if __name__ == "__main__":
    main()
