#!/bin/bash
#SBATCH --output=prep_files-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate

# Define directories:
phy="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/phylogenomics/orthofinder"
data="/home/montoliu/pprotegens/data/genome_annotations/all_annotations"

python ./rename_annotations_for_phylo.py -in ${data} -out ${phy} 
