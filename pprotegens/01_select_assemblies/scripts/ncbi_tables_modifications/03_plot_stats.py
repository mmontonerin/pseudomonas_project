import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import argparse


def plot_assembly_stats(input_file, output_name=None):
    # Read input CSV file into pandas dataframe
    df = pd.read_csv(input_file)

    # Number of samples (rows of data plotted)
    n_samples = len(df)

    # Plot histogram of #Contigs and save it as PDF
    plt.figure(figsize=(8, 6))
    plt.hist(df['#Contigs'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of #Contigs')
    plt.xlabel('#Contigs')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.text(0.95, 0.95, f'n = {n_samples}', ha='right', va='top', transform=plt.gca().transAxes)
    if output_name:
        filename1pdf = f'contigs_vs_busco_{output_name}.pdf'
    else:
        filename1pdf = 'contigs_vs_busco.pdf'
    plt.savefig(filename1pdf)
    plt.savefig(filename1png)
    plt.close()  # Close the plot to clear the current figure

    # Create a new figure and axes for scatter plot
    fig, axs = plt.subplots(1, 1, figsize=(8, 6))
    mbcontigsbusco = axs.scatter(df['#Contigs'], df['Total_length'], c=df['BUSCO-C'], cmap='plasma')
    colorbar = fig.colorbar(mbcontigsbusco, ax=axs, extend='both')
    colorbar.set_label('BUSCO-C')
    axs.set_xlabel('#Contigs')
    axs.set_ylabel('Total length')
    axs.set_title('Total length / # Contigs')
    plt.text(0.95, 0.95, f'n = {n_samples}', ha='right', va='top', transform=plt.gca().transAxes)
    if output_name:
        filename2pdf = f'contigs_vs_busco_{output_name}.pdf'
    else:
        filename2pdf = 'contigs_vs_busco.pdf'
    plt.savefig(filename2pdf)
    plt.savefig(filename2png)
    plt.close()  # Close the plot to clear the current figure
    
    # Create a new figure and axes for scatter plot
    fig, axs = plt.subplots(1, 1, figsize=(8, 6))
    mbcontigsbusco2 = axs.scatter(df['#Contigs'], df['BUSCO-C'], c=df['Total_length'], cmap='plasma')
    colorbar = fig.colorbar(mbcontigsbusco2, ax=axs, extend='both')
    colorbar.set_label('Assembly size')
    axs.set_xlabel('#Contigs')
    axs.set_ylabel('BUSCO completeness (%)')
    axs.set_title('Total length / # Contigs')
    plt.text(0.95, 0.95, f'n = {n_samples}', ha='right', va='top', transform=plt.gca().transAxes)
    if output_name:
        filename3pdf = f'contigs_vs_busco_{output_name}.pdf'
    else:
        filename3pdf = 'contigs_vs_busco.pdf'
    plt.savefig(filename3pdf)
    plt.savefig(filename3png)
    plt.close()  # Close the plot to clear the current figure



if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Plot assembly stats")
    parser.add_argument("input_file", help="Path to the input table file")
    parser.add_argument("-on", "--output_name", help="Specific string to add to each plot name")
    args = parser.parse_args()

    # Call the filter_table function with the input file path
    plot_assembly_stats(args.input_file, args.output_name)


