# Financial Analytics Package

A Python package for analyzing financial news data, providing tools for descriptive statistics, text analysis, time series analysis, and publisher analysis.

## Features

- **Descriptive Statistics**: Analyze headline lengths, publisher activity, and publication date trends
- **Text Analysis**: Extract keywords, perform topic modeling, and analyze text patterns
- **Time Series Analysis**: Analyze publication frequency, detect seasonality, and test stationarity
- **Publisher Analysis**: Analyze publisher activity, domains, content patterns, and timing

## Installation

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Descriptive Statistics

```python
from src.analytics.descriptive_statistics import analyze_headline_lengths, analyze_publishers

# Load your data
df = pd.read_csv('data/processed_data.csv')

# Analyze headline lengths
headline_stats = analyze_headline_lengths(df)

# Analyze publishers
publisher_counts = analyze_publishers(df)
```

### Text Analysis

```python
from src.analytics.text_analysis import extract_keywords, perform_topic_modeling

# Extract keywords
keywords_df = extract_keywords(df, n_keywords=20)

# Perform topic modeling
topics = perform_topic_modeling(df, n_topics=5)
```

### Time Series Analysis

```python
from src.analytics.time_series_analysis import analyze_publication_frequency, detect_seasonality

# Analyze publication frequency
daily_ts = analyze_publication_frequency(df)

# Detect seasonality
decomposition = detect_seasonality(daily_ts)
```

### Publisher Analysis

```python
from src.analytics.publisher_analysis import analyze_publisher_activity, analyze_publisher_domains

# Analyze publisher activity
publisher_counts, publisher_percentages = analyze_publisher_activity(df)

# Analyze publisher domains
domain_counts = analyze_publisher_domains(df)
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=src
```

### Linting

```bash
pylint src
```

## Project Structure

```
financial-analytics/
├── src/
│   └── analytics/
│       ├── __init__.py
│       ├── descriptive_statistics.py
│       ├── text_analysis.py
│       ├── time_series_analysis.py
│       └── publisher_analysis.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_descriptive_statistics.py
│   ├── test_text_analysis.py
│   ├── test_time_series_analysis.py
│   └── test_publisher_analysis.py
├── data/
│   └── processed_data.csv
├── results/
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── setup.py
├── pytest.ini
├── .coveragerc
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.