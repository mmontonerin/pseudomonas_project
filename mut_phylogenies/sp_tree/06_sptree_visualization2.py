import os 
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, TextFace

# Ensure Qt uses the offscreen platform (useful for headless environments like servers)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Input files
tree_file = "/home/montoliu/mut_phylogenies/sp_tree/sp_tree300.treefile"
pdf_output = "/home/montoliu/mut_phylogenies/sp_tree/sptree_try10.pdf"
png_output = "/home/montoliu/mut_phylogenies/sp_tree/sptree_try10.png"

# The tree
t = Tree(tree_file, format=1)

# Name mappings
name_map = {
    "psyr0981": "P. syringae",
    "psav0127": "P. savastanoi",
    "pvir0082": "P. viridiflava",
    "ppro0099": "P. protegens",
    "pbra0020": "P. brassicacearum",
    "pflu0183": "P. fluorescens",
    "ecol": "E. coli"
}

# Color mappings
color_map = {
    "P. syringae": "#679699",
    "P. savastanoi": "#74B3A2",
    "P. viridiflava": "#C9E8AE",
    "P. protegens": "#F5D58B",
    "P. brassicacearum": "#EA9C7E",
    "P. fluorescens": "#CC5E58",
    "E. coli": "black"
}

# Set E. coli as the outgroup and manually scale the outgroup branch length
outgroup = t & "ecol"
original_dist = outgroup.dist  # Store original distance
outgroup.dist = outgroup.dist / 3  # Scale the outgroup by reducing its branch length

# Set outgroup so the root is between the outgroup and the rest of the tree
t.set_outgroup(outgroup)

# Define the species names in the order you want to arrange them
species_order = ["psyr0981", "psav0127", "pvir0082", "ppro0099", "pbra0020", "pflu0183"]

# Find the species nodes based on the names
species_nodes = {species: t.search_nodes(name=species)[0] for species in species_order}

# Find common ancestors for the different pairs of species
psyr_psav_ancestor = species_nodes["psyr0981"].get_common_ancestor(species_nodes["psav0127"])
ppro_pbra_ancestor = species_nodes["ppro0099"].get_common_ancestor(species_nodes["pbra0020"])
psyr_ppro_ancestor = species_nodes["ppro0099"].get_common_ancestor(species_nodes["psyr0981"])

# Swap children nodes for the common ancestors to reorder them
psyr_psav_ancestor.swap_children()  # Swap Psyr and Psav
ppro_pbra_ancestor.swap_children()  # Swap Ppro and Pbra
psyr_ppro_ancestor.swap_children()
# No need to swap Pflu as it should already be last in the tree

# Define node style once
nstyle = NodeStyle()
nstyle["size"] = 0  # Ensure blue dots are removed
nstyle["hz_line_width"] = 1
nstyle["vt_line_width"] = 1

# Rename the tips and add colored labels
for node in t.traverse():
    node.set_style(nstyle)

    if node.is_leaf():
        species_name = name_map.get(node.name, node.name)
        node.name = species_name  # Rename the tip

        # Set the text color based on the species name
        if species_name == "E. coli":
            text_color = "white"  # E. coli will have white text
        else:
            text_color = "black"  # All other species will have black text

        # Create a colored text face with the appropriate color
        tf = TextFace(species_name, fsize=10, fstyle="italic", fgcolor=text_color)
        tf.background.color = color_map.get(species_name, "gray")  # Use mapped color

        # Attach face to the node
        node.add_face(tf, column=0, position="branch-right")



# Create a tree style
ts = TreeStyle()
ts.show_leaf_name = False  # We will use TextFace instead
ts.scale = 200  # Adjust for better spacing

# Set the tree mode to rectangular to get a more squared appearance
ts.mode = "r"  # Rectangular mode

# Set branch scaling to make it squared
ts.optimal_scale_level = "mid"

ts.branch_vertical_margin = 5

# Adjust extra line type for dotted lines
ts.extra_branch_line_type = 2  # 0=solid, 1=dashed, 2=dotted
ts.extra_branch_line_color = "gray"  # Set dotted line color to gray

t.swap_children()

# Render and save the tree
t.render(pdf_output, tree_style=ts, dpi=800, w=3000, h=3000)
t.render(png_output, tree_style=ts, dpi=800, w=3000, h=3000)

print(f"Tree visualization saved as {pdf_output} and {png_output}")





