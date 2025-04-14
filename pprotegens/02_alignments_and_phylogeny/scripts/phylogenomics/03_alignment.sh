#!/bin/bash
#SBATCH --output=slurm_mafft-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml MAFFT/7.505-GCC-11.3.0-with-extensions

# Define directories:

seq="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/phylogenomics/orthofinder/OrthoFinder/Results_Sep02/Single_Copy_Orthologue_Sequences"
ali="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/phylogenomics/sco_alignments" 


for file in ${seq}/*fa
do
	file_name=$(basename "$file" .fa)

	mafft $file > ${ali}/${file_name}_mafft.fa
done

