#!/bin/python
import numpy as np
from PIL import Image
img = Image.open('wand1.png')
im = np.array(img)
a = len(im[1,1]) == 4 


#print(a)
#print ('FOO',len(im),len(im[0]))
for y in range(len(im)):
	for x in range(len(im[31])):
		if a and im[y,x,3] == 0:
			continue
		rgb = (im[y,x,0],im[y,x,1],im[y,x,2])
		rgbstr = "" 
		for i in range(3):
			s = str(hex(rgb[i]))[2:]
			rgbstr += s.zfill(2).upper()
		print('PX', x+100, y+100,rgbstr)

