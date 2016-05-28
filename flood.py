#!/usr/bin/env python

import socket
import sys
import threading
import time

from convertStill import generateFrame

class ImageSender:
    def __init__(self, address, port, imageLines):
        self.__address = address
        self.__port = port
        self.__data = bytes("\n".join(imageLines).encode("ascii"))

    def __sendImage(self):
        pixelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pixelSocket.connect((self.__address, self.__port))
        pixelSocket.sendall(self.__data)
        pixelSocket.shutdown(socket.SHUT_WR)

    def Send(self, sendAsync=True):
        if sendAsync:
            thread = threading.Thread(target=self.__sendImage)
            thread.start()
        else:
            self.__sendImage()


def main(address, port, filePath, xoffset=0, yoffset=0):
    #address = "94.45.233.241"
    #port = 1234
    
    print("generating lines... ", end="")
    imageLines = generateFrame(filePath, int(xoffset), int(yoffset))
    print("done")

    sender = ImageSender(address, int(port), imageLines)
    print("sending lines... ", end="")
    while True:
        sender.Send()
        time.sleep(0.1)
    print("done")


if __name__ == "__main__":
    if len(sys.argv) >= 4 :
        main(*sys.argv[1:])
    else:
        sys.stderr.write("Usage: %s <address> <port> <file> [xoffset] [yoffset]\n")
        sys.exit(1)

