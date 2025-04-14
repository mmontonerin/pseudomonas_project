#!/bin/bash
#SBATCH --output=iqtree-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --cpus-per-task=40
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
path="/home/montoliu/mut_phylogenies/sp_tree/SCOs_300/alignments"

iqtree -s ${path} --prefix sp_tree300 -B 1000 -T AUTO -ntmax 40