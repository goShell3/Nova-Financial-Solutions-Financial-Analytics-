import seaborn as sns 
import pandas as pd 
import matplotlib.pyplot as plt


class DataExplorer:
    """
    A class for exploring financial data through visualizations.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame.
        """
        self.df = df

    def plot_time_series(self, column: str, title: str = None):
        """
        Plot a time series for a specified column in the DataFrame.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.df.index, self.df[column], label=column)
        plt.title(title if title else f'Time Series of {column}')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid()
        plt.show()
        
        
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
