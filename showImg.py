#!/bin/python
import bildwandlib.convertStill as imgc
import sys

def main(path, offx=0, offy=0):
    print('\n'.join(imgc.main(path,offx,offy)))

if __name__ == '__main__' :
		if len(sys.argv) == 4:
			main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
		main(sys.argv[1])
