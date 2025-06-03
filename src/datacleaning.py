import pandas as pd 
import numpy as np


# data cleamimg class for financial data(stock market data)
class DataCleaning:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame.
        """
        self.df = df

    def remove_nan_values(self, columns: list) -> pd.DataFrame:
        """
        Remove rows with NaN values in specified columns.
        """
        self.df = self.df.dropna(subset=columns)
        return self.df

    def remove_duplicates(self) -> pd.DataFrame:
        """
        Remove duplicate rows.
        """
        self.df = self.df.drop_duplicates()
        return self.df

    def reset_index(self) -> pd.DataFrame:
        """
        Reset the index of the DataFrame.
        """
        self.df = self.df.reset_index(drop=True)
        return self.df
    
    def convert_to_datetime(self, column: str) -> pd.DataFrame:
        """
        Convert a specified column to datetime format.
        """
        self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
        return self.df
    def fill_missing_values(self, method: str = 'ffill', value=None) -> pd.DataFrame:
        """
        Fill missing values using specified method or value.
        :param method: Method to fill missing values ('ffill', 'bfill', 'mean', etc.).
        :param value: Value to fill missing values with (if method is 'value').
        """  
           
        if method == 'ffill':
            self.df = self.df.fillna(method='ffill')
        elif method == 'bfill':
            self.df = self.df.fillna(method='bfill')
        elif method == 'mean':
            self.df = self.df.fillna(self.df.mean())
        elif value is not None:
            self.df = self.df.fillna(value)
        else:
            raise ValueError("Invalid method or value for filling missing values.")