#!/bin/bash

path="/home/montoliu/mut_phylogenies/mut_genes/alignments"

sed -i 's/^MVKR/MKR/;s/^MAVKR/MKR/;s/^MP.*VKR/MKR/;s/^MNVKR/MKR/;s/^ML.*VKR/MKR/' ${path}/mutT.fasta

#sed 's/^MP.*MN/MN/;s/^MP.*MS/MS/;s/^MSL.*MN/MN/;s/^ML.*MN/MN/;s/^ML.*MS/MS/;s/^MG.*MN/MN/;s/^MG.*MS/MS/;s/^MH.*MN/MN/;s/^MH.*MS/MS/;s/^MW.*MN/MN/;s/^MW.*MS/MS/;s/^MSH.*MN/MN/;s/^MR.*MN/MN/;s/^MR.*MS/MS/;s/^MSS.*MN/MN/;s/^MSQ.*MN/MN/;s/^MSH.*MN/MN/;s/^MSP.*MN/MN/' ${path}/mutS.fasta > ${path}/mutS_fixed.fasta 
