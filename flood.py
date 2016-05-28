#!/usr/bin/env python

import argparse
import socket
import sys
import threading
import time

from convertStill import generateFrame

class ImageSender:
    def __init__(self, address, port, imageLines):
        self.__address = address
        self.__port = port
        self.__data = bytes("\n".join(l.strip() for l in imageLines).encode("ascii"))

    def __sendImage(self):
        pixelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pixelSocket.connect((self.__address, self.__port))
        pixelSocket.sendall(self.__data)
        pixelSocket.shutdown(socket.SHUT_WR)

    def Send(self, sendAsync=True, threadCount=1):
        if sendAsync:
            thread = threading.Thread(target=self.__sendImage)
            thread.start()
        elif threadCount == 1:
            self.__sendImage()

    def SendContinuously(self):
        pass


def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("address")
    parser.add_argument("port", type=int)
    
    parser.add_argument("-x", "--xoffset", type=int, default=0)
    parser.add_argument("-y", "--yoffset", type=int, default=0)
    parser.add_argument("-f", "--file")
    parser.add_argument("-l", "--linesFile")

    args = parser.parse_args()
    return args

def main():
    args = parseArgs()
    
    if args.file is not None:
        print("generating lines... ", end="")
        imageLines = generateFrame(args.file, args.xoffset, args.yoffset)
        print("done")
    elif args.linesFile is not None:
        print("reading lines file")
        imageLines = open(args.linesFile).readlines()
    else:
        print("must specify input")
        sys.exit(1)

    print("connecting to %s port %d" % (args.address, args.port))
    sender = ImageSender(args.address, args.port, imageLines)
    print("sending lines... ", end="")
    while True:
        sender.Send()
        time.sleep(0.1)
    print("done")


if __name__ == "__main__":
    main()

