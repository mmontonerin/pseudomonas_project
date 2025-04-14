import os
import pandas as pd

# Read NCBI table
df = pd.read_csv('/home/montoliu/pprotegens/01_select_assemblies/scripts/ncbi_tables_modifications/final_table_of_genome_assemblies_4.csv', encoding='ascii', sep=',')

outdir='/home/montoliu/pprotegens/data/genome_annotations'
fastadir='/home/montoliu/pprotegens/data/assemblies_selection_final2'

# Number of commands per batch
batch_size = 25

# Create a list to store the commands
commands = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', f'{fasta_file}.fasta')

    # Construct the Prokka command
    prokka_command = f"prokka --cpus 8 --outdir {outdir}/{accession} --prefix {accession} {fasta_path}\n"
    
    # Add the command to the list
    commands.append(prokka_command)

# Write the commands to separate script files in batches of 50
for i in range(0, len(commands), batch_size):
    batch_commands = commands[i:i + batch_size]
    script_filename = f"/home/montoliu/pprotegens/01_select_assemblies/scripts/genome_annotation/batch_scripts/prokka_commands_batch_{i // batch_size + 1}.sh"
    
    with open(script_filename, 'w') as f:
        f.writelines(batch_commands)
