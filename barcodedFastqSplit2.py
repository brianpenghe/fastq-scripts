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

def run():

    if len(sys.argv) < 2:
        print 'usage: python %s fastq config ' % sys.argv[0]
        print 'format of the config file: <index sequence> <tab> <outputfile prefix>'
        print 'assumed format of the input fastq file:'
        print '    @HWI-ST501_0041:2:1:1398:2028#ATCACG/1'
        print '    CTGCTATAAAGACAGAACAGAACTCAGTTTGCTCCCAGTGAACTCACATT'
        print '    +HWI-ST501_0041:2:1:1398:2028#ATCACG/1'
        print '    [XTRRTVW[bSa`TXOMW_TbbbV\KJZWTYNT``BBBBBBBBBBBBBBB'
        sys.exit(1)

    inputfilename = sys.argv[1]
    config = sys.argv[2]

    StatsDict={}
    IndexDict={}
    input_stream = open(config)
    i=0
    for line in input_stream:
        fields=line.strip().split('\t')
        index=fields[0]
        prefix=fields[1]
        IndexDict[index]=open(prefix+'.fastq', 'w')
        StatsDict[index]=0

    StatsDict['others']=0

    BarcodeSeqCounts={}

    processed=0
    i=0
    input_stream = open(inputfilename)
    CurrentOutputFile=''
    for line in input_stream:
        i+=1
        if i % 20000000 == 0:
            print str(i/4) + 'M reads processed'
        if i % 4 == 1 and line.startswith('@'):
            barcodeSeq=line.strip().split('#')[1].split('/1')[0]
            if BarcodeSeqCounts.has_key(barcodeSeq):
                pass
            else:
                BarcodeSeqCounts[barcodeSeq]=0
            BarcodeSeqCounts[barcodeSeq]+=1
            if IndexDict.has_key(barcodeSeq):
                CurrentOutputFile=IndexDict[barcodeSeq]
                CurrentOutputFile.write(line)
                StatsDict[barcodeSeq]+=1
            else:
                CurrentOutputFile=''
        else:
            if CurrentOutputFile!='':
                CurrentOutputFile.write(line)
            else:
                continue

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

run()

