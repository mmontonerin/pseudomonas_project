from Bio import SeqIO
import pandas as pd
import re
import sys

sys.stdout = open('debug_output.txt', 'w')

def find_unique_protein_clusters(mut_genes, input_directory, output_directory, csv_file, output_csv):
    # Read the CSV file
    print("Processing CSV file...")
    df = pd.read_csv(csv_file, dtype={'num': str})  # Ensure 'num' is read as a string
    
    for gene in mut_genes:
        fasta_file = f"{input_directory}/{gene}_id.fasta"
        output_fasta = f"{output_directory}/{gene}_clusters.fasta"

        # Dictionary to hold unique sequences and their clusters
        sequences = {}
        cluster_counter = 1
        sequence_to_cluster = {}
        
        print(f"Processing FASTA file for {gene}...")
        for record in SeqIO.parse(fasta_file, "fasta"):
            seq = str(record.seq)
            record_id = record.id.strip()
            
            # Assign a cluster to the sequence if it’s unique
            if seq not in sequences:
                cluster_name = f"cluster{cluster_counter}"
                sequences[seq] = cluster_name
                cluster_counter += 1
            
            # Map the sequence to the cluster
            cluster_name = sequences[seq]
            if record_id not in sequence_to_cluster:
                sequence_to_cluster[record_id] = []
            sequence_to_cluster[record_id].append(cluster_name)
        
        # Write unique sequences to a new FASTA file 
        with open(output_fasta, "w") as out_fasta:
            for seq, cluster in sequences.items():
                out_fasta.write(f">{cluster}\n{seq}\n")
        
        # Add gene_cluster column to DataFrame
        def find_cluster(name):
            clusters = sequence_to_cluster.get(name, [])
            return clusters[0] if clusters else "none"
        
        column_name = f"{gene}_cluster"
        df[column_name] = df['psg_num'].apply(find_cluster)
        
        # Debugging: Check for unmatched IDs
        unmatched = [num for num in df['psg_num'] if num not in sequence_to_cluster]
        print(f"\nUnmatched IDs in {gene} CSV:", unmatched)
        
        print(f"Unique sequences saved to {output_fasta}")
    
    # Save updated CSV
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")

# Example usage
mut_genes = ["mutS", "mutT", "mutY", "mutL", "dnaQ", "uvrD"]
input_directory = "/home/montoliu/psyringae_group/mut_genes/protein_analysis/alignments"
output_directory = "/home/montoliu/psyringae_group/mut_genes/protein_analysis/alignments/clusters"
csv_file = "final_table_of_genome_assemblies_final_psgnum.csv"
output_csv = "psyr_master_table_clusters.csv"

find_unique_protein_clusters(mut_genes, input_directory, output_directory, csv_file, output_csv)