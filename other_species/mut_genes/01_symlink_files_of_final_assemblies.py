import pandas as pd
from Bio import SeqIO
import os
import re
import argparse


def symlink_faa_files(input_file, output_prefix):
    # Read NCBI table in
    df = pd.read_csv(input_file, encoding='ascii', sep=',', dtype={'num': str})

    # Create a separate folder with the fasta files as symlinks
    faa_output_directory = os.path.join('/home/montoliu/other_species/mut_genes/faa_files', output_prefix)
    os.makedirs(faa_output_directory, exist_ok=True)

    for filename in df['Accession']:
        faa_file = os.path.join('/home/montoliu/other_species/data/genome_annotation/genome_annotations', output_prefix, filename, f'{filename}.faa')
        symlink_path = os.path.join(faa_output_directory, f'{filename}.faa')
        if not os.path.exists(symlink_path):  # Check if symlink does not exist
            os.symlink(faa_file, symlink_path)


def symlink_ffn_files(input_file, output_prefix):
    # Read NCBI table in
    df = pd.read_csv(input_file, encoding='ascii', sep=',', dtype={'num': str})

    # Create a separate folder with the fasta files as symlinks
    ffn_output_directory = os.path.join('/home/montoliu/other_species/mut_genes/ffn_files', output_prefix)
    os.makedirs(ffn_output_directory, exist_ok=True)

    for filename in df['Accession']:
        ffn_file = os.path.join('/home/montoliu/other_species/data/genome_annotation/genome_annotations', output_prefix, filename, f'{filename}.ffn')
        symlink_path = os.path.join(ffn_output_directory, f'{filename}.ffn')
        if not os.path.exists(symlink_path):  # Check if symlink does not exist
            os.symlink(ffn_file, symlink_path)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Select and symlink protein files based on presence on final master table")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input table file")
    parser.add_argument("-o", "--output_prefix", required=True, help="prefix of the output files")
    args = parser.parse_args()

    # Call the filter_table function with the input and output file paths
    symlink_faa_files(args.input_file, args.output_prefix)
    symlink_ffn_files(args.input_file, args.output_prefix)