import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_headline_lengths(df):
    """Analyze the length of headlines"""
    df['headline_length'] = df['headline'].str.len()
    headline_stats = df['headline_length'].describe()
    return headline_stats

def analyze_publishers(df):
    """Analyze publisher activity"""
    publisher_counts = df['publisher'].value_counts()
    return publisher_counts

def analyze_publication_dates(df):
    """Analyze publication date trends"""
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    df['day_of_week'] = df['publication_date'].dt.day_name()
    df['hour'] = df['publication_date'].dt.hour
    
    # Daily publication counts
    daily_counts = df.groupby('day_of_week').size()
    
    # Hourly publication counts
    hourly_counts = df.groupby('hour').size()
    
    return daily_counts, hourly_counts

def plot_publication_trends(df):
    """Plot publication trends"""
    # Daily trend
    plt.figure(figsize=(12, 6))
    df.groupby('publication_date').size().plot()
    plt.title('Publication Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('publication_trends.png')
    plt.close()

def main():
    # Load your data
    df = pd.read_csv('data/processed_data.csv')
    
    # Perform analyses
    headline_stats = analyze_headline_lengths(df)
    publisher_counts = analyze_publishers(df)
    daily_counts, hourly_counts = analyze_publication_dates(df)
    
    # Save results
    with open('results/descriptive_statistics.txt', 'w') as f:
        f.write("Headline Length Statistics:\n")
        f.write(str(headline_stats))
        f.write("\n\nPublisher Activity:\n")
        f.write(str(publisher_counts))
        f.write("\n\nDaily Publication Counts:\n")
        f.write(str(daily_counts))
        f.write("\n\nHourly Publication Counts:\n")
        f.write(str(hourly_counts))
    
    # Generate plots
    plot_publication_trends(df)

if __name__ == "__main__":
    main() 