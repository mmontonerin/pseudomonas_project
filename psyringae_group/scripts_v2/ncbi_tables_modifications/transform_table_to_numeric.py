import pandas as pd
import numpy as np
import argparse

def modify_table(input_file, output_file):
    # Read input CSV file into pandas dataframe
    df = pd.read_csv(input_file)

    # Get the list of genes (column names)
    genes = ['mutT', 'mutY', 'mutS', 'mutL', 'dnaQ','uvrD']

    # Iterate over each cell in the gene columns and perform modifications
    for gene in genes:
        # Modify values of the form "fragmented:number" to keep only the number
        df[gene] = df[gene].apply(lambda x: int(x.split(':')[1]) if isinstance(x, str) and ':' in x else x)

        # Change "missing" values to 0
        df.loc[df[gene] == 'missing', gene] = 0

    # Save the modified dataframe to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Modify table")
    parser.add_argument("input_file", help="Path to the input table file")
    parser.add_argument("output_file", help="Path to save the modified table")
    args = parser.parse_args()

    # Call the modify_table function with the input and output file paths
    modify_table(args.input_file, args.output_file)
