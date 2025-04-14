import os
from Bio import AlignIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# List of genes and their associated clusters
genes_clusters = {
    "dnaQ": "cluster18", #100 copies
    "mutL": "cluster5", #69 copies
    "mutS": "cluster8", #67 copies
    "mutT": "cluster8", #65 copies
    "mutY": "cluster19", #68 copies
    "uvrD": "cluster6" #137 copies
}

# Base path to MSA files
msa_dir = "/home/montoliu/psyringae_group/mut_genes/protein_analysis/alignments/clusters"

# Output directory for images
output_dir = "/home/montoliu/psyringae_group/mut_genes/protein_analysis/alignment_visualization"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Loop through each gene and its cluster
for gene, cluster in genes_clusters.items():
    msa_file = os.path.join(msa_dir, f"{gene}_clusters_mafft.fasta")  # Construct MSA file path
    output_file = os.path.join(output_dir, f"msa_visualization_{gene}.png")  # Output figure file
    
    print(f"Processing {gene} with master sequence {cluster}...")

    # Load the MSA
    try:
        with open(msa_file, "r") as handle:
            alignment = list(AlignIO.parse(handle, "fasta"))[0]  # Extract the first alignment
    except FileNotFoundError:
        print(f"Warning: MSA file {msa_file} not found. Skipping {gene}.")
        continue
    except Exception as e:
        print(f"Error reading {msa_file}: {e}")
        continue

    # Find the master sequence
    master_seq = None
    for record in alignment:
        if record.id == cluster:
            master_seq = record.seq
            break
    if not master_seq:
        print(f"Warning: Master sequence {cluster} not found in {msa_file}. Skipping {gene}.")
        continue

    # Initialize arrays for % identity and differences
    seq_count = len(alignment)
    seq_length = len(master_seq)

    identity = np.zeros(seq_length)  # Stores % identity
    differences = np.zeros(seq_length)  # Stores count of differences

    # Loop through alignment positions
    for i in range(seq_length):
        ref_residue = master_seq[i]
        match_count = 0
        diff_count = 0

        for seq in alignment:  # Compare other sequences
            residue = seq.seq[i]
            if residue == ref_residue:
                match_count += 1
            elif residue != ref_residue or residue == "-":
                diff_count += 1

        identity[i] = (match_count / seq_count) * 100  # Normalize by total sequences
        differences[i] = diff_count

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw={"height_ratios": [5, 1]})

    # **Top plot: Line plot for number of differences**
    ax[0].plot(range(seq_length), differences, color="black", linewidth=1.5, label="Differences")
    ax[0].set_ylabel("#Sequences that differ")
    ax[0].set_ylim(0, max(10, differences.max()))  # Dynamic limit
    ax[0].set_xlim(0, seq_length)
    ax[0].set_title(f"Protein Alignment Comparison: {gene}")

    # **Bottom plot: Bar plot for % identity gradient**
    cmap = sns.color_palette("plasma", as_cmap=True)  # Color gradient
    colors = cmap(identity / 100)  # Normalize to 0-1 for colormap
    ax[1].bar(range(seq_length), [1] * seq_length, color=colors, width=1)  # Thin bar at bottom

    ax[1].set_yticks([])  # Hide y-axis for bar
    ax[1].set_xlabel("Sequence Position")
    ax[1].set_xlim(0, seq_length)

    # Add color legend
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=100))
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", fraction=0.05, pad=0.01)
    cbar.set_label("% Identity")

    # Adjust layout
    plt.subplots_adjust(hspace=0.05, right=0.85)

    # Save figure
    plt.savefig(output_file, dpi=800)
    plt.close()

    print(f"Saved visualization: {output_file}")

print("All analyses completed.")