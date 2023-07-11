#!/usr/bin/env python3

__author__ = 'Andrea Silverj'
__version__='1.0'
__date__='17 June 2023'

import os
import sys
import argparse as ap
from random import sample
from Bio import SeqIO
from Bio.SeqIO import FastaIO


# Parser
def read_args(args):

	parser = ap.ArgumentParser(description = '# Randomly select a subset of sequences from FASTA files #\n')

	required = parser.add_argument_group('required arguments')

	required.add_argument('-f',
						required = True,
						metavar = 'fasta_file',
						nargs = '?',
						help = "FASTA file",
						type = str)

	required.add_argument('-n',
						required = False,
						metavar = ('num_seqs'),
						nargs = '?',
						help = 'number of seqs to subsample',
						type = str)

	required.add_argument('-p',
						required = False,
						metavar = ('perc_seqs'),
						nargs = '?',
						help = 'percentage of seqs to subsample',
						type = str)

	required.add_argument('-o',
						required = True,
						metavar = ('output_name'),
						nargs = '?',
						help = 'name of the output file',
						type = str)

	return vars(parser.parse_args())


# Functions
def check_missing_files(args):

	if not os.path.isfile(args['f']):
		print("Error: file '"+args['f']+" is not accessible.")
		sys.exit(1)


if __name__ == '__main__':

	args = read_args(sys.argv)
	
	check_missing_files(args)

	fasta=args['f']
	numsubseqs=args['n']
	percsubseqs=args['p']

	# Handle options
	if numsubseqs != None and percsubseqs != None:
		print("The options 'n' and 'p' cannot be used together. Please, select either the number or the percentage of sequences to subsample.")
		sys.exit(1)

	if numsubseqs == None and percsubseqs == None:
		print("No sampling strategy has been specified. Please, select either the number or the percentage of sequences to subsample.")
		sys.exit(1)

	if numsubseqs!=None and percsubseqs == None:
		try: 
			samptype="num"
			sampvalue=int(numsubseqs)
		except:
			print("The number of sequences must be an integer.")
			sys.exit(1)

	if percsubseqs!=None and numsubseqs == None:
		try:
			samptype="per"
			if 0 < round(float(percsubseqs),3) < 100:
				sampvalue=round(float(percsubseqs),3)
			else:
				print("Choose any float value > 0 and < 100.")
				sys.exit(1)
		except:
			print("The percentage of sequences must be expressed as an integer or a float, ranging from 0 to 100 (with 0 and 100 excluded).")
			sys.exit(1)

	# Main
	with open(fasta) as seqs, open(args['o'], 'w') as result:

		record_dict = SeqIO.to_dict(SeqIO.parse(seqs, 'fasta'))
		list_ids=list(record_dict.keys())
		tot_seqs=len(list_ids)

		if samptype=="num":
			if 0 < sampvalue <= tot_seqs:
				subsampled_ids=sample(list_ids,sampvalue)
			else:
				print("Choose any value between 1 and the maximum number of sequences in your alignment -1.\nYour file contains "+str(tot_seqs)+" sequences.")
				sys.exit(1)
		else:
			sampvalue=round((round((tot_seqs/100),3)*sampvalue))
			if sampvalue >= int(tot_seqs):
				sampvalue = (int(sampvalue)-1)

			subsampled_ids=sample(list_ids,sampvalue)

		result_records = [record_dict[id_] for id_ in subsampled_ids]
		fasta_writer = FastaIO.FastaWriter(result, wrap=None)
		fasta_writer.write_file(result_records)
