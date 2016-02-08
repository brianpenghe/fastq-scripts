##################################
#                                #
# Last modified 12/03/2014       # 
#                                #
# Georgi Marinov                 #
#                                # 
##################################

import sys

def run():

    if len(sys.argv) < 3:
        print 'usage: python %s fastq string newstring' % sys.argv[0]
        print '\tUse - for stdin; the script will print to stdout by default'
        print '\tIf you want to replace spaces, use _space_ as the string character'
        sys.exit(1)

    fastq = sys.argv[1]
    oldstring = sys.argv[2]
    if oldstring == '_space_':
        oldstring = ' '
    newstring = sys.argv[3]

    i=0
    pos=1
    if fastq == '-':
        input_stream = sys.stdin
    else:
        input_stream = open(fastq)
    for line in input_stream:
        i+=1
        if pos==1 and line.startswith('@'):
            print line.strip().replace(oldstring,newstring)
            pos=2
            continue
        if pos==1 and line[0] != '@':
            print 'fastq broken'
            sys.exit(1)
        if pos==2:
            print line.strip()
            pos=3
            continue
        if pos==3:
            print line.strip()
            pos=4
            continue
        if pos==4:
            print line.strip()
            pos=1
            continue

run()

