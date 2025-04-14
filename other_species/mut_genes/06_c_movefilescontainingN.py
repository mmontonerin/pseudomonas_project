import os
import shutil
import re
import pandas as pd

def move_files_based_on_existing_files(input_base_dir, output_base_dir, prefixes, mut_genes, file_extension, input_csv_files):
    """
    Move sequence files based on existing files in the 'removed' folder and update CSVs.

    Args:
        input_base_dir (str): Base directory containing the prefix/mutation subfolders.
        output_base_dir (str): Directory to move files with 'N' or 'n'.
        prefixes (list): List of folder prefixes to iterate over (e.g., ['pbra', 'pflu']).
        mut_genes (list): List of mut genes subfolders to iterate over (e.g., ['mutS', 'mutT']).
        file_extension (str): File extension to process (e.g., '.fasta').
        input_csv_files (dict): Dictionary of input CSV file paths, keyed by prefix.
    """
    # Dictionary to store the accessions that need to be moved, keyed by prefix
    accessions_to_move = {prefix: set() for prefix in prefixes}

    # Process each prefix's CSV file
    for prefix in prefixes:
        # Read the input CSV for the prefix
        csv_file = input_csv_files.get(prefix)
        if not csv_file or not os.path.exists(csv_file):
            print(f"Skipping non-existent or missing CSV file: {csv_file}")
            continue

        # Load the CSV into a pandas DataFrame
        df = pd.read_csv(csv_file, dtype={'num': str})  # Ensure 'num' column is read as string

        # Prepare a DataFrame for sequences without 'N'
        df_no_ns = df.copy()

        for mut in mut_genes:
            folder_path = os.path.join(input_base_dir, prefix, mut)
            if not os.path.exists(folder_path):
                print(f"Skipping non-existent folder: {folder_path}")
                continue

            for file in os.listdir(folder_path):
                if file.endswith(file_extension):
                    file_path = os.path.join(folder_path, file)

                    # Extract the Accession from the CSV row
                    for _, row in df.iterrows():
                        accession = row['Accession']
                        
                        # Check if the file starts with the accession (even with extra characters like _2)
                        if file.startswith(accession) and file.endswith(file_extension):
                            # Check if the file exists in the 'removed' folder
                            removed_file_path = os.path.join(output_base_dir, prefix, mut, file)
                            if os.path.exists(removed_file_path):
                                # If the file is in the 'removed' folder, add it to the accessions to move
                                accessions_to_move[prefix].add(accession)

                                # Remove the row from df_no_ns (as this sequence should be removed)
                                df_no_ns = df_no_ns[df_no_ns['Accession'] != accession]

        # Save the new CSV file for sequences without 'N' (remaining sequences)
        df_no_ns.to_csv(f'{prefix}_sequences_without_Ns.csv', index=False)

    # Now move all files with the same accession across other folders (even if they were not previously in the 'Ns' folder)
    for prefix in prefixes:
        for mut in mut_genes:
            folder_path = os.path.join(input_base_dir, prefix, mut)
            if not os.path.exists(folder_path):
                continue

            for file in os.listdir(folder_path):
                if file.endswith(file_extension):
                    file_path = os.path.join(folder_path, file)

                    # Extract the Accession from the file name and check against accessions_to_move
                    for accession in accessions_to_move[prefix]:
                        # Check if the file starts with the accession (even with extra characters like _2)
                        if file.startswith(accession) and file.endswith(file_extension):
                            destination_folder = os.path.join(output_base_dir, prefix, mut)
                            os.makedirs(destination_folder, exist_ok=True)

                            new_file_path = os.path.join(destination_folder, file)
                            try:
                                shutil.move(file_path, new_file_path)
                                print(f"Moved file: {file_path} -> {new_file_path}")
                            except Exception as e:
                                print(f"Error moving file {file_path}: {e}")


# Data and files
input_directory = "/home/montoliu/other_species/mut_genes/mut_sequences_nt"
output_directory = "/home/montoliu/other_species/mut_genes/mut_sequences_nt/removed"
prefixes = ["pbra", "pflu", "psav", "pvir"]
mut_genes = ["mutS", "mutT", "mutY", "mutL", "dnaQ", "uvrD"]
file_ext = ".fasta"

# Map each prefix to its corresponding CSV file
input_csv_files = {
    'pbra': "/home/montoliu/other_species/mut_genes/pbra_mastertable_final.csv",
    'pflu': "/home/montoliu/other_species/mut_genes/pflu_mastertable_final.csv",
    'psav': "/home/montoliu/other_species/mut_genes/psav_mastertable_final.csv",
    'pvir': "/home/montoliu/other_species/mut_genes/pvir_mastertable_final.csv"
}

move_files_based_on_existing_files(input_directory, output_directory, prefixes, mut_genes, file_ext, input_csv_files)