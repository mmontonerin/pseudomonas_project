#!/bin/bash
#SBATCH --output=02_organize_dataset-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J organize_dataset
#SBATCH --partition=medium 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

# Working directory
path="/home/montoliu/other_species/data"

mkdir -p ${path}/genome_assemblies/pbra
mkdir -p ${path}/genome_assemblies/pflu
mkdir -p ${path}/genome_assemblies/psav
mkdir -p ${path}/genome_assemblies/pvir

for assembly in ${path}/pbrassicacearum/ncbi_dataset/data/GCA*/GCA*fna
do
	name=$(basename "$assembly" .fna)
	sed -E 's/^>([^ ]+).*/>\1/' ${assembly} > ${path}/genome_assemblies/pbra/${name}.fasta
done

for assembly in ${path}/pfluorescens/ncbi_dataset/data/GCA*/GCA*fna
do
	name=$(basename "$assembly" .fna)
	sed -E 's/^>([^ ]+).*/>\1/' ${assembly} > ${path}/genome_assemblies/pflu/${name}.fasta
done

for assembly in ${path}/psavastanoi/ncbi_dataset/data/GCA*/GCA*fna
do
	name=$(basename "$assembly" .fna)
	sed -E 's/^>([^ ]+).*/>\1/' ${assembly} > ${path}/genome_assemblies/psav/${name}.fasta
done

for assembly in ${path}/pviridiflava/ncbi_dataset/data/GCA*/GCA*fna
do
	name=$(basename "$assembly" .fna)
	sed -E 's/^>([^ ]+).*/>\1/' ${assembly} > ${path}/genome_assemblies/pvir/${name}.fasta
done
