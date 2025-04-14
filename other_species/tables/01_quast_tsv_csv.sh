#!/bin/bash

cd /home/montoliu/other_species/data/quast

mkdir -p stats_all

cd /home/montoliu/other_species/data/quast/pbra
mkdir -p stats_all

for folder_name in ./GCA*
do
	for report in ${folder_name}/transposed_report.tsv
	do
		sed 's/\t/,/g' ${report} > ./stats_all/${folder_name}.csv
	done
done 

cd /home/montoliu/other_species/data/quast/pflu
mkdir -p stats_all

for folder_name in ./GCA*
do
	for report in ${folder_name}/transposed_report.tsv
	do
		sed 's/\t/,/g' ${report} > ./stats_all/${folder_name}.csv
	done
done 

cd /home/montoliu/other_species/data/quast/psav
mkdir -p stats_all

for folder_name in ./GCA*
do
	for report in ${folder_name}/transposed_report.tsv
	do
		sed 's/\t/,/g' ${report} > ./stats_all/${folder_name}.csv
	done
done 

cd /home/montoliu/other_species/data/quast/pvir
mkdir -p stats_all

for folder_name in ./GCA*
do
	for report in ${folder_name}/transposed_report.tsv
	do
		sed 's/\t/,/g' ${report} > ./stats_all/${folder_name}.csv
	done
done 