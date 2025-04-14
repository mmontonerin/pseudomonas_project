#!/bin/bash
#SBATCH --output=mafft-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml MAFFT/7.505-GCC-11.3.0-with-extensions

out_nt="/home/montoliu/other_species/mut_genes/alignments_nt"
out_aa="/home/montoliu/other_species/mut_genes/alignments_aa"

for prefix in pbra pflu psav pvir
do
	for mut in mutS mutT mutY mutL dnaQ uvrD
        do
                mafft ${out_nt}/${prefix}/${mut}_id.fasta > ${out_nt}/${prefix}/${mut}_mafft.fasta
                mafft ${out_aa}/${prefix}/${mut}_id.fasta > ${out_aa}/${prefix}/${mut}_mafft.fasta

        done
done