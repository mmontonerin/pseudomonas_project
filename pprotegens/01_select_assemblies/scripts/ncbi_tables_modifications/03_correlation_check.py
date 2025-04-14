import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.cm as cm

# Load the data
data = pd.read_csv("final_table_of_genome_assemblies_4.csv")

# Select relevant columns
columns_of_interest = ['dnaQ', 'mutL', 'mutT', 'mutS', 'mutY', 'uvrD', '#Contigs', 'GC(%)', 'BUSCO-C', 'Total_length']
df = data[columns_of_interest]

# Check correlation matrix
correlation_matrix = df.corr()

# Visualize correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix_filter4.pdf')
plt.close()

# Visualize pairwise relationships
pairplot = sns.pairplot(df)
pairplot.savefig('pairwise_relationships_filter4.pdf')
plt.close()

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Apply PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_data)
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Plot PCA results with a colorbar for #Contigs
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(x='PC1', y='PC2', hue=data['#Contigs'], data=principal_df, palette='plasma')
plt.title('PCA of Variables\nExplained Variance Ratio: PC1={:.2f}, PC2={:.2f}'.format(pca.explained_variance_ratio_[0], pca.explained_variance_ratio_[1]))
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Create a colorbar
norm = plt.Normalize(data['#Contigs'].min(), data['#Contigs'].max())
sm = cm.ScalarMappable(cmap='plasma', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label('#Contigs')


plt.savefig('pca_plot_with_colorbar_contigs_filter4.pdf')
plt.close()

# Plot PCA results with a colorbar for BUSCO-C
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(x='PC1', y='PC2', hue=data['BUSCO-C'], data=principal_df, palette='plasma')
plt.title('PCA of Variables\nExplained Variance Ratio: PC1={:.2f}, PC2={:.2f}'.format(pca.explained_variance_ratio_[0], pca.explained_variance_ratio_[1]))
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Create a colorbar
norm = plt.Normalize(data['BUSCO-C'].min(), data['BUSCO-C'].max())
sm = cm.ScalarMappable(cmap='plasma', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label('BUSCO-C (%)')

plt.savefig('pca_plot_with_colorbar_busco_filter4.pdf')
plt.close()


