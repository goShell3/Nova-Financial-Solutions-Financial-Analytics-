import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from datetime import datetime
import os

class ArticleSentimentAnalyzer:
    def __init__(self, data):
        """
        Initialize the ArticleSentimentAnalyzer with data path.
        
        Args:
            data_path (str): Path to the CSV file containing article data
        """
        self.df = data
        self.output_dir = 'data/processed'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def compute_sentiment(self, text_col='headline'):
        """
        Compute sentiment scores for the specified text column.
        
        Args:
            text_col (str): Column name containing text to analyze
            
        Returns:
            pd.DataFrame: DataFrame with added sentiment column
        """
        self.df['sentiment'] = self.df[text_col].astype(str).apply(
            lambda x: TextBlob(x).sentiment.polarity
        )
        return self.df
    
    def plot_sentiment_distribution(self, save_path=None):
        """
        Plot the distribution of sentiment scores.
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x='sentiment', bins=50)
        plt.title('Distribution of Sentiment Scores')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Count')
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
        print("\nSentiment Score Statistics:")
        print(self.df['sentiment'].describe())
    
    def analyze_publisher_sentiment(self, top_n=10, save_path=None):
        """
        Analyze sentiment patterns by publisher.
        
        Args:
            top_n (int): Number of top publishers to analyze
            save_path (str, optional): Path to save the plot
        """
        publisher_sentiment = self.df.groupby('publisher')['sentiment'].agg(['mean', 'std', 'count'])
        publisher_sentiment = publisher_sentiment.sort_values('count', ascending=False).head(top_n)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=publisher_sentiment.reset_index(), x='publisher', y='mean')
        plt.title(f'Average Sentiment by Top {top_n} Publishers')
        plt.xlabel('Publisher')
        plt.ylabel('Average Sentiment Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
        print("\nPublisher Sentiment Statistics:")
        print(publisher_sentiment)
    
    def analyze_stock_sentiment(self, top_n=10, save_path=None):
        """
        Analyze sentiment patterns by stock.
        
        Args:
            top_n (int): Number of top stocks to analyze
            save_path (str, optional): Path to save the plot
        """
        stock_sentiment = self.df.groupby('stock')['sentiment'].agg(['mean', 'std', 'count'])
        stock_sentiment = stock_sentiment.sort_values('count', ascending=False).head(top_n)
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df[self.df['stock'].isin(stock_sentiment.index)], 
                   x='stock', y='sentiment')
        plt.title(f'Sentiment Distribution for Top {top_n} Stocks')
        plt.xlabel('Stock')
        plt.ylabel('Sentiment Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
        print("\nStock Sentiment Statistics:")
        print(stock_sentiment)
    
    def analyze_temporal_sentiment(self, freq='M', save_path=None):
        """
        Analyze sentiment trends over time.
        
        Args:
            freq (str): Frequency for resampling ('D' for daily, 'M' for monthly)
            save_path (str, optional): Path to save the plot
        """
        temporal_sentiment = self.df.set_index('date').resample(freq)['sentiment'].agg(['mean', 'std', 'count'])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Plot mean sentiment
        ax1.plot(temporal_sentiment.index, temporal_sentiment['mean'], label='Mean Sentiment')
        ax1.fill_between(temporal_sentiment.index, 
                        temporal_sentiment['mean'] - temporal_sentiment['std'],
                        temporal_sentiment['mean'] + temporal_sentiment['std'],
                        alpha=0.2)
        ax1.set_title(f'{freq}ly Average Sentiment Trend')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sentiment Score')
        ax1.legend()
        
        # Plot article count
        ax2.bar(temporal_sentiment.index, temporal_sentiment['count'])
        ax2.set_title(f'{freq}ly Article Count')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of Articles')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    
    def analyze_daily_sentiment_by_stock(self, top_n=5, save_path=None):
        """
        Analyze daily sentiment patterns for top stocks.
        
        Args:
            top_n (int): Number of top stocks to analyze
            save_path (str, optional): Path to save the plot
        """
        # Get top stocks by article count
        top_stocks = self.df['stock'].value_counts().nlargest(top_n).index
        
        # Aggregate daily sentiment
        daily_sentiment = self.df.groupby(['date', 'stock'])['sentiment'].mean().reset_index()
        
        plt.figure(figsize=(15, 8))
        for stock in top_stocks:
            stock_data = daily_sentiment[daily_sentiment['stock'] == stock]
            plt.plot(stock_data['date'], stock_data['sentiment'], label=stock)
        
        plt.title(f'Daily Average Sentiment for Top {top_n} Stocks')
        plt.xlabel('Date')
        plt.ylabel('Average Sentiment Score')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    
    def save_processed_data(self, filename='processed_articles_with_sentiment.csv'):
        """
        Save the processed data with sentiment scores.
        
        Args:
            filename (str): Name of the output file
        """
        output_path = os.path.join(self.output_dir, filename)
        self.df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")
    
    def run_full_analysis(self):
        """
        Run a complete sentiment analysis with all visualizations.
        """
        # Compute sentiment
        self.compute_sentiment()
        
        # Create plots directory
        plots_dir = os.path.join(self.output_dir, 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate all analyses and plots
        self.plot_sentiment_distribution(save_path=os.path.join(plots_dir, 'sentiment_distribution.png'))
        self.analyze_publisher_sentiment(save_path=os.path.join(plots_dir, 'publisher_sentiment.png'))
        self.analyze_stock_sentiment(save_path=os.path.join(plots_dir, 'stock_sentiment.png'))
        self.analyze_temporal_sentiment(save_path=os.path.join(plots_dir, 'temporal_sentiment.png'))
        self.analyze_daily_sentiment_by_stock(save_path=os.path.join(plots_dir, 'daily_sentiment_by_stock.png'))
        
        # Save processed data
        self.save_processed_data()

if __name__ == "__main__":
    # Example usage
    analyzer = ArticleSentimentAnalyzer("data/raw_analyst_ratings.csv")
    analyzer.run_full_analysis() 