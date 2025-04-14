#!/bin/bash

data='/home/montoliu/pprotegens/data/assemblies'
scripts='/home/montoliu/pprotegens/scripts/ncbi_tables_modifications'

cd $data

echo 'filename' > ${scripts}/01_filelist

ls *fasta >> ${scripts}/01_filelist

sed 's/.fasta//g' ${scripts}/01_filelist > ${scripts}/01_assemblynames

# Remove all intermediary files

rm ${scripts}/01_filelist
