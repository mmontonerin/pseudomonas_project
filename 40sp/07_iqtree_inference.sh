#!/bin/bash
#SBATCH --output=iqtree-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=10        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
dir="/home/montoliu/40sp/mut_sequences/alignments"

for alignment in ${dir}/*mafft.fasta 
do
	iqtree -s ${alignment} -B 1000 -T auto -ntmax 10  
done