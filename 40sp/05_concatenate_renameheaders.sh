#!/bin/bash

path="/home/montoliu/40sp/mut_sequences"

cat ${path}/mutS/*fasta >> ${path}/alignments/mutS.fasta
cat ${path}/mutL/*fasta >> ${path}/alignments/mutL.fasta
cat ${path}/mutT/*fasta >> ${path}/alignments/mutT.fasta
cat ${path}/mutY/*fasta >> ${path}/alignments/mutY.fasta
cat ${path}/uvrD/*fasta >> ${path}/alignments/uvrD.fasta
cat ${path}/dnaQ/*fasta >> ${path}/alignments/dnaQ.fasta
cat ${path}/mutH/*fasta >> ${path}/alignments/mutH.fasta

for file in ${path}/alignments/*fasta
do
	filename=$(basename "$file" .fasta)
    sed '/^>/ s/_.*//' ${file} > ${path}/alignments/${filename}_id.fasta

done