#!/bin/bash
#SBATCH --output=slurm_phylogeny-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=3        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate phylo

# Define directories:
phy="/home/montoliu/psyringae_group/results/phylogeny_test_laura"

#for ali in ${phy}/*mafft_curated.fasta
#do
#    name=$(basename "$ali" .fasta)
#    sed -E 's/>.{4}_/>psg_/g' ${ali} > ${name}_renamed.fasta
#done  

# Separate phylogeny
#for ali in ${phy}/*mafft_curated_renamed.fasta
#do
#    iqtree -s ${ali} -m MFP -B 100
#done

iqtree -s ${phy}/mutS_mafft_curated_renamed.fasta -m MFP -B 1000 &
iqtree -s ${phy}/uvrD_mafft_curated_renamed.fasta -m MFP -B 1000 &
iqtree -s ${phy}/mutY_mafft_curated_renamed.fasta -m MFP -B 1000 &

wait

# Joint phylogeny mutY, mutS, uvrD
#cat ${phy}/*mafft_curated_renamed.fasta >> ${phy}/mutS-mutY-uvrD.fasta

#iqtree -p ${phy}/mutS-mutY-uvrD.fasta 


