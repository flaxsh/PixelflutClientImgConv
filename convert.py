#!/bin/python
import numpy as np
import sys
from PIL import Image

#generates a list of Strings containing the image in the pixelflut format
#expects an PIL PNG image in RGBA format

def main (img,offx=0, offy=0):
	im = np.array(img)
	return buildlines(im,len(im[1,1])==4,offx,offy)


def buildlines(im,a,offx,offy):
	rlist = []
	for y in range(len(im)):
		for x in range(len(im[31])):
			#skip fully transparent if alpha channel is present
			if a and im[y,x,3] == 0 :
				continue
			#pixelflut syntax is: 'PX' X Y RR GG BB
			rgbstr = buildrgbstr(im[y,x][:3])
			rlist.append('PX %d %d %s' %(x+offx,y+offy,rgbstr))
	return rlist

def buildrgbstr(rgb):
	return''.join(str(hex(c))[2:].zfill(2).upper() for c in rgb)
