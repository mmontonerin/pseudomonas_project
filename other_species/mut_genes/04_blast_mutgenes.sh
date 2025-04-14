#!/bin/bash
#SBATCH --output=blast-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=2        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

gene="/home/montoliu/other_species/mut_genes/genes" #genes to blast
faa_dir="/home/montoliu/other_species/mut_genes/faa_files_renamed"
ffn_dir="/home/montoliu/other_species/mut_genes/ffn_files_renamed"
ffn_results="/home/montoliu/other_species/mut_genes/blast_results_ffn"
faa_results="/home/montoliu/other_species/mut_genes/blast_results_faa"

mkdir -p ${faa_results}
mkdir -p ${faa_results}/blast_raw

mkdir -p ${ffn_results}
mkdir -p ${ffn_results}/blast_raw

(
for prefix in pbra pflu psav pvir
do
    mkdir -p ${ffn_results}/${prefix}
    mkdir -p ${ffn_results}/blast_raw/${prefix}

    for db in ${ffn_dir}/${prefix}/*ffn 
    do
	    for mut in ${gene}/*_nt.fasta
	    do
        	dbname=$(basename "$db" .ffn)
        	gname=$(basename "$mut" _nt.fasta)
 
        	mkdir -p ${ffn_results}/blast_raw/${prefix}/${gname}
            mkdir -p ${ffn_results}/${prefix}/${gname}

	        # Run blastn with filtering and no filtering
        	blastn -task blastn -db ${db} -query ${mut} -outfmt 6 -evalue 1e-25 -out ${ffn_results}/${prefix}/${gname}/${dbname}_${gname}.out 
            blastn -task blastn -db ${db} -query ${mut} -outfmt 6 -out ${ffn_results}/blast_raw/${prefix}/${gname}/${dbname}_${gname}.out 
        done
    done
done
) &

(
for prefix in pbra pflu psav pvir
do
    mkdir -p ${faa_results}/${prefix}
    mkdir -p ${faa_results}/blast_raw/${prefix}

    for db in ${faa_dir}/${prefix}/*faa 
    do
	    for mut in ${gene}/*_aa.fasta
	    do
        	dbname=$(basename "$db" .faa)
        	gname=$(basename "$mut" _aa.fasta)
 
        	mkdir -p ${faa_results}/blast_raw/${prefix}/${gname}
            mkdir -p ${faa_results}/${prefix}/${gname}

	        # Run blastp with filtering and no filtering
        	blastp -task blastp -db ${db} -query ${mut} -outfmt 6 -evalue 1e-25 -out ${faa_results}/${prefix}/${gname}/${dbname}_${gname}.out 
            blastp -task blastp -db ${db} -query ${mut} -outfmt 6 -out ${faa_results}/blast_raw/${prefix}/${gname}/${dbname}_${gname}.out 
        done
    done
done
) &


wait