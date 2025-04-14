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
        "Gammaproteobacteria": "#8b64d1",
        "Betaproteobacteria": "#c55ea0",
        "Alphaproteobacteria": "#7487c8",
        "Outgroups": "black",
    }
    return order_colors.get(order, "black")

def annotate_support(node):
     """Annotate node with its support value (from bootstrap or posterior probability)."""
     if node.support:
         return f"{node.support}"
     return "No support"

# Input files
tree_file = "./mut_sequences/alignments/mutL_id_mafft.fasta.treefile"
csv_file = "40_species.csv"
pdf_output = "./mut_sequences/alignments/mutL_tree.pdf"
png_output = "./mut_sequences/alignments/mutL_tree.png"

# Load mappings
abbr_to_species, abbr_to_order = load_csv_mapping(csv_file)

# Load the tree
t = Tree(tree_file)

# print("Tree leaf names:")
# for leaf in t.iter_leaves():
#     print(leaf.name)

# # Specify the target outgroup species for rerooting
# target_outgroup_species = ["cjeju", "hpylo", "ctrac"]

# # Find all target outgroup nodes by matching names in the tree
# outgroup_nodes = [
#     leaf for leaf in t.iter_leaves() if leaf.name in target_outgroup_species
# ]

# # Ensure we have found all specified outgroup nodes
# missing_species = [species for species in target_outgroup_species if species not in [leaf.name for leaf in outgroup_nodes]]
# if missing_species:
#     print(f"Error: Could not find the following species in the tree: {missing_species}")
# else:
#     # Find the most recent common ancestor (MRCA) of the target outgroup species
#     outgroup_mrca = t.get_common_ancestor(outgroup_nodes)
    
#     # Reroot the tree at the MRCA of the target outgroup species
#     t.set_outgroup(outgroup_mrca)
#     print(f"Tree rerooted at the common ancestor of: {', '.join(target_outgroup_species)}")



# # Find all leaves that are labeled as "Outgroups" in the CSV and add them to the outgroup list
outgroup_nodes = [leaf for leaf in t.iter_leaves() if abbr_to_order.get(leaf.name, "") == "Outgroups"]

# # Ensure we have found all outgroup nodes
if outgroup_nodes:
    # Find the most recent common ancestor (MRCA) of the outgroup species
    outgroup_mrca = t.get_common_ancestor(outgroup_nodes)
    
    # Reroot the tree at the MRCA of the outgroup cluster
    t.set_outgroup(outgroup_mrca)
    print("Tree rerooted at the common ancestor of the outgroups.")
else:
    print("No outgroup species found in the tree.")

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

    # Add support values to leaf nodes (only if available)
    support_value = annotate_support(leaf)
    leaf.add_features(support=support_value)

# Set up the tree style
ts = TreeStyle()
ts.orientation = 1 # facing left side for comparison with sp tree
ts.show_leaf_name = True
ts.scale = 100
ts.show_branch_support = True  # Enable support display on branches

# To make sure the root appears at the bottom, apply ladderize or reverse the branches:
#t.ladderize()  # This will place the root at the bottom by sorting branches
t.swap_children()

# Render and save the tree
t.render(pdf_output, tree_style=ts)
t.render(png_output, tree_style=ts)

print(f"Tree visualization saved as {pdf_output} and {png_output}")