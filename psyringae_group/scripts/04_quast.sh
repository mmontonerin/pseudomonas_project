#!/bin/bash
#SBATCH --output=slurm_04_quast_psyr-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J quast-psyringae_group_assemblies
#SBATCH --ntasks=4        
#SBATCH --nodes=1                  
#SBATCH --partition=long 
#SBATCH --time=8-00:00:00          # total run time limit in DD-HH:MM:SS

# Activate conda to use Quast
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate quast

# Define directories:
psyr="/home/montoliu/psyringae_group" #main directory of the analysis
as="/home/montoliu/psyringae_group/data/assemblies" #assembly references
result="/home/montoliu/psyringae_group/results/quast" #results folder
run="/home/montoliu/psyringae_group/scripts" #scripts folder

# Run basic Quast to get assembly stats in all assembly files:

for assembly in ${as}/*.fasta
do 
	aname=$(basename "$assembly" .fasta)
	quast -o ${result}/${aname} -t 8 --no-plots --no-html ${assembly}

done

