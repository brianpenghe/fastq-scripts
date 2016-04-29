##################################
#                                #
# Last modified 07/06/2011       # 
#                                #
# Georgi Marinov                 #
#                                # 
##################################

import sys
import string
import random
from sets import Set

def main(argv):

    if len(argv) < 2:
        print 'usage: python %s fastq outfileprefix' % argv[0]
        sys.exit(1)

    input = argv[1]
    outprefix = argv[2]

    OutfileDict={}

    lineslist = open(input)
    i=0
    j=0
    for line in lineslist:
        i+=1
        if i==1:
            j+=1
            if j % 1000000 == 0:
                print j, 'reads processed'
            fields = line.strip().split('@')[1].split(':')
            lane=fields[0]+'_s_'+fields[1]
            if OutfileDict.has_key(lane):
                pass
            else:
                OutfileDict[lane]=open(outprefix+'_'+lane+'.fastq','w')
                print outprefix+'_'+lane+'.fastq'
            OutfileDict[lane].write(line)
        if i==2:
            OutfileDict[lane].write(line)
        if i==3:
            OutfileDict[lane].write(line)
        if i==4:
            OutfileDict[lane].write(line)
            i=0

    for lane in OutfileDict.keys():
        OutfileDict[lane].close()

if __name__ == '__main__':
    main(sys.argv)
