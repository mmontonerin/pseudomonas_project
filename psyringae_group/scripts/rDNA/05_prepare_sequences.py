import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('final_table_of_genome_assemblies_3.csv', encoding='ascii', sep=',')

# Copy extracted sequences and change the fasta header to ps_num, so that it can be used in alignments 

# List directories
path = "/home/montoliu/psyringae_group/results/rDNA/sequences"
output_directory_seq = "/home/montoliu/psyringae_group/results/rDNA/alignment" 
os.makedirs(output_directory_seq, exist_ok=True)

# Iterate over filenames and corresponding numbers
for filename, num in zip(df['filename'], df['num']):
    found = False
    # Check if fasta file is in directory
    fasta_files = [file for file in os.listdir(path) if file.startswith(filename) and file.endswith('.fasta')]
    for fasta_file in fasta_files:
        # Modify fasta header and save to output directory
        fasta_path = os.path.join(path, fasta_file)
        record = SeqIO.read(fasta_path, 'fasta')
        record.id = f"psyr{num}"
        record.description = ""
        new_fasta_path = os.path.join(output_directory_seq, f'{filename}.fasta')
        SeqIO.write(record, new_fasta_path, 'fasta')
        found = True
    if not found:
        print(f"No sequence found for strain ppro{num}: {filename}")
