#!/bin/bash
#SBATCH --output=mafft-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml MAFFT/7.505-GCC-11.3.0-with-extensions

path="/home/montoliu/40sp/mut_sequences/alignments"

for file in ${path}/*_id.fasta
do
	filename=$(basename "$file" .fasta)
	mafft ${file} > ${path}/${filename}_mafft.fasta
done