#!/bin/bash
#SBATCH --output=slurm_03.2_blast_extractseq-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=2        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=06:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

# Define directories:
psyr="/home/montoliu/psyringae_group" #main directory of the analysis
as="/home/montoliu/psyringae_group/data/assemblies" #assembly references
gen="/home/montoliu/psyringae_group/data/genes" #genes to blast
result="/home/montoliu/psyringae_group/results/blastn/blastn_out" #results folder
seq="/home/montoliu/psyringae_group/results/sequences" #extracted sequences folder
run="/home/montoliu/psyringae_group/scripts" #scripts folder
frag="/home/montoliu/psyringae_group/results/sequences/fragmented" #extracted sequences folder for the frafmented assemblies

# Create empty script that will be used to append the commands to extract the sequences
echo '#!/bin/bash' > ${run}/extract_blast_seq.sh
echo '#!/bin/bash' > ${run}/extract_blast_seq_frag.sh


for assembly in ${as}/*.fasta
do 
        for gene in ${gen}/*fasta
        do
                # Simplify names of files
                aname=$(basename "$assembly" .fasta)
                gname=$(basename "$gene" .fasta)

		# If it does not exist, it creates a folder for each gene
                mkdir -p ${seq}/${gname}
		mkdir -p ${frag}/${gname}

		# Prepare a script to extract the specific gene sequences for each genome assembly but separate the ones that are fragmented
		if [[ $(wc -l <"${result}/${gname}/${aname}_${gname}.out") -ge 2 ]]; then
    		# Multiple hits on the same contig, extract full sequence range
    		awk -v assembly="$assembly" -v a_name="$aname" -v g_name="$gname" -v seq="$frag" -F"\t" '
        		NR==1 {
				contig_id = $2
            			min_start = ($10 < $9) ? $9 : $10
            			max_end = ($10 > $9) ? $10 : $9
        		}
        		{
				
				if ($2 != contig_id) {
			                contig_id = $2
                			if (min_start < max_end) {
                    				print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " min_start "-" max_end " -strand plus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "plus.fasta"
                			} else {
                    				print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " max_end "-" min_start " -strand minus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "minus.fasta"
                			}
                			min_start = $10
                			max_end = $9
            			} else {
                			if ($10 > $9) {
                    				if ($9 < min_start) min_start = $9
                    				if ($10 > max_end) max_end = $10
                			} else {
                    				if ($10 < min_start) min_start = $10
                    				if ($9 > max_end) max_end = $9
                			}
            			}
            			prev_contig_id = $2
        		}
        		END {
            			if (min_start < max_end) {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " min_start "-" max_end " -strand plus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "plus.fasta"
            			} else {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " max_end "-" min_start " -strand minus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "minus.fasta"
            			}
        		}' "${result}/${gname}/${aname}_${gname}.out" >>"${run}/extract_blast_seq_frag.sh"
		else
    		# Single hit or no hits on the same contig, extract sequences as before
    		awk -v assembly="$assembly" -v a_name="$aname" -v g_name="$gname" -v seq="$seq" -F"\t" '
        		{
            			if ($10 > $9) {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $9 "-" $10 " -strand plus -out " seq "/" g_name "/" a_name "_" $2 "_" $9 "-" $10 "plus.fasta"
            			} else {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $10 "-" $9 " -strand minus -out " seq "/" g_name "/" a_name "_" $2 "_" $9 "-" $10 "minus.fasta"
            			}
        		}' "${result}/${gname}/${aname}_${gname}.out" >>"${run}/extract_blast_seq.sh"
fi

done
done

# Make the script executable
chmod +x ${run}/extract_blast_seq.sh
chmod +x ${run}/extract_blast_seq_frag.sh

# Run the script to extract all sequences
${run}/extract_blast_seq.sh &
${run}/extract_blast_seq_frag.sh &

# Wait for both commands to finish
wait
