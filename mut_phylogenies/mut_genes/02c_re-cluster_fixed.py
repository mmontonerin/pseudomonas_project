import os
from Bio import SeqIO
import pandas as pd
import re
import sys

def find_unique_protein_clusters(mut_genes, input_directory, output_directory):
    
    for gene in mut_genes:
        fasta_file = os.path.join(input_directory, f"{gene}_fixed.fasta")
        output_fasta = os.path.join(output_directory, f"{gene}_fixed_clusters.fasta")

        # Dictionary to store sequences and their corresponding names
        sequences = {}

        print(f"Processing FASTA file for {gene}...")

        for record in SeqIO.parse(fasta_file, "fasta"):
            seq = str(record.seq)
            record_id = record.id.strip()
            
            if seq not in sequences:
                # Store the first occurrence of the sequence with its original name
                sequences[seq] = [record_id]
            else:
                # Append additional sequence names to the existing one
                sequences[seq].append(record_id)
        
        # Write unique sequences to a new FASTA file 
        with open(output_fasta, "w") as out_fasta:
            for seq, names in sequences.items():
                # If more than one name, join them with "|"
                cluster_name = "|".join(names)
                out_fasta.write(f">{cluster_name}\n{seq}\n")

# Example usage
mut_genes = ["mutS", "mutT"]
input_directory = "/home/montoliu/mut_phylogenies/mut_genes/alignments"
output_directory = "/home/montoliu/mut_phylogenies/mut_genes/alignments"

find_unique_protein_clusters(mut_genes, input_directory, output_directory)