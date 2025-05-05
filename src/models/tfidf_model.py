from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

class TfidfModel:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
    
    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = text.lower()
        text = ' '.join(text.split())
        return text
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, float]]:
        processed_text = self.preprocess_text(text)
        tfidf_matrix = self.vectorizer.fit_transform([processed_text])
        feature_names = self.vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        keyword_scores = [(feature_names[i], tfidf_scores[i]) 
                         for i in range(len(feature_names))]
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        return keyword_scores[:top_n]
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        processed_text1 = self.preprocess_text(text1)
        processed_text2 = self.preprocess_text(text2)
        tfidf_matrix = self.vectorizer.fit_transform([processed_text1, processed_text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    
    def get_missing_keywords(self, resume_text: str, job_description: str, threshold: float = 0.1) -> List[str]:
        job_keywords = self.extract_keywords(job_description)
        processed_resume = self.preprocess_text(resume_text)
        tfidf_matrix = self.vectorizer.transform([processed_resume])
        resume_scores = tfidf_matrix.toarray()[0]
        missing_keywords = []
        for keyword, importance in job_keywords:
            keyword_idx = self.vectorizer.vocabulary_.get(keyword)
            if keyword_idx is not None:
                score = resume_scores[keyword_idx]
                if score < threshold:
                    missing_keywords.append(keyword)
        return missing_keywords
    
    def get_keyword_coverage(self, resume_text: str, job_description: str) -> Dict[str, float]:
        job_keywords = self.extract_keywords(job_description)
        processed_resume = self.preprocess_text(resume_text)
        tfidf_matrix = self.vectorizer.transform([processed_resume])
        resume_scores = tfidf_matrix.toarray()[0]
        total_keywords = len(job_keywords)
        matched_keywords = 0
        strong_matches = 0
        
        for keyword, importance in job_keywords:
            keyword_idx = self.vectorizer.vocabulary_.get(keyword)
            if keyword_idx is not None:
                score = resume_scores[keyword_idx]
                if score > 0:
                    matched_keywords += 1
                if score > 0.5:
                    strong_matches += 1
        
        coverage_percentage = (matched_keywords / total_keywords * 100) if total_keywords > 0 else 0
        strong_match_percentage = (strong_matches / total_keywords * 100) if total_keywords > 0 else 0
        
        return {
            'coverage_percentage': coverage_percentage,
            'strong_match_percentage': strong_match_percentage,
            'total_keywords': total_keywords,
            'matched_keywords': matched_keywords,
            'strong_matches': strong_matches
        }
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        similarity_score = self.compute_similarity(resume_text, job_description)
        missing_keywords = self.get_missing_keywords(resume_text, job_description)
        coverage_stats = self.get_keyword_coverage(resume_text, job_description)
        overall_score = (similarity_score * 0.4 + coverage_stats['coverage_percentage'] / 100 * 0.6) * 100
        
        improvement_suggestions = []
        
        if missing_keywords:
            improvement_suggestions.append(f"Add experience with: {', '.join(missing_keywords[:5])}")
        
        if coverage_stats['coverage_percentage'] < 70:
            improvement_suggestions.append("Expand your resume to better match the job requirements")
        
        if coverage_stats['strong_match_percentage'] < 30:
            improvement_suggestions.append("Highlight your relevant experience more prominently")
        
        return {
            'overall_score': overall_score,
            'similarity_score': similarity_score,
            'missing_keywords': missing_keywords,
            'coverage_stats': coverage_stats,
            'improvement_suggestions': improvement_suggestions
        } 