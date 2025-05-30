"""
Shared test fixtures
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_news_data():
    """Create a comprehensive sample dataset for testing"""
    # Generate dates
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(24)]
    
    data = {
        'headline': [
            'Financial Markets Show Strong Growth',
            'Economic Indicators Point to Recovery',
            'Stock Market Reaches New Highs',
            'Investors Optimistic About Future',
            'Global Markets React to Policy Changes',
            'Tech Sector Leads Market Gains',
            'Central Bank Announces New Measures',
            'Inflation Data Shows Positive Trends',
            'Corporate Earnings Exceed Expectations',
            'Market Analysts Predict Continued Growth',
            'Financial Markets Show Strong Growth',
            'Economic Indicators Point to Recovery',
            'Stock Market Reaches New Highs',
            'Investors Optimistic About Future',
            'Global Markets React to Policy Changes',
            'Tech Sector Leads Market Gains',
            'Central Bank Announces New Measures',
            'Inflation Data Shows Positive Trends',
            'Corporate Earnings Exceed Expectations',
            'Market Analysts Predict Continued Growth',
            'Financial Markets Show Strong Growth',
            'Economic Indicators Point to Recovery',
            'Stock Market Reaches New Highs',
            'Investors Optimistic About Future'
        ],
        'text': [
            'The financial markets have shown remarkable growth in recent months.',
            'Various economic indicators suggest a strong recovery is underway.',
            'The stock market has reached unprecedented levels this week.',
            'Investors are showing increased confidence in market prospects.',
            'Global financial markets are responding to recent policy changes.',
            'Technology companies are driving significant market gains.',
            'The central bank has implemented new monetary measures.',
            'Latest inflation data indicates positive economic trends.',
            'Major corporations are reporting better-than-expected earnings.',
            'Leading analysts forecast continued market growth.',
            'The financial markets have shown remarkable growth in recent months.',
            'Various economic indicators suggest a strong recovery is underway.',
            'The stock market has reached unprecedented levels this week.',
            'Investors are showing increased confidence in market prospects.',
            'Global financial markets are responding to recent policy changes.',
            'Technology companies are driving significant market gains.',
            'The central bank has implemented new monetary measures.',
            'Latest inflation data indicates positive economic trends.',
            'Major corporations are reporting better-than-expected earnings.',
            'Leading analysts forecast continued market growth.',
            'The financial markets have shown remarkable growth in recent months.',
            'Various economic indicators suggest a strong recovery is underway.',
            'The stock market has reached unprecedented levels this week.',
            'Investors are showing increased confidence in market prospects.'
        ],
        'publisher': [
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com',
            'publisher1@domain1.com',
            'publisher2@domain2.com',
            'publisher3@domain3.com'
        ],
        'publication_date': dates
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_time_series_data():
    """Create sample time series data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='H')
    values = np.random.normal(100, 10, len(dates))
    return pd.Series(values, index=dates) 