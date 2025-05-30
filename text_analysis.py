import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import seaborn as sns

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """Preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

def extract_keywords(df, column='headline', n_keywords=20):
    """Extract most common keywords"""
    # Preprocess text
    df['processed_text'] = df[column].apply(preprocess_text)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=n_keywords)
    tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
    
    # Get feature names
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate average TF-IDF scores
    avg_tfidf = tfidf_matrix.mean(axis=0).A1
    
    # Create keyword dataframe
    keywords_df = pd.DataFrame({
        'keyword': feature_names,
        'tfidf_score': avg_tfidf
    }).sort_values('tfidf_score', ascending=False)
    
    return keywords_df

def perform_topic_modeling(df, column='headline', n_topics=5):
    """Perform topic modeling using LDA"""
    # Preprocess text
    df['processed_text'] = df[column].apply(preprocess_text)
    
    # Create document-term matrix
    vectorizer = CountVectorizer(max_df=0.95, min_df=2)
    doc_term_matrix = vectorizer.fit_transform(df['processed_text'])
    
    # Perform LDA
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda_output = lda.fit_transform(doc_term_matrix)
    
    # Get feature names
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top words for each topic
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10-1:-1]]
        topics.append(top_words)
    
    return topics

def plot_keyword_distribution(keywords_df):
    """Plot keyword distribution"""
    plt.figure(figsize=(12, 6))
    sns.barplot(x='tfidf_score', y='keyword', data=keywords_df.head(10))
    plt.title('Top 10 Keywords by TF-IDF Score')
    plt.xlabel('TF-IDF Score')
    plt.ylabel('Keyword')
    plt.tight_layout()
    plt.savefig('keyword_distribution.png')
    plt.close()

def main():
    # Load your data
    df = pd.read_csv('data/processed_data.csv')
    
    # Extract keywords
    keywords_df = extract_keywords(df)
    
    # Perform topic modeling
    topics = perform_topic_modeling(df)
    
    # Save results
    with open('results/text_analysis.txt', 'w') as f:
        f.write("Top Keywords:\n")
        f.write(str(keywords_df))
        f.write("\n\nIdentified Topics:\n")
        for i, topic in enumerate(topics):
            f.write(f"\nTopic {i+1}:\n")
            f.write(', '.join(topic))
    
    # Generate plots
    plot_keyword_distribution(keywords_df)

if __name__ == "__main__":
    main() 