import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('40_species.csv', encoding='ascii', sep=',')

# Create a separate folder with the fasta files as symlinks
output_directory = "/home/montoliu/40sp/data"
os.makedirs(output_directory, exist_ok=True)

path = "/home/montoliu/40sp/ncbi-data"

for index, row in df.iterrows():
    abreviation = row['abreviation']
    refseq = row['refseq']
    
    protein_file = os.path.join(path, abreviation, "ncbi_dataset", "data", refseq, "protein.faa")
    symlink_path = os.path.join(output_directory, f'{abreviation}.faa')

    if os.path.exists(protein_file):
            os.symlink(protein_file, symlink_path)

