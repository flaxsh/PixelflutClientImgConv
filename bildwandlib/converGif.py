#!/bin/python
from bildwandlib import convert
import sys
from PIL import Image

def main (path,offx=0, offy=0):
    #TODO get frames from gif as lists of img objects
    frames = []
    #    frames = Image.open(path)
    for img in frames:
            print('\n'.join(convert.main(img,offx,offy)))
            print('\n')
if __name__ == '__main__' :
		if len(sys.argv) == 4:
			main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
		main(sys.argv[1])
