# To use TA-Lib, you need to install its C library first.
# You can download and install it using:
# wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
# tar -xzvf ta-lib-0.4.0-src.tar.gz
# cd ta-lib
# ./configure --prefix=/usr
# make
# sudo make install

import talib as ta
import pynance as pn
from typing import List, Dict, Union
import pandas as pd


class TechnicalIndicators:
    
    def __init__(self, ohlc: pd.DataFrame):
        """
        Initialize with OHLC data.
        
        :param ohlc: DataFrame containing Open, High, Low, Close prices.
        """
        self.ohlc = ohlc
        self.close = ohlc['Close'].values
        self.high = ohlc['High'].values
        self.low = ohlc['Low'].values
        self.open = ohlc['Open'].values
        self.volume = ohlc['Volume'].values if 'Volume' in ohlc.columns else None
        
    def moving_average(self, period: int) -> pd.Series:
        """Calculate the moving average for a given period.
        This method calculates the simple moving average (SMA) for the closing prices over a specified period.

        Args:
            period (int): The number of periods over which to calculate the moving average.

        Returns:
            pd.Series: A pandas Series containing the moving average values.
        """
        
        return pd.Series(ta.SMA(self.close, timeperiod=period), name=f'SMA_{period}', index=self.ohlc.index)
    
    def relative_strength_index(self, period: int) -> pd.Series:
        """Calculate the Relative Strength Index (RSI) for a given period.
        
        Args:
            period (int): The number of periods over which to calculate the RSI.
        
        Returns:
            pd.Series: A pandas Series containing the RSI values.
        """
        
        return pd.Series(ta.RSI(self.close, timeperiod=period), name=f'RSI_{period}', index=self.ohlc.index)
    
    def moving_average_convergence_divergence(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> pd.DataFrame:
        """Calculate the Moving Average Convergence Divergence (MACD).
        
        Args:
            fastperiod (int): The period for the fast EMA.
            slowperiod (int): The period for the slow EMA.
            signalperiod (int): The period for the signal line.
        
        Returns:
            pd.DataFrame: A DataFrame containing MACD, Signal Line, and MACD Histogram.
        """
        
        macd, macdsignal, macdhist = ta.MACD(self.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        return pd.DataFrame({
            'MACD': macd,
            'Signal_Line': macdsignal,
            'MACD_Histogram': macdhist
        }, index=self.ohlc.index)
        
    