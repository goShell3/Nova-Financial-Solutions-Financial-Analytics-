import seaborn as sns 
import pandas as pd 
import matplotlib.pyplot as plt

def plot_distribution(df, columns):
    for col in columns:
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.show()

def plot_correlation_matrix(df):
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
