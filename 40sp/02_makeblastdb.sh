#!/bin/bash
#SBATCH --output=makeblastdb-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=02:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

dir="/home/montoliu/40sp/data_renamed"

#Create database from annotation faa files
for file in ${dir}/*faa 
do
	makeblastdb -in ${file} -dbtype prot  -parse_seqids 	
done 