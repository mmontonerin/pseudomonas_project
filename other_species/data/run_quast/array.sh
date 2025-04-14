#!/bin/bash
#SBATCH --job-name=quast_othersp
#SBATCH --partition=medium
#SBATCH --time=1-00:00:00
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --array=1-105
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

# Activate conda to use Quast
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate quast

path_config='/home/montoliu/other_species/data/run_quast'

# Read from the config file and get the filename corresponding to the array task ID
script=$(awk -v line=${SLURM_ARRAY_TASK_ID} 'NR==line {print $2}' ${path_config}/quast_config.txt)

chmod +x ${script}

${script}