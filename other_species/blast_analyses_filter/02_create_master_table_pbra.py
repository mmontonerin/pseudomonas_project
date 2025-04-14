import pandas as pd
from Bio import SeqIO
import os
import re

"""
# Read NCBI table in
df_ncbi = pd.read_csv('pbra.csv', encoding='ascii', sep=',')
"""
# Read filenames table, final table to be built from here
df_fn = pd.read_csv('pbra_master_table_clusters.csv', dtype={'num': str})
"""
# Number genome assembly files.
# To be used for alignment methods that require very short names
# We add zero padding so that we always have the same number of digits
ending_number = len(df_fn)
df_fn.insert(0, 'num', [str(i).zfill(4) for i in range(1, ending_number + 1)])


# Add BioProject and BioProject accession numbers

# Extract accession from 'filename' column
# Grab the part of filename that matches the Assembly Accession number
# So that GCA_000007805.1_ASM780v1_genomic matches with GCA_000007805.1

# We divide the string in sections separated by '_'
# We merge the first two sections again to obtain GCA_000007805.1 from the GCA and 000007805.1 splits
df_fn['Accession'] = df_fn['filename'].str.split('_').apply(lambda x: '_'.join(x[:2]))

# Create a dictionary to map accession numbers to the corresponding values in df_ncbi
accession_to_values = df_ncbi.set_index('Assembly Accession').to_dict(orient='index')

######## BioProject

# Process to add the column with the BioProject accession number
column_bioproject_ncbi = 'Assembly BioProject Accession'
column_bioproject = 'BioProject'
df_fn[column_bioproject] = df_fn['Accession'].apply(lambda x: accession_to_values[x][column_bioproject_ncbi] if x in accession_to_values else None)

####### BioSample

# Process to add the column with the BioSample accession number
column_biosample_ncbi = 'Assembly BioSample Accession'
column_biosample = 'BioSample'
df_fn[column_biosample] = df_fn['Accession'].apply(lambda x: accession_to_values[x][column_biosample_ncbi] if x in accession_to_values else None)

######## Organism Name

# Add column for Organism Name
column_organism_ncbi = 'Organism Name'
column_organism = 'Organism'
df_fn[column_organism] = df_fn['Accession'].apply(lambda x: accession_to_values[x][column_organism_ncbi].replace(' ', '_') if x in accession_to_values else None)

####### Strain ID
column_strain = 'Strain'
column_strain_ncbi = 'Organism Infraspecific Names Strain'
column_isolate_ncbi = 'Organism Infraspecific Names Isolate'
column_ecotype_ncbi = 'Organism Infraspecific Names Ecotype'

# Strain IDs can be in multiple columns, we take it from the non-empty ones.
# If in multiple columns, separate them with dash ('-')
# If IDs contain spaces, replace them with underscores ('_') 

# Function to extract strain IDs
def extract_strain(row):
    accession = row['Accession']
    if accession in accession_to_values:
        strain_parts = []

        for col in [column_strain_ncbi, column_isolate_ncbi, column_ecotype_ncbi]:
            strain = accession_to_values[accession].get(col)
            if pd.notna(strain):
                # Remove spaces and replace with underscores
                strain = strain.replace(' ', '_')
                strain_parts.append(strain)

        # Join strain parts with dashes
        return '-'.join(strain_parts) if strain_parts else None
    else:
        return None

# Add 'Strain' column to df_fn
df_fn[column_strain] = df_fn.apply(extract_strain, axis=1)
"""


####### Mut Gene information

# Function to extract sequence length if single copy
# Add information if gene contains Ns inside to print the sequence length + N
# or fragmented:length-length-...
# or missing

# Function to extract sequence length from FASTA file and check for Ns
def extract_sequence_length(filename, main_directory, other_directory):
    # Check if the sequence is found in the main FASTA directory
    fasta_files = [f for f in os.listdir(main_directory) if f.startswith(filename)]
    if fasta_files:
        # Construct the path to the first matching FASTA file in the main directory
        fasta_file = os.path.join(main_directory, fasta_files[0])
        # Parse the FASTA file and calculate sequence length
        with open(fasta_file) as handle:
            record = SeqIO.read(handle, 'fasta')
            sequence = str(record.seq)
            sequence_length = len(sequence)
            if 'N' in sequence.upper():
                print(f"Sequence {filename} contains Ns.")
                sequence_length_str = f"{sequence_length}N"
            else:
                sequence_length_str = str(sequence_length)
        return sequence_length_str
    else:
        # Check if the sequence is found in the other directory
        other_files = [f for f in os.listdir(other_directory) if f.startswith(filename)]
        if other_files:
            lengths_other = []  # Store sequence lengths from other directory
            for other_file in other_files:
                # Construct the path to each matching FASTA file in the other directory
                other_file_path = os.path.join(other_directory, other_file)
                # Parse the FASTA file and calculate sequence lengths
                with open(other_file_path) as handle:
                    for record in SeqIO.parse(handle, 'fasta'):
                        sequence = str(record.seq)
                        sequence_length = len(sequence)
                        if 'N' in sequence.upper():
                            print(f"Sequence {filename} contains Ns.")
                            sequence_length_str = f"fragmented:{sequence_length}N"
                        else:
                            lengths_other.append(sequence_length)
            # If there are lengths from other files, convert lengths to string and join with underscores
            if lengths_other:
                lengths_other_str = '_'.join(map(str, lengths_other))
                #print(f"Debug: lengths_other = {lengths_other}")  # Print list before joining
                #print(f"Debug: lengths_other_str = {lengths_other_str}")  # Check final string
                sequence_length_str = f"fragmented:{lengths_other_str}"
            else:
                sequence_length_str = 'missing'
            return sequence_length_str
        else:
            return 'missing'

