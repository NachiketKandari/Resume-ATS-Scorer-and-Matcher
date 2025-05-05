import json
import glob
import os
import PyPDF2
from typing import Optional

def convert_resume_to_txt(resume_json):
    """Convert a resume JSON object to formatted text"""
    text = []
    
    # Personal Information
    text.append(resume_json['name'].upper())
    text.append(f"Email: {resume_json['email']}")
    text.append(f"Phone: {resume_json['phone']}")
    text.append(f"Location: {resume_json['location']}")
    text.append("\n")
    
    # Summary
    text.append("PROFESSIONAL SUMMARY")
    text.append("-" * 20)
    text.append(resume_json['summary'])
    text.append("\n")
    
    # Skills
    text.append("SKILLS")
    text.append("-" * 20)
    text.append(", ".join(resume_json['skills']))
    text.append("\n")
    
    # Experience
    text.append("PROFESSIONAL EXPERIENCE")
    text.append("-" * 20)
    for exp in resume_json['experience']:
        text.append(f"{exp['title']} at {exp['company']}")
        text.append(f"Duration: {exp['duration']}")
        for desc in exp['description']:
            text.append(f"• {desc}")
        text.append("")
    text.append("\n")
    
    # Education
    text.append("EDUCATION")
    text.append("-" * 20)
    for edu in resume_json['education']:
        text.append(f"{edu['degree']} in {edu['field']}")
        text.append(f"{edu['university']}, {edu['year']}")
        text.append("")
    
    return "\n".join(text)

def convert_all_resumes():
    # Create output directory if it doesn't exist
    os.makedirs("data/raw/resumes_txt", exist_ok=True)
    
    # Get all JSON resume files
    resume_files = glob.glob("data/raw/resumes/resume_*.json")
    
    # Convert each resume
    for resume_file in resume_files:
        # Read JSON
        with open(resume_file, 'r') as f:
            resume_json = json.load(f)
        
        # Convert to text
        resume_text = convert_resume_to_txt(resume_json)
        
        # Write to text file
        output_file = resume_file.replace("/resumes/", "/resumes_txt/").replace(".json", ".txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resume_text)

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    try:
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            return None
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None

def convert_all_resumes(input_dir: str, output_dir: str) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            txt_path = os.path.join(output_dir, filename.replace('.pdf', '.txt'))
            
            text = extract_text_from_pdf(pdf_path)
            if text:
                with open(txt_path, 'w', encoding='utf-8') as file:
                    file.write(text)
                print(f"Successfully converted {filename} to text")
            else:
                print(f"Failed to convert {filename} to text")

def main():
    input_dir = "data/raw/resumes"
    output_dir = "data/raw/resumes_txt"
    convert_all_resumes(input_dir, output_dir)

if __name__ == "__main__":
    main() 