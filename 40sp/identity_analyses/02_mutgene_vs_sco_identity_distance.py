import os
import csv
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from itertools import combinations
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_csv_mapping(csv_file):
    """Load CSV file and return mappings for abbreviations to orders and species."""
    abbr_to_species = {}
    abbr_to_order = {}

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species_name = " ".join(row["Species"].split("_")[:2])
            abbr_to_species[row["abreviation"]] = species_name
            abbr_to_order[row["abreviation"]] = row["Order"]

    return abbr_to_species, abbr_to_order

def color_by_order(order):
    """Return a color based on the order."""
    order_colors = {
        "Enterobacteriaceae": "#3dbbb8",
        "Gammaproteobacteria": "#8b64d1",
        "Betaproteobacteria": "#c55ea0",
        "Alphaproteobacteria": "#7487c8",
        "Outgroups": "black",
        "Mixed": "lightgray",
    }
    return order_colors.get(order, "black")

def calculate_pairwise_identity(alignment):
    """
    Calculate pairwise identity for all sequence combinations in an alignment.
    Returns a dict: {(species1, species2): identity}
    """
    records = list(alignment)
    pairwise_identities = {}
    for rec1, rec2 in combinations(records, 2):
        id1, id2 = sorted([rec1.id, rec2.id])
        matches = sum(a == b for a, b in zip(rec1.seq, rec2.seq) if a != '-' and b != '-')
        length = sum((a != '-' and b != '-') for a, b in zip(rec1.seq, rec2.seq))
        identity = matches / length if length else 0
        pairwise_identities[(id1, id2)] = identity
    return pairwise_identities

def parse_alignment(file_path):
    return AlignIO.read(file_path, "fasta")

def build_dataframe(core_dict, gene_dicts, abbr_to_order):
    data = []
    for pair, core_ident in core_dict.items():
        sp1, sp2 = pair
        order1 = abbr_to_order.get(sp1)
        order2 = abbr_to_order.get(sp2)
        shared_order = order1 if order1 == order2 else "Mixed"

        row = {
            'Species1': sp1,
            'Species2': sp2,
            'Core_Distance': 1 - core_ident,
            'Order': shared_order  # used for coloring
        }
        for gene, g_dict in gene_dicts.items():
            row[f"{gene}_Identity"] = g_dict.get(pair)
        data.append(row)
    return pd.DataFrame(data)

def plot_identity_vs_distance_colored(df, output_prefix="identity_vs_core_distance_coloredbyorder"):
    # Melt the DataFrame
    df_melt = df.melt(
        id_vars=['Core_Distance', 'Order'],
        value_vars=[col for col in df.columns if col.endswith('_Identity')],
        var_name='Gene', value_name='Identity'
    )

    # Fixed color mapping
    order_palette = {
        "Enterobacteriaceae": "#3dbbb8",
        "Gammaproteobacteria": "#8b64d1",
        "Betaproteobacteria": "#c55ea0",
        "Alphaproteobacteria": "#7487c8",
        "Outgroups": "black",
        "Mixed": "lightgray",
    }

    plt.figure(figsize=(12, 7))
    scatter = sns.scatterplot(
        data=df_melt,
        x='Core_Distance', y='Identity',
        hue='Order', style='Gene',
        palette=order_palette,
        alpha=0.8, s=40, edgecolor=None
    )

    # Optional: Add average trend lines per gene
    for gene in df_melt['Gene'].unique():
        sns.lineplot(
            data=df_melt[df_melt['Gene'] == gene],
            x='Core_Distance', y='Identity',
            label=f"{gene} trend", lw=1.5
        )

    plt.title("Gene Identity vs. Core Genome Distance (Colored by Order)")
    plt.xlabel("Core Genome Distance (1 - identity)")
    plt.ylabel("Gene Sequence Identity")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_colored.png", dpi=1200)
    plt.savefig(f"{output_prefix}_colored.svg")


def main():
    # === Input paths ===
    core_path = "core_alignment.fasta"
    gene_paths = {
        "mutT": "mutT_id_mafft.fasta",
        "mutH": "mutH_id_mafft.fasta",
        "mutS": "mutS_id_mafft.fasta",
    }
    mapping_csv="/home/montoliu/40sp/40_species.csv"

    # === Load mapping ===
    abbr_to_species, abbr_to_order = load_csv_mapping(mapping_csv)

    # === Load alignments ===
    core_alignment = AlignIO.read(core_path, "fasta")
    gene_alignments = {gene: AlignIO.read(path, "fasta") for gene, path in gene_paths.items()}

    # === Calculate identities ===
    core_id = calculate_pairwise_identity(core_alignment)
    gene_ids = {gene: calculate_pairwise_identity(aln) for gene, aln in gene_alignments.items()}

    # === Build DataFrame ===
    df = build_dataframe(core_id, gene_ids, abbr_to_order)

    # === Plot ===
    plot_identity_vs_distance_colored(df)

if __name__ == "__main__":
    main()
