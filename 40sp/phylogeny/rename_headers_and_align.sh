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

path="/home/montoliu/40sp/data_renamed/OrthoFinder/Results_Nov14/Single_Copy_Orthologue_Sequences"
out="/home/montoliu/40sp/phylogeny/alignments"
mkdir -p ${out}

for file in ${path}/*fa
do
	filename=$(basename ${file} .fa)
    sed '/^>/ s/_.*//' ${file} > ${out}/${filename}.fa
done

for file in ${out}/*fa
do
	file_name=$(basename ${file} .fa)

	mafft ${file} > ${out}/${file_name}_mafft.fa
done
