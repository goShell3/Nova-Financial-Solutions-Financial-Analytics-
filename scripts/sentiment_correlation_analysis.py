import pandas as pd
import numpy as np
from textblob import TextBlob
# import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_processed_stock_data(ticker: str) -> pd.DataFrame:
    """
    Load processed stock data from the data directory
    """
    try:
        file_path = os.path.join('data', 'yfinance_data', 'processed', f'{ticker}_processed_data.csv')
        stock_data = pd.read_csv(file_path)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        stock_data.set_index('Date', inplace=True)
        return stock_data
    except Exception as e:
        logger.error(f"Error loading processed stock data: {e}")
        raise

def calculate_daily_returns(stock_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns from stock data
    """
    stock_data['Daily_Return'] = stock_data['Close'].pct_change() * 100
    return stock_data

def analyze_sentiment(text: str) -> float:
    """
    Analyze sentiment of text using TextBlob
    Returns a polarity score between -1 (negative) and 1 (positive)
    """
    try:
        return TextBlob(text).sentiment.polarity
    except Exception as e:
        logger.warning(f"Error analyzing sentiment: {e}")
        return 0.0

def process_news_data(news_data: pd.DataFrame) -> pd.DataFrame:
    """
    Process news data and calculate daily sentiment scores
    """
    # Ensure date column is datetime
    news_data['Date'] = pd.to_datetime(news_data['Date'])
    
    # Calculate sentiment for each headline
    news_data['Sentiment'] = news_data['Headline'].apply(analyze_sentiment)
    
    # Calculate daily average sentiment
    daily_sentiment = news_data.groupby(news_data['Date'].dt.date)['Sentiment'].mean().reset_index()
    daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
    
    return daily_sentiment

def align_data(stock_data: pd.DataFrame, news_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Align stock and news data by date
    """
    # Ensure both datasets have datetime index
    stock_data.index = pd.to_datetime(stock_data.index)
    news_data.set_index('Date', inplace=True)
    
    # Find common dates
    common_dates = stock_data.index.intersection(news_data.index)
    
    # Filter both datasets to common dates
    aligned_stock = stock_data.loc[common_dates]
    aligned_news = news_data.loc[common_dates]
    
    return aligned_stock, aligned_news

def calculate_correlation(stock_data: pd.DataFrame, news_data: pd.DataFrame) -> float:
    """
    Calculate correlation between daily returns and sentiment scores
    """
    correlation = stock_data['Daily_Return'].corr(news_data['Sentiment'])
    return correlation

def plot_correlation(stock_data: pd.DataFrame, news_data: pd.DataFrame, ticker: str):
    """
    Create visualization of correlation between sentiment and returns
    """
    plt.figure(figsize=(12, 6))
    
    # Create subplot for stock returns
    plt.subplot(2, 1, 1)
    plt.plot(stock_data.index, stock_data['Daily_Return'], label='Daily Returns')
    plt.title(f'{ticker} Daily Returns')
    plt.legend()
    
    # Create subplot for sentiment
    plt.subplot(2, 1, 2)
    plt.plot(news_data.index, news_data['Sentiment'], label='News Sentiment', color='orange')
    plt.title('News Sentiment Score')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'correlation_analysis_{ticker}.png')
    plt.close()

def main():
    # List of tickers to analyze
    tickers = ['AAPL', 'GOOG', 'META']
    
    for ticker in tickers:
        logger.info(f"Processing {ticker}...")
        
        # Load processed stock data
        stock_data = load_processed_stock_data(ticker)
        stock_data = calculate_daily_returns(stock_data)
        
        # Load news data (you'll need to implement this based on your news data source)
        # news_data = pd.read_csv('path_to_news_data.csv')
        # news_data = process_news_data(news_data)
        
        # Align data
        # aligned_stock, aligned_news = align_data(stock_data, news_data)
        
        # Calculate correlation
        # correlation = calculate_correlation(aligned_stock, aligned_news)
        # logger.info(f"Correlation between news sentiment and stock returns for {ticker}: {correlation:.4f}")
        
        # Plot correlation
        # plot_correlation(aligned_stock, aligned_news, ticker)
        
        logger.info(f"Completed processing {ticker}")

if __name__ == "__main__":
    main() 