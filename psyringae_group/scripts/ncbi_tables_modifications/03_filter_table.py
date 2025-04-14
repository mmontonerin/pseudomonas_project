import pandas as pd
import re
import argparse

def filter_table(input_file):
    # Read the input table
    df_fn = pd.read_csv(input_file)

    #### Filter out genes that appear fragmented and in different contigs

    # We have two types of fragmented genes
    # fragmented:1299_1207 # Pieces of the gene are in separate contigs
    # fragmented:3054 # Pieces of the gene are in the same contig, and we extracted the sequence in between as well

    # Define a regular expression pattern to match fragmented values with only one number after the colon
    # We want those to be included in the final table
    pattern_frag = r'^fragmented:\d+(?:_\d+)+$'
    pattern_N = r'\d+N$'
    min_length = 4000000
    max_length = 8000000
    busco_complete = 95.0 
    contigs = 400    

    # Define the condition to filter out lines with 'fragmented' values containing multiple numbers
    # Those containing multiple numbers are fragmented in multiple contigs, thus we do not want those.
    
    df_condition_pass = pd.DataFrame(columns=df_fn.columns)
    df_condition_fail = pd.DataFrame(columns=df_fn.columns)

    # Iterate over each row of the DataFrame
    for index, row in df_fn.iterrows():
        if re.match(pattern_frag, str(row['dnaQ'])): 
            df_condition_fail.loc[index] = row
        elif re.match(pattern_frag, str(row['mutT'])):
            df_condition_fail.loc[index] = row 
        elif re.match(pattern_frag, str(row['mutL'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_frag, str(row['mutS'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_frag, str(row['mutY'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_frag, str(row['uvrD'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_N, str(row['dnaQ'])): 
            df_condition_fail.loc[index] = row
        elif re.match(pattern_N, str(row['mutT'])):
            df_condition_fail.loc[index] = row 
        elif re.match(pattern_N, str(row['mutL'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_N, str(row['mutS'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_N, str(row['mutY'])):
            df_condition_fail.loc[index] = row
        elif re.match(pattern_N, str(row['uvrD'])):
            df_condition_fail.loc[index] = row
        elif row['Total_length'] < min_length or row['Total_length'] > max_length:
            df_condition_fail.loc[index] = row
        elif row['BUSCO-C'] < busco_complete:
            df_condition_fail.loc[index] = row
        elif row['#Contigs'] > contigs:
            df_condition_fail.loc[index] = row
        else:
            df_condition_pass.loc[index] = row 

    
    # Save filtered data to one file
    df_condition_fail.to_csv('filtered_out_4.csv', index=False)

    # Save unfiltered data to another file
    df_condition_pass.to_csv('final_table_of_genome_assemblies_4.csv', index=False)

# Filter 1 set to     
#    min_length = 4000000
#    max_length = 8000000
#    busco_complete = 95.0
#    contigs = 1000

# Filter 2 set to
#    min_length = 5000000
#    max_length = 7000000
#    busco_complete = 95.0
#    contigs = 400

# Filter 3 set to
#    min_length = 4000000
#    max_length = 8000000
#    busco_complete = 95.0
#    contigs = 400

# Filter 4 set to
#    min_length = 4000000
#    max_length = 8000000
#    busco_complete = 95.0
#    contigs = 400
#    No Ns in genes
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Filter table based on specified conditions")
    parser.add_argument("input_file", help="Path to the input table file")
    args = parser.parse_args()

    # Call the filter_table function with the input file path
    filter_table(args.input_file)


