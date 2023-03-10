#!/bin/sh
fasta_file=$1
FILENAME=$(basename ${fasta_file%%.fa*});

# Step 1
clean_seqs.py -f ${FILENAME}.fa -minl 10000 > ${FILENAME}_10000.fasta
# Step 2
clean_seqs.py -f ${FILENAME}_10000.fasta -std_characters > ${FILENAME}_10000_std.fasta
# Step 3
clean_seqs.py -f ${FILENAME}_10000_std.fasta -np 10 > ${FILENAME}_10000_std_np10.fasta
