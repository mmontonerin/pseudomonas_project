#!/bin/bash

# Remove RefSeq sequences (GCF*)
# Remove any commas that are already in the file to create a good csv file
grep -v "GCF" ncbi_pprotegens_101.tsv | sed 's/,//g;s/;//g' > ncbi_pprotegens_101_nocomma.tsv

# Change tsv to csv
awk 'BEGIN { FS="\t"; OFS="," } {$1=$1; print}' ncbi_pprotegens_101_nocomma.tsv > ncbi_pprotegens_101.csv

# Remove all intermediary files
rm ncbi_pprotegens_101_nocomma.tsv
