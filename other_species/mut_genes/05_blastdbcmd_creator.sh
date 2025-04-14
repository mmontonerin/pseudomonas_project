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

gene="/home/montoliu/other_species/mut_genes/genes"
faa_dir="/home/montoliu/other_species/mut_genes/faa_files_renamed"
ffn_dir="/home/montoliu/other_species/mut_genes/ffn_files_renamed"
ffn_results="/home/montoliu/other_species/mut_genes/blast_results_ffn"
faa_results="/home/montoliu/other_species/mut_genes/blast_results_faa"
seq_faa="/home/montoliu/other_species/mut_genes/mut_sequences_protein"
seq_ffn="/home/montoliu/other_species/mut_genes/mut_sequences_nt"
run="/home/montoliu/other_species/mut_genes"

mkdir -p ${seq_ffn}
mkdir -p ${seq_faa}
echo '#!/bin/bash' > ${run}/06_extract_blast_seq_faa.sh
echo '#!/bin/bash' > ${run}/06_extract_blast_seq_ffn.sh

(
for prefix in pbra pflu psav pvir
do
	mkdir -p ${seq_ffn}/${prefix}
	for db in ${ffn_dir}/${prefix}/*ffn  
	do
		for mut in ${gene}/*_nt.fasta
	    do
        	dbname=$(basename "$db" .ffn)
        	gname=$(basename "$mut" _nt.fasta)
 
        	mkdir -p ${seq_ffn}/${prefix}/${gname}

			awk -v prefix="$prefix" -v database="$db" -v db_name="${dbname}" -v g_name="${gname}" -v seq="${seq_ffn}" -F"\t" 'NR==1 {contig_id = $2; print "blastdbcmd -db " database " -dbtype nucl -entry " contig_id " -out " seq "/" prefix "/" g_name "/" db_name ".fasta"}' "${ffn_results}/blast_raw/${prefix}/${gname}/${dbname}_${gname}.out" >> ${run}/06_extract_blast_seq_ffn.sh

		done
	done
done 
) &

(
for prefix in pbra pflu psav pvir
do
	mkdir -p ${seq_faa}/${prefix}
	for db in ${faa_dir}/${prefix}/*faa  
	do
		for mut in ${gene}/*_aa.fasta
	    do
        	dbname=$(basename "$db" .faa)
        	gname=$(basename "$mut" _aa.fasta)
 
        	mkdir -p ${seq_faa}/${prefix}/${gname}

			awk -v prefix="$prefix" -v database="$db" -v db_name="${dbname}" -v g_name="${gname}" -v seq="${seq_faa}" -F"\t" 'NR==1 {contig_id = $2; print "blastdbcmd -db " database " -dbtype prot -entry " contig_id " -out " seq "/" prefix "/" g_name "/" db_name ".fasta"}' "${faa_results}/blast_raw/${prefix}/${gname}/${dbname}_${gname}.out" >> ${run}/06_extract_blast_seq_faa.sh

		done
	done
done 
) &

wait