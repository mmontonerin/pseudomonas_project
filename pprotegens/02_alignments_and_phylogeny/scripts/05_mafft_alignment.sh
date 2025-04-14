#!/bin/bash
#SBATCH --output=slurm_mafft-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=6        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml MAFFT/7.505-GCC-11.3.0-with-extensions

# Define directories:
ali="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/alignments"

mkdir -p /home/montoliu/pprotegens/02_alignments_and_phylogeny/results/alignments

mafft ${ali}/mutT.fasta > ${ali}/mutT_mafft.fasta &
mafft ${ali}/uvrD.fasta > ${ali}/uvrD_mafft.fasta &
mafft ${ali}/dnaQ.fasta > ${ali}/dnaQ_mafft.fasta &
mafft ${ali}/mutY.fasta > ${ali}/mutY_mafft.fasta &
mafft ${ali}/mutL.fasta > ${ali}/mutL_mafft.fasta &
mafft ${ali}/mutS.fasta > ${ali}/mutS_mafft.fasta &

# Wait for all alignments to finish
wait


