import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    """
    Preprocess text by removing special characters, converting to lowercase,
    removing stopwords, and lemmatizing.
    
    Args:
        text (str): Input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize
    doc = nlp(' '.join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]
    
    return ' '.join(lemmatized_tokens)

def extract_skills(text):
    """
    Extract skills from text using NLP techniques.
    
    Args:
        text (str): Input text to extract skills from
        
    Returns:
        list: List of extracted skills
    """
    if not text:
        return []
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Extract noun phrases and named entities as potential skills
    skills = []
    
    # Add noun phrases
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Limit to phrases of 3 words or less
            skills.append(chunk.text.lower())
    
    # Add named entities
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'TECH']:
            skills.append(ent.text.lower())
    
    # Remove duplicates and sort
    skills = list(set(skills))
    skills.sort()
    
    return skills

def extract_keywords(text, top_n=10):
    """
    Extract keywords from text using TF-IDF approach.
    
    Args:
        text (str): Input text to extract keywords from
        top_n (int): Number of top keywords to extract
        
    Returns:
        list: List of extracted keywords
    """
    if not text:
        return []
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Count word frequencies
    word_freq = {}
    for token in doc:
        if not token.is_stop and not token.is_punct and token.is_alpha:
            word = token.text.lower()
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Return top N words
    return [word for word, _ in sorted_words[:top_n]] 