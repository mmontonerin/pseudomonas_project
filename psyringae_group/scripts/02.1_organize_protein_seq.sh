#!/bin/bash
#SBATCH --output=slurm_02_organize_dataset-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J organize_dataset
#SBATCH --partition=medium 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:00:00          # total run time limit in DD-HH:MM:SS
#SBATCH --mail-type=END,FAIL       # send email when job ends or fails
#SBATCH --mail-user=merce.montoliu@upm.es

# Working directory
input="/home/montoliu/psyringae_group/data/ncbi_dataset/data"
output="/home/montoliu/psyringae_group/data/proteins"

mkdir -p ${output}

# Simplify headers from FASTA files so that a header like this:
#	>NHSS01000001.1 Pseudomonas syringae strain RMX.24.a.1 seq113_Contig1, whole genome shotgun
# becomes this:
#	>NHSS01000001.1
# This is necessary for makeblastdb and blastn correct funcioning


for folder in ${input}/GCA*
do

	name=$(basename "$folder")
	input_file="${folder}/protein.faa"
	output_file="${output}/${name}.faa"

	if [ -s "${input_file}" ]; then	
		echo "processing $input_file in $folder to $output_file"
		sed -E 's/^>([^ ]+).*/>\1/' ${input_file} > ${output_file}
	fi
done

