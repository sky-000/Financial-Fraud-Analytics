# step1 Import all the library needed for the project
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pd.set_option('display.float_format', lambda x: '%.2f' % x) # to force pandas to display float values instead of scientific notation

# step 2 for making sure when uploading to github it gives warning to the user as why its not working
def finacial_report(file_path='Synthetic_Financial_datasets_log.csv'):
    if not os.path.exists(file_path):
        print(f"error {file_path} does not exist")
        print("Please download the data file")
        return
        
    # step3 load the csv file
    df = pd.read_csv(file_path)
    
    # step4 data cleaning
    # handle missing value , correct data types, remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Step5 transformation : 
    # feature engineering - new column addition
    # categorization - group of numeric data for better analysis.
    # FIX: Expanded the upper boundary to 1 Billion to catch large transactions safely
    df['amount_category'] = pd.cut(df['amount'], bins=[0, 5000, 10000, 1000000000], labels=['Low', 'Medium', 'High'])
    
    # step6: data aggregation - groupby or pivot using pandas
    # FIX: Grouped by BOTH 'type' and 'amount_category' so Seaborn's 'hue' works perfectly!
    detailed_summary = df.groupby(['type', 'amount_category']).agg(
        Total_Amount=('amount', 'sum'),
        Average_amount=('amount', 'mean'),
        Count_Transaction=('amount', 'count')
    ).reset_index()
    
    print(detailed_summary)
    
    # step7 visualization - bar plot , histogram, scatter plot 
    
    # --- CHART 1: GROUPED BAR PLOT ---
    plt.figure(figsize=(10, 6))
    sns.barplot(x='type', y='Total_Amount', hue='amount_category', data=detailed_summary)
    
    # Formatting the aesthetics
    plt.yscale('log') # Added log scale so smaller categories remain visible next to billions
    plt.title("Bank Data: Total Amount Volume by Transaction Type & Size", fontsize=14, fontweight='bold')
    plt.xlabel("Transaction Type", fontsize=12)
    plt.ylabel("Total Amount Volume (Log Scale)", fontsize=12)
    plt.tight_layout()
    plt.savefig('transaction_bar_chart.png') # 💾 Saves immediately without blocking
    plt.close()
    
    # --- CHART 2: HISTOGRAM ON RAW DATA ---
# --- CHART 2: HISTOGRAM (ZOOMED IN) ---
    plt.figure(figsize=(10, 6))
    
    # Filter out extreme outliers by only plotting transactions under 100,000
    df_filtered = df[df['amount'] <= 100000]
    
    # Plot using the filtered data
    sns.histplot(x='amount', data=df_filtered, bins=50, color='purple', kde=True)
    
    # Formatting
    plt.title("Distribution of Transaction Amounts (Up to $100K)", fontsize=14, fontweight='bold')
    plt.xlabel("Transaction Amount", fontsize=12)
    plt.ylabel("Frequency (Count of Transactions)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('transaction_histogram.png')
    plt.close()
    
    # --- CHART 3: SCATTER PLOT ---
    plt.figure(figsize=(10, 6))
    
    # Track transaction frequency on X and financial volume on Y
    # 'hue' colors the dots by transaction type, 'style' changes shapes based on size bracket
    sns.scatterplot(
        x='Count_Transaction', 
        y='Total_Amount', 
        hue='type', 
        style='amount_category', 
        data=detailed_summary, 
        s=120  # Increases dot size to make them clearly visible
    )
    
    # Apply log scales because payment volumes dwarf debit/transfer metrics
    plt.xscale('log')
    plt.yscale('log')
    
    # Formatting aesthetics
    plt.title("Transaction Density: Frequency vs. Financial Volume", fontsize=14, fontweight='bold')
    plt.xlabel("Transaction Count (Log Scale)", fontsize=12)
    plt.ylabel("Total Amount Volume (Log Scale)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('transaction_scatterplot_chart.png') # 💾 Saves immediately without blocking
    plt.close()

finacial_report()