# Define directories
dirs = {   
    'mutS': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/mutS', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/mutS'),
    'mutT': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/mutT', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/mutT'),
    'mutY': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/mutY', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/mutY'),
    'mutL': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/mutL', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/mutL'),
    'dnaQ': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/dnaQ', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/dnaQ'),
    'uvrD': ('/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/uvrD', '/home/montoliu/other_species/blast_analyses_filter/mut_sequences/pbra/fragmented/uvrD')
}

# Apply the function to create gene columns
for gene, (main_dir, other_dir) in dirs.items():
    df_fn[gene] = df_fn['filename'].apply(extract_sequence_length, args=(main_dir, other_dir))


"""
####### Assembly stats

#quast directory
quast_directory = '/home/montoliu/other_species/data/quast/pbra/stats_all'

def extract_assembly_stats(filename, qstat):
    report = os.path.join(quast_directory, f"{filename}.csv")
    if os.path.exists(report):
        # Read quast report table in
        df_quast = pd.read_csv(report, encoding='ascii', sep=',')
        #print(df_quast)
        # Create a dictionary to map filenames to the corresponding values in df_fn
        stat = df_quast.at[0, qstat]
        return stat
	
    else:
        None

# Define column names
quast_stats = {
    '#Contigs': '# contigs',
    'Total_length': 'Total length',
    'GC(%)': 'GC (%)',
    'N50': 'N50',
    'N75': 'N75',
    'L50': 'L50',
    'L75': 'L75',
    'Ns/100kb': "# N's per 100 kbp"   
}

for qstat, (quastdb_stat) in quast_stats.items():
    #print(quastdb_stat)
    df_fn[qstat] = df_fn['Accession'].apply(extract_assembly_stats, qstat=quastdb_stat)


####### BUSCO summary

busco_directory = '/home/montoliu/other_species/data/busco/pbra'

def extract_busco_results(filename, busco_stat):
    busco_results_file = os.path.join(busco_directory, filename, f"short_summary.specific.pseudomonadales_odb10.{filename}.txt")     
    if os.path.exists(busco_results_file):
        with open(busco_results_file, 'r') as file:
            for line in file:
                match = re.search(r'C:(\d+\.\d+)%\[S:(\d+\.\d+)%,D:(\d+\.\d+)%\],F:(\d+\.\d+)%,M:(\d+\.\d+)%,n:(\d+)', line)
                if match:
                    c_value = float(match.group(1))
                    s_value = float(match.group(2))
                    d_value = float(match.group(3))
                    f_value = float(match.group(4))
                    m_value = float(match.group(5))
                    n_value = int(match.group(6))
                    if busco_stat == 'BUSCO-C':
                        return c_value
                    elif busco_stat == 'BUSCO-C(S)':
                        return s_value
                    elif busco_stat == 'BUSCO-C(D)':
                        return d_value
                    elif busco_stat == 'BUSCO-F':
                        return f_value
                    elif busco_stat == 'BUSCO-M':
                        return m_value
                    elif busco_stat == 'BUSCO-#_genes':
                        return n_value
    return None

# Define column names
busco_stats = ['BUSCO-C', 'BUSCO-C(S)', 'BUSCO-C(D)', 'BUSCO-F', 'BUSCO-M', 'BUSCO-#_genes']

# Apply the function to create BUSCO stats columns
for busco_stat in busco_stats:
    df_fn[busco_stat] = df_fn['Accession'].apply(extract_busco_results, busco_stat=busco_stat)
"""

# Write the DataFrame to a new CSV file
df_fn.to_csv('pbra_mastertable_fragmented_check.csv', index=False)

#print(df_fn)
#print(df_ncbi)