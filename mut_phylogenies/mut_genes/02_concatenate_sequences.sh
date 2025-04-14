#!/bin/bash

input="/home/montoliu/mut_phylogenies/mut_genes/sequences"
output="/home/montoliu/mut_phylogenies/mut_genes/alignments"

mkdir -p ${output}

for mutgene in dnaQ mutL mutS mutT mutY uvrD
do  
    cat ${input}/*${mutgene}.fasta >> ${output}/${mutgene}.fasta
done