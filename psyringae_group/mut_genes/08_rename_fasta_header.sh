#!/bin/bash

path="/home/montoliu/psyringae_group/mut_genes/alignments"

for file in ${path}/*fasta
do
	filename=$(basename "$file" .fasta)
sed '/^>/ s/_.*//' ${file} > ${path}/${filename}_id.fasta

done

