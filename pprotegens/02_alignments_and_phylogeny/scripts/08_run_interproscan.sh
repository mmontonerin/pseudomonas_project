#!/bin/bash
#SBATCH --output=slurm_interproscan-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=16        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=long 
#SBATCH --time=4-00:00:00          # total run time limit in DD-HH:MM:SS

# Iniciate conda for alignments to use MACSE 2
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate phylo

# Define directories:
phylo="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/alignments"
interpro="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/interproscan"

mkdir -p /home/montoliu/pprotegens/02_alignments_and_phylogeny/results/interproscan

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/dnaQ.fasta -t n -d ${interpro} -cpu 16

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/mutS.fasta -t n -d ${interpro} -cpu 16

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/mutY.fasta -t n -d ${interpro} -cpu 16

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/mutL.fasta -t n -d ${interpro} -cpu 16

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/mutT.fasta -t n -d ${interpro} -cpu 16

/home/montoliu/miniconda3/envs/phylo/share/InterProScan/interproscan.sh -i ${phylo}/uvrD.fasta -t n -d ${interpro} -cpu 16


