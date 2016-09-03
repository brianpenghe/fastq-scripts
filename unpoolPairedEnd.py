##################################
#                                #
# Last modified 09/01/2016       # 
#                                #
# Brian Peng He                  #
#                                #
#this is only for TophatOutput!  # 
##################################

import sys

try:
	import psyco
	import string
	psyco.full()
except:
	pass

def main(argv):

    if len(argv) < 1:
        print 'usage: python %s inputfilename ' % argv[0]
        print 'This script splits the unmapped reads from Tophat output' 
        sys.exit(1)

    inputfilename = argv[1]
    outfile = []
    outfile.append(open(inputfilename + '1.fastq', 'w'))
    outfile.append(open(inputfilename + '2.fastq', 'w'))
	
    lineslist = open(inputfilename)
    i=0
    split=0
    for line in lineslist:
        i+=1
        if i % 10000000 == 0:
            print str(i/1000000) + 'M lines processed'
        if ( i % 4 ) == 0 and line.startswith('@'):
            outfile[( i / 4 ) % 2].write(line[:-2])
        else:
            outfile[( i / 4 ) % 2].write(line)
    outfile[0].close()
    outfile[1].close()

if __name__ == '__main__':
    main(sys.argv)

