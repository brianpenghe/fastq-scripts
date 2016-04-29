##################################
#                                #
# Last modified 12/26/2010       # 
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
        print 'usage: python %s fastq_end1 fastq_end2 config ' % argv[0]
        print 'format of the config file: <index sequence> <tab> <outputfile prefix>'
        print 'the second fastq file is assumed to have the barcode, and match its strand; it need not be trimmed to match the index length'
        sys.exit(1)

    end1 = argv[1]
    end2 = argv[2]
    config = argv[3]

    IndexDict={}
    StatsDict={}

    input_stream = open(config)
    i=0
    for line in input_stream:
        if line.strip() == '':
            continue
        fields=line.strip().split('\t')
        index=fields[0]
        prefix=fields[1]
        IndexDict[index]=open(prefix+'.fastq', 'w')
        StatsDict[index]=0
        indexlength=len(index)

    StatsDict['others']=0

    BarcodeSeqCounts={}

    processed=0
    input_stream1 = open(end1)
    input_stream2 = open(end2)
    barcodeMatch=False
    i=0
    for line1 in input_stream1:
        i+=1
        if i % 20000000 == 0:
            print str(i/4) + 'M reads processed'
        line2 = input_stream2.readline()
        if i % 4 == 1:
            if line1.startswith('@'):
                readID=line1
                continue
            else:
                print line1,line2
                print 'fastq file broken'
                sys.exit(0)
        if i % 4 == 2:
            sequence=line1
            barcodeSeq=line2[0:indexlength]
            if BarcodeSeqCounts.has_key(barcodeSeq):
                pass
            else:
                BarcodeSeqCounts[barcodeSeq]=0
            BarcodeSeqCounts[barcodeSeq]+=1
            if IndexDict.has_key(barcodeSeq):
                barcodeMatch=True
                StatsDict[barcodeSeq]+=1
            else:
                barcodeMatch=False
        if i % 4 == 3 and line.startswith('+'):
            continue
        if i % 4 == 0:
            if barcodeMatch:
                IndexDict[barcodeSeq].write(readID)
                IndexDict[barcodeSeq].write(sequence)
                IndexDict[barcodeSeq].write('+\n')
                IndexDict[barcodeSeq].write(line1)
                readID=''
                sequence=''

    StatsDict['others']=i/4
    for index in IndexDict.keys():
        StatsDict['others']=StatsDict['others']-StatsDict[index]

    for index in IndexDict.keys():
        IndexDict[index].close()

    outfile = open(config+'.stats', 'w')

    for index in IndexDict.keys():
        print 'found', StatsDict[index], 'reads for index', index, 'sample', IndexDict[index]
        outline='found ' +str(StatsDict[index]) + ' reads for index ' + index + ' and sample ' + str(IndexDict[index])
        outfile.write(outline+'\n')

    print 'could not assign', StatsDict['others'], 'reads to samples'
    outline='could not assign ' + str(StatsDict['others']) + ' reads to samples'
    outfile.write(outline+'\n')

    outline='#Barcode\tCounts'
    outfile.write(outline+'\n')   
    keys=BarcodeSeqCounts.keys()
    keys.sort()
    for barcode in keys:
        outline=barcode+'\t'+str(BarcodeSeqCounts[barcode])
        outfile.write(outline+'\n')

    outfile.close()

if __name__ == '__main__':
    main(sys.argv)

