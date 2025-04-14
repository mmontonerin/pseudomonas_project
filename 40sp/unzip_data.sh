#!/bin/bash
#SBATCH --output=prep_files-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

#Unzip and create a descriptive
for file in ./*zip
do
	filename=$(basename ${file} .zip)
	unzip ${file} -d ${filename}
done