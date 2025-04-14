#!/bin/bash
#SBATCH --output=orthofinder-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=20        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=long 
#SBATCH --time=10-00:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
phy="/home/montoliu/40sp/data_renamed"

orthofinder -t 20 -a 20 -f ${phy}