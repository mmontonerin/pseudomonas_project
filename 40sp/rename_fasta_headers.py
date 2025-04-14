import pandas as pd
from Bio import SeqIO
import os
import re
import argparse

# Read NCBI table in
df = pd.read_csv('40_species.csv', encoding='ascii', sep=',')

def rename_fasta_headers(input_directory, output_directory):
    for filename in df['abreviation']:
        fasta_files = [file for file in os.listdir(input_directory) if file.startswith(filename) and file.endswith('.faa')]
        for fasta_file in fasta_files:
            fasta_path = os.path.join(input_directory, fasta_file)
            records = list(SeqIO.parse(fasta_path, 'fasta'))
            new_records = []
            for record in records:
                record.id = f"{filename}_{record.id}"
                record.description = ""
                new_records.append(record)
            new_fasta_path = os.path.join(output_directory, f'{filename}.faa')
            SeqIO.write(new_records, new_fasta_path, 'fasta')

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Provide input directory of fasta files and output directory for files with renamed fasta headers")
    parser.add_argument("-in","--input_directory", help="Path to the directory containing input files")
    parser.add_argument("-out","--output_directory", help="Path to the directory for output files")
    args = parser.parse_args()

    # Call the filter_table function with the input file path
    rename_fasta_headers(args.input_directory,args.output_directory)