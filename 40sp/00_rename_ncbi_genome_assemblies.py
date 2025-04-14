import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('40_species.csv', encoding='ascii', sep=',')

# Create a separate folder with the fasta files as symlinks
output_directory = "/home/montoliu/40sp/genome_assemblies"
os.makedirs(output_directory, exist_ok=True)

path = "/home/montoliu/40sp/ncbi-data"

for index, row in df.iterrows():
    abbreviation = row['abreviation']
    refseq = row['refseq']
    
    # Match the first {refseq}*.fasta file in the directory
    dir_path = os.path.join(path, abbreviation, "ncbi_dataset", "data", refseq)
    fasta_file = next(
        (os.path.join(dir_path, f) for f in os.listdir(dir_path) if re.match(rf"{refseq}.+\.fna$", f)),
        None
    )


        # Skip if no file is found
    if fasta_file is None or not os.path.exists(fasta_file):
        print(f"No matching file found for {refseq} in {dir_path}")
        continue
    # Create the symlink
    symlink_path = os.path.join(output_directory, f'{abbreviation}.fasta')
    
    if os.path.exists(fasta_file):
            os.symlink(fasta_file, symlink_path)

