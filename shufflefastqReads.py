##################################
#                                #
# Last modified 08/12/2014       # 
#                                #
# Georgi Marinov                 #
#                                # 
##################################

import sys
import string
import random

def main(argv):

    if len(argv) < 1:
        print 'usage: python %s inputfilename' % argv[0]
        print '\tuse - for stdin; the script will print to stdout by default'
        sys.exit(1)

    inputfilename = argv[1]

    ReadList = []

    if inputfilename == '-':
        listoflines = sys.stdin
    else:
        listoflines = open(inputfilename)
    i=1
    for line in listoflines:
        if line == '':
            break
        if i==1:
            if line[0]=='@':
                ID = line.strip()
                i = 2
            else:
                print 'fastq file broken'
                sys.exit(1)
            continue
        if i==2:
            i = 3
            sequence = line.strip()
            continue
        if i==3:
            if line[0]=='+':
                i = 4
            else:
                print 'fastq file broken'
                sys.exit(1)
            continue
        if i==4:
            i = 1
            scores = line.strip()
            ReadList.append((ID,sequence,scores))
            continue

    random.shuffle(ReadList)
    for (ID,sequence,scores) in ReadList:
        print ID
        print sequence
        print '+'
        print scores

    

if __name__ == '__main__':
    main(sys.argv)

