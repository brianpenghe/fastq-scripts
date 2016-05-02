##################################
#                                #
# Last modified 07/10/2011       # 
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
        print 'usage: python %s <list of fastqfiles> outfilename' % argv[0]
        sys.exit(1)

    inputfilename = argv[1]
    outputfilename = argv[2]

    outfile = open(outputfilename, 'w')

    input_stream = open(inputfilename)
    for line1 in input_stream:
        file=line1.strip().split('\t')[0]
        linelist=open(file)
        i=0
        print file
        for line in linelist:
            i+=1
            if i==2:
                read=len(line.strip())
                outfile.write(file + '\t' + str(read) + '\n')
                break
    outfile.close()

if __name__ == '__main__':
    main(sys.argv)

