import os
import pandas as pd
import json
from typing import Dict, List, Any
from models.simplified_model import SimplifiedModel
from preprocessing.resume_parser import ResumeParser

def load_job_descriptions(jobs_file: str) -> pd.DataFrame:
    return pd.read_csv(jobs_file)

def analyze_resume(resume_path: str, job_descriptions: pd.DataFrame, model: SimplifiedModel, parser: ResumeParser) -> List[Dict[str, Any]]:
    results = []
    resume_text = parser.extract_text_from_txt(resume_path)
    
    if not resume_text:
        print(f"Failed to extract text from {resume_path}")
        return results
    
    for _, job in job_descriptions.iterrows():
        analysis = model.analyze_resume(resume_text, job['description'])
        results.append({
            'job_title': job['title'],
            'score': analysis['score'],
            'missing_keywords': analysis['missing_keywords'],
            'suggestions': analysis['suggestions']
        })
    
    return results

def save_results(results: List[Dict[str, Any]], output_dir: str, resume_name: str) -> None:
    resume_output_dir = os.path.join(output_dir, resume_name)
    os.makedirs(resume_output_dir, exist_ok=True)
    
    with open(os.path.join(resume_output_dir, 'analysis_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    with open(os.path.join(resume_output_dir, 'analysis_summary.txt'), 'w') as f:
        f.write(f"Analysis Results for {resume_name}\n")
        f.write("=" * 50 + "\n\n")
        
        for result in results:
            f.write(f"Job Title: {result['job_title']}\n")
            f.write(f"Score: {result['score']:.2f}%\n")
            f.write("\nMissing Keywords:\n")
            for keyword in result['missing_keywords']:
                f.write(f"- {keyword}\n")
            f.write("\nSuggestions:\n")
            for suggestion in result['suggestions']:
                f.write(f"- {suggestion}\n")
            f.write("\n" + "=" * 50 + "\n\n")

def main():
    jobs_file = "data/raw/jobs/sample_jobs.csv"
    resumes_dir = "data/raw/resumes_txt"
    output_dir = "output"
    
    model = SimplifiedModel()
    parser = ResumeParser()
    
    job_descriptions = load_job_descriptions(jobs_file)
    
    for filename in os.listdir(resumes_dir):
        if filename.endswith('.txt'):
            resume_path = os.path.join(resumes_dir, filename)
            resume_name = os.path.splitext(filename)[0]
            
            try:
                results = analyze_resume(resume_path, job_descriptions, model, parser)
                save_results(results, output_dir, resume_name)
                print(f"Completed analysis for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main() 