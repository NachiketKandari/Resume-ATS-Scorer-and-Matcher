import os
from fpdf import FPDF
from typing import Optional

def convert_text_to_pdf(text: str, output_path: str) -> bool:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        lines = text.split('\n')
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=1, align='L')
        
        pdf.output(output_path)
        return True
    
    except Exception as e:
        print(f"Error converting text to PDF: {e}")
        return False

if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    text_path = os.path.join(script_dir, '..', '..', 'data', 'raw', 'resumes', 'sample_resume.txt')
    pdf_path = os.path.join(script_dir, '..', '..', 'data', 'raw', 'resumes', 'sample_resume.pdf')
    
    convert_text_to_pdf(text_path, pdf_path) 