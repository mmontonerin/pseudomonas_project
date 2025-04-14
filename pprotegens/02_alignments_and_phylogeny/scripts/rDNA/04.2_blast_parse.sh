#!/bin/bash
#SBATCH --output=slurm-blast_extractseq-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=06:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

# Create sequences directories if they don't exist:
mkdir -p /home/montoliu/pprotegens/results/rDNA/sequences

# Define directories:
ppro="/home/montoliu/pprotegens" #main directory of the analysis
as="/home/montoliu/pprotegens/data/assemblies" #assembly references
gen="/home/montoliu/pprotegens/data/genes" #genes to blast
result="/home/montoliu/pprotegens/results/rDNA" #results folder
seq="/home/montoliu/pprotegens/results/rDNA/sequences" #extracted sequences folder
run="/home/montoliu/pprotegens/scripts/rDNA" #scripts folder


# Create empty script that will be used to append the commands to extract the sequences
echo '#!/bin/bash' > ${run}/extract_blast_seq.sh

for assembly in ${as}/*.fasta
do 
    # Simplify names of files
    aname=$(basename "$assembly" .fasta)
    awk -v assembly="$assembly" -v a_name="$aname" -v seq="$seq" -F"\t" 'NR==1 {
            if ($10 > $9) {
                    print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $9 "-" $10 " -strand plus -out " seq "/" a_name "_" $2 "_" $9 "-" $10 "plus.fasta"
            } else {
                    print "blastdbcmd -db " assembly " -dbtype nucl -entry " $2 " -range " $10 "-" $9 " -strand minus -out " seq "/" a_name "_" $2 "_" $9 "-" $10 "minus.fasta"
            }
    }' ${result}/${aname}_16s.out >> ${run}/extract_blast_seq.sh

done

# Make the script executable
chmod +x ${run}/extract_blast_seq.sh

# Run the script to extract all sequences
${run}/extract_blast_seq.sh 

