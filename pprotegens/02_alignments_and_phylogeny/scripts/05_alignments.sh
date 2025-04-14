#!/bin/bash
#SBATCH --output=slurm_macse-%j.%N.out # STDOUT file, %j for job id, %N for hostname
#SBATCH --ntasks=6        
#SBATCH --nodes=1                      # request for tasks to be in the same node
#SBATCH --partition=medium 
#SBATCH --time=12:00:00          # total run time limit in DD-HH:MM:SS

# Iniciate conda for alignments to use MACSE 2
source /home/montoliu/miniconda3/etc/profile.d/conda.sh

conda activate ali

# Define directories:
seq="/home/montoliu/pprotegens/01_select_assemblies/results/sequences_extrabp_selection"
ali="/home/montoliu/pprotegens/02_alignments_and_phylogeny/results/alignments"

mkdir -p /home/montoliu/pprotegens/02_alignments_and_phylogeny/results/alignments

#If it has run already, remove files to re-run it again and not concatenate
rm ${ali}/*.fasta

cd ${seq}
cat mutT/*fasta >> ${ali}/mutT.fasta &
cat uvrD/*fasta >> ${ali}/uvrD.fasta &
cat dnaQ/*fasta >> ${ali}/dnaQ.fasta &
cat mutY/*fasta >> ${ali}/mutY.fasta &
cat mutL/*fasta >> ${ali}/mutL.fasta &
cat mutS/*fasta >> ${ali}/mutS.fasta &

# Wait for all concatenations to finish
wait

sed -i 's/>[^_]\+_/>ppro/g' ${ali}/mutL.fasta &
sed -i 's/>[^_]\+_/>ppro/g' ${ali}/uvrD.fasta &
sed -i 's/>[^_]\+_/>ppro/g' ${ali}/dnaQ.fasta &
sed -i 's/>[^_]\+_/>ppro/g' ${ali}/mutT.fasta &
sed -i 's/>[^_]\+_/>ppro/g' ${ali}/mutY.fasta &
sed -i 's/>[^_]\+_/>ppro/g' ${ali}/mutS.fasta &

wait

macse -prog alignSequences -seq ${ali}/mutT.fasta -gc_def 11 -out_AA ${ali}/mutT_AA.fasta -out_NT ${ali}/mutT_NT.fasta &
macse -prog alignSequences -seq ${ali}/uvrD.fasta -gc_def 11 -out_AA ${ali}/uvrD_AA.fasta -out_NT ${ali}/uvrD_NT.fasta &
macse -prog alignSequences -seq ${ali}/dnaQ.fasta -gc_def 11 -out_AA ${ali}/dnaQ_AA.fasta -out_NT ${ali}/dnaQ_NT.fasta &
macse -prog alignSequences -seq ${ali}/mutY.fasta -gc_def 11 -out_AA ${ali}/mutY_AA.fasta -out_NT ${ali}/mutY_NT.fasta &
macse -prog alignSequences -seq ${ali}/mutL.fasta -gc_def 11 -out_AA ${ali}/mutL_AA.fasta -out_NT ${ali}/mutL_NT.fasta &
macse -prog alignSequences -seq ${ali}/mutS.fasta -gc_def 11 -out_AA ${ali}/mutS_AA.fasta -out_NT ${ali}/mutS_NT.fasta &

wait

macse -prog exportAlignment -gc_def 11 -align ${ali}/mutT_NT.fasta -out_stat_per_seq ${ali}/mutT_stats_per_seq_nt.csv -out_stat_per_site ${ali}/mutT_stats_per_site_nt.csv &
macse -prog exportAlignment -gc_def 11 -align ${ali}/uvrD_NT.fasta -out_stat_per_seq ${ali}/uvrD_stats_per_seq_nt.csv -out_stat_per_site ${ali}/uvrD_stats_per_site_nt.csv &
macse -prog exportAlignment -gc_def 11 -align ${ali}/dnaQ_NT.fasta -out_stat_per_seq ${ali}/dnaQ_stats_per_seq_nt.csv -out_stat_per_site ${ali}/dnaQ_stats_per_site_nt.csv &
macse -prog exportAlignment -gc_def 11 -align ${ali}/mutY_NT.fasta -out_stat_per_seq ${ali}/mutY_stats_per_seq_nt.csv -out_stat_per_site ${ali}/mutY_stats_per_site_nt.csv &
macse -prog exportAlignment -gc_def 11 -align ${ali}/mutL_NT.fasta -out_stat_per_seq ${ali}/mutL_stats_per_seq_nt.csv -out_stat_per_site ${ali}/mutL_stats_per_site_nt.csv &
macse -prog exportAlignment -gc_def 11 -align ${ali}/mutS_NT.fasta -out_stat_per_seq ${ali}/mutS_stats_per_seq_nt.csv -out_stat_per_site ${ali}/mutS_stats_per_site_nt.csv &

wait





