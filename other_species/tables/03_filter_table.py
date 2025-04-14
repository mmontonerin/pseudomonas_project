import pandas as pd
import re
import argparse

# Usage: python 03_filter_table.py -i file.csv -o prefix

def filter_table(input_file, output_prefix):
    # Read the input table
    df_fn = pd.read_csv(input_file, dtype={'num': str})

    busco_complete = 95.0 
    contigs = 400    
    
    df_condition_pass = pd.DataFrame(columns=df_fn.columns)
    df_condition_fail = pd.DataFrame(columns=df_fn.columns)

    # Iterate over each row of the DataFrame
    for index, row in df_fn.iterrows():
        if row['BUSCO-C'] < busco_complete:
            df_condition_fail.loc[index] = row
        elif row['#Contigs'] > contigs:
            df_condition_fail.loc[index] = row
        else:
            df_condition_pass.loc[index] = row 
    
    # Save filtered data to one file
    df_condition_fail.to_csv(f'{output_prefix}_excluded.csv', index=False)

    # Save unfiltered data to another file
    df_condition_pass.to_csv(f'{output_prefix}_mastertable_final.csv', index=False)

# FINAL FILTER
#    busco_complete = 95.0
#    contigs = 400

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Filter table based on specified conditions")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input table file")
    parser.add_argument("-o", "--output_prefix", required=True, help="prefix of the output files")
    args = parser.parse_args()

    # Call the filter_table function with the input and output file paths
    filter_table(args.input_file, args.output_prefix)


