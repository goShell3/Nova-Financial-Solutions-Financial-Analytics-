import pandas as pd
import numpy as np

class TechnicalIndicators:
    
    def __init__(self, ohlc: pd.DataFrame):
        """
        Initialize with OHLC data.
        """
        self.ohlc = ohlc
        self.close = ohlc['Close']
        self.high = ohlc['High']
        self.low = ohlc['Low']
        self.open = ohlc['Open']
        self.volume = ohlc['Volume'] if 'Volume' in ohlc.columns else None
        
    def moving_average(self, period: int) -> pd.Series:
        """Simple Moving Average (SMA)"""
        return self.close.rolling(window=period).mean().rename(f'SMA_{period}')
    
    def relative_strength_index(self, period: int) -> pd.Series:
        """Relative Strength Index (RSI)"""
        delta = self.close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.rename(f'RSI_{period}')
    
    def moving_average_convergence_divergence(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> pd.DataFrame:
        """MACD, Signal Line, MACD Histogram"""
        ema_fast = self.close.ewm(span=fastperiod, adjust=False).mean()
        ema_slow = self.close.ewm(span=slowperiod, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=signalperiod, adjust=False).mean()
        hist = macd - signal
        
        return pd.DataFrame({
            'MACD': macd,
            'Signal_Line': signal,
            'MACD_Histogram': hist
        }, index=self.ohlc.index)
