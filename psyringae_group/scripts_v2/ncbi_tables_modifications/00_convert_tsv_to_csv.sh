#!/bin/bash

# Remove RefSeq sequences (GCF*)
# Remove any commas that are already in the file to create a good csv file
grep -v "GCF" ncbi_psyringae_group_3016_genomes.tsv | sed 's/,//g' > ncbi_psyringae_group_3016_genomes_nocomma.tsv

# Change tsv to csv
awk 'BEGIN { FS="\t"; OFS="," } {$1=$1; print}' ncbi_psyringae_group_3016_genomes_nocomma.tsv > ncbi_psyringae_group_3016_genomes.csv

# Remove all intermediary files
rm ncbi_psyringae_group_3016_genomes_nocomma.tsv
