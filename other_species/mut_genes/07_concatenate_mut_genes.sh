#!/bin/bash
#SBATCH --output=concatenate-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

dir_nt="/home/montoliu/other_species/mut_genes/mut_sequences_nt"
dir_aa="/home/montoliu/other_species/mut_genes/mut_sequences_protein"

out_nt="/home/montoliu/other_species/mut_genes/alignments_nt"
out_aa="/home/montoliu/other_species/mut_genes/alignments_aa"

mkdir -p ${out_nt}
mkdir -p ${out_aa}

#Concatenate fasta sequences
for prefix in pbra pflu psav pvir
do
        mkdir -p ${out_nt}/${prefix}
        mkdir -p ${out_aa}/${prefix}

	for mut in mutS mutT mutY mutL dnaQ uvrD
        do
                for file in ${dir_nt}/${prefix}/${mut}/*fasta
                do
                        cat ${file} >> ${out_nt}/${prefix}/${mut}.fasta
                done

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
                sed '/^>/ s/_.*//' ${out_nt}/${prefix}/${mut}.fasta > ${out_nt}/${prefix}/${mut}_id.fasta
                sed '/^>/ s/_.*//' ${out_aa}/${prefix}/${mut}.fasta > ${out_aa}/${prefix}/${mut}_id.fasta

        done
done