import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('final_table_missing_annotations.csv', encoding='ascii', sep=',')

# Create a separate folder with the fasta files as symlinks
output_directory = "/home/montoliu/psyringae_group/data/proteins_new_annotations/genome_assemblies_to_annotate"
os.makedirs(output_directory, exist_ok=True)

for filename in df['filename']:
    fasta_file = os.path.join('/home/montoliu/psyringae_group/data/assemblies', f'{filename}.fasta')
    symlink_path = os.path.join(output_directory, f'{filename}.fasta')
    if not os.path.exists(symlink_path):  # Check if symlink does not exist
        os.symlink(fasta_file, symlink_path)



