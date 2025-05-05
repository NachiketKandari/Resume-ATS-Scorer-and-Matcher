from typing import Dict, List, Tuple
import numpy as np
from src.models.bert_model import BertModel
from src.models.tfidf_model import TfidfModel
from src.preprocessing.resume_parser import ResumeParser


class ResumeScorer:
    def __init__(self, model_type: str = 'bert'):
        self.model_type = model_type.lower()
        if self.model_type == 'bert':
            self.model = BertModel()
        elif self.model_type == 'tfidf':
            self.model = TfidfModel()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        self.parser = ResumeParser()
    
    def analyze_resume(self, resume_path: str, job_description: str) -> Dict:
        resume_text = self.parser.extract_text(resume_path)
        if not resume_text:
            return {
                'overall_score': 0,
                'similarity_score': 0,
                'keyword_score': 0,
                'missing_keywords': [],
                'coverage_stats': {
                    'coverage_percentage': 0,
                    'strong_match_percentage': 0,
                    'total_keywords': 0,
                    'matched_keywords': 0,
                    'strong_matches': 0
                },
                'improvement_suggestions': ["Error: Could not extract text from resume"]
            }
        
        similarity_score = self.model.compute_similarity(resume_text, job_description)
        missing_keywords = self.model.get_missing_keywords(resume_text, job_description)
        coverage_stats = self.model.get_keyword_coverage(resume_text, job_description)
        
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
            'keyword_score': coverage_stats['coverage_percentage'] / 100,
            'missing_keywords': missing_keywords,
            'coverage_stats': coverage_stats,
            'improvement_suggestions': improvement_suggestions
        }
    
    def get_detailed_analysis(self, resume_path: str, job_description: str) -> Dict:
        resume_data = self.parser.parse_resume(resume_path)
        if not resume_data:
            return {
                'error': "Could not parse resume",
                'analysis': None
            }
        
        analysis = self.analyze_resume(resume_path, job_description)
        
        return {
            'resume_data': resume_data,
            'analysis': analysis
        }
    
    def compare_resumes(self, resume_paths: List[str], job_description: str) -> List[Tuple[str, float]]:
        resume_scores = []
        
        for resume_path in resume_paths:
            analysis = self.analyze_resume(resume_path, job_description)
            resume_name = resume_path.split('/')[-1]
            resume_scores.append((resume_name, analysis['overall_score']))
        
        resume_scores.sort(key=lambda x: x[1], reverse=True)
        return resume_scores 