import pandas as pd

df = pd.read_csv("final_table_of_genome_assemblies_final.csv")

# Format column num so that all numbers have the same number of digits. 
# 1 becomes 0001, 10 becomes 0010, etc

# Format the 'num' column to have leading zeros and four digits
df['num'] = df['num'].apply(lambda x: f'{int(x):04d}')

# Save the updated DataFrame back to CSV
df.to_csv("final_table_of_genome_assemblies_final_num.csv", index=False)

# Check the output
print(df.head())