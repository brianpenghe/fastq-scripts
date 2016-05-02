##################################
#                                #
# Last modified 10/16/2013       # 
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

    if len(argv) < 3:
        print 'usage: python %s inputfilename outfilename [-f | -q]' % argv[0]
        print '\tuse - for stdinout instead a input filename'
        sys.exit(1)

    inputfilename = argv[1]
    outputfilename = argv[2]
    type = argv[3]

    outfile = open(outputfilename, 'w')

    if inputfilename == '-':
        input_stream  = sys.stdin
    else:
        input_stream = open(inputfilename)
    i=0 
    LenDict={}
    seq=''    
    if type == '-f':
        for line in input_stream:
            if i % 1000000 == 0:
                print i, 'reads processed'
            i=i+1
            if line[0]=='>':
                if seq=='':
                    continue
                length=len(seq)
                if LenDict.has_key(length):
                    pass
                else:
                    LenDict[length]=0
                LenDict[length]+=1
                seq=''
            else:
                seq=seq+line.strip()
    skipNext=False
    seqNext=False
    if type == '-q':
        for line in input_stream:
            if line[0]=='+':
                skipNext=True
                continue
            if skipNext:
                skipNext=False
                continue
            if line[0]=='@':
                seqNext=True
                continue
            if seqNext:
                length=len(line.strip())
                if LenDict.has_key(length):
                    LenDict[length]+=1
                else:
                    LenDict[length]=1
                seqNext=False
                i=i+1
                if i % 1000000 == 0:
                    print i, 'reads processed'
                continue

    Lengths=LenDict.keys()
    Lengths.sort()
    for L in Lengths:
        outline=str(L)+'\t'+str(LenDict[L])+'\n'
        outfile.write(outline)
    outfile.close()

if __name__ == '__main__':
    main(sys.argv)

