#!/bin/bash
#SBATCH --output=prep_files-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=06:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate

# Define directories:
faa="/home/montoliu/other_species/mut_genes/faa_files"
ffn="/home/montoliu/other_species/mut_genes/ffn_files"
faa_out="/home/montoliu/other_species/mut_genes/faa_files_renamed"
ffn_out="/home/montoliu/other_species/mut_genes/ffn_files_renamed"

mkdir -p ${faa_out}
mkdir -p ${ffn_out}

#Change headers to not contain spaces and reduce header size so that BLAST can work with it properly:
for prefix in pbra pflu psav pvir
do
	mkdir -p ${faa_out}/${prefix}
	mkdir -p ${ffn_out}/${prefix}

	for file in ${ffn}/${prefix}/*ffn
	do
		filename=$(basename "$file" .ffn)
		sed '/^>/ s/ /_/g' ${file} > ${ffn_out}/${prefix}/${filename}.ffn
	done

	for file in ${faa}/${prefix}/*faa
	do
		filename=$(basename "$file" .faa)
		sed '/^>/ s/ /_/g' ${file} > ${faa_out}/${prefix}/${filename}.faa
	done

	python ./rename_fasta_headers_ffn.py -in ${ffn_out}/${prefix} -out ${ffn_out}/${prefix} -pre ${prefix}
	python ./rename_fasta_headers_faa.py -in ${faa_out}/${prefix} -out ${faa_out}/${prefix} -pre ${prefix}

	for file in ${ffn_out}/${prefix}/*ffn
	do
		awk '/^>/ {split($0, a, "_"); $0 = a[1] "_" a[2] "_" a[3]}; 1' ${file} > temp.fasta && mv temp.fasta ${file}
	done  

	for file in ${faa_out}/${prefix}/*faa
	do
		awk '/^>/ {split($0, a, "_"); $0 = a[1] "_" a[2] "_" a[3]}; 1' ${file} > temp.fasta && mv temp.fasta ${file}
	done
done