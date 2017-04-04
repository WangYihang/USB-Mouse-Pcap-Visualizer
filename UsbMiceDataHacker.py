#!/usr/bin/env python

import sys
import os

DataFileName = "usb.dat"
data = []

def main():
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
    
    print data

    # handle move

    # handle click

    # handle left drag

    # handle right drag
   
    # TODO handle scolling 

if __name__ == "__main__":
    main()
