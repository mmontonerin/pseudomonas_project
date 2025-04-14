import os
import argparse

def extract_sequences(assembly, a_name, g_name, seq, result, run):
    input_file = os.path.join(result, g_name, f"{a_name}_{g_name}.out")
    if os.path.getsize(input_file) >= 2:
        frag_script = True
    else:
        frag_script = False

    with open(input_file, 'r') as infile:
        contig_id = None
        min_start = None
        max_end = None
        prev_contig_id = None
        for line in infile:
            fields = line.strip().split('\t')
            if contig_id is None:
                contig_id = fields[1]
                min_start = min(int(fields[9]), int(fields[10]))
                max_end = max(int(fields[9]), int(fields[10]))
            else:
                if fields[1] != contig_id:
                    frag_seq = f"{seq}/fragmented"
                    print_blastdbcmd(assembly, a_name, g_name, frag_seq, prev_contig_id, min_start, max_end)
                    min_start = int(fields[10])
                    max_end = int(fields[9])
                else:
                    min_start = min(min_start, int(fields[9]))
                    max_end = max(max_end, int(fields[10]))
            prev_contig_id = fields[1]

        # Print the blastdbcmd command for the last contig
        print_blastdbcmd(assembly, a_name, g_name, seq, prev_contig_id, min_start, max_end, frag_script)

def print_blastdbcmd(assembly, a_name, g_name, seq, contig_id, min_start, max_end, frag_script=False):
    plus_strand = min_start < max_end  # Determine strand based on min_start and max_end

    if plus_strand:
        cmd = f"blastdbcmd -db {assembly} -dbtype nucl -entry {contig_id} -range {min_start}-{max_end} -strand plus -out {seq}/{g_name}/{a_name}_{contig_id}_{min_start}-{max_end}plus.fasta"
    else:
        cmd = f"blastdbcmd -db {assembly} -dbtype nucl -entry {contig_id} -range {min_start}-{max_end} -strand minus -out {seq}/{g_name}/{a_name}_{contig_id}_{min_start}-{max_end}minus.fasta"

    outfile = f"{run}/extract_blast_seq_frag.sh" if frag_script else f"{run}/extract_blast_seq.sh"

    print(cmd)
    with open(outfile, 'a') as outfile:
        outfile.write(cmd + '\n')

def main():
    parser = argparse.ArgumentParser(description="Extract specific gene sequences for each genome assembly")
    parser.add_argument("-a", "--assembly", required=True, help="Path to the assembly")
    parser.add_argument("-n", "--aname", required=True, help="Name of the assembly")
    parser.add_argument("-g", "--gname", required=True, help="Name of the gene")
    parser.add_argument("-s", "--seq", required=True, help="Path to store sequences")
    parser.add_argument("-r", "--result", required=True, help="Path to the blast result")
    parser.add_argument("-u", "--run", required=True, help="Path to store output script")

    args = parser.parse_args()

    extract_sequences(args.assembly, args.aname, args.gname, args.seq, args.result, args.run)

if __name__ == "__main__":
    main()
