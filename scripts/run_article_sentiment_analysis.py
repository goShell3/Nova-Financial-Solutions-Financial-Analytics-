import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.append(src_path)

from article_sentiment_analysis import ArticleSentimentAnalyzer

def main():
    # Initialize the analyzer
    data_path = "data/raw_analyst_ratings.csv"
    analyzer = ArticleSentimentAnalyzer(data_path)
    
    # Run the full analysis
    analyzer.run_full_analysis()
    
    print("Analysis complete! Check the data/processed directory for results.")

if __name__ == "__main__":
    main() 