import os 
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, TextFace

# Ensure Qt uses the offscreen platform (useful for headless environments like servers)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Input files
tree_file = "/home/montoliu/mut_phylogenies/sp_tree/sp_tree300.treefile"
pdf_output = "/home/montoliu/mut_phylogenies/sp_tree/sptree_try1.pdf"
png_output = "/home/montoliu/mut_phylogenies/sp_tree/sptree_try1.png"

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

# Rename the tips
for node in t.traverse():
    if node.is_leaf():
        node.name = name_map.get(node.name, node.name)  # Replace with proper name

# Set E. coli as the outgroup
t.set_outgroup(t & "E. coli")

# Create a tree style
ts = TreeStyle()
ts.show_leaf_name = True 
ts.scale = 200  # Adjust for better spacing

t.swap_children()

# Render and save the tree
t.render(pdf_output, tree_style=ts)
t.render(png_output, tree_style=ts)

print(f"Tree visualization saved as {pdf_output} and {png_output}")





