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

    def GetDataChunk(self, chunkCount=1, chunkIndex=0):
        #chunkSize = min(math.ceil(len(self.__data) / chunkCount), maxChunkSize)
        #startIndex = chunkSize * chunkIndex
        #endIndex = min(chunkSize * (chunkIndex + 1) - 1, len(self.__data) - 1)
        #return self.__data[startIndex:endIndex]
        return b"".join(self.__data[chunkIndex::chunkCount])


class NetworkSender:
    def __init__(self, address, port):
        self.__address = address
        self.__port = port

    def Send(self, data, continuous=False, delay=0.0):
        raise NotImplementedException("must be defined in child class")

class TCPSender(NetworkSender):
    def __init__(self, address, port):
        self.__address = address
        self.__port = port

    def Send(self, data, continuous=False, delay=0.0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__address, self.__port))

        if continuous:
            while True:
                sock.sendall(data)
                time.sleep(delay)
        else:
            sock.sendall(data)

class UDPSender(NetworkSender):
    def __init__(self, address, port, mtu=1500):
        self.__address = address
        self.__port = port
        self.__mtu = mtu

    def Send(self, data, continuous=False, delay=0.0):
        dataChunks = []
        startIndex = 0
        while startIndex < len(data):
            endIndex = data[startIndex:startIndex + self.__mtu].rfind(b"\n") + 1
            dataChunks.append(data[startIndex:endIndex])
            startIndex = endIndex

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            for dataChunk in dataChunks:
                sock.sendto(dataChunk, (self.__address, self.__port))

            if continuous:
                time.sleep(delay)
            else:
                break


class ImageSender:
    def __init__(self, imageLines, sender=None):
        if sender is None:
            self.__sender = TCPSender("localhost", 1234)
        else:
            self.__sender = sender
        self.__dataBuffer = LinesBuffer(imageLines, randomize=True)

    def Send(self, sync=False, threadCount=1):
        if sync and threadCount == 1:
            self.__sendData()
        else:
            threads = []
            for i in range(threadCount):
                data = self.__dataBuffer.GetDataChunk(threadCount, i)
                threads.append(threading.Thread(target=self.__sender.Send, args=(data, True, 0.5)))
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

    parser.add_argument("-p", "--proto", choices=("tcp", "udp"), default="tcp")

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
    if args.proto == "tcp":
        netSender = TCPSender(args.address, args.port)
    else:
        netSender = UDPSender(args.address, args.port)
    sender = ImageSender(imageLines, netSender)
    print("sending lines... ", end="")
    sender.Send(False, 5)
    print("done")


if __name__ == "__main__":
    main()

