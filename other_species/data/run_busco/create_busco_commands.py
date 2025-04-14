import os
import pandas as pd

# Read NCBI table
df_pbra = pd.read_csv('/home/montoliu/other_species/tables/pbra_mastertable.csv', encoding='ascii', sep=',')
df_pflu = pd.read_csv('/home/montoliu/other_species/tables/pflu_mastertable.csv', encoding='ascii', sep=',')
df_psav = pd.read_csv('/home/montoliu/other_species/tables/psav_mastertable.csv', encoding='ascii', sep=',')
df_pvir = pd.read_csv('/home/montoliu/other_species/tables/pvir_mastertable.csv', encoding='ascii', sep=',')

outdir='/home/montoliu/other_species/data/busco'
fastadir='/home/montoliu/other_species/data/genome_assemblies'
scriptdir='/home/montoliu/other_species/data/run_busco/batch_scripts'

busco_database='/home/montoliu/psyringae_group/data/busco_tests/run_sep_annotations/busco_downloads'
lineage='/home/montoliu/psyringae_group/data/busco_tests/run_sep_annotations/busco_downloads/lineages/pseudomonadales_odb10'

# Number of commands per batch
batch_size = 10

# Create a list to store the commands
commands = []

# Iterate over each row in the DataFrame
for index, row in df_pbra.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pbra', f'{fasta_file}.fasta')

    # Construct the BUSCO command
    busco_command = f"busco -i {fasta_path} -m genome -l {lineage} -c 8 --out_path {outdir}/pbra -o {accession} --offline --download_path {busco_database}\n"

    # Add the command to the list
    commands.append(busco_command)

# Iterate over each row in the DataFrame
for index, row in df_pflu.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pflu', f'{fasta_file}.fasta')

    # Construct the BUSCO command
    busco_command = f"busco -i {fasta_path} -m genome -l {lineage} -c 8 --out_path {outdir}/pflu -o {accession} --offline --download_path {busco_database}\n"

    # Add the command to the list
    commands.append(busco_command)

# Iterate over each row in the DataFrame
for index, row in df_psav.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'psav', f'{fasta_file}.fasta')

    # Construct the BUSCO command
    busco_command = f"busco -i {fasta_path} -m genome -l {lineage} -c 8 --out_path {outdir}/psav -o {accession} --offline --download_path {busco_database}\n"

    # Add the command to the list
    commands.append(busco_command)

# Iterate over each row in the DataFrame
for index, row in df_pvir.iterrows():
    accession = row['Accession']
    fasta_file = row['filename']

    fasta_path = os.path.join(f'{fastadir}', 'pvir', f'{fasta_file}.fasta')

    # Construct the BUSCO command
    busco_command = f"busco -i {fasta_path} -m genome -l {lineage} -c 8 --out_path {outdir}/pvir -o {accession} --offline --download_path {busco_database}\n"

    # Add the command to the list
    commands.append(busco_command)

# Write the commands to separate script files in batches of 10
for i in range(0, len(commands), batch_size):
    batch_commands = commands[i:i + batch_size]
    script_filename = f"{scriptdir}/busco_commands_batch_{i // batch_size + 1}.sh"
    
    with open(script_filename, 'w') as f:
        f.writelines(batch_commands)
