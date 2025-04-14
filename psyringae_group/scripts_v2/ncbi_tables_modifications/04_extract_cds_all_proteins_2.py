import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('final_table_of_genome_assemblies_final_num.csv', encoding='ascii', sep=',')

# Create a separate folder with the cds fasta files as symlinks
output_directory = "/home/montoliu/psyringae_group/data/cds_selection"
os.makedirs(output_directory, exist_ok=True)

for Accession in df['Accession']:
    fasta_file = os.path.join('/home/montoliu/psyringae_group/data/proteins_new_annotations/genome_annotations', f'{Accession}', f'{Accession}.fna')
    symlink_path = os.path.join(output_directory, f'{Accession}.fna')
    if os.path.exists(fasta_file):  # Check if fasta file exists
        if not os.path.exists(symlink_path):  # Check if symlink does not exist
            os.symlink(fasta_file, symlink_path)