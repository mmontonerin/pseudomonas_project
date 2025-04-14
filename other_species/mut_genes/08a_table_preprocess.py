import pandas as pd

def preprocess_csv(input_csv, output_csv, prefix):
    # Read the CSV file
    df = pd.read_csv(input_csv, dtype={'num': str})  # Ensure 'num' is read as a string

    # Add new column with the specified prefix
    df[f'{prefix}_num'] = prefix + df['num']

    # Save the updated CSV with the new prefixed column
    df.to_csv(output_csv, index=False)

# Define prefixes
prefixes = ["pbra", "psav", "pflu", "pvir"]

# Process each CSV file
for prefix in prefixes:
    preprocess_csv(
        input_csv=f"{prefix}_sequences_without_Ns.csv",  # Adjust filename as needed
        output_csv=f"{prefix}_master_table_precluster.csv",  # Output for each prefix
        prefix=prefix
    )
