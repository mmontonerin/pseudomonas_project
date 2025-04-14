#!/bin/bash
#SBATCH --output=slurm_phylogeny-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

# Iniciate conda for alignments to use MACSE 2
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate phylo

# Define directories:
phylo="/home/montoliu/psyringae_group/results/rDNA/phylogeny"
align="/home/montoliu/psyringae_group/results/rDNA/alignment"

cd ${phylo}

iqtree -s ${align}/16s_NT.fasta -m MFP -B 1000

