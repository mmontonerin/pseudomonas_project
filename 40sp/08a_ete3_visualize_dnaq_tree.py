import os
from ete3 import PhyloTree, TreeStyle, NodeStyle
import csv

# Ensure Qt uses the offscreen platform (useful for headless environments like servers)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

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
        "Gammaproteobacteria": "#8b64d1",
        "Betaproteobacteria": "#c55ea0",
        "Alphaproteobacteria": "#7487c8",
        "Outgroups": "black",
    }
    return order_colors.get(order, "black")

# def annotate_support(node):
#     """Annotate node with its support value (from bootstrap or posterior probability)."""
#     if node.support:
#         return f"{node.support}"
#     return "No support"

# Input files
tree_file = "/home/montoliu/40sp/mut_sequences/alignments/dnaQ.nw"
csv_file = "40_species.csv"
pdf_output = "/home/montoliu/40sp/mut_sequences/alignments/dnaQ.pdf"
png_output = "/home/montoliu/40sp/mut_sequences/alignments/dnaQ.png"
alignment_file = "/home/montoliu/40sp/mut_sequences/alignments/dnaQ_id_mafft.fasta"

# Load mappings
abbr_to_species, abbr_to_order = load_csv_mapping(csv_file)

# Load the tree
t = PhyloTree(tree_file)

# Replace abbreviations with full species names and apply styles
for leaf in t:
    abbr = leaf.name
    species = abbr_to_species.get(abbr, abbr)
    order = abbr_to_order.get(abbr, "Unknown")

    # Update the leaf name
    leaf.name = species

    # Apply coloring based on order
    nstyle = NodeStyle()
    nstyle['fgcolor'] = color_by_order(order)
    nstyle['size'] = 10
    leaf.set_style(nstyle)

    # # Add support values to leaf nodes (only if available)
    # support_value = annotate_support(leaf)
    # leaf.add_features(support=support_value)

# Link the tree to the alignment (must match sequence IDs between tree and alignment)
with open(alignment_file, "r") as f:
    alignment_txt = f.read()

t.link_to_alignment(alignment=alignment_txt, alg_format="fasta")

# Set up the tree style with alignment next to the tree
ts = TreeStyle()
ts.show_leaf_name = True  # Display leaf names
ts.show_branch_length = True  # Show branch lengths
#ts.show_branch_support = True  # Show support values on branches
ts.scale = 100  # Set scale to a larger value to better display branch lengths


# # Add the alignment to the tree visualization
# ts.show_align = True  # Enable showing the alignment next to the tree
# ts.align_pos = 1  # Position the alignment on the right (can be 1 for right, -1 for left)
# ts.align_width = 200  # Adjust the width of the alignment display (in pixels)
# ts.alignment = alignment_file  # Point to the FASTA alignment file

# Render and save the tree with alignment
t.render(pdf_output, tree_style=ts)
t.render(png_output, tree_style=ts)

print(f"Tree with alignment visualization saved as {pdf_output} and {png_output}")

# # Set up the tree style
# ts = TreeStyle()
# ts.show_leaf_name = True
# ts.scale = 100
# # ts.show_branch_support = True  # Enable support display on branches

# # Render and save the tree
# t.render(pdf_output, tree_style=ts)
# t.render(png_output, tree_style=ts)

# print(f"Tree visualization saved as {pdf_output} and {png_output}")