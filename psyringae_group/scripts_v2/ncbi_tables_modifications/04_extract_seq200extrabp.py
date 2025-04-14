import pandas as pd
from Bio import SeqIO
import os
import re

# Read NCBI table in
df = pd.read_csv('final_table_of_genome_assemblies_final.csv', encoding='ascii', sep=',')

# Create a separate folder with the fasta files as symlinks
#output_directory = "/home/montoliu/psyringae_group/data/assemblies_selection_final3"
#os.makedirs(output_directory, exist_ok=True)

#for filename in df['filename']:
#    fasta_file = os.path.join('/home/montoliu/psyringae_group/data/assemblies', f'{filename}.fasta')
#    symlink_path = os.path.join(output_directory, f'{filename}.fasta')
#    if not os.path.exists(symlink_path):  # Check if symlink does not exist
#        os.symlink(fasta_file, symlink_path)


# Copy extracted sequences and change the fasta header to ps_num, so that it can be used in alignments 

# List directories
directories = ['mutT', 'mutS', 'mutY', 'mutL', 'dnaQ', 'uvrD']
path = "/home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness"
output_directory_seq = "/home/montoliu/psyringae_group/results/sequences_selection_200extrabp_new" 
os.makedirs(output_directory_seq, exist_ok=True)

for directory in directories:
    new_dir = os.path.join(output_directory_seq, directory)
    os.makedirs(new_dir, exist_ok=True)

# Iterate over filenames and corresponding numbers
for filename, num in zip(df['filename'], df['num']):
    # Print status
    print(f"Working on filename {filename}")
    
    sequence_found = False  # Flag to track if a valid sequence is found for the current filename
    
    for directory in directories:
        # Check if fasta file is in directory
        fasta_files = [file for file in os.listdir(os.path.join(path, directory)) if file.startswith(filename) and file.endswith('.fasta')]
        
        for fasta_file in fasta_files:
            # Modify fasta header and save to output directory
            fasta_path = os.path.join(path, directory, fasta_file)

            # Check if file exists and is not empty
            if os.path.isfile(fasta_path) and os.path.getsize(fasta_path) > 0:
                try:
                    # Parse each file explicitly
                    for record in SeqIO.parse(fasta_path, 'fasta'):
                        # Process each record as needed
                        record.id = f"{directory}_{num}"
                        record.description = ""
                        new_fasta_path = os.path.join(output_directory_seq, directory, f'{filename}.fasta')
                        SeqIO.write(record, new_fasta_path, 'fasta')
                        sequence_found = True
                        print(f"Processed {fasta_file} successfully")
                except Exception as e:
                    print(f"An error occurred while processing {fasta_path}: {e}")
            else:
                print(f"File {fasta_path} is missing or empty")
    
    if not sequence_found:
        print(f"No sequence found for filename {filename} in any directory")


