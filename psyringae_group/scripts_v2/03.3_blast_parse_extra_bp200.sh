#!/bin/bash
#SBATCH --output=slurm-blast_extractseq-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=4        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=06:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

# Create sequences directories if they don't exist:
mkdir -p /home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness
mkdir -p /home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness/fragmented
mkdir -p /home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness_endcontig
mkdir -p /home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness_endcontig/fragmented

# Define directories:
ppro="/home/montoliu/psyringae_group" #main directory of the analysis
as="/home/montoliu/psyringae_group/data/assemblies" #assembly references
gen="/home/montoliu/psyringae_group/data/genes" #genes to blast
result="/home/montoliu/psyringae_group/results/blastn/blastn_out" #results folder
seq="/home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness" #extracted sequences folder
run="/home/montoliu/psyringae_group/scripts_v2" #scripts folder
frag="/home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness/fragmented" #extracted sequences folder for the fragmented assemblies
end="/home/montoliu/psyringae_group/results/sequences_200extrabp_contig_completeness_endcontig/" 

# Create empty script that will be used to append the commands to extract the sequences
#echo '#!/bin/bash' > ${run}/extract_blast_seq_extrabp200.sh
#echo '#!/bin/bash' > ${run}/extract_blast_seq_frag_extrabp200.sh


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
		
                mkdir -p ${end}/${gname}
                mkdir -p ${end}/fragmented/${gname}

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
                    				print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " (min_start-200) "-" (max_end+200) " -strand plus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" (min_start-200) "-" (max_end+200) "plus_200bp.fasta"
                			} else {
                    				print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " (max_end-200) "-" (min_start+200) " -strand minus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" (max_end-200) "-" (min_start+200) "minus_200bp.fasta"
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
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " (min_start-200) "-" (max_end+200) " -strand plus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" (min_start-200) "-" (max_end+200) "plus_200bp.fasta"
            			} else {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " (max_end-200) "-" (min_start+200) " -strand minus -out " seq "/" g_name "/" a_name "_" prev_contig_id "_" (max_end-200) "-" (min_start+200) "minus_200bp.fasta"
            			}
        		}' "${result}/${gname}/${aname}_${gname}.out" >>"${run}/extract_blast_seq_frag_extrabp200.sh"
		else
    		# Single hit or no hits on the same contig, extract sequences as before
    		awk -v assembly="$assembly" -v a_name="$aname" -v g_name="$gname" -v seq="$seq" -F"\t" '
        		{
            			if ($10 > $9) {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " ($9-200) "-" ($10+200) " -strand plus -out " seq "/" g_name "/" a_name "_" $2 "_" ($9-200) "-" ($10+200) "plus_200bp.fasta"
            			} else {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " ($10-200) "-" ($9+200) " -strand minus -out " seq "/" g_name "/" a_name "_" $2 "_" ($10-200) "-" ($9+200) "minus_200bp.fasta"
            			}
        		}' "${result}/${gname}/${aname}_${gname}.out" >>"${run}/extract_blast_seq_extrabp200.sh"
fi

done
done

#If there is negative values it means that the gene is found at the begining or the end of the contig, and we cannot trust the sequence, so we will put those separately

grep -E 'range -[0-9]+|--[0-9]+ -strand' ${run}/extract_blast_seq_extrabp200.sh > ${run}/extract_blast_seq_extrabp200_endcontig.sh
grep -E 'range -[0-9]+|--[0-9]+ -strand' ${run}/extract_blast_seq_frag_extrabp200.sh > ${run}/extract_blast_seq_frag_extrabp200_endcontig.sh 

grep -Ev 'range -[0-9]+|--[0-9]+ -strand' ${run}/extract_blast_seq_extrabp200.sh > ${run}/extract_blast_seq_extrabp200_complete.sh
grep -Ev 'range -[0-9]+|--[0-9]+ -strand' ${run}/extract_blast_seq_frag_extrabp200.sh > ${run}/extract_blast_seq_frag_extrabp200_complete.sh


# If the range gets negative, turn to 1 instead

sed -i -E 's/range -[0-9]+/range 1/g;s/--[0-9]+ -strand/-1 -strand/g;s/completeness/completeness_endcontig/g' ${run}/extract_blast_seq_extrabp200_endcontig.sh
sed -i -E 's/range -[0-9]+/range 1/g;s/--[0-9]+ -strand/-1 -strand/g;s/completeness/completeness_endcontig/g' ${run}/extract_blast_seq_frag_extrabp200_endcontig.sh


# Make the script executable
#chmod +x ${run}/extract_blast_seq_extrabp200_endcontig.sh
#chmod +x ${run}/extract_blast_seq_frag_extrabp200_endcontig.sh
chmod +x ${run}/extract_blast_seq_extrabp200_complete.sh
chmod +x ${run}/extract_blast_seq_frag_extrabp200_complete.sh

# Run the script to extract all sequences
${run}/extract_blast_seq_extrabp_complete.sh &
${run}/extract_blast_seq_frag_extrabp_complete.sh &
#${run}/extract_blast_seq_extrabp_endcontig.sh &
#${run}/extract_blast_seq_frag_extrabp_endcontig.sh &

# Wait for all commands to finish
wait
