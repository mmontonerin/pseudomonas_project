import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = 'ppro_master_table_clusters.csv'
df = pd.read_csv(file_path, dtype={'num': str})

# Select the columns of interest
group_columns = [
    'BioProject', 'dnaQ_cluster', 'mutL_cluster', 'mutS_cluster', 
    'mutT_cluster', 'mutY_cluster', 'uvrD_cluster'
]

# Group by the specified columns and count the occurrences of each group
grouped = df.groupby(group_columns).size().reset_index(name='count')

# Get the number of unique occurrences
unique_occurrences = len(grouped)

# Print the result
print(f"Number of unique occurrences: {unique_occurrences}")
print("\nDetails of occurrences:")
print(grouped)

# Save the grouped DataFrame as a new CSV file
output_file = 'grouped_occurrences.csv'
grouped.to_csv(output_file, index=False)

print(f"\nThe grouped data has been saved to {output_file}.")
