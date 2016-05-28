#!/usr/bin/env python

import argparse
import math
import random
import socket
import sys
import threading
import time

from convertStill import generateFrame

class LinesBuffer:
    def __init__(self, imageLines, encoding="ascii", randomize=False):
        encodedLines = [(l.strip() + "\n").encode(encoding) for l in imageLines]
        if randomize:
            random.shuffle(encodedLines)
        self.__data = [bytes(l) for l in encodedLines]

    def GetData(self, chunkCount=1, chunkIndex=0):
        #chunkSize = math.ceil(len(self.__data) / chunkCount)
        #startIndex = chunkSize * chunkIndex
        #endIndex = min(chunkSize * (chunkIndex + 1) - 1, len(self.__data))
        #return self.__data[startIndex:endIndex]
        return b"".join(self.__data[chunkIndex::chunkCount])


class ImageSender:
    def __init__(self, address, port, imageLines):
        self.__address = address
        self.__port = port
        self.__dataBuffer = LinesBuffer(imageLines, randomize=True)

    def __sendData(self, data, continuous=False, delay=0.0):
        pixelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pixelSocket.connect((self.__address, self.__port))

        if continuous:
            while True:
                pixelSocket.sendall(data)
                time.sleep(delay)
        else:
            pixelSocket.sendall(data)

        pixelSocket.shutdown(socket.SHUT_WR)

    def Send(self, sync=False, threadCount=1):
        if sync and threadCount == 1:
            self.__sendImage()
        else:
            threads = []
            for i in range(threadCount):
                data = self.__dataBuffer.GetData(threadCount, i)
                threads.append(threading.Thread(target=self.__sendData, args=(data,)))
                threads[i].start()

            if sync:
                for i in range(threadCount):
                    threads[i].join()


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
        sender.Send(False, 5)
        time.sleep(0.5)
    print("done")


if __name__ == "__main__":
    main()

