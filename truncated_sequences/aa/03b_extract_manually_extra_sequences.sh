#!/bin/bash
#Load modules
module use /beegfs/easybuild/CentOS/7.6.1810/Skylake/modules/all
module use /beegfs/easybuild/common/modules/all

ml BLAST+/2.9.0-gompi-2019a

blastdbcmd -db /home/montoliu/other_species/mut_genes/faa_files_renamed/pflu/GCA_028869255.1.faa -dbtype prot -entry pflu00520_DFGLHBMA_04928 -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/pflu_mutL_GCA_000194805.1_new.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/pflu/GCA_963970985.1_RL_5y_Pfl2_36_genomic.fasta -dbtype nucl -entry CAXAQK010000019.1 -range 101777-102556 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/pflu_uvrD_GCA_963970985.1_RL_5y_Pfl2_36_genomic_new1.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/pflu/GCA_963970985.1_RL_5y_Pfl2_36_genomic.fasta -dbtype nucl -entry CAXAQK010000012.1 -range 5-1520 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/pflu_uvrD_GCA_963970985.1_RL_5y_Pfl2_36_genomic_new2.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/psav/GCA_001401285.1_PsvICMP4352_genomic.fasta -dbtype nucl -entry LJRJ01000121.1 -range 3-2417 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/psav_mutS_GCA_001401285.1_PsvICMP4352_genomic_new1.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/psav/GCA_001401285.1_PsvICMP4352_genomic.fasta -dbtype nucl -entry LJRJ01000084.1 -range 44708-44874 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/psav_mutS_GCA_001401285.1_PsvICMP4352_genomic_new2.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/psav/GCA_003699215.1_ASM369921v1_genomic.fasta -dbtype nucl -entry RBPF01000158.1 -range 1-2415 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/psav_mutS_GCA_003699215.1_ASM369921v1_genomic_new1.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/psav/GCA_003699215.1_ASM369921v1_genomic.fasta -dbtype nucl -entry RBPF01000287.1 -range 42891-43057 -strand plus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/psav_mutS_GCA_003699215.1_ASM369921v1_genomic_new2.fasta
blastdbcmd -db /home/montoliu/other_species/data/genome_assemblies/pflu/GCA_009818265.1_ASM981826v1_genomic.fasta -dbtype nucl -entry CP046874.1 -range 365915-366973 -strand minus -out /home/montoliu/truncated_sequences/aa/manual_check_lastones/pflu_mutY_GCA_009818265.1_ASM981826v1_genomic_new.fasta
