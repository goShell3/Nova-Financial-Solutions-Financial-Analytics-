"""
Tests for the publisher analysis module
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics.publisher_analysis import (
    analyze_publisher_activity,
    analyze_publisher_domains,
    analyze_publisher_content,
    analyze_publisher_timing
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    data = {
        'publisher': ['publisher1@domain1.com', 'publisher2@domain2.com', 
                     'publisher1@domain1.com', 'publisher3@domain3.com'],
        'headline': ['Headline 1', 'Headline 2', 'Headline 3', 'Headline 4'],
        'text': ['Text 1', 'Text 2', 'Text 3', 'Text 4'],
        'publication_date': ['2024-01-01 10:00:00', '2024-01-01 14:00:00',
                           '2024-01-02 09:00:00', '2024-01-02 15:00:00']
    }
    return pd.DataFrame(data)

def test_analyze_publisher_activity(sample_data):
    """Test publisher activity analysis"""
    counts, percentages = analyze_publisher_activity(sample_data)
    
    # Check counts
    assert counts['publisher1@domain1.com'] == 2
    assert counts['publisher2@domain2.com'] == 1
    assert counts['publisher3@domain3.com'] == 1
    
    # Check percentages
    assert percentages['publisher1@domain1.com'] == 50.0
    assert percentages['publisher2@domain2.com'] == 25.0
    assert percentages['publisher3@domain3.com'] == 25.0

def test_analyze_publisher_domains(sample_data):
    """Test publisher domain analysis"""
    domain_counts = analyze_publisher_domains(sample_data)
    
    assert domain_counts['domain1.com'] == 2
    assert domain_counts['domain2.com'] == 1
    assert domain_counts['domain3.com'] == 1

def test_analyze_publisher_content(sample_data):
    """Test publisher content analysis"""
    content = analyze_publisher_content(sample_data)
    
    # Check article counts
    assert content.loc['publisher1@domain1.com', 'article_count'] == 2
    assert content.loc['publisher2@domain2.com', 'article_count'] == 1
    assert content.loc['publisher3@domain3.com', 'article_count'] == 1
    
    # Check average text length
    assert 'avg_text_length' in content.columns

def test_analyze_publisher_timing(sample_data):
    """Test publisher timing analysis"""
    timing = analyze_publisher_timing(sample_data)
    
    # Check if timing analysis returns expected columns
    assert ('hour', 'mean') in timing.columns
    assert ('hour', 'std') in timing.columns
    assert ('day_of_week', '<lambda>') in timing.columns 