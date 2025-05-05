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

def convert_all_resumes(input_dir: str, output_dir: str) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.txt', '.pdf'))
            
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            if convert_text_to_pdf(text, output_path):
                print(f"Successfully converted {filename} to PDF")
            else:
                print(f"Failed to convert {filename} to PDF") 