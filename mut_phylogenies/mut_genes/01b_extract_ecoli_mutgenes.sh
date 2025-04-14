#!/bin/bash
#SBATCH --output=makeblastdb-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

dir="/home/montoliu/mut_phylogenies/mut_genes/ecoli"

file="/home/montoliu/mut_phylogenies/data/refsp/ecol_refsp.faa"

#Create database from annotation faa file
#makeblastdb -in ${file} -dbtype prot -parse_seqids 	

gene="/home/montoliu/other_species/mut_genes/genes" #gene folder to blast

for mut in ${gene}/*_aa.fasta
do
    gname=$(basename "$mut" _aa.fasta)

	# Run blastp with filtering and no filtering
    #blastp -task blastp -db ${file} -query ${mut} -outfmt 6 -out ${dir}/ecoli_${gname}.out 

    awk -v database="${file}" -v g_name="${gname}" -v seq="${dir}" -F"\t" 'NR==1 {contig_id = $2; print "blastdbcmd -db " database " -dbtype prot -entry " contig_id " -out " seq "/ecoli_" g_name ".fasta"}' "${dir}/ecoli_${gname}.out" >> 01c_blastdbcmd_faa.sh        
done

chmod +x 01c_blastdbcmd_faa.sh

./01c_blastdbcmd_faa.sh