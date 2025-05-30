#!/usr/bin/env python
"""
Script to run all financial news analyses
"""

import os
import sys
import logging
from datetime import datetime

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.analytics.descriptive_statistics import main as run_descriptive_stats
from src.analytics.text_analysis import main as run_text_analysis
from src.analytics.time_series_analysis import main as run_time_series
from src.analytics.publisher_analysis import main as run_publisher_analysis

def setup_logging():
    """Set up logging configuration"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'analysis_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    """Run all analyses"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting financial news analysis")
        
        # Run descriptive statistics
        logger.info("Running descriptive statistics analysis")
        run_descriptive_stats()
        
        # Run text analysis
        logger.info("Running text analysis")
        run_text_analysis()
        
        # Run time series analysis
        logger.info("Running time series analysis")
        run_time_series()
        
        # Run publisher analysis
        logger.info("Running publisher analysis")
        run_publisher_analysis()
        
        logger.info("All analyses completed successfully")
        
    except Exception as e:
        logger.error(f"Error running analyses: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 