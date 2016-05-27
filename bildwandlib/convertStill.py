#!/bin/python
from bildwandlib import convert
import sys
from PIL import Image

def main (path,offx=0, offy=0):
    img = Image.open(path)
    return convert.main(img,offx,offy)

if __name__ == '__main__' :
		if len(sys.argv) == 4:
			main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
		main(sys.argv[1])
