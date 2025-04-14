#!/bin/bash
#SBATCH --output=jobname-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=1
#SBATCH --nodes=1                  # request for cores to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

conda activate

python ./02_create_master_table.py 

