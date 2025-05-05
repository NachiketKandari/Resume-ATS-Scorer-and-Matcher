import os
import pandas as pd
from typing import List, Dict
import json
from pathlib import Path
from src.models.simplified_model import SimplifiedModel
from src.preprocessing.resume_parser import ResumeParser
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(s))]

def load_job_descriptions(csv_path: str) -> List[Dict]:
    df = pd.read_csv(csv_path)
    jobs = []
    for _, row in df.iterrows():
        job = {
            'title': row['title'],
            'description': row['description'],
            'required_skills': row['required_skills']
        }
        jobs.append(job)
    return jobs

def analyze_resume(resume_path: str, jobs: List[Dict], model: SimplifiedModel, parser: ResumeParser) -> Dict:
    resume_text = parser.extract_text_from_pdf(resume_path)
    
    results = {}
    for job in jobs:
        job_text = f"{job['description']} {job['required_skills']}"
        analysis = model.analyze_resume(resume_text, job_text)
        
        results[job['title']] = {
            'score': analysis['overall_score'],
            'similarity': analysis['similarity_score'],
            'missing_keywords': analysis['missing_keywords'],
            'coverage': analysis['coverage_stats'],
            'suggestions': analysis['improvement_suggestions']
        }
    
    return results

def save_results(resume_name: str, results: Dict):
    output_dir = Path('output') / resume_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'detailed_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    summary = []
    summary.append(f"Analysis Results for {resume_name}\n")
    summary.append("=" * 50 + "\n")
    
    for job_title, result in results.items():
        summary.append(f"\nJob: {job_title}")
        summary.append(f"Overall Score: {result['score']:.2f}%")
        summary.append(f"Similarity Score: {result['similarity']:.2f}")
        summary.append("\nCoverage Statistics:")
        summary.append(f"- Total Keywords: {result['coverage']['total_keywords']}")
        summary.append(f"- Matched Keywords: {result['coverage']['matched_keywords']}")
        summary.append(f"- Coverage Percentage: {result['coverage']['coverage_percentage']:.2f}%")
        summary.append(f"- Strong Matches: {result['coverage']['strong_matches']}")
        
        if result['missing_keywords']:
            summary.append("\nMissing Keywords:")
            summary.append(", ".join(result['missing_keywords'][:5]))
        
        if result['suggestions']:
            summary.append("\nImprovement Suggestions:")
            for suggestion in result['suggestions']:
                summary.append(f"- {suggestion}")
        
        summary.append("\n" + "=" * 50)
    
    with open(output_dir / 'summary.txt', 'w') as f:
        f.write('\n'.join(summary))

def main():
    model = SimplifiedModel()
    parser = ResumeParser()
    
    jobs = load_job_descriptions('data/raw/jobs/sample_jobs.csv')
    print(f"Loaded {len(jobs)} job descriptions")
    
    resume_dir = Path('data/raw/resumes')
    resume_files = sorted(resume_dir.glob('*.txt'), key=natural_sort_key)
    
    for resume_file in resume_files:
        print(f"\nProcessing {resume_file.name}...")
        try:
            results = analyze_resume(str(resume_file), jobs, model, parser)
            save_results(resume_file.stem, results)
            print(f"Successfully analyzed {resume_file.name}")
        except Exception as e:
            print(f"Error processing {resume_file.name}: {str(e)}")

if __name__ == '__main__':
    main() 