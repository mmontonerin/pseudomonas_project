#!/bin/bash
#SBATCH --output=concatenate-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=2:00:00          # total run time limit in DD-HH:MM:SS

dir="/home/montoliu/psyringae_group/mut_genes/mut_sequences"

out="/home/montoliu/psyringae_group/mut_genes/alignments"

mkdir -p ${out}

for file in ${dir}/mutS/*fasta
do
	cat $file >> ${out}/mutS.fasta
done

for file in ${dir}/mutL/*fasta
do
        cat $file >> ${out}/mutL.fasta
done

for file in ${dir}/uvrD/*fasta
do
        cat $file >> ${out}/uvrD.fasta
done

for file in ${dir}/mutT/*fasta
do
        cat $file >> ${out}/mutT.fasta
done

for file in ${dir}/mutY/*fasta
do
        cat $file >> ${out}/mutY.fasta
done

for file in ${dir}/dnaQ/*fasta
do
        cat $file >> ${out}/dnaQ.fasta
done

