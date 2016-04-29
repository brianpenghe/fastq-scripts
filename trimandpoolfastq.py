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

    if len(argv) < 3:
        print 'usage: python %s <list of input files> outfileprefix <bpToKeep | max> [-trim5 bp] [-flowcellID flowcell] [-addEnd 1 | 2] [-replace string newstring | blank]' % argv[0]
        sys.exit(1)

    inputfilename = argv[1]
    doMax=False
    if argv[3] == 'max':
        doMax=True
        trim='max'
    else: 
        trim = int(argv[3])
    outputfilename = argv[2] + '.' + str(trim) + 'mers.fastq'
    doFlowcellID=False
    if '-flowcellID' in argv:
        doFlowcellID=True
        flowcellID=argv[argv.index('-flowcellID')+1]
        print 'will include flowcell ID', flowcellID, 'in reads headers'
    dotrim5=False
    if '-trim5' in argv:
        dotrim5=True
        trim=int(argv[argv.index('-trim5')+1])
        print 'will trim ', trim, 'bp from the 5-end'
        outputfilename = inputfilename.split('.fastq')[0] + '.' +str(trim)+'bp-5prim-trim.fastq'
    doAddEnd=False
    if '-addEnd' in argv:
        doAddEnd=True
        END=argv[argv.index('-addEnd')+1]
        print 'will add',  '/'+END, 'to read IDs'
    doReplace=False
    if '-replace' in argv:
        doReplace=True
        oldstring=argv[argv.index('-replace')+1]
        newstring=argv[argv.index('-replace')+2]
        if newstring == 'blank':
            newstring=''
        print 'will replace',  oldstring, 'with', newstring, 'in read IDs'



    linelist=open(inputfilename)
    outfile = open(outputfilename, 'w')
    for line1 in linelist:
        file=line1.strip().split('\t')[0]
        input_stream = open(file)
        i=0 
        shorter=0
        if dotrim5:
            i=1
            j=0
            for line in input_stream:
                if i==3 and line[0]=='+':
                    plus='+\n'
                    i=4
                    continue
                if i==1 and line[0]=='@':
                    if doFlowcellID and flowcellID not in line:
                        ID='@'+flowcellID+'_'+line.replace(' ','_')[1:-1]+'\n'
                    else:
                        ID=line.replace(' ','_')
                    if doAddEnd:
                        ID=ID.strip()+'/'+END+'\n'
                    if doReplace:
                        ID=ID.replace(oldstring,newstring)
                    i=2
                    continue
                if i==4:
                    scores=line
                    i=1
                    if doMax: 
                        scores=line
                    else:
                        scores=line[trim:len(line)]+'\n'
                    continue
                if i==2:
                    i=3
                    plus=''
                    plus=ID
                    j=j+1
                    if j % 1000000 == 0:
                        print file, j, 'reads processed'
                    if doMax: 
                        outfile.write(ID)
                        outfile.write(line.replace('.','N'))
                        outfile.write(plus)
                        outfile.write(scores)
                    else:
                        sequence=line[0:trim].replace('.','N')+'\n'
                        outfile.write(ID)
                        outfile.write(sequence)
                        outfile.write(plus)
                        outfile.write(scores)
                    continue
        else:
            i=1
            j=0
            for line in input_stream:
                if i==1 and line[0]=='@':
                    if doFlowcellID and flowcellID not in line:
                        ID='@'+flowcellID+'_'+line.replace(' ','_')[1:-1]+'\n'
                    else:
                        ID=line.replace(' ','_')
                    if doAddEnd:
                        ID=ID.strip()+'/'+END+'\n'
                    if doReplace:
                        ID=ID.replace(oldstring,newstring)
                    i=2
                    continue
                if i==2:
                    i=3
                    j=j+1
                    if j % 1000000 == 0:
                        print file, j, 'reads processed'
                    if doMax: 
                        sequence=line
                    else:
                        if len(line.strip())<trim:
                            shorter+=1
                            sequence=line.strip().replace('.','N')+'\n'
                        else:
                            sequence=line[0:trim].replace('.','N')+'\n'
                    continue
                if i==3 and line[0]=='+':
                    plus='+\n'
                    i=4
                    continue
                if i==4:
                    i=1
                    if doMax: 
                        scores=line
                        outfile.write(ID)
                        outfile.write(sequence)
                        outfile.write(plus)
                        outfile.write(line)
                    else:
                        if len(line.strip())<trim:
                            continue
                        scores=line[0:trim]+'\n'
                        outfile.write(ID)
                        outfile.write(sequence)
                        outfile.write(plus)
                        outfile.write(scores)
                    continue
    outfile.close()

    if shorter>0:
        print shorter, 'sequences shorter than desired length'


if __name__ == '__main__':
    main(sys.argv)

