import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('/home/montoliu/psyringae_group/scripts_v2/ncbi_tables_modifications/final_table_of_genome_assemblies_final_num.csv', encoding='ascii', sep=',')

#Create a table to parse through assemblies that contained faa files
has_faa_files =[]

for Accession in df['Accession']:
    fasta_file = os.path.join('/home/montoliu/psyringae_group/data/proteins', f'{Accession}.faa')
    if os.path.exists(fasta_file):  # Check if fasta file exists
        has_faa_files.append(df[df['Accession'] == Accession])


# Create a DataFrame from the missing_files list
has_faa_files_df = pd.concat(has_faa_files)

# Save the missing files DataFrame to a new CSV
has_faa_files_df.to_csv('ncbi_assemblies_with_annotations.csv', index=False, encoding='ascii', sep=',') 