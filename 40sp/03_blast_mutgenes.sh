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

gene="/home/montoliu/40sp/mut_genes_ecoli" #genes to blast
dir="/home/montoliu/40sp/data_renamed"
results="/home/montoliu/40sp/blast_results"

mkdir -p ${results}
mkdir -p ${results}/blastn_raw

#Create database from annotation fna files

for db in ${dir}/*faa 
do
	for mut in ${gene}/*fasta
	do
        	dbname=$(basename "$db" .faa)
        	gname=$(basename "$mut" .fasta)
 
        	mkdir -p ${results}/blastn_raw/${gname}
            mkdir -p ${results}/${gname}

	        # Run blastn with filtering and no filtering
        	blastp -task blastp -db ${db} -query ${mut} -outfmt 6 -evalue 1e-04 -out ${results}/${gname}/${dbname}_${gname}.out 
            blastp -task blastp -db ${db} -query ${mut} -outfmt 6 -out ${results}/blastn_raw/${gname}/${dbname}_${gname}.out 

done
done