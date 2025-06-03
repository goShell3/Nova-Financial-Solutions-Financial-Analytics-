import pandas as pd
from pathlib import Path
import os

class CSVLoader:
    """Handles loading and basic EDA of CSV files from a specified directory"""
    
    def __init__(self, data_dir="data"):
        """
        Args:
            data_dir: Path to directory containing CSV files
             # Cell 1: Import libraries
        import pandas as pd
        import matplotlib.pyplot as plt
        import talib
        from pynance import stocks
        
        # Cell 2: Load and prepare the data
        data_path = '../data/AAPL.csv'
        df = pd.read_csv(data_path, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.dropna(inplace=True)
        df.head()
        
        # Cell 3: Apply TA-Lib technical indicators
        df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
        df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD'] = macd
        df['MACD_Signal'] = macdsignal
        
        # Cell 4: Use PyNance for financial metrics (example: daily returns)
        df['Daily_Return'] = stocks.returns(df['Close'])
        
        # Cell 5: Visualize the data and indicators
        plt.figure(figsize=(14, 8))
        plt.subplot(3, 1, 1)
        plt.plot(df['Close'], label='Close Price')
        plt.plot(df['SMA_20'], label='20-day SMA')
        plt.title('AAPL Close Price & 20-day SMA')
        plt.legend()
        
        plt.subplot(3, 1, 2)
        plt.plot(df['RSI_14'], label='RSI (14)')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title('AAPL RSI (14)')
        plt.legend()
        
        plt.subplot(3, 1, 3)
        plt.plot(df['MACD'], label='MACD')
        plt.plot(df['MACD_Signal'], label='MACD Signal')
        plt.title('AAPL MACD')
        plt.legend()
        
        plt.tight_layout()
        plt.show()   """
        self.data_dir = Path(data_dir)
        self.available_files = self._list_csv_files()
        
    def _list_csv_files(self):
        """Scan directory for CSV files and return {filename: path} mapping"""
        files = {}
        for file in self.data_dir.glob("*.csv"):
            files[file.stem] = file  # Store without .csv extension
        return files
    
    def show_available_files(self):
        """Display available CSV files for selection"""
        print("Available CSV files:")
        for i, name in enumerate(self.available_files.keys(), 1):
            print(f"{i}. {name}")
        return list(self.available_files.keys())
    
    def load_csv(self, file_input):
        """
        Load CSV by filename (with or without extension) or index
        
        Args:
            file_input: Either filename (str) or index (int) from show_available_files()
        Returns:
            pandas.DataFrame
        """
        # Handle numeric index input
        if isinstance(file_input, int):
            try:
                file_key = list(self.available_files.keys())[file_input - 1]
                filepath = self.available_files[file_key]
            except IndexError:
                raise ValueError(f"Invalid index. Choose 1-{len(self.available_files)}")
        # Handle string filename input
        else:
            file_input = Path(file_input).stem  # Remove extension if provided
            filepath = self.available_files.get(file_input)
            if not filepath:
                raise FileNotFoundError(f"File '{file_input}' not found. Available files: {list(self.available_files.keys())}")
        
        return pd.read_csv(filepath)
    
    def quick_eda(self, df):
        """Perform basic EDA on loaded DataFrame"""
        eda_results = {
            "head": df.head(),
            "info": df.info(),
            "describe": df.describe(include='all'),
            "nulls": df.isnull().sum(),
            "duplicates": df.duplicated().sum()
        }
        return eda_results