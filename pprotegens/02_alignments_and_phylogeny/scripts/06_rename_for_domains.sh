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
#phylo="/home/montoliu/pprotegens/results/phylogeny/mut_phylogeny_final"

#for fasta in ${ali}/*.fasta 
#do
#    name=$(basename ${fasta} .fasta)

#    sed 's/>[^_]\+_/>ppro/g' ${fasta} > ${phylo}/${name}_renamed.fasta

#done

sed 's/>[^_]\+_/>ppro/g' ${ali}/mutL.fasta > ${ali}/domains/mutL.fasta
sed 's/>[^_]\+_/>ppro/g' ${ali}/uvrD.fasta > ${ali}/domains/uvrD.fasta
sed 's/>[^_]\+_/>ppro/g' ${ali}/dnaQ.fasta > ${ali}/domains/dnaQ.fasta
sed 's/>[^_]\+_/>ppro/g' ${ali}/mutT.fasta > ${ali}/domains/mutT.fasta
sed 's/>[^_]\+_/>ppro/g' ${ali}/mutY.fasta > ${ali}/domains/mutY.fasta
sed 's/>[^_]\+_/>ppro/g' ${ali}/mutS.fasta > ${ali}/domains/mutS.fasta


