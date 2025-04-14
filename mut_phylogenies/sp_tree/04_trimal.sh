#!/bin/bash
#SBATCH --output=trimal-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast
#SBATCH --time=01:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
path="/home/montoliu/mut_phylogenies/sp_tree/SCOs_300"

cd ${path}

#Trim sections of the alignment not covered by more than 0.28 fraction of the sequences.
#This means we remove sections only covered by one of the sequences
for file in ${path}/*mafft.fasta
do
        filename=$(basename "$file" .fasta)
        sed -i 's/_.*//' ${file}
        trimal -in ${file} -out ${filename}_trimal.phy -phylip -gt 0.28
done

mkdir -p ${path}/alignments

ln -s ${path}/*phy ${path}/alignments/ 
