import pandas as pd

# Load the table from a CSV file (adjust the file name as needed)
df = pd.read_csv("ppro_master_table.csv")

# Format the 'num' column to have leading zeros (4 digits)
df['num'] = df['num'].apply(lambda x: f"{int(x):04}")

# Save the modified table back to a new CSV file
df.to_csv("ppro_master_table_num.csv", index=False)