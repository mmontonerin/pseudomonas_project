import os
import shutil
from Bio import SeqIO

def move_files_with_ns(input_base_dir, output_base_dir, prefixes, mutations, file_extension):
    """
    Iterate through folders with specified prefixes and mutations, moving sequence files containing 'N' or 'n'.

    Args:
        input_base_dir (str): Base directory containing the prefix/mutation subfolders.
        output_base_dir (str): Directory to move files with 'N' or 'n'.
        prefixes (list): List of folder prefixes to iterate over (e.g., ['pbra', 'pflu']).
        mut_genes (list): List of mut genes subfolders to iterate over (e.g., ['mutS', 'mutT']).
        file_extension (str): File extension to process (e.g., '.fasta').
    """
    for prefix in prefixes:
        for mut in mut_genes:
            folder_path = os.path.join(input_base_dir, prefix, mut)
            if not os.path.exists(folder_path):
                print(f"Skipping non-existent folder: {folder_path}")
                continue

            for file in os.listdir(folder_path):
                if file.endswith(file_extension):
                    file_path = os.path.join(folder_path, file)

                    # Check if any sequence in the file contains 'N' or 'n'
                    contains_n = False
                    for record in SeqIO.parse(file_path, "fasta"):
                        if 'N' in record.seq.upper():
                            contains_n = True
                            break

                    # Move the file if it contains sequences with 'N' or 'n'
                    if contains_n:
                        destination_folder = os.path.join(output_base_dir, prefix, mut)
                        os.makedirs(destination_folder, exist_ok=True)

                        new_file_path = os.path.join(destination_folder, file)
                        try:
                            shutil.move(file_path, new_file_path)
                            print(f"Moved file: {file_path} -> {new_file_path}")
                        except Exception as e:
                            print(f"Error moving file {file_path}: {e}")

# Example usage
input_directory = "/home/montoliu/other_species/mut_genes/mut_sequences_nt"
output_directory = "/home/montoliu/other_species/mut_genes/mut_sequences_nt/removed"
prefixes = ["pbra", "pflu", "psav", "pvir"]
mut_genes = ["mutS", "mutT", "mutY", "mutL", "dnaQ", "uvrD"]
file_ext = ".fasta"

move_files_with_ns(input_directory, output_directory, prefixes, mut_genes, file_ext)
