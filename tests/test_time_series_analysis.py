"""
Tests for the time series analysis module
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics.time_series_analysis import (
    analyze_publication_frequency,
    analyze_publishing_times,
    detect_seasonality,
    test_stationarity
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='H')
    data = {
        'publication_date': dates,
        'headline': [f'Headline {i}' for i in range(len(dates))],
        'text': [f'Text {i}' for i in range(len(dates))]
    }
    return pd.DataFrame(data)

def test_analyze_publication_frequency(sample_data):
    """Test publication frequency analysis"""
    daily_ts = analyze_publication_frequency(sample_data)
    
    # Check if the result is a time series
    assert isinstance(daily_ts, pd.Series)
    
    # Check if the index is datetime
    assert isinstance(daily_ts.index, pd.DatetimeIndex)
    
    # Check if we have daily frequency
    assert daily_ts.index.freq == 'D'

def test_analyze_publishing_times(sample_data):
    """Test publishing times analysis"""
    heatmap_data = analyze_publishing_times(sample_data)
    
    # Check if the result is a DataFrame
    assert isinstance(heatmap_data, pd.DataFrame)
    
    # Check if we have the expected columns (hours)
    assert all(hour in heatmap_data.columns for hour in range(24))
    
    # Check if we have the expected index (days of week)
    expected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                    'Friday', 'Saturday', 'Sunday']
    assert all(day in heatmap_data.index for day in expected_days)

def test_detect_seasonality(sample_data):
    """Test seasonality detection"""
    daily_ts = analyze_publication_frequency(sample_data)
    decomposition = detect_seasonality(daily_ts)
    
    # Check if we have all components
    assert hasattr(decomposition, 'trend')
    assert hasattr(decomposition, 'seasonal')
    assert hasattr(decomposition, 'resid')
    
    # Check if components are time series
    assert isinstance(decomposition.trend, pd.Series)
    assert isinstance(decomposition.seasonal, pd.Series)
    assert isinstance(decomposition.resid, pd.Series)

def test_test_stationarity(sample_data):
    """Test stationarity testing"""
    daily_ts = analyze_publication_frequency(sample_data)
    result = test_stationarity(daily_ts)
    
    # Check if we have all required statistics
    assert 'ADF Statistic' in result
    assert 'p-value' in result
    assert 'Critical Values' in result
    
    # Check if critical values are present
    assert isinstance(result['Critical Values'], dict)
    assert all(key in result['Critical Values'] for key in ['1%', '5%', '10%']) 