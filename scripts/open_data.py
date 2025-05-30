import pandas as pd
from pathlib import Path
import os

class CSVLoader:
    """Handles loading and basic EDA of CSV files from a specified directory"""
    
    def __init__(self, data_dir="data"):
        """
        Args:
            data_dir: Path to directory containing CSV files
        """
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