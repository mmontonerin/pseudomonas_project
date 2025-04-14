#!/bin/bash
#SBATCH --output=slurm-quast_ppro-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J quast-pprotegens_assemblies
#SBATCH --ntasks=8        
#SBATCH --nodes=1                  
#SBATCH --partition=long 
#SBATCH --time=2-00:00:00          # total run time limit in DD-HH:MM:SS

# Activate conda to use Quast
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate quast

# If results directory does not exist, it creates it:
mkdir -p /home/montoliu/pprotegens/results/quast

# Define directories:
ppro="/home/montoliu/pprotegens" #main directory of the analysis
as="/home/montoliu/pprotegens/data/assemblies" #assembly references
result="/home/montoliu/pprotegens/results/quast" #results folder

# Run basic Quast to get assembly stats in all assembly files:

for assembly in ${as}/*.fasta
do 
	aname=$(basename "$assembly" .fasta)
	quast -o ${result}/${aname} -t 8 --no-plots --no-html ${assembly}
done