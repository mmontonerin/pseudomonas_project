#!/bin/bash

path="/home/montoliu/psyringae_group/mut_genes/protein_analysis"

cat ${path}/mut_sequences/mutS/*fasta >> ${path}/alignments/mutS.fasta
cat ${path}/mut_sequences/mutL/*fasta >> ${path}/alignments/mutL.fasta
cat ${path}/mut_sequences/mutT/*fasta >> ${path}/alignments/mutT.fasta
cat ${path}/mut_sequences/mutY/*fasta >> ${path}/alignments/mutY.fasta
cat ${path}/mut_sequences/uvrD/*fasta >> ${path}/alignments/uvrD.fasta
cat ${path}/mut_sequences/dnaQ/*fasta >> ${path}/alignments/dnaQ.fasta

for file in ${path}/alignments/*fasta
do
	filename=$(basename "$file" .fasta)
    sed '/^>/ s/_.*//;s/psg0/psg/' ${file} > ${path}/alignments/${filename}_id.fasta

done