#!/bin/bash
#SBATCH --output=iqtree-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=20        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=long 
#SBATCH --time=20-00:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
phy="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/phylogenomics/sco_alignments"

iqtree -s ${phy} --prefix pprotegens -B 1000 -T AUTO -ntmax 20

