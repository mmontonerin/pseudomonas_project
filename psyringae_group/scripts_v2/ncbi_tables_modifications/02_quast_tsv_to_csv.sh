#!/bin/bash

cd /home/montoliu/psyringae_group/results/quast

mkdir stats_all

for folder_name in ./GCA*
do
	for report in ./${folder_name}/transposed_report.tsv
	do
		sed 's/\t/,/g' ${report} > ./stats_all/${folder_name}.csv
	done
done 





