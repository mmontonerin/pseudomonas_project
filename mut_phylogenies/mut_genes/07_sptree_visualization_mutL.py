import os 
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, TextFace, CircleFace, RectFace

# Ensure Qt uses the offscreen platform (useful for headless environments like servers)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Input files
tree_file = "/home/montoliu/mut_phylogenies/mut_genes/mutL.treefile"
pdf_output = "/home/montoliu/mut_phylogenies/mut_genes/trees/mutL2.pdf"
png_output = "/home/montoliu/mut_phylogenies/mut_genes/trees/mutL2.png"
svg_output = "/home/montoliu/mut_phylogenies/mut_genes/trees/mutL2.svg"

# The tree
t = Tree(tree_file, format=1)

# Name mappings
name_map = {
    "psyr": "P. syringae",
    "psav": "P. savastanoi",
    "pvir": "P. viridiflava",
    "ppro": "P. protegens",
    "pbra": "P. brassicacearum",
    "pflu": "P. fluorescens",
    "ecol": "E. coli"
}

# Color mappings
color_map = {
    "P. syringae": "#58B4D1",
    "P. savastanoi": "#126782",
    "P. viridiflava": "#023047",
    "P. protegens": "#FFB703",
    "P. brassicacearum": "#FC9201",
    "P. fluorescens": "#BB3E03",
    "E. coli": "black"
}

# Set E. coli as the outgroup and manually scale the outgroup branch length
outgroup = t & "ecol_mutL"
original_dist = outgroup.dist  # Store original distance
outgroup.dist = outgroup.dist / 5  # Scale the outgroup by reducing its branch length

# Set outgroup so the root is between the outgroup and the rest of the tree
t.set_outgroup(outgroup)

# Define node style once
nstyle = NodeStyle()
nstyle["size"] = 0  # Ensure blue dots are removed
nstyle["hz_line_width"] = 1
nstyle["vt_line_width"] = 1

# Rename leaves and add colored circles
for node in t.traverse():
    node.set_style(nstyle)
    if node.is_leaf():
        # Find the prefix in the leaf name
        species_prefix = node.name.split("_")[0]
        species_name = name_map.get(species_prefix, node.name)

        # Assign the full species name
        node.name = species_name

        # Create a circle face with the color for the species
        color = color_map.get(species_name, "gray")  # Default to gray if no color is found
        #circle_face = CircleFace(radius=2, color=color)  # Radius for the circle
        rect_face = RectFace(width=50, height=2, fgcolor=color, bgcolor=color)

        # Attach the circle face to the node
        #node.add_face(circle_face, column=0, position="aligned")
        node.add_face(rect_face, column=0, position="aligned")



# Create a circular tree style
ts = TreeStyle()
ts.mode = "c"  # Circular tree
ts.show_leaf_name = False  # Don't show leaf names
#ts.show_scale = False  # Don't show scale
ts.scale = 200
ts.allow_face_overlap = True
ts.optimal_scale_level = "full"

#ts.draw_guiding_lines = True
#ts.guiding_lines_type = 1 
#ts.guiding_lines_color = "gray" 

t.swap_children()

#ts.branch_vertical_margin = 10  # Adjust spacing if needed

# Render and save the tree
#t.render(pdf_output, tree_style=ts, dpi=1200, w=3000, h=3000)
t.render(png_output, tree_style=ts, dpi=2400, w=20000, h=20000)
#t.render(svg_output, tree_style=ts, dpi=1200, w=3000, h=3000)

print(f"Tree visualization saved as {pdf_output} and {png_output} and {svg_output}")
