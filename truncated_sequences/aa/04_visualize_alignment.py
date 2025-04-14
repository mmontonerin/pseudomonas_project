import os
import sys
import matplotlib.pyplot as plt
from Bio import SeqIO

def parse_alignment(fasta_file):
    """Reads a FASTA alignment file and extracts sequences."""
    records = list(SeqIO.parse(fasta_file, "fasta"))
    if not records:
        raise ValueError(f"No sequences found in {fasta_file}")
    return records

def get_species_color(fasta_file):
    """Determines the color mapping based on the file name prefix."""
    color_map = {
        "psyr": "#58B4D1",
        "psav": "#126782",
        "pvir": "#023047",
        "ppro": "#FFB703",
        "pbra": "#FC9201",
        "pflu": "#BB3E03"
    }
    prefix = os.path.basename(fasta_file).split("_")[0]
    return color_map.get(prefix, "#D3D3D3")  # Default to light gray if unknown

def plot_alignment(fasta_file, output_dir):
    records = parse_alignment(fasta_file)
    ref_seq = str(records[0].seq)  # First sequence is the reference
    species_color = get_species_color(fasta_file)
    num_seqs = len(records)
    seq_length = len(ref_seq)
    
    fig, ax = plt.subplots(figsize=(seq_length / 10, num_seqs))
    
    for i, record in enumerate(records):
        seq = str(record.seq)
        for j, (ref_res, res) in enumerate(zip(ref_seq, seq)):
            if res == "-":
                continue  # Leave gaps empty
            color = "black" if i == 0 else ("gray" if res != ref_res else species_color)
            ax.add_patch(plt.Rectangle((j, num_seqs - i - 1), 1, 0.8, color=color))
    
    ax.set_xlim(0, seq_length)
    ax.set_ylim(0, num_seqs)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    output_base = os.path.join(output_dir, os.path.basename(fasta_file).replace(".fasta", ""))
    plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"{output_base}.svg", bbox_inches='tight')
    plt.close()

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    fasta_files = [f for f in os.listdir(input_dir) if f.endswith(".fasta")]
    
    for fasta_file in fasta_files:
        plot_alignment(os.path.join(input_dir, fasta_file), output_dir)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])