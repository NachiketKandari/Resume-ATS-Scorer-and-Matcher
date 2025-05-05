import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

class BertModel:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()
    
    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = text.lower()
        text = ' '.join(text.split())
        return text
    
    def get_embeddings(self, text: str) -> np.ndarray:
        processed_text = self.preprocess_text(text)
        inputs = self.tokenizer(processed_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
        return embeddings[0]
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        embedding1 = self.get_embeddings(text1)
        embedding2 = self.get_embeddings(text2)
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return float(similarity)
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, float]]:
        processed_text = self.preprocess_text(text)
        tokens = word_tokenize(processed_text)
        tokens = [token for token in tokens if token not in self.stop_words]
        
        word_freq = {}
        for token in tokens:
            if token in word_freq:
                word_freq[token] += 1
            else:
                word_freq[token] = 1
        
        keyword_scores = [(word, score) for word, score in word_freq.items()]
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        return keyword_scores[:top_n]
    
    def get_missing_keywords(self, resume_text: str, job_description: str, threshold: float = 0.1) -> List[str]:
        job_keywords = self.extract_keywords(job_description)
        processed_resume = self.preprocess_text(resume_text)
        resume_tokens = word_tokenize(processed_resume)
        resume_tokens = [token for token in resume_tokens if token not in self.stop_words]
        
        missing_keywords = []
        for keyword, importance in job_keywords:
            if keyword not in resume_tokens:
                missing_keywords.append(keyword)
        
        return missing_keywords
    
    def get_keyword_coverage(self, resume_text: str, job_description: str) -> Dict[str, float]:
        job_keywords = self.extract_keywords(job_description)
        processed_resume = self.preprocess_text(resume_text)
        resume_tokens = word_tokenize(processed_resume)
        resume_tokens = [token for token in resume_tokens if token not in self.stop_words]
        
        total_keywords = len(job_keywords)
        matched_keywords = 0
        strong_matches = 0
        
        for keyword, importance in job_keywords:
            if keyword in resume_tokens:
                matched_keywords += 1
                if importance > 0.5:
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