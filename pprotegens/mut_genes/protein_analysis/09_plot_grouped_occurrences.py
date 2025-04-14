import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os

# Generate Whittaker plot based on cluster frequency
def plot_whittaker_by_frequency(df, cluster_columns, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for col in cluster_columns:
        # Count occurrences of each cluster
        cluster_counts = df[col].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Count"]

        # Sort by count in descending order
        cluster_counts = cluster_counts.sort_values("Count", ascending=False)

        # Create rank-abundance data
        cluster_counts["Rank"] = range(1, len(cluster_counts) + 1)

        # Log-transform counts
        cluster_counts["LogCount"] = cluster_counts["Count"].apply(lambda x: np.log10(x))

        # Plot
        plt.figure(figsize=(8, 6))
        plt.plot(cluster_counts["Rank"], cluster_counts["LogCount"], marker='o', linestyle='-', color='teal')
        plt.xlabel("Rank (Cluster)")
        plt.ylabel("Log10(Number of strains)")
        plt.title(f"Whittaker Plot for {col}")
        plt.grid(visible=True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # Save the plot
        plt.savefig(os.path.join(output_dir, f"{col}_whittaker_plot_frequency.png"), dpi=300)
        plt.savefig(os.path.join(output_dir, f"{col}_whittaker_plot_frequency.pdf"))
        plt.close()

def plot_whittaker_by_frequency_nolog(df, cluster_columns, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for col in cluster_columns:
        # Count occurrences of each cluster
        cluster_counts = df[col].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Count"]

        # Sort by count in descending order
        cluster_counts = cluster_counts.sort_values("Count", ascending=False)

        # Create rank-abundance data
        cluster_counts["Rank"] = range(1, len(cluster_counts) + 1)

        # Plot
        plt.figure(figsize=(8, 6))
        plt.plot(cluster_counts["Rank"], cluster_counts["Count"], marker='o', linestyle='-', color='teal')
        plt.xlabel("Rank (Cluster)")
        plt.ylabel("Number of strains")
        plt.title(f"Whittaker Plot for {col}")
        plt.grid(visible=True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # Save the plot
        plt.savefig(os.path.join(output_dir, f"{col}_whittaker_plot_frequency_nolog.png"), dpi=300)
        plt.savefig(os.path.join(output_dir, f"{col}_whittaker_plot_frequency_nolog.pdf"))
        plt.close()

# Main script adjustment for the new dataset
if __name__ == "__main__":
    input_file = "grouped_occurrences.csv"
    output_dir = "/home/montoliu/pprotegens/mut_genes/protein_analysis/alignments/clusters/plots_output_grouped"

    # Load the dataset
    df = pd.read_csv(input_file)

    # Define the cluster columns
    cluster_columns = ["dnaQ_cluster", "mutL_cluster", "mutS_cluster", "mutT_cluster", "mutY_cluster", "uvrD_cluster"]

    # Generate Whittaker plots based on frequency
    plot_whittaker_by_frequency(df, cluster_columns, output_dir)

    # Generate Whittaker plots based on frequency
    plot_whittaker_by_frequency_nolog(df, cluster_columns, output_dir)

    print("Whittaker plots based on frequency have been saved in:", output_dir)