#!/bin/bash
#SBATCH --output=concatenate-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

dir_aa="/home/montoliu/other_species/mut_genes/mut_sequences_protein"
out_aa="/home/montoliu/other_species/mut_genes/protein_analysis"

mkdir -p ${out_aa}

#Concatenate fasta sequences
for prefix in pbra pflu psav pvir
do
        mkdir -p ${out_aa}/${prefix}

	for mut in mutS mutT mutY mutL dnaQ uvrD
        do
                for file in ${dir_aa}/${prefix}/${mut}/*fasta
                do
                        cat ${file} >> ${out_aa}/${prefix}/${mut}.fasta
                done
        done
done

#Rename fasta headers (for alignment)
for prefix in pbra pflu psav pvir
do
	for mut in mutS mutT mutY mutL dnaQ uvrD
        do
                sed '/^>/ s/\([auvr]\)0/\1/;s/_.*//' ${out_aa}/${prefix}/${mut}.fasta > ${out_aa}/${prefix}/${mut}_id.fasta

        done
done