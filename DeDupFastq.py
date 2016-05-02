##################################
#                                #
# Last modified 11/19/2014       # 
#                                #
# Georgi Marinov                 #
#                                # 
##################################

import sys
import os

try:
	import psyco
	psyco.full()
except:
	pass

def main(argv):

    if len(argv) < 1:
        print 'usage: python %s <inputfilename> [-minFrequency value] [-PrintFrequencyDistribution outfile]' % argv[0]
        print '\tUse - to specify standard input, the script will print to standard output by default'
        sys.exit(1)

    inputfilename = argv[1]

    doMinFreq = False
    if '-minFrequency' in argv:
        doMinFreq = True
        MF = int(argv[argv.index('-minFrequency')+ 1])

    if inputfilename == '-':
        lineslist  = sys.stdin
    else:
        lineslist  = open(inputfilename)

    SeqDict = {}

    i=0
    for line in lineslist:
        i+=1
        if i == 1:
            if line.startswith('@'):
                pass
            else:
                print 'fastq file broken, exiting'
                sys.exit(1)
            continue
        if i == 2:
            seq = line.strip()
            if SeqDict.has_key(seq):
                pass
            else:
                SeqDict[seq] = 0
            SeqDict[seq] += 1
            continue
        if i== 3:
            continue
        if i == 4:
            i = 0 
            continue

    i=0
    for seq in SeqDict.keys():
        if doMinFreq and SeqDict[seq] < MF:
            continue
        i+=1
        print '>read' + str(i)
        print seq

    if '-PrintFrequencyDistribution' in argv:
        DistDict = {}
        outfile = open(argv[argv.index('-PrintFrequencyDistribution')+ 1],'w')
        for seq in SeqDict.keys():
            counts = SeqDict[seq]
            if DistDict.has_key(counts):
                pass
            else:
                DistDict[counts] = 0
            DistDict[counts]+=1
        counts = DistDict.keys()
        counts.sort()
        outfile.write('#Counts\tNumber_reads\n')
        for c in counts:
            outline = str(c) + '\t' + str(DistDict[c])
            outfile.write(outline + '\n')
        outfile.close()

if __name__ == '__main__':
    main(sys.argv)

