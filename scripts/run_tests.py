#!/usr/bin/env python
"""
Script to run tests with coverage
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

def setup_logging():
    """Set up logging configuration"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'tests_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def run_tests():
    """Run tests with coverage"""
    logger = logging.getLogger(__name__)
    
    try:
        # Run pytest with coverage
        logger.info("Running tests with coverage")
        result = subprocess.run(
            ['pytest', '--cov=src', '--cov-report=term-missing'],
            capture_output=True,
            text=True
        )
        
        # Log test results
        logger.info("Test output:\n%s", result.stdout)
        
        if result.stderr:
            logger.warning("Test warnings/errors:\n%s", result.stderr)
        
        # Check if tests passed
        if result.returncode != 0:
            logger.error("Tests failed")
            sys.exit(1)
        
        logger.info("All tests passed successfully")
        
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}", exc_info=True)
        sys.exit(1)

def main():
    """Main function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting test run")
        run_tests()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 