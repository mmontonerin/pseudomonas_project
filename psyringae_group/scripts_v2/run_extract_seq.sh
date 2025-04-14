#!/bin/bash
#SBATCH --output=slurm-blast_extractseq-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=2        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=06:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

run="/home/montoliu/psyringae_group/scripts_v2" #scripts folder

# Make the script executable
chmod +x ${run}/extract_blast_seq_extrabp200_endcontig.sh
chmod +x ${run}/extract_blast_seq_frag_extrabp200_endcontig.sh
chmod +x ${run}/extract_blast_seq_extrabp200_complete.sh
chmod +x ${run}/extract_blast_seq_frag_extrabp200_complete.sh

# Run the script to extract all sequences
${run}/extract_blast_seq_extrabp200_complete.sh &
${run}/extract_blast_seq_frag_extrabp200_complete.sh &
${run}/extract_blast_seq_extrabp200_endcontig.sh &
${run}/extract_blast_seq_frag_extrabp200_endcontig.sh &

# Wait for all commands to finish
wait

