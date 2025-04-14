#!/bin/bash

cd /home/montoliu/psyringae_group/data/assemblies

echo 'filename' > /home/montoliu/psyringae_group/scripts/ncbi_tables_modifications/01_filelist

ls *fasta >> /home/montoliu/psyringae_group/scripts/ncbi_tables_modifications/01_filelist

sed 's/.fasta//g' /home/montoliu/psyringae_group/scripts/ncbi_tables_modifications/01_filelist > /home/montoliu/psyringae_group/scripts/ncbi_tables_modifications/01_assemblynames

# Remove all intermediary files

rm /home/montoliu/psyringae_group/scripts/ncbi_tables_modifications/01_filelist
