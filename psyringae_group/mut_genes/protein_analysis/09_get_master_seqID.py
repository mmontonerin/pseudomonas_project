import pandas as pd

# Input the CSV file
input_file = "/home/montoliu/psyringae_group/mut_genes/protein_analysis/psyr_grouped_occurrences.csv"  # Replace with your file path
df = pd.read_csv(input_file)

# Find the most frequent cluster for each gene
results = {}
for gene in df.columns[1:-1]:  # Skip BioProject and count columns
    most_common_cluster = df[gene].value_counts().idxmax()
    most_common_count = df[gene].value_counts().max()
    results[gene] = (most_common_cluster, most_common_count)

# Print results
for gene, (cluster, count) in results.items():
    print(f"Master sequence for {gene}: {cluster} ({count} copies)")