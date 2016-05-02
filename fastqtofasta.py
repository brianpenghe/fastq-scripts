##################################
#                                #
# Last modified 11/03/2013       # 
#                                #
# Georgi Marinov                 #
#                                # 
##################################

import sys

try:
	import psyco
	psyco.full()
except:
	pass

def main(argv):

    if len(argv) < 2:
        print 'usage: python %s inputfilename bpToKeep [-notrim] [-CS]' % argv[0]
        print '\tuse - for stdin; the script will print to stdout by default'
        sys.exit(1)

    inputfilename = argv[1]
    trim = int(argv[2])

    doTrim=True
    if '-notrim' in argv:
        doTrim=False
        outputfilename = argv[1].split('fastq')[0]+'fa'

    doCS=False
    if '-CS' in argv:
        doCS=True
        doTrim=False
#        print 'will treat data as color space; will not trim reads'
        
    doStdInput = False
    if inputfilename == '-':
        doStdInput = True

    if doStdInput:
        input_stream = sys.stdin
    else:
        input_stream = open(inputfilename)
    i=0 
    skipNext=False
    seqNext=False
    shorter=0
    for line in input_stream:
        if line[0]=='+':
            skipNext=True
            continue
        if skipNext:
            skipNext=False
            continue
        if line[0]=='@':
            ID=line.strip().replace('@','>')
            seqNext=True
            continue
        if seqNext:
            if len(line.strip())<trim and doTrim:
                shorter+=1
                continue
            print ID
            if doCS:
                print line.strip()
            else:
                if doTrim:
                    print line[0:trim].replace('.','N')
                else:
                    print line.strip().replace('.','N')
            seqNext=False
#            i=i+1
#            if i % 1000000 == 0:
#                print i, 'reads processed'
            continue

#    if shorter>0:
#        print shorter, 'sequences shorter than desired length, skipped'

if __name__ == '__main__':
    main(sys.argv)

