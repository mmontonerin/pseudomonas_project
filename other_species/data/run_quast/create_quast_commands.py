import os
import pandas as pd

# Read NCBI table
df_pbra = pd.read_csv('/home/montoliu/other_species/tables/pbra_mastertable.csv', encoding='ascii', sep=',')
df_pflu = pd.read_csv('/home/montoliu/other_species/tables/pflu_mastertable.csv', encoding='ascii', sep=',')
df_psav = pd.read_csv('/home/montoliu/other_species/tables/psav_mastertable.csv', encoding='ascii', sep=',')
df_pvir = pd.read_csv('/home/montoliu/other_species/tables/pvir_mastertable.csv', encoding='ascii', sep=',')

outdir='/home/montoliu/other_species/data/quast'
fastadir='/home/montoliu/other_species/data/genome_assemblies'
scriptdir='/home/montoliu/other_species/data/run_quast/batch_scripts'

# Number of commands per batch
batch_size = 25

# Create a list to store the commands
commands = []

# Iterate over each row in the DataFrame
for index, row in df_pbra.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pbra', f'{fasta_file}.fasta')

    # Construct the QUAST command
    quast_command = f"quast -o {outdir}/pbra/{accession} -t 8 --no-plots --no-html {fasta_path}\n"

    # Add the command to the list
    commands.append(quast_command)

# Iterate over each row in the DataFrame
for index, row in df_pflu.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pflu', f'{fasta_file}.fasta')

    # Construct the QUAST command
    quast_command = f"quast -o {outdir}/pflu/{accession} -t 8 --no-plots --no-html {fasta_path}\n"

    # Add the command to the list
    commands.append(quast_command)

# Iterate over each row in the DataFrame
for index, row in df_psav.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'psav', f'{fasta_file}.fasta')

    # Construct the QUAST command
    quast_command = f"quast -o {outdir}/psav/{accession} -t 8 --no-plots --no-html {fasta_path}\n"

    # Add the command to the list
    commands.append(quast_command)

# Iterate over each row in the DataFrame
for index, row in df_pvir.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pvir', f'{fasta_file}.fasta')

    # Construct the QUAST command
    quast_command = f"quast -o {outdir}/pvir/{accession} -t 8 --no-plots --no-html {fasta_path}\n"

    # Add the command to the list
    commands.append(quast_command)

# Write the commands to separate script files in batches of 10
for i in range(0, len(commands), batch_size):
    batch_commands = commands[i:i + batch_size]
    script_filename = f"{scriptdir}/quast_commands_batch_{i // batch_size + 1}.sh"
    
    with open(script_filename, 'w') as f:
        f.writelines(batch_commands)
