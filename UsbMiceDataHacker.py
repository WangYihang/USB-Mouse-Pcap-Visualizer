#!/usr/bin/env python

import sys
import os
from PIL import Image

DataFileName = "usb.dat"
data = []

screenWidth = 1024
screenHeight = 800

mousePositionX = screenWidth / 2
mousePositionY = screenHeight / 2

INCASEOVERFLOW = 5

def main():
    global mousePositionX
    global mousePositionY
    # check argv
    if len(sys.argv) != 4:
        print "Usage : "
        print "        python UsbMiceHacker.py data.pcap out.png [LEFT|RIGHT|MOVE|ALL]"
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
    type = sys.argv[3]
    if type != "LEFT" and type != "RIGHT" and type != "MOVE":
        type = "ALL"
    
    Io = Image.new("L", (screenWidth * INCASEOVERFLOW, screenHeight * INCASEOVERFLOW), 0) # in case of overflow

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
	    # print "[+] Left butten."
	    offsetX = int(Bytes[2], 16)
	    offsetY = int(Bytes[4], 16)
	    if offsetX > 0x7F:
		offsetX -= 0xFF
	    if offsetY > 0x7F:
		offsetY -= 0xFF
	    mousePositionX += offsetX
	    mousePositionY += offsetY
	    # print "[+] (%d, %d)" % (mousePositionX, mousePositionY)
	    if type == "LEFT":
		# draw point to the image panel
		Io.putpixel((mousePositionX, mousePositionY,),255)
	elif Bytes[0] == "02":
	    # print "[+] Right Butten." 
	    offsetX = int(Bytes[2], 16)
	    offsetY = int(Bytes[4], 16)
	    if offsetX > 0x7F:
		offsetX -= 0xFF
	    if offsetY > 0x7F:
		offsetY -= 0xFF
	    mousePositionX += offsetX
	    mousePositionY += offsetY
	    # print "[+] (%d, %d)" % (mousePositionX, mousePositionY)
	    if type == "RIGHT":
		# draw point to the image panel
		Io.putpixel((mousePositionX, mousePositionY,),255)
	elif Bytes[0] == "00":
	    # print "[+] Move." 
	    offsetX = int(Bytes[2], 16)
	    offsetY = int(Bytes[4], 16)
	    if offsetX > 0x7F:
		offsetX -= 0xFF
	    if offsetY > 0x7F:
		offsetY -= 0xFF
	    mousePositionX += offsetX
	    mousePositionY += offsetY
	    # print "[+] (%d, %d)" % (mousePositionX, mousePositionY)
	    # draw point to the image panel
	    if type == "MOVE":
		Io.putpixel((mousePositionX, mousePositionY,),255)
	    # print "[+] Moving."
	else:
	    # print "[-] Known operate."
	    pass
	if type == "ALL":
	    # draw point to the image panel
	    Io.putpixel((mousePositionX, mousePositionY,),255)
    # show image
    Io.show()
    
    # save the Image
    Io.save("./%s" % (outputImagePath))

    # clean temp data
    os.system("rm ./%s" % (DataFileName))

if __name__ == "__main__":
    main()
