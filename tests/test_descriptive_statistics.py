"""
Tests for the descriptive statistics module
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics.descriptive_statistics import (
    analyze_headline_lengths,
    analyze_publishers,
    analyze_publication_dates
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    data = {
        'headline': [
            'Short Headline',
            'This is a longer headline for testing',
            'Another headline',
            'A very long headline that contains more words than the others'
        ],
        'publisher': [
            'Publisher A',
            'Publisher B',
            'Publisher A',
            'Publisher C'
        ],
        'publication_date': [
            '2024-01-01 10:00:00',
            '2024-01-01 14:00:00',
            '2024-01-02 09:00:00',
            '2024-01-02 15:00:00'
        ]
    }
    return pd.DataFrame(data)

def test_analyze_headline_lengths(sample_data):
    """Test headline length analysis"""
    stats = analyze_headline_lengths(sample_data)
    
    # Check if result is a Series
    assert isinstance(stats, pd.Series)
    
    # Check if we have the expected statistics
    assert 'count' in stats
    assert 'mean' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    
    # Check if the statistics make sense
    assert stats['count'] == 4  # Number of headlines
    assert stats['min'] <= stats['mean'] <= stats['max']

def test_analyze_publishers(sample_data):
    """Test publisher analysis"""
    publisher_counts = analyze_publishers(sample_data)
    
    # Check if result is a Series
    assert isinstance(publisher_counts, pd.Series)
    
    # Check if counts are correct
    assert publisher_counts['Publisher A'] == 2
    assert publisher_counts['Publisher B'] == 1
    assert publisher_counts['Publisher C'] == 1
    
    # Check if counts are sorted
    assert publisher_counts.is_monotonic_decreasing

def test_analyze_publication_dates(sample_data):
    """Test publication date analysis"""
    daily_counts, hourly_counts = analyze_publication_dates(sample_data)
    
    # Check if results are Series
    assert isinstance(daily_counts, pd.Series)
    assert isinstance(hourly_counts, pd.Series)
    
    # Check if we have the expected days
    assert 'Monday' in daily_counts.index
    assert 'Tuesday' in daily_counts.index
    
    # Check if we have the expected hours
    assert 9 in hourly_counts.index
    assert 10 in hourly_counts.index
    assert 14 in hourly_counts.index
    assert 15 in hourly_counts.index
    
    # Check if counts are correct
    assert daily_counts['Monday'] == 2  # Two articles on Monday
    assert daily_counts['Tuesday'] == 2  # Two articles on Tuesday 