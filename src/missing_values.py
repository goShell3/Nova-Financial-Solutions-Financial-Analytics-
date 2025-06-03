import pandas as pd 
import numpy as np
from typing import List


def remove_nan_values(df, columns: List):

    df = pd.DataFrame(columns=columns)
    if df.isnull().sum() >= 1:
        df.dropna()
    
