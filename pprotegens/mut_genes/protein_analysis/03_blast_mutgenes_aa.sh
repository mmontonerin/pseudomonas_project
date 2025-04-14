#!/bin/bash
#SBATCH --output=blast-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

gene="/home/montoliu/pprotegens/data/genes/aa" #genes to blast
faa_dir="/home/montoliu/pprotegens/mut_genes/protein_analysis/faa_renamed"
faa_results="/home/montoliu/pprotegens/mut_genes/protein_analysis/blast_results_faa"
seq_faa="/home/montoliu/pprotegens/mut_genes/protein_analysis/mut_sequences"
run="/home/montoliu/pprotegens/mut_genes/protein_analysis"

mkdir -p ${faa_results}

    for db in ${faa_dir}/*faa 
    do
	    for mut in ${gene}/*_aa.fasta
	    do
        	dbname=$(basename "$db" .faa)
        	gname=$(basename "$mut" _aa.fasta)
 
        	mkdir -p ${faa_results}/${gname}

	        # Run blastp with filtering and no filtering
            blastp -task blastp -db ${db} -query ${mut} -outfmt 6 -out ${faa_results}/${gname}/${dbname}_${gname}.out 

            mkdir -p ${seq_faa}/${gname}
            awk -v database="$db" -v db_name="${dbname}" -v g_name="${gname}" -v seq="${seq_faa}" -F"\t" 'NR==1 {contig_id = $2; print "blastdbcmd -db " database " -dbtype prot -entry " contig_id " -out " seq "/" g_name "/" db_name ".fasta"}' "${faa_results}/${gname}/${dbname}_${gname}.out" >> ${run}/04_blastdbcmd_faa.sh        
        done
    done
