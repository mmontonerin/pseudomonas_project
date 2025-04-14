#!/bin/bash
#SBATCH --output=blast_othersp-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=8        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=long 
#SBATCH --time=5-00:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

# Define directories:
gene="/home/montoliu/other_species/mut_genes/genes" #genes to blast
as="/home/montoliu/other_species/data/genome_assemblies" #assembly references
results="/home/montoliu/other_species/blast_analyses_filter/blast_results"
run="/home/montoliu/other_species/blast_analyses_filter" #scripts folder
seq="/home/montoliu/other_species/blast_analyses_filter/mut_sequences"
#frag="/home/montoliu/other_species/blast_analyses_filter/mut_sequences/fragmented" #extracted sequences folder for the frafmented assemblies

# Create empty script that will be used to append the commands to extract the sequences
#echo '#!/bin/bash' > ${run}/extract_blast_seq.sh
#echo '#!/bin/bash' > ${run}/extract_blast_seq_frag.sh

for prefix in pbra pflu psav pvir
do
    mkdir -p ${results}/${prefix}
    mkdir -p ${results}/blast_raw/${prefix}

	mkdir -p ${seq}/${prefix}

    for db in ${as}/${prefix}/*fasta
    do
        #Create blast database
        #makeblastdb -in ${db} -dbtype nucl -parse_seqids

	    for mut in ${gene}/*_nt.fasta
	    do
        	dbname=$(basename "$db" .fasta)
        	gname=$(basename "$mut" _nt.fasta)
 
        	mkdir -p ${results}/blast_raw/${prefix}/${gname}
            mkdir -p ${results}/${prefix}/${gname}
			mkdir -p ${seq}/${prefix}/${gname}
			mkdir -p ${seq}/${prefix}/fragmented/${gname}

	        # Run blastn with filtering and no filtering
        	#blastn -task blastn -num_threads 8 -db ${db} -query ${mut} -outfmt 6 -evalue 1e-50 -out ${results}/${prefix}/${gname}/${dbname}_${gname}.out 
            #blastn -task blastn -num_threads 8 -db ${db} -query ${mut} -outfmt 6 -out ${results}/blast_raw/${prefix}/${gname}/${dbname}_${gname}.out 


		    # Prepare a script to extract the specific gene sequences for each genome assembly but separate the ones that are fragmented
		    if [[ $(wc -l <"${results}/${prefix}/${gname}/${dbname}_${gname}.out") -ge 2 ]]; then
    		    # Multiple hits on the same contig, extract full sequence range
    		    awk -v assembly="$db" -v prefix="$prefix" -v a_name="$dbname" -v g_name="$gname" -v seq="$seq" -F"\t" '
        		    NR==1 {
				    contig_id = $2
            			min_start = ($10 < $9) ? $9 : $10
            			max_end = ($10 > $9) ? $10 : $9
        		    }
        		    {
				
				    if ($2 != contig_id) {
                		next
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
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " min_start "-" max_end " -strand plus -out " seq "/" prefix "/fragmented/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "plus.fasta"
            			} else {
                			print "blastdbcmd -db " assembly " -dbtype nucl -entry " prev_contig_id " -range " max_end "-" min_start " -strand minus -out " seq "/" prefix "/fragmented/" g_name "/" a_name "_" prev_contig_id "_" min_start "-" max_end "minus.fasta"
            			}
        		    }' "${results}/${prefix}/${gname}/${dbname}_${gname}.out" >> "${run}/${prefix}_extract_blast_seq_frag_fix.sh"
            #else
    		# Single hit or no hits on the same contig, extract sequences as normal
    		#awk -v assembly="$db" -v prefix="$prefix" -v a_name="$dbname" -v g_name="$gname" -v seqf="$frag" -v seq="$seq" -F"\t" '
        		#{
            			#if ($10 > $9) {
                		#	print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $9 "-" $10 " -strand plus -out " seq "/" prefix "/" g_name "/" a_name "_" $2 "_" $9 "-" $10 "plus.fasta"
            			#} else {
                		#	print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $10 "-" $9 " -strand minus -out " seq "/" prefix "/" g_name "/" a_name "_" $2 "_" $9 "-" $10 "minus.fasta"
            			#}
        		#}' "${results}/${prefix}/${gname}/${dbname}_${gname}.out" >> "${run}/${prefix}_extract_blast_seq.sh"
		    fi
        done
    done

# Make the script executable
chmod +x ${run}/${prefix}_extract_blast_seq.sh
chmod +x ${run}/${prefix}_extract_blast_seq_frag_fix.sh
# Run the script to extract all sequences
echo "extracting BLAST sequences ${prefix}"
${run}/${prefix}_extract_blast_seq.sh
${run}/${prefix}_extract_blast_seq_frag_fix.sh

done

