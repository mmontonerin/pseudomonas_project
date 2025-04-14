#!/bin/bash
#SBATCH --output=iqtree-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --cpus-per-task=40
#SBATCH --partition=long 
#SBATCH --time=3-00:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
path="/home/montoliu/mut_phylogenies/mut_genes/alignments"

for prefix in mutS mutT mutY uvrD
do
    for alignment in ${path}/${prefix}*phy
    do
        filename=$(basename "$alignment" _mafft_trimal.phy)
        iqtree -s ${alignment} --prefix ${filename} -B 1000 -T AUTO -ntmax 40
    done
done