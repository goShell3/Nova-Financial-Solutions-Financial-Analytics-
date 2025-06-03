import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

class Visualizer:
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def plot_stock_with_indicators(
        self,
        sma_columns: list[str] = None,
        macd_columns: tuple[str, str, str] = None,
        rsi_column: str = None,
        volume: bool = True,
        title: str = 'Stock Price with Indicators'
    ) -> None:
        """
        Plot candlestick with optional volume, SMA, MACD and RSI.

        Parameters:
        - sma_columns: list of SMA column names to plot on price chart.
        - macd_columns: tuple of (MACD, Signal, Histogram) column names.
        - rsi_column: RSI column name for separate subplot.
        - volume: whether to show volume bars.
        - title: plot title.
        """
        # Determine number of rows for subplots
        rows = 1  # Price + SMA + MACD overlay on price
        if volume:
            rows += 1
        if rsi_column:
            rows += 1
        
        fig, axes = plt.subplots(rows, 1, figsize=(14, 7 + 2*rows), sharex=True,
                                 gridspec_kw={'height_ratios': [3] + [1]*(rows-1)})
        
        if rows == 1:
            axes = [axes]  # Ensure axes is iterable
        
        # Plot candlestick using matplotlib's bar chart (OHLC)
        ax_price = axes[0]
        self._plot_candlestick(ax_price)
        
        # Plot SMA lines if provided
        if sma_columns:
            for col in sma_columns:
                ax_price.plot(self.data.index, self.data[col], label=col)
        
        # Plot MACD and Signal on price chart (usually MACD is below price, but here overlay for demo)
        if macd_columns:
            macd_col, signal_col, hist_col = macd_columns
            ax_price.plot(self.data.index, self.data[macd_col], label=macd_col, linestyle='--')
            ax_price.plot(self.data.index, self.data[signal_col], label=signal_col, linestyle=':')
        
        ax_price.set_title(title)
        ax_price.set_ylabel('Price')
        ax_price.legend(loc='upper left')
        ax_price.grid(True)
        
        # Volume subplot if requested
        if volume:
            ax_vol = axes[1]
            ax_vol.bar(self.data.index, self.data['Volume'], color='grey')
            ax_vol.set_ylabel('Volume')
            ax_vol.grid(True)
        
        # RSI subplot if requested
        if rsi_column:
            ax_rsi = axes[-1]
            ax_rsi.plot(self.data.index, self.data[rsi_column], color='purple')
            ax_rsi.axhline(70, color='red', linestyle='--')
            ax_rsi.axhline(30, color='green', linestyle='--')
            ax_rsi.set_ylabel('RSI')
            ax_rsi.set_ylim(0, 100)
            ax_rsi.grid(True)
        
        # Format x-axis with date labels nicely
        ax_price.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax_price.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
        
        plt.tight_layout()
        plt.show()
        
    def _plot_candlestick(self, ax):
        """
        Plot a simple candlestick chart on the given axis.
        This uses matplotlib bar plots for open-high-low-close visualization.
        """
        o = self.data['Open']
        h = self.data['High']
        l = self.data['Low']
        c = self.data['Close']
        
        width = 0.6  # Width of candlestick bars
        width2 = 0.1  # Width of the lines (wicks)
        
        dates = mdates.date2num(self.data.index.to_pydatetime())
        
        # Color up/down days
        colors = ['green' if c_i >= o_i else 'red' for c_i, o_i in zip(c, o)]
        
        # Plot the candle body
        for i in range(len(self.data)):
            color = colors[i]
            # Candle body
            ax.bar(dates[i], abs(c[i] - o[i]), width, bottom=min(o[i], c[i]), color=color)
            # Wick line
            ax.vlines(dates[i], l[i], h[i], color=color, linewidth=width2*10)
