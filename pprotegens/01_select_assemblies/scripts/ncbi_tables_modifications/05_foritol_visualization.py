import pandas as pd
from Bio import SeqIO
import os
import re

import pandas as pd

# Read the original CSV file
df = pd.read_csv('final_table_of_genome_assemblies_4.csv', encoding='ascii', sep=',')

# Define a function to add prefix "ppro" to a value
def add_prefix(value):
    return "ppro" + str(value)

# Apply the function to the specified column
df['num'] = df['num'].apply(add_prefix)

# Divide 'Total_length' column by 1000000
df['Total_length'] = df['Total_length'] / 1000000

# Select the columns you want to keep
selected_columns = ['num', 'Total_length', '#Contigs', 'BUSCO-C']

# Create a new DataFrame with only the selected columns
new_df = df[selected_columns]

# Write the selected columns to a new CSV file
new_df.to_csv('for_itol_visualization.csv', index=False, header=False)



