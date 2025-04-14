#!/bin/bash

path='/home/montoliu/other_species/data/run_quast/batch_scripts'
counter=1

# Iterate over each row in the DataFrame
for batch in ${path}/*.sh
do
    # Construct the Prokka command
    echo "${counter} ${batch}" >> quast_config.txt
    counter=$((counter + 1))
done
