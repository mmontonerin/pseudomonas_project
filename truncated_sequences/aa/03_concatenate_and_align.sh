#!/bin/bash
#SBATCH --output=mafft-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=fast 
#SBATCH --time=02:00:00          # total run time limit in DD-HH:MM:SS

module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml MAFFT/7.505-GCC-11.3.0-with-extensions

path="/home/montoliu/truncated_sequences/aa"

for prefix in pbra pflu ppro psav psyr pvir
do
    for mut in dnaQ mutS mutL mutT mutY uvrD
    do
        #Concatenate files
        cat ${path}/${prefix}/master_seq/${prefix}_${mut}_master_sequence.fasta > ${path}/${prefix}/${prefix}_${mut}.fasta
        echo 'concatenating ${path}/${prefix}/master_seq/${prefix}_${mut}_master_sequence.fasta'
        cat ${path}/${prefix}/${mut}/*.fasta >> ${path}/${prefix}/${prefix}_${mut}.fasta

        #Align files
        mafft ${path}/${prefix}/${prefix}_${mut}.fasta > ${path}/${prefix}/${prefix}_${mut}_mafft.fasta
    done
done