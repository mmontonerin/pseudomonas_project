#!/bin/bash
#SBATCH --output=slurm_trimal-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

# Iniciate conda for alignments to use MACSE 2
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate phylo

# Define directories:
ali="/home/montoliu/pprotegens/results/sequences_selection_final/alignments"
phylo="/home/montoliu/pprotegens/results/phylogeny/mut_phylogeny_final/alignments"

mkdir -p /home/montoliu/pprotegens/results/phylogeny/mut_phylogeny_final/alignments

for fasta in ${ali}/*AA.fasta 
do
    name=$(basename ${fasta} .fasta)
    trimal -in ${fasta} -out ${phylo}/${name}_trimmed.fasta -gt 0.1

    sed 's/>[^_]\+_/>ppro/g' ${phylo}/${name}_trimmed.fasta > ${phylo}/${name}_trimmed_renamed.fasta

done



