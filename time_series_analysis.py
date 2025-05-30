import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

def analyze_publication_frequency(df):
    """Analyze publication frequency over time"""
    # Convert to datetime
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    
    # Create time series
    ts = df.groupby('publication_date').size()
    
    # Resample to daily frequency
    daily_ts = ts.resample('D').sum()
    
    return daily_ts

def analyze_publishing_times(df):
    """Analyze publishing time patterns"""
    # Extract hour and day of week
    df['hour'] = df['publication_date'].dt.hour
    df['day_of_week'] = df['publication_date'].dt.day_name()
    
    # Create heatmap data
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().unstack()
    
    return heatmap_data

def detect_seasonality(ts):
    """Detect seasonality in publication frequency"""
    # Perform seasonal decomposition
    decomposition = seasonal_decompose(ts, period=7)  # Assuming weekly seasonality
    
    return decomposition

def test_stationarity(ts):
    """Test time series stationarity"""
    # Perform Augmented Dickey-Fuller test
    result = adfuller(ts.dropna())
    
    return {
        'ADF Statistic': result[0],
        'p-value': result[1],
        'Critical Values': result[4]
    }

def plot_time_series(ts, title):
    """Plot time series data"""
    plt.figure(figsize=(15, 6))
    ts.plot()
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{title.lower().replace(" ", "_")}.png')
    plt.close()

def plot_heatmap(heatmap_data):
    """Plot publishing time heatmap"""
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd')
    plt.title('Publication Frequency by Day and Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.tight_layout()
    plt.savefig('publication_heatmap.png')
    plt.close()

def main():
    # Load your data
    df = pd.read_csv('data/processed_data.csv')
    
    # Analyze publication frequency
    daily_ts = analyze_publication_frequency(df)
    
    # Analyze publishing times
    heatmap_data = analyze_publishing_times(df)
    
    # Detect seasonality
    decomposition = detect_seasonality(daily_ts)
    
    # Test stationarity
    stationarity_test = test_stationarity(daily_ts)
    
    # Save results
    with open('results/time_series_analysis.txt', 'w') as f:
        f.write("Publication Frequency Statistics:\n")
        f.write(str(daily_ts.describe()))
        f.write("\n\nStationarity Test Results:\n")
        f.write(str(stationarity_test))
        f.write("\n\nSeasonal Decomposition:\n")
        f.write(f"Trend:\n{decomposition.trend.describe()}\n")
        f.write(f"Seasonal:\n{decomposition.seasonal.describe()}\n")
        f.write(f"Residual:\n{decomposition.resid.describe()}\n")
    
    # Generate plots
    plot_time_series(daily_ts, 'Daily Publication Frequency')
    plot_heatmap(heatmap_data)
    
    # Plot decomposition components
    plt.figure(figsize=(15, 10))
    plt.subplot(411)
    daily_ts.plot()
    plt.title('Original Time Series')
    plt.subplot(412)
    decomposition.trend.plot()
    plt.title('Trend')
    plt.subplot(413)
    decomposition.seasonal.plot()
    plt.title('Seasonal')
    plt.subplot(414)
    decomposition.resid.plot()
    plt.title('Residual')
    plt.tight_layout()
    plt.savefig('time_series_decomposition.png')
    plt.close()

if __name__ == "__main__":
    main() 