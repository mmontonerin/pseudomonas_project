#!/bin/bash
#SBATCH --output=prep_files-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate

# Define directories:
out="/home/montoliu/pprotegens/mut_genes/protein_analysis/faa_renamed"
data="/home/montoliu/pprotegens/data/genome_annotations/all_annotations"

mkdir -p ${out}

#Change headers to not contain spaces and reduce header size so that BLAST can work with it properly:
for file in ${data}/*faa
do
	filename=$(basename "$file" .faa)
	sed '/^>/ s/ /_/g' ${file} > ${out}/${filename}.faa
done

#Add ppro{num} to the begining of the header, for taxon id
python ./rename_fasta_headers.py -in ${out} -out ${out}

for file in ${out}/*faa
do
	awk '/^>/ {split($0, a, "_"); $0 = a[1] "_" a[2] "_" a[3]}; 1' ${file} > temp.fasta && mv temp.fasta ${file}
done 