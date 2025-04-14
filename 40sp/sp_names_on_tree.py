import csv
import re

# Read the CSV and create a mapping of abbreviations to formatted names
csv_file = "40_species.csv"
abbr_to_species = {}

with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Take only the first two words of the "Species" column, replacing underscores with spaces
        species_name = " ".join(row["Species"].split("_")[:2])
        abbr_to_species[row["abreviation"]] = species_name

# Read the tree file and replace abbreviations with species names
tree_file = "./mut_sequences/alignments/uvrD_id_mafft.fasta.treefile"
output_tree_file = "./mut_sequences/alignments/uvrD_id_mafft_renamed.fasta.treefile"

with open(tree_file, "r") as f:
    tree_data = f.read()

# Replace abbreviations with species names in the tree
pattern = re.compile(r"\b(" + "|".join(map(re.escape, abbr_to_species.keys())) + r")\b")
updated_tree_data = pattern.sub(lambda x: abbr_to_species[x.group()], tree_data)

# Write the updated tree to a new file
with open(output_tree_file, "w") as f:
    f.write(updated_tree_data)

print("Updated tree file saved as:", output_tree_file)