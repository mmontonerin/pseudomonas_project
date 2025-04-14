#!/bin/bash
#SBATCH --output=slurm_01_download_dataset-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH -J ncbi_download_dataset
#SBATCH --partition=medium 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=1-00:00:00          # total run time limit in DD-HH:MM:SS

# Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate ncbi_datasets

# Datasets of Pseudomonas protegens: taxid=380021

cd /home/montoliu/pprotegens/data

datasets download genome taxon "380021" --include genome,protein,gff3 --assembly-source GenBank
