"""
Publisher Analysis Module for Financial News Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

def analyze_publisher_activity(df):
    """Analyze publisher activity and contribution"""
    # Count articles per publisher
    publisher_counts = df['publisher'].value_counts()
    
    # Calculate percentage of total articles
    publisher_percentages = (publisher_counts / len(df) * 100).round(2)
    
    return publisher_counts, publisher_percentages

def analyze_publisher_domains(df):
    """Analyze publisher email domains"""
    # Extract domains from email addresses
    def extract_domain(email):
        if '@' in str(email):
            return email.split('@')[1]
        return email
    
    df['domain'] = df['publisher'].apply(extract_domain)
    domain_counts = df['domain'].value_counts()
    
    return domain_counts

def analyze_publisher_content(df):
    """Analyze content patterns by publisher"""
    # Group by publisher and analyze content
    publisher_content = df.groupby('publisher').agg({
        'headline': 'count',
        'text': lambda x: x.str.len().mean()  # Average text length
    }).rename(columns={
        'headline': 'article_count',
        'text': 'avg_text_length'
    })
    
    return publisher_content

def analyze_publisher_timing(df):
    """Analyze publishing patterns by publisher"""
    # Convert to datetime
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    
    # Extract hour and day
    df['hour'] = df['publication_date'].dt.hour
    df['day_of_week'] = df['publication_date'].dt.day_name()
    
    # Analyze timing patterns by publisher
    timing_patterns = df.groupby('publisher').agg({
        'hour': ['mean', 'std'],
        'day_of_week': lambda x: x.mode()[0] if not x.empty else None
    })
    
    return timing_patterns

def plot_publisher_distribution(publisher_counts):
    """Plot publisher distribution"""
    plt.figure(figsize=(12, 6))
    publisher_counts.head(10).plot(kind='bar')
    plt.title('Top 10 Publishers by Article Count')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('publisher_distribution.png')
    plt.close()

def plot_domain_distribution(domain_counts):
    """Plot domain distribution"""
    plt.figure(figsize=(12, 6))
    domain_counts.head(10).plot(kind='bar')
    plt.title('Top 10 Publisher Domains')
    plt.xlabel('Domain')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('domain_distribution.png')
    plt.close()

def main():
    # Load your data
    df = pd.read_csv('data/processed_data.csv')
    
    # Analyze publisher activity
    publisher_counts, publisher_percentages = analyze_publisher_activity(df)
    
    # Analyze publisher domains
    domain_counts = analyze_publisher_domains(df)
    
    # Analyze publisher content
    publisher_content = analyze_publisher_content(df)
    
    # Analyze publisher timing
    timing_patterns = analyze_publisher_timing(df)
    
    # Save results
    with open('results/publisher_analysis.txt', 'w') as f:
        f.write("Publisher Activity Analysis:\n")
        f.write("\nTop Publishers by Article Count:\n")
        f.write(str(publisher_counts.head(10)))
        f.write("\n\nPublisher Percentages:\n")
        f.write(str(publisher_percentages.head(10)))
        f.write("\n\nTop Publisher Domains:\n")
        f.write(str(domain_counts.head(10)))
        f.write("\n\nPublisher Content Analysis:\n")
        f.write(str(publisher_content))
        f.write("\n\nPublisher Timing Patterns:\n")
        f.write(str(timing_patterns))
    
    # Generate plots
    plot_publisher_distribution(publisher_counts)
    plot_domain_distribution(domain_counts)

if __name__ == "__main__":
    main() 