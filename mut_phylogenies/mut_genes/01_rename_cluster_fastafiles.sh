#!/bin/bash

input="/home/montoliu/mut_phylogenies/data/mut_sequences/clusters"
output="/home/montoliu/mut_phylogenies/mut_genes/sequences"

mkdir -p ${output}

for prefix in pbra pflu ppro psav psyr pvir
do
  for file in ${input}/${prefix}/*.fasta
  do
    filename=$(basename "$file" _clusters.fasta)
    sed "s/^>/>${prefix}_/" ${file} > ${output}/${prefix}_${filename}.fasta
  done
done