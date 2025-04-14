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
from matplotlib.patches import Wedge
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib.markers import MarkerStyle

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

def plot_identity_vs_distance_colored_panels(df, abbr_to_order, output_prefix="identity_vs_core_distance_panels"):
    # Melt DataFrame for easier plotting
    df_melt = df.melt(
        id_vars=['Core_Distance', 'Order', 'Species1', 'Species2'],
        value_vars=[col for col in df.columns if col.endswith('_Identity')],
        var_name='Gene', value_name='Identity'
    )

    # Gene names and fixed colors
    genes = df_melt['Gene'].unique()
    order_colors = {
        "Enterobacteriaceae": "#3dbbb8",
        "Gammaproteobacteria": "#8b64d1",
        "Betaproteobacteria": "#c55ea0",
        "Alphaproteobacteria": "#7487c8",
        "Outgroups": "black",
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    x_max = df["Core_Distance"].max()

    for ax, gene in zip(axes, genes):
        subset = df_melt[df_melt['Gene'] == gene]

        for _, row in subset.iterrows():
            x, y = row["Core_Distance"], row["Identity"]

            if row["Order"] != "Mixed":
                color = order_colors.get(row["Order"], "gray")
                ax.scatter(x, y, color=color, edgecolor=color, s=60, alpha=0.7, linewidth=0.6)
            else:
                # Mixed case: two half-circles with rotated marker styles
                order1 = abbr_to_order.get(row["Species1"], "gray")
                order2 = abbr_to_order.get(row["Species2"], "gray")
                color1 = order_colors.get(order1, "gray")
                color2 = order_colors.get(order2, "gray")

                # Half-circle markers
                ax.scatter(x, y, color=color1, marker=MarkerStyle('o', fillstyle='left'),
                           edgecolor=color1, s=60, alpha=0.7, linewidth=0.6)
                ax.scatter(x, y, color=color2, marker=MarkerStyle('o', fillstyle='right'),
                           edgecolor=color2, s=60, alpha=0.7, linewidth=0.6)

        # Linear regression fit
        sns.regplot(
            data=subset,
            x="Core_Distance", y="Identity",
            scatter=False, ax=ax,
            color="black", line_kws={'lw': 2, 'linestyle': 'dashed'}
        )

        # Axis formatting
        ax.set_title(gene.replace("_Identity", ""), fontsize=13)
        ax.set_xlabel("Core Genome Distance")
        ax.set_xlim(left=-0.02, right=x_max * 1.05)
        if ax == axes[0]:
            ax.set_ylabel("Gene Sequence Identity")
        else:
            ax.set_ylabel("")

    plt.suptitle("Gene Identity vs. Core Genome Distance", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
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
    plot_identity_vs_distance_colored_panels(df, abbr_to_order)

if __name__ == "__main__":
    main()
