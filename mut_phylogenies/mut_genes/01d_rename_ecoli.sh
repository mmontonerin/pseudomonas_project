#!/bin/bash

for mutgene in dnaQ mutS mutL mutT mutY uvrD
do

    sed "s/>.*/>ecol_${mutgene}/" /home/montoliu/mut_phylogenies/mut_genes/ecoli/ecoli_${mutgene}.fasta > /home/montoliu/mut_phylogenies/mut_genes/sequences/ecol_${mutgene}.fasta
done