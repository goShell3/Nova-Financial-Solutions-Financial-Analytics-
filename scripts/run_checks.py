#!/usr/bin/env python
"""
Script to run all checks (tests and linting)
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
    log_file = os.path.join(log_dir, f'checks_{timestamp}.log')
    
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
            return False
        
        logger.info("All tests passed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}", exc_info=True)
        return False

def run_lint():
    """Run pylint on the codebase"""
    logger = logging.getLogger(__name__)
    
    try:
        # Run pylint on src directory
        logger.info("Running pylint on src directory")
        result = subprocess.run(
            ['pylint', 'src'],
            capture_output=True,
            text=True
        )
        
        # Log lint results
        logger.info("Lint output:\n%s", result.stdout)
        
        if result.stderr:
            logger.warning("Lint warnings/errors:\n%s", result.stderr)
        
        # Check if linting passed
        if result.returncode != 0:
            logger.error("Linting failed")
            return False
        
        logger.info("Linting completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running lint: {str(e)}", exc_info=True)
        return False

def main():
    """Main function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting checks")
        
        # Run tests
        tests_passed = run_tests()
        
        # Run linting
        lint_passed = run_lint()
        
        # Check if all checks passed
        if not (tests_passed and lint_passed):
            logger.error("Some checks failed")
            sys.exit(1)
        
        logger.info("All checks passed successfully")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 