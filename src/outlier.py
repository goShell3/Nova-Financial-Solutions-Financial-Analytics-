import numpy as np
import pandas as pd
from scipy.stats import zscore


class OutlierDetection:
    """
    A class for detecting and removing outliers in a DataFrame using IQR and Z-score methods.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def iqr_outliers(self, columns=None):
        """
        Detect outliers using the Interquartile Range (IQR) method.

        :param columns: List of columns to check. If None, uses all numeric columns.
        :return: Dictionary of DataFrames containing outliers per column.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()

        outliers = {}
        for col in columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers[col] = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]

        return outliers

    def z_score_outliers(self, columns=None, threshold=3):
        """
        Detect outliers using the Z-score method.

        :param columns: List of columns to check. If None, uses all numeric columns.
        :param threshold: Z-score threshold for flagging outliers.
        :return: Dictionary of DataFrames containing outliers per column.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()

        outliers = {}
        for col in columns:
            z_scores = np.abs(zscore(self.df[col], nan_policy='omit'))
            outliers[col] = self.df[z_scores > threshold]

        return outliers

    def remove_outliers(self, method='iqr', columns=None, threshold=3):
        """
        Remove outliers from the DataFrame using the specified method.

        :param method: 'iqr' or 'z_score'
        :param columns: List of columns to check. If None, uses all numeric columns.
        :param threshold: Z-score threshold if using z_score method.
        :return: Cleaned DataFrame without outliers.
        """
        if method == 'iqr':
            outliers = self.iqr_outliers(columns)
        elif method == 'z_score':
            outliers = self.z_score_outliers(columns, threshold)
        else:
            raise ValueError("Method must be 'iqr' or 'z_score'")

        for col in outliers:
            self.df = self.df[~self.df.index.isin(outliers[col].index)]

        return self.df
