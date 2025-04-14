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

gene="/home/montoliu/psyringae_group/data/genes" #genes to blast
dir="/home/montoliu/psyringae_group/mut_genes/ffn_renamed"
run="/home/montoliu/psyringae_group/mut_genes/"
seq="/home/montoliu/psyringae_group/mut_genes/mut_sequences"
results="/home/montoliu/psyringae_group/mut_genes/blast_results"

mkdir -p ${seq} 
echo '#!/bin/bash' > ${run}/06_extract_blast_seq.sh

for db in ${dir}/*ffn 
do
	for mut in ${gene}/*fasta
	do
        	dbname=$(basename "$db" .ffn)
        	gname=$(basename "$mut" .fasta)
 
        	mkdir -p ${seq}/${gname}

		awk -v database="$db" -v db_name="${dbname}" -v g_name="${gname}" -v seq="${seq}" -F"\t" 'NR==1 {contig_id = $2; print "blastdbcmd -db " database " -dbtype nucl -entry " contig_id " -out " seq "/" g_name "/" db_name ".fasta"}' "${results}/${gname}/${dbname}_${gname}.out" >> ${run}/06_extract_blast_seq.sh

done
done 