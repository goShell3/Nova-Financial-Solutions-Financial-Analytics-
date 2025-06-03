import numpy as np
import scipy as stats


def iqr_outliers(df):
    Q1, Q3 = np.percentile(df, [25, 75])
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    
    return np.where((df < lower) | (df > upper))

def remove_outlier(df, columns):
    ...

def z_score_outliers(df, threshold=3):
    z_scores = np.abs(stats.zscore(df))
    return np.where(z_scores > threshold)