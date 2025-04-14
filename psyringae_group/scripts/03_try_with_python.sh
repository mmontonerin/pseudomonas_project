#!/bin/bash
#SBATCH --output=slurm_03_blast_psyr-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=8        # number of cores
#SBATCH --nodes=1                      # request for cores to be in the same node
#SBATCH --partition=long 
#SBATCH --time=2-00:00:00          # total run time limit in DD-HH:MM:SS


# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

source /home/montoliu/miniconda3/etc/profile.d/conda.sh
# For python
conda activate


# Define directories:
psyr="/home/montoliu/psyringae_group" #main directory of the analysis
as="/home/montoliu/psyringae_group/data/assemblies" #assembly references
gen="/home/montoliu/psyringae_group/data/genes" #genes to blast
result="/home/montoliu/psyringae_group/results/blastn" #results folder
seq="/home/montoliu/psyringae_group/results/sequences" #extracted sequences folder
run="/home/montoliu/psyringae_group/scripts" #scripts folder
frag="/home/montoliu/psyringae_group/results/sequences/fragmented" #extracted sequences folder for the frafmented assemblies

# Create empty script that will be used to append the commands to extract the sequences
echo '#!/bin/bash' > ${run}/extract_blast_seq.sh
echo '#!/bin/bash' > ${run}/extract_blast_seq_frag.sh

# blast mut genes to the P. syringae genome assemblies

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

		# If it does not exist, it creates a folder for each gene
                mkdir -p ${result}/${gname}
		# If it does not exist, it creates a folder for each gene
                mkdir -p ${seq}/${gname}
		mkdir -p ${frag}/${gname}

                blastn -task blastn -num_threads 8 -db ${assembly} -query ${gene} -outfmt 6 -evalue 0.01 -out ${result}/${gname}/${aname}_${gname}.out
		python create_extract_seq_scripts.py --assembly ${assembly} --aname ${aname} --gname ${gname} --seq ${seq} --result ${result} --run ${run} 
done
done






