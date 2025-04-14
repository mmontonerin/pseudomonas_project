#!/bin/bash
#SBATCH --job-name=prokka_pprotegens
#SBATCH --partition=long
#SBATCH --time=6-00:00:00
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --array=1-4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate prokka

# Read from the config file and get the filename corresponding to the array task ID
script=$(awk -v line=${SLURM_ARRAY_TASK_ID} 'NR==line {print $2}' config.txt)

chmod +x ${script}

${script}
