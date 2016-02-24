#!/bin/bash
#Run these codes in the current SERVER directory
#$1 should be the 5' primer sequence
#$2 should be the fastq file's name
echo '' > testTrim3
echo '' > testTrim5
barcode=$1
barc_len=$(expr length $1)
echo $barc_len
declare -i i=0
while [ $i -lt $barc_len ]
	do
		echo $i
		grep ^${barcode:0:$(echo $barc_len-$i | bc)} $2 | wc -l >> testTrim3
		grep ^${barcode:$i:$(echo $barc_len-$i | bc)} $2 | wc -l >> testTrim5
		i=$i+1
	done
grep -v @ $2 | grep -v + | grep -v D | sort | uniq -c | sort -k1,1nr | head -50
 


