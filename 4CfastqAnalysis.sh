#!/bin/bash
#Run these codes in the current SERVER directory
#$1 should be the 5' primer sequence
#$2 should be the fastq file's name
barcode=$1
barc_len=$(expr length $1)
declare -i i=0
while [ i -lt $barc_len ]
	do
		grep ${barcode:0:$(echo $barc_len-$i | bc)} $2 | wc -l > testTrim3
		grep ${barcode:$i:$(echo $barc_len-$i | bc)} $2 | wc -l > testTrim5
	done
 grep -v @ $2 | grep -v + | sort | uniq -c | sort -k1,1nr | head -50
 


