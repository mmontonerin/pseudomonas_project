#!/bin/bash

data='/home/montoliu/other_species/data/genome_assemblies'
scripts='/home/montoliu/other_species/tables'

for abv in pbra pflu psav pvir
do
    echo 'filename' > ${scripts}/${abv}_filelist

    cd ${data}/${abv}
    ls *fasta >> ${scripts}/${abv}_filelist
    sed 's/.fasta//g' ${scripts}/${abv}_filelist > ${scripts}/${abv}_assembly_names.txt

    # Remove all intermediary files
    rm ${scripts}/${abv}_filelist
done