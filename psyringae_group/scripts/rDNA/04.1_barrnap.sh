#!/bin/bash
#SBATCH --output=slurm_barrnap-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=8        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

# Load conda environment
source /home/montoliu/miniconda3/etc/profile.d/conda.sh
conda activate rdna

# If results folder does not exist, it creates it
mkdir -p /home/montoliu/psyringae_group/results/rDNA/barrnap

# Define directories:
ppro="/home/montoliu/psyringae_group" #main directory of the analysis
as="/home/montoliu/psyringae_group/data/assemblies" #assembly references
gen="/home/montoliu/psyringae_group/data/genes/others" #genes to blast
result="/home/montoliu/psyringae_group/results/rDNA/barrnap" #results folder
run="/home/montoliu/psyringae_group/scripts" #scripts folder

# blast rDNA 18S to the P. syringaes genome assemblies

for assembly in ${as}/*.fasta
do 
    # Build a database from each of the genome assemblies
    #makeblastdb -in ${assembly} -dbtype nucl -parse_seqids
    # Simplify names of files
    aname=$(basename "$assembly" .fasta)
    
    barrnap --threads 8 --kingdom bac 

    # Run blastn with e-value of 1e-50 to ensure no hits to homologs that are not the actual gene
    blastn -task blastn -num_threads 8 -db ${assembly} -query ${gen}/16s.fasta -outfmt 6 -evalue 1e-10 -word_size 1500 -out ${result}/${aname}_16s.out

done

