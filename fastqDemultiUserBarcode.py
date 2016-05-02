##################################
#                                #
# Last modified 02/08/2016       # 
#                                #
# Georgi Marinov, Peng He        #
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
        print 'usage: python %s input outfilename barcodeSeq [-v]' % argv[0]
        print '\tuse - for stdinout instead a input or output filename'
        sys.exit(1)

    inputfilename = argv[1]
    outputfilename = argv[2]
    barcodeSeq = argv[3]

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
            line0 = line
            continue
        if i == 2:
            line1 = line
            continue
        if i == 3:
            if line.startswith('+'):
                pass
            else:
                print 'fastq input is broken, exiting'
                sys.exit(1)
            line2 = line
            continue
        if i == 4:
            line3 = line
            i=0
            if (line1.startswith(barcodeSeq) and '-v' not in argv) or (not line1.startswith(barcodeSeq) and '-v' in argv):
                if doStdOut:
                    print line0 + line1 + line2 + line3.strip()
                else:
                    outfile.write(line0 + line1 + line2 + line3.strip())
            continue

    if not doStdOut:
        outfile.close()

if __name__ == '__main__':
    main(sys.argv)

