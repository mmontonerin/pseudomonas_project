import os
from Bio import AlignIO, SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from collections import defaultdict

def concatenate_alignments(alignment_folder, output_file):
    """
    Concatenates aligned sequences from individual FASTA files into a core alignment.
    Assumes that all files have the same set of species and sequences are aligned.
    """
    concatenated = defaultdict(str)
    all_species = set()
    alignment_lengths = []

    # Sort files to ensure consistent order
    files = sorted(f for f in os.listdir(alignment_folder) if f.endswith(".fa"))

    for file in files:
        path = os.path.join(alignment_folder, file)
        alignment = AlignIO.read(path, "fasta")

        seq_dict = {rec.id: str(rec.seq) for rec in alignment}
        current_species = set(seq_dict.keys())
        all_species.update(current_species)
        alignment_lengths.append(len(next(iter(seq_dict.values()))))  # track alignment lengths

        for species in all_species:
            if species in seq_dict:
                concatenated[species] += seq_dict[species]
            else:
                # If missing, add gap sequence of same length
                concatenated[species] += '-' * alignment_lengths[-1]

    # Write concatenated alignment
    records = [SeqRecord(Seq(seq), id=species, description="") for species, seq in concatenated.items()]
    SeqIO.write(records, output_file, "fasta")
    print(f"✅ Concatenated alignment written to: {output_file}")

if __name__ == "__main__":
    # === Customize these paths ===
    alignment_folder = "/home/montoliu/40sp/phylogeny/alignments/"      # folder with your MAFFT alignments
    output_file = "/home/montoliu/40sp/identity_analyses/core_alignment.fasta"   # output file for the concatenated SCOs

    concatenate_alignments(alignment_folder, output_file)
