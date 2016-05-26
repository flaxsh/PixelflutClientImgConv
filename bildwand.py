#!/bin/python
import numpy as np
import sys
from PIL import Image


def main (path,offx=0, offy=0):
	img = Image.open(path)
	im = np.array(img)
	linelist = buildlines(im,len(im[1,1])==4,offx,offy)


#print(a)
#print ('FOO',len(im),len(im[0]))

def buildlines(im,a,offx,offy):
	for y in range(len(im)):
		for x in range(len(im[31])):
			if a and im[y,x,3] == 0:
				continue
			rgb = (im[y,x,0],im[y,x,1],im[y,x,2])
			rgbstr = ""
			for i in range(3):
				s = str(hex(rgb[i]))[2:]
				rgbstr += s.zfill(2).upper()
			print('PX', x+offx, y+offy,rgbstr)


if __name__ == '__main__' :
		if len(sys.argv) == 4:
			main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
		main(sys.argv[1])
