#!/bin/bash
#SBATCH --output=slurm_02_organize_dataset-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J organize_dataset
#SBATCH --partition=medium 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=03:00:00          # total run time limit in DD-HH:MM:SS

# Working directory
cd /home/montoliu/pprotegens/data

# Create a folder assemblies if it does not exist
mkdir -p assemblies

# Unzip dataset
unzip ncbi_dataset.zip

# Move README inside ncbi_dataset folder
mv README.md ncbi_dataset/

# Simplify headers from FASTA files so that a header like this:
#	>NHSS01000001.1 Pseudomonas syringae strain RMX.24.a.1 seq113_Contig1, whole genome shotgun
# becomes this:
#	>NHSS01000001.1
# This is necessary for makeblastdb and blastn correct funcioning

for assembly in ./ncbi_dataset/data/GCA*/*fna
do

	name=$(basename "$assembly" .fna)

	sed -E 's/^>([^ ]+).*/>\1/' ${assembly} > ./assemblies/${name}.fasta
done

