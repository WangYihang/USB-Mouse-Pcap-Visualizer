#!/usr/bin/env python
# coding:utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

mousePositionX = 0
mousePositionY = 0

X = []
Y = []

DataFileName = "usb.dat"
data = []

def main():
    global mousePositionX
    global mousePositionY
    # check argv
    if len(sys.argv) != 3:
        print "Usage : "
        print "        python UsbMiceHacker.py data.pcap [LEFT|RIGHT|MOVE|ALL]"
        print "Tips : "
        print "        To use this python script , you must install the numpy,matplotlib first."
        print "        You can use `sudo pip install matplotlib numpy` to install it"
        print "Author : "
        print "        WangYihang <wangyihanger@gmail.com>"
        print "        If you have any questions , please contact me by email."
        print "        Thank you for using."
        exit(1)

    # get argv
    pcapFilePath = sys.argv[1]
    action = sys.argv[2]

    if action != "LEFT" and action != "RIGHT" and action != "MOVE":
        action = "ALL"

    # get data of pcap
    command = "tshark -r '%s' -T fields -e usb.capdata > %s" % (
        pcapFilePath, DataFileName)
    print command
    os.system(command)

    # read data
    with open(DataFileName, "r") as f:
        for line in f:
            data.append(line[0:-1])

    # handle move
    for i in data:
        Bytes = i.split(":")
        if len(Bytes) == 8:
            horizontal = 2  # -
            vertical = 4  # |
        elif len(Bytes) == 4:
            horizontal = 1  # -
            vertical = 2  # |
        else:
            continue
        offsetX = int(Bytes[horizontal], 16)
        offsetY = int(Bytes[vertical], 16)
        if offsetX > 127:
            offsetX -= 256
        if offsetY > 127:
            offsetY -= 256
        mousePositionX += offsetX
        mousePositionY += offsetY
        if Bytes[0] == "01":
            # print "[+] Left butten."
            if action == "LEFT":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        elif Bytes[0] == "02":
            # print "[+] Right Butten."
            if action == "RIGHT":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        elif Bytes[0] == "00":
            # print "[+] Move."
            if action == "MOVE":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        else:
            # print "[-] Known operate."
            pass
        if action == "ALL":
            # draw point to the image panel
            X.append(mousePositionX)
            Y.append(-mousePositionY)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_title('[%s]-[%s] Author : WangYihang' % (pcapFilePath, action))
    ax1.scatter(X, Y, c='r', marker='o')
    plt.show()

    # clean temp data
    os.system("rm ./%s" % (DataFileName))

if __name__ == "__main__":
    main()
