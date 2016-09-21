#DLB 030216
#Script to quality filter multiple FASTQ files with USEARCH8
#and output as fasta files for use in QIIME

import subprocess
import csv
import os
import argparse

#########################################################################
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to the input sequence folder", type=str)
ap.add_argument("-o", "--output", required=False,
	help="output directory", type=str, default="rf_ouput")
ap.add_argument("-q", "--q_thresh", required=False,
	help="Q score threshold", type=int, default= 13)
ap.add_argument("-n", "--seq_len", required=False,
	help="Q score threshold", type=int, default= 220)
args = vars(ap.parse_args())

#assign arguments
input_path = args["input"]
output_path = args["output"]
log_path = output_path[:-1] + "_quality_logs/"
q = args["q_thresh"]
l = args["seq_len"]
#########################################################################


if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(log_path):
    os.makedirs(log_path)

#create list of filenames
filenames = next(os.walk(input_path))[2]
filenames.sort()

for file_call in filenames: 	
	p = subprocess.Popen("usearch8 -fastq_filter " +  #save BASH call
		input_path + file_call +

		" -log " + log_path + file_call[:-20] + ".txt" + 

		#USEARCH options from:
		#http://www.earthmicrobiome.org/emp-standard-protocols/16s-taxonomic-assignments/
		#Quality score threshold meanings:
		#http://drive5.com/usearch/manual/quality_score.html
		" -fastq_trunclen " + str(l) + " -fastq_truncqual " + str(q) + " -fastq_maxns 1 -fastaout " + 

		output_path + file_call[:-20] + ".fasta", shell=True) #output file

	print file_call[:-20] + " doing its thing"
	p.communicate() #make BASH call and wait with communication


print "Done!"

