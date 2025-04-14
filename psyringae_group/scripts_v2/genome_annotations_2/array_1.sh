#!/bin/bash
#SBATCH --job-name=prokka_1
#SBATCH --partition=medium
#SBATCH --time=1-00:00:00
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --array=1-103
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate prokka

path_config='/home/montoliu/psyringae_group/scripts_v2/genome_annotations_2/config_files'

# Read from the config file and get the filename corresponding to the array task ID
script=$(awk -v line=${SLURM_ARRAY_TASK_ID} 'NR==line {print $2}' ${path_config}/config_batch_1.txt)

chmod +x ${script}

${script}
