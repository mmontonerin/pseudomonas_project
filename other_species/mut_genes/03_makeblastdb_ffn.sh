#!/bin/bash
#SBATCH --output=makeblastdb-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

dir="/home/montoliu/other_species/mut_genes/ffn_files_renamed"

#Create database from annotation ffn files
for prefix in pbra pflu psav pvir
do
	for file in ${dir}/${prefix}/*ffn
	do
		makeblastdb -in ${file} -dbtype nucl -parse_seqids 	
	done 
done