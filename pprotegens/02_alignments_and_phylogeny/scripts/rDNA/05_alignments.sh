#!/bin/bash
#SBATCH --output=slurm_macse-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=6        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

# Iniciate conda for alignments to use MACSE 2
source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate ali

# Define directories:
ali="/home/montoliu/pprotegens/results/rDNA/alignment"

#If it has run already, remove files to re-run it again and not concatenate

cd ${ali}
cat GCA*fasta >> 16s.fasta 

macse -prog alignSequences -seq 16s.fasta -gc_def 11 -out_AA 16s_AA.fasta -out_NT 16s_NT.fasta

macse -prog exportAlignment -gc_def 11 -align 16s_NT.fasta -out_stat_per_seq 16s_stats_per_seq.csv -out_stat_per_site 16s_stats_per_site.csv 


