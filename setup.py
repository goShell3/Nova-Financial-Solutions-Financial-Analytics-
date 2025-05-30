from setuptools import setup, find_packages

setup(
    name="financial-analytics",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "nltk",
        "statsmodels"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pylint"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Financial Analytics Package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-analytics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 