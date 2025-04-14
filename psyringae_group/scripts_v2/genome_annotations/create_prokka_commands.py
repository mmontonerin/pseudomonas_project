import os
import pandas as pd

# Read NCBI table
df = pd.read_csv('/home/montoliu/psyringae_group/scripts_v2/ncbi_tables_modifications/final_table_missing_annotations.csv', encoding='ascii', sep=',')

path='/home/montoliu/psyringae_group/data/proteins_new_annotations'

# Number of commands per batch
batch_size = 50

# Create a list to store the commands
commands = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    outdir = os.path.join(f'{path}', 'genome_annotations', f'{accession}')
    fasta_path = os.path.join(f'{path}', 'genome_assemblies_to_annotate', f'{fasta_file}.fasta')    

    # Construct the Prokka command
    prokka_command = f"prokka --proteins {path}/ref_proteins/reference_proteins.faa --cpus 8 --outdir {outdir} --prefix {accession} {fasta_path}\n"
    
    # Add the command to the list
    commands.append(prokka_command)

# Write the commands to separate script files in batches of 50
for i in range(0, len(commands), batch_size):
    batch_commands = commands[i:i + batch_size]
    script_filename = f"/home/montoliu/psyringae_group/scripts_v2/genome_annotations/batch_scripts/prokka_commands_batch_{i // batch_size + 1}.sh"
    
    with open(script_filename, 'w') as f:
        f.writelines(batch_commands)
