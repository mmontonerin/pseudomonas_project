import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('final_table_of_genome_assemblies_final.csv', encoding='ascii', sep=',')

# Create a separate folder with the fasta files as symlinks
output_directory = "/home/montoliu/psyringae_group/data/proteins_selection"
os.makedirs(output_directory, exist_ok=True)

missing_files =[]

for Accession in df['Accession']:
    fasta_file = os.path.join('/home/montoliu/psyringae_group/data/proteins', f'{Accession}.faa')
    symlink_path = os.path.join(output_directory, f'{Accession}.faa')
    if os.path.exists(fasta_file):  # Check if fasta file exists
        if not os.path.exists(symlink_path):  # Check if symlink does not exist
            os.symlink(fasta_file, symlink_path)
    else:
        # Add the row to the missing_files list
        missing_files.append(df[df['Accession'] == Accession])

# Create a DataFrame from the missing_files list
missing_files_df = pd.concat(missing_files)

# Save the missing files DataFrame to a new CSV
missing_files_df.to_csv('final_table_missing_annotations.csv', index=False, encoding='ascii', sep=',')    
