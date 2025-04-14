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
seq="/home/montoliu/psyringae_group/results/sequences_selection_200extrabp_new"
ali="/home/montoliu/psyringae_group/results/sequences_selection_200extrabp_new/alignments" #extracted sequences folder
run="/home/montoliu/psyringae_group/scripts_v2" #scripts folder

mkdir -p /home/montoliu/psyringae_group/results/sequences_selection_200extrabp_new/alignments

cd ${seq}
cat mutT/*fasta >> ${ali}/mutT.fasta &
cat uvrD/*fasta >> ${ali}/uvrD.fasta &
cat dnaQ/*fasta >> ${ali}/dnaQ.fasta &
cat mutY/*fasta >> ${ali}/mutY.fasta &
cat mutL/*fasta >> ${ali}/mutL.fasta &
cat mutS/*fasta >> ${ali}/mutS.fasta &

# Wait for all concatenations to finish
wait

mafft ${ali}/mutT.fasta > ${ali}/mutT_mafft.fasta &
mafft ${ali}/uvrD.fasta > ${ali}/uvrD_mafft.fasta &
mafft ${ali}/dnaQ.fasta > ${ali}/dnaQ_mafft.fasta &
mafft ${ali}/mutY.fasta > ${ali}/mutY_mafft.fasta &
mafft ${ali}/mutL.fasta > ${ali}/mutL_mafft.fasta &
mafft ${ali}/mutS.fasta > ${ali}/mutS_mafft.fasta &

# Wait for all alignments to finish
wait