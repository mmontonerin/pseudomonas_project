import pandas as pd
from Bio import SeqIO
import os

def find_master_seq(mut_genes, csv_file, output_file, prefix):

    # Input the CSV file
    df = pd.read_csv(csv_file)

    # Find the most frequent cluster for each gene
    results = []
    for gene in df.columns[1:-1]:  # Skip BioProject and count columns
        most_common_cluster = df[gene].value_counts().idxmax()
        most_common_count = df[gene].value_counts().max()
        results.append([gene, most_common_cluster, most_common_count])

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(results, columns=["Gene", "Most_Common_Cluster", "Count"])

    # Print results
    for gene, cluster, count in results:
        print(f"Master sequence for {prefix} - {gene}: {cluster} ({count} copies)")

    # Save results to a text file
    with open(output_file, 'w') as f:
        for gene, cluster, count in results:  # Use list iteration instead of .items()
            f.write(f"Master sequence for {prefix} - {gene}: {cluster} ({count} copies)\n")

    print(f"Results saved to {output_file}")

    # Extract corresponding sequences from the FASTA file for each gene
    for gene, cluster, _ in results:
        for mut_gene in mut_genes:
            extract_sequences(prefix, mut_gene, cluster)

def extract_sequences(prefix, mut_gene, cluster):
    # Define the FASTA file dynamically based on the prefix and mut_gene
    fasta_file = f"/home/montoliu/truncated_sequences/aa/{prefix}/clusters/{mut_gene}_clusters.fasta"

    # Check if the FASTA file exists
    if not os.path.exists(fasta_file):
        return

    # Define the output folder and create it if it doesn't exist
    output_folder = f"/home/montoliu/truncated_sequences/aa/{prefix}/master_seq"
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a separate FASTA file for each prefix and gene
    output_fasta_file = os.path.join(output_folder, f"{prefix}_{mut_gene}_master_sequence.fasta")
    
    # Open the output FASTA file for writing
    with open(output_fasta_file, 'w') as fasta_out:
        found = False  # Flag to track if the first matching sequence has been found
        for record in SeqIO.parse(fasta_file, "fasta"):
            # Compare the record.id with the cluster
            if record.id == cluster:
                # Write the first matching sequence to the output file
                found = True
                fasta_out.write(f">{record.id}\n{record.seq}\n")
                break  # Stop after the first match

        if found:
            print(f"Master sequence for {prefix} - {mut_gene} (cluster {cluster}) saved to {output_fasta_file}")

# Define prefixes and genes
prefixes = ["pbra", "psav", "pflu", "pvir", "psyr", "ppro"]
mut_genes = ["mutS", "mutT", "mutY", "mutL", "dnaQ", "uvrD"]

# Process each prefix
for prefix in prefixes:
    csv_file = f"grouped_occurrences_{prefix}.csv"
    output_file = f"{prefix}_master_sequences.txt"
    find_master_seq(mut_genes,csv_file, output_file, prefix)
