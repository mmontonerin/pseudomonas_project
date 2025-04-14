#!/bin/bash
#SBATCH --output=slurm-busco_pprotegens-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J busco-pprotegens_assemblies
#SBATCH --ntasks=40        
#SBATCH --nodes=1                  
#SBATCH --partition=long 
#SBATCH --time=2-00:00:00          # total run time limit in DD-HH:MM:SS

module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BUSCO/5.1.2-foss-2019a

# If result folder does not exist, creates it:
mkdir -p /home/montoliu/pprotegens/results/busco

# Define directories:
ppro="/home/montoliu/pprotegens" #main directory of the project
as="/home/montoliu/pprotegens/data/assemblies" #assembly references
result="/home/montoliu/pprotegens/results/busco" #results folder

# Run BUSCO for all assembly files:

for assembly in ${as}/*.fasta
do 
	aname=$(basename "$assembly" .fasta)
	busco -i ${assembly} -l pseudomonadales_odb10 -o ${aname} -m genome -c 40 --out_path ${result}

done
