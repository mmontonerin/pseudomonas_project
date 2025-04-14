#!/bin/bash
#SBATCH --output=concatenate-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

dir_aa="/home/montoliu/pprotegens/mut_genes/protein_analysis/mut_sequences"
out_aa="/home/montoliu/pprotegens/mut_genes/protein_analysis/alignments"

mkdir -p ${out_aa}

#Concatenate fasta sequences
#for mut in mutS mutT mutY mutL dnaQ uvrD
#    do
#        for file in ${dir_aa}/${mut}/*fasta
#        do
#            cat ${file} >> ${out_aa}/${mut}.fasta
#        done
#    done
#done

#Rename fasta headers (for alignment)
for mut in mutS mutT mutY mutL dnaQ uvrD
    do
        sed '/^>/ s/_.*//' ${out_aa}/${mut}.fasta > ${out_aa}/${mut}_id.fasta
    done
done