"""
Tests for the text analysis module
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics.text_analysis import (
    preprocess_text,
    extract_keywords,
    perform_topic_modeling
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    data = {
        'headline': [
            'Financial Markets Show Strong Growth',
            'Economic Indicators Point to Recovery',
            'Stock Market Reaches New Highs',
            'Investors Optimistic About Future'
        ],
        'text': [
            'The financial markets have shown remarkable growth in recent months.',
            'Various economic indicators suggest a strong recovery is underway.',
            'The stock market has reached unprecedented levels this week.',
            'Investors are showing increased confidence in market prospects.'
        ]
    }
    return pd.DataFrame(data)

def test_preprocess_text():
    """Test text preprocessing"""
    text = "The Financial Markets are showing STRONG growth!"
    processed = preprocess_text(text)
    
    # Check if text is lowercase
    assert processed.islower()
    
    # Check if stopwords are removed
    assert 'the' not in processed
    assert 'are' not in processed
    
    # Check if punctuation is removed
    assert '!' not in processed

def test_extract_keywords(sample_data):
    """Test keyword extraction"""
    keywords_df = extract_keywords(sample_data, n_keywords=5)
    
    # Check if result is a DataFrame
    assert isinstance(keywords_df, pd.DataFrame)
    
    # Check if we have the expected columns
    assert 'keyword' in keywords_df.columns
    assert 'tfidf_score' in keywords_df.columns
    
    # Check if we have the requested number of keywords
    assert len(keywords_df) == 5
    
    # Check if keywords are sorted by score
    assert keywords_df['tfidf_score'].is_monotonic_decreasing

def test_perform_topic_modeling(sample_data):
    """Test topic modeling"""
    topics = perform_topic_modeling(sample_data, n_topics=2)
    
    # Check if we have the requested number of topics
    assert len(topics) == 2
    
    # Check if each topic has words
    assert all(len(topic) > 0 for topic in topics)
    
    # Check if words are strings
    assert all(isinstance(word, str) for topic in topics for word in topic) 