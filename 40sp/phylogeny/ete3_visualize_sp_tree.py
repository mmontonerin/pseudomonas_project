import os
from ete3 import Tree, TreeStyle, NodeStyle
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
        "Enterobacteriaceae": "#3dbbb8",
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
tree_file = "40sp_ordered.nw"
csv_file = "../40_species.csv"
pdf_output = "sp_tree.pdf"
png_output = "sp_tree.png"

# Load mappings
abbr_to_species, abbr_to_order = load_csv_mapping(csv_file)

# Load the tree
t = Tree(tree_file)

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

# Set up the tree style
ts = TreeStyle()
ts.show_leaf_name = True
ts.scale = 100
# ts.show_branch_support = True  # Enable support display on branches

# Render and save the tree
t.render(pdf_output, tree_style=ts)
t.render(png_output, tree_style=ts)

print(f"Tree visualization saved as {pdf_output} and {png_output}")