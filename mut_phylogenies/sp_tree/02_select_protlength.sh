#!/bin/bash
#conda activate phylo

# Define input and output directories
input="/home/montoliu/mut_phylogenies/sp_tree/SCOs"
output="/home/montoliu/mut_phylogenies/sp_tree/SCOs_500"

# Create the output directory if it doesn't exist
mkdir -p ${output}

# Loop through all FASTA files in the input directory
for fasta in ${input}/*.fa
do
    # Use seqkit to check sequence lengths and look for any sequence > 300
    echo "Processing file: ${fasta}"

    # Check the seqkit stats output to verify the max length
    seqkit stats ${fasta}
    
    # Now apply awk to check if any sequence is > 500, make sure that there is no commas when number is higher than 1000, we then force it to be treated as numeric by adding a 0
    if seqkit stats ${fasta} | awk 'NR > 1 {gsub(",", "", $8); if ($8+0 > 500) {found=1}} END {if (found) exit 0; else exit 1}'; then
        echo "File contains sequences > 500 amino acids. Symlinking: ${fasta}"
        ln -fs "$(realpath ${fasta})" ${output}
    else
        echo "No sequences > 500 amino acids found in: ${fasta}"
    fi
done