import os
import glob

# Define the number of jobs per batch
batch_size = 10

# Get the list of Prokka command script files
prokka_script_files = glob.glob('/home/montoliu/psyringae_group/scripts_v2/genome_annotations/batch_scripts/prokka_commands_batch_*.sh')

# Create a counter for the config files
config_counter = 1

# Iterate over the Prokka script files and batch them
for i in range(0, len(prokka_script_files), batch_size):
    batch_files = prokka_script_files[i:i + batch_size]
    config_filename = f"/home/montoliu/psyringae_group/scripts_v2/genome_annotations/config_files/config_batch_{config_counter}.txt"
    
    # Write the batch to a config file
    with open(config_filename, 'w') as f:
        for job_number, script_file in enumerate(batch_files, start=1):
            f.write(f"{job_number} {script_file}\n")
    
    config_counter += 1
