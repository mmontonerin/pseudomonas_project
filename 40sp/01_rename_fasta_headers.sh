#!/bin/bash

path="/home/montoliu/40sp/genome_annotation/genome_annotations"
out="/home/montoliu/40sp/data_renamed"
mkdir -p ${out}

for file in ${path}/*/*faa
do
	filename=$(basename ${file} .faa)
    sed '/^>/ s/ .*$//' ${file} > ${out}/${filename}.faa
done

python ./rename_fasta_headers.py -in ${out} -out ${out}

