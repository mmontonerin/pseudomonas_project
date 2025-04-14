#!/bin/bash
#SBATCH --output=slurm_03_BLAST-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=8        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

# If results folder does not exist, it creates it
mkdir -p /home/montoliu/pprotegens/results/blastn

# Define directories:
ppro="/home/montoliu/pprotegens" #main directory of the analysis
as="/home/montoliu/pprotegens/data/assemblies" #assembly references
gen="/home/montoliu/pprotegens/data/genes" #genes to blast
result="/home/montoliu/pprotegens/results/blastn" #results folder
run="/home/montoliu/pprotegens/scripts" #scripts folder

# blast mut genes to the P. protegens genome assemblies

for assembly in ${as}/*.fasta
do 
    # Build a database from each of the genome assemblies
    #makeblastdb -in ${assembly} -dbtype nucl -parse_seqids

    for gene in ${gen}/*fasta
    do
        echo "BLASTing ${gene} in ${assembly}"
        # Simplify names of files
        aname=$(basename "$assembly" .fasta)
        gname=$(basename "$gene" .fasta)

        # If it does not exist, it crates a folder for the raw results and one for the best hits only
	# If it does not exist, it creates a folder for each gene
        mkdir -p ${result}/raw_blastn_out
        mkdir -p ${result}/blastn_out
        
        mkdir -p ${result}/raw_blastn_out/${gname}
        mkdir -p ${result}/blastn_out/${gname}

        # Run blastn with no filtering at all
        blastn -task blastn -num_threads 8 -db ${assembly} -query ${gene} -outfmt 6 -out ${result}/raw_blastn_out/${gname}/${aname}_${gname}.out	

        # Run blastn with e-value of 1e-50 to ensure no hits to homologs that are not the actual gene
        blastn -task blastn -num_threads 8 -db ${assembly} -query ${gene} -outfmt 6 -evalue 1e-50 -out ${result}/blastn_out/${gname}/${aname}_${gname}.out

done
done

for assembly in ${as}/*.fasta
do
    # Build a database from each of the genome assemblies
    #makeblastdb -in ${assembly} -dbtype nucl -parse_seqids

    for gene in ${gen}/aa/*fasta
    do
        echo "BLASTing ${gene} in ${assembly}"
        # Simplify names of files
        aname=$(basename "$assembly" .fasta)
        gname=$(basename "$gene" .fasta)

        # If it does not exist, it crates a folder for the raw results and one for the best hits only
        # If it does not exist, it creates a folder for each gene
        mkdir -p ${result}/raw_tblastn_out
        mkdir -p ${result}/tblastn_out

        mkdir -p ${result}/raw_tblastn_out/${gname}
        mkdir -p ${result}/tblastn_out/${gname}

        # Run blastn with no filtering at all
        tblastn -task tblastn -num_threads 8 -db ${assembly} -query ${gene} -outfmt 6 -out ${result}/raw_tblastn_out/${gname}/${aname}_${gname}.out

        # Run blastn with e-value of 1e-50 to ensure no hits to homologs that are not the actual gene
        tblastn -task tblastn -num_threads 8 -db ${assembly} -query ${gene} -outfmt 6 -evalue 1e-50 -out ${result}/tblastn_out/${gname}/${aname}_${gname}.out

done
done


