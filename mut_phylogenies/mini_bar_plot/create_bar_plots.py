import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# Load data from CSV
species_data = pd.read_csv("table.csv")

def plot_bar(name, n, mapped_n, color, filename, vertical=False):
    total = n + mapped_n
    percentage = (mapped_n / total) * 100  # Grey zone percentage
    
    fig, ax = plt.subplots(figsize=(5, 1) if not vertical else (1, 5))
    if vertical:
        ax.bar(0, n, color=color, width=0.5)
        ax.bar(0, mapped_n, bottom=n, color="grey", width=0.5)
        ax.text(0, n / 2, f"n={n}\n{percentage:.1f}%", ha='center', va='center', fontsize=10, color='white')
    else:
        ax.barh(0, n, color=color, height=0.5)
        ax.barh(0, mapped_n, left=n, color="grey", height=0.5)
        ax.text(n / 2, 0, f"n={n}\n{percentage:.1f}%", ha='center', va='center', fontsize=10, color='white')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

# Individual species plots (horizontal bars)
for _, row in species_data.iterrows():
    plot_bar(row["name"], row["n"], row["mapped_n"], row["color"], f"{row['species']}.png", vertical=False)

# Combined gradient plots (vertical bars)
def gradient_bar(colors, total_n, total_mapped_n, filename):
    total = total_n + total_mapped_n
    percentage = (total_mapped_n / total) * 100  # Grey zone percentage
    
    fig, ax = plt.subplots(figsize=(1, 5))  # Vertical orientation
    gradient = np.linspace(0, 1, 256).reshape(256, 1)  # Vertical gradient
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors)
    ax.imshow(gradient, aspect='auto', cmap=custom_cmap, extent=[-0.25, 0.25, 0, total_n])
    
    # Add grey zone bar on top
    ax.bar(0, total_n, color='none', width=0.5)
    ax.bar(0, total_mapped_n, bottom=total_n, color="grey", width=0.5)
    
    ax.text(0, total_n / 2, f"n={total_n}\n{percentage:.1f}%", ha='center', va='center', fontsize=10, color='white')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    plt.savefig(filename, bbox_inches='tight', dpi=800)
    plt.close()

# Define gradients with total counts
gradient_bar(["#58B4D1", "#126782", "#023047"], species_data.loc[:2, "n"].sum(), species_data.loc[:2, "mapped_n"].sum(), "group1.png")
gradient_bar(["#FFB703", "#FC9201", "#BB3E03"], species_data.loc[3:, "n"].sum(), species_data.loc[3:, "mapped_n"].sum(), "group2.png")
gradient_bar(["#58B4D1", "#126782", "#023047", "#FFB703", "#FC9201", "#BB3E03"], species_data["n"].sum(), species_data["mapped_n"].sum(), "all_species.png")
