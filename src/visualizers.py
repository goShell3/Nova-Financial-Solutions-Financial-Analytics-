import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union
import pandas as pd
from pandas import DataFrame

class Visualizer:
    
    def __init__(self, data: DataFrame):
        """
        Initialize the Visualizer with a DataFrame.
        
        :param data: DataFrame containing the data to visualize.
        """
        self.data = data
        
    def plot_time_series(self, column: str, title: str = None, xlabel: str = 'Date', ylabel: str = 'Value') -> None:
        """
        Plot a time series for a specified column in the DataFrame.
        
        :param column: The column name to plot.
        :param title: Title of the plot.
        :param xlabel: Label for the x-axis.
        :param ylabel: Label for the y-axis.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data[column], label=column)
        plt.title(title if title else f'Time Series of {column}')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()
        plt.show()
        
    def plot_correlation_matrix(self, title: str = 'Correlation Matrix') -> None:
        """
        Plot a correlation matrix for the DataFrame.
        
        :param title: Title of the plot.
        """
        plt.figure(figsize=(10, 8))
        corr = self.data.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True)
        plt.title(title)
        plt.show()
        
    def plot_distribution(self, column: str, title: str = None) -> None:
        """
        Plot the distribution of a specified column in the DataFrame.
        
        :param column: The column name to plot.
        :param title: Title of the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], kde=True, bins=30)
        plt.title(title if title else f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid()
        plt.show()
        
    def plot_boxplot(self, column: str, title: str = None) -> None:
        """
        Plot a boxplot for a specified column in the DataFrame.
        
        :param column: The column name to plot.
        :param title: Title of the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.data[column])
        plt.title(title if title else f'Boxplot of {column}')
        plt.xlabel(column)
        plt.grid()
        plt.show()
        
    def plot_pairwise(self, columns: Union[list, str] = None, title: str = 'Pairwise Plot') -> None:
        """
        Plot pairwise relationships in the DataFrame.
        
        :param columns: List of columns to plot. If None, all columns are used.
        :param title: Title of the plot.
        """
        if isinstance(columns, str):
            columns = [columns]
        elif columns is None:
            columns = self.data.columns.tolist()
        
        sns.pairplot(self.data[columns])
        plt.suptitle(title, y=1.02)
        plt.show()
        
    def plot_heatmap(self, title: str = 'Heatmap') -> None:
        """
        Plot a heatmap of the DataFrame.
        
        :param title: Title of the plot.
        """
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.data, annot=True, fmt=".2f", cmap='viridis', cbar=True)
        plt.title(title)
        plt.show()
        plt.tight_layout()
        plt.close()
