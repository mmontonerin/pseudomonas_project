#!/bin/bash
#SBATCH --output=blast-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

run="/home/montoliu/psyringae_group/mut_genes/protein_analysis"

chmod +x ${run}/blastdbcmd_commands.sh

${run}/blastdbcmd_commands.sh