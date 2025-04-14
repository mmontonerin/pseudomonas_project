#!/bin/bash

# Remove RefSeq sequences (GCF*)
# Remove any commas that are already in the file to create a good csv file

for tsv in ./*.tsv
do
    tsvname=$(basename ${tsv} .tsv)
    grep -v "GCF" ${tsv} | sed 's/,//g;s/;//g' > ${tsvname}_nocomma.tsv

    # Change tsv to csv
    awk 'BEGIN { FS="\t"; OFS="," } {$1=$1; print}' ${tsvname}_nocomma.tsv > ${tsvname}.csv

    # Remove all intermediary files
    rm ${tsvname}_nocomma.tsv
done