import pandas as pd

def preprocess_csv(csv_file, output_csv):
    # Read the CSV file
    df = pd.read_csv(csv_file, dtype={'num': str})  # Ensure 'num' is read as a string

    # Add 'ppro' prefix to the 'num' column for consistency with FASTA file as a new column ppro_num
    df['ppro_num'] = 'ppro' + df['num'] 

    # Save the updated CSV with the new 'psg_num' column
    df.to_csv(output_csv, index=False)
    
# Example usage
preprocess_csv(
    csv_file="ppro_master_table_num.csv",
    output_csv="ppro_master_table_num_precluster.csv"
)