import PyPDF2
import os
import re
from typing import Dict, List, Optional

class ResumeParser:
    def __init__(self):
        self.section_headers = [
            'EDUCATION', 'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT HISTORY',
            'PROFESSIONAL EXPERIENCE', 'SKILLS', 'TECHNICAL SKILLS', 'CORE COMPETENCIES',
            'PROJECTS', 'CERTIFICATIONS', 'AWARDS', 'ACHIEVEMENTS', 'SUMMARY',
            'PROFESSIONAL SUMMARY', 'OBJECTIVE', 'CAREER OBJECTIVE'
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
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
    
    def extract_text_from_txt(self, txt_path: str) -> Optional[str]:
        try:
            if not os.path.exists(txt_path):
                print(f"File not found: {txt_path}")
                return None
            
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return text.strip()
        
        except Exception as e:
            print(f"Error reading text file {txt_path}: {e}")
            return None
    
    def extract_text(self, file_path: str) -> Optional[str]:
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.txt'):
            return self.extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            return None
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        current_section = "HEADER"
        current_content = []
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            is_header = False
            for header in self.section_headers:
                if re.match(f"^{header}$", line, re.IGNORECASE):
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = header
                    current_content = []
                    is_header = True
                    break
            
            if not is_header:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        contact_info = {}
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
        
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        
        return contact_info
    
    def extract_skills(self, text: str) -> List[str]:
        skills = []
        
        skill_section = None
        for header in self.section_headers:
            if header.lower() in text.lower():
                skill_section = header
                break
        
        if skill_section:
            skill_pattern = r'(?i)' + skill_section + r':(.*?)(?=\n\n|\Z)'
            skill_match = re.search(skill_pattern, text, re.DOTALL)
            
            if skill_match:
                skill_text = skill_match.group(1)
                skills = [skill.strip() for skill in re.split(r'[,•]', skill_text) if skill.strip()]
        
        return skills
    
    def parse_resume(self, file_path: str) -> Dict:
        text = self.extract_text(file_path)
        if not text:
            return {}
        
        sections = self.extract_sections(text)
        contact_info = self.extract_contact_info(text)
        skills = self.extract_skills(text)
        
        return {
            'sections': sections,
            'contact_info': contact_info,
            'skills': skills,
            'raw_text': text
        } 