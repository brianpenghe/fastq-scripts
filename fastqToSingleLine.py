##################################
#                                #
# Last modified 11/12/2014       # 
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

def run():

    if len(sys.argv) < 2:
        print 'usage: python %s input outfilename' % sys.argv[0]
        print '\tuse - for stdinout instead a input or output filename'
        sys.exit(1)

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]

    if outputfilename == '-':
        doStdOut = True
    else:
        doStdOut = False
        outfile = open(outputfilename, 'w')

    if inputfilename == '-':
        input_stream  = sys.stdin
    else:
        input_stream = open(inputfilename)
    i=0
    for line in input_stream:
        i+=1
        if i == 1:
            if line.startswith('@'):
                pass
            else:
                print 'fastq input is broken, exiting'
                sys.exit(1)
            ID = line.strip()[1:]
            continue
        if i == 2:
            seq = line.strip()
            continue
        if i == 3:
            if line.startswith('+'):
                pass
            else:
                print 'fastq input is broken, exiting'
                sys.exit(1)
            continue
        if i == 4:
            qscores = line.strip()
            i=0
            if doStdOut:
                print ID + '\t' + seq + '\t' + qscores
            else:
                outfile.write(ID + '\t' + seq + '\t' + qscores + 'n')
            continue

    if not doStdOut:
        outfile.close()

run()

