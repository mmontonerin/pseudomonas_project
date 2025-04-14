#!/bin/bash
#SBATCH --job-name=busco_othersp
#SBATCH --partition=medium
#SBATCH --time=1-00:00:00
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --array=1-261
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BUSCO/5.1.2-foss-2019a

path_config='/home/montoliu/other_species/data/run_busco'

# Read from the config file and get the filename corresponding to the array task ID
script=$(awk -v line=${SLURM_ARRAY_TASK_ID} 'NR==line {print $2}' ${path_config}/busco_config.txt)

chmod +x ${script}

${script}