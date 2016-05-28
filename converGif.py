#!/bin/python
import convert
import sys
from subprocess import call
from PIL import Image
import os
def main (path,offx=0, offy=0):
    call(['mkdir','tmpdir'])
    cmdstr = 'tmpdir/out%d.png'
    call(["convert",path,'-coalesce',cmdstr])
    for filename in sorted(os.listdir('tmpdir')):
            print('\n'.join(convert.main(Image.open('tmpdir/'+str(filename)).convert('RGBA'),offx,offy)))
#            print('\n')
    call(['rm','-R','tmpdir'])
if __name__ == '__main__' :
		if len(sys.argv) == 4:
			main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
		main(sys.argv[1])
