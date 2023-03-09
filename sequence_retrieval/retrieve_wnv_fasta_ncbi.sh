#!/bin/bash
#PBS -q global.q
#PBS -l select=1:ncpus=2:mem=5gb

source ~/.bashrc
source /nfs1/silverja/anaconda3/etc/profile.d/conda.sh

cd /nfs1/silverja/wnv/data_retrieval_ncbi

conda activate r4-base

Rscript retrieve_wnv_fasta_ncbi.R

head -n -2 out.o > temp.txt ; mv temp.txt out.o

final_numseq=$(grep -c ">" wnv.fasta)

echo -e "\n A total number of $final_numseq sequences were downloaded." >> out.o

# Remove spaces in the final fasta file:
sed -i '/^$/d' wnv.fasta
