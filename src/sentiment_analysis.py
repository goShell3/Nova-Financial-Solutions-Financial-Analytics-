import pandas as pd
from textblob import TextBlob

def compute_sentiment(df, text_col='headline'):
    """
    Adds a 'sentiment' column to the DataFrame with polarity scores.
    """
    df['sentiment'] = df[text_col].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    return df

def aggregate_daily_sentiment(df, date_col='date', stock_col='stock', sentiment_col='sentiment'):
    """
    Aggregates sentiment by date and stock (mean).
    """
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    daily_sentiment = df.groupby([date_col, stock_col])[sentiment_col].mean().reset_index()
    return daily_sentiment

def compute_daily_returns(df, date_col='Date', close_col='Close'):
    """
    Computes daily returns and returns a DataFrame with date and return columns.
    """
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    df = df.sort_values(date_col)
    df['return'] = df[close_col].pct_change()
    return df[[date_col, 'return']].dropna()

def merge_sentiment_returns(sentiment_df, returns_df, date_col='date', stock_col='stock'):
    """
    Merges sentiment and returns DataFrames on date and stock.
    """
    merged = pd.merge(sentiment_df, returns_df, left_on=[date_col, stock_col], right_on=[date_col, stock_col])
    return merged

def compute_correlation(merged_df, sentiment_col='sentiment', return_col='return'):
    """
    Computes Pearson and Spearman correlation between sentiment and returns.
    """
    pearson = merged_df[sentiment_col].corr(merged_df[return_col], method='pearson')
    spearman = merged_df[sentiment_col].corr(merged_df[return_col], method='spearman')
    return {'pearson': pearson, 'spearman': spearman}
