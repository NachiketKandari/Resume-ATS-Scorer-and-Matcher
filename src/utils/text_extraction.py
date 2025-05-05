import PyPDF2
import os
from typing import Optional

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    try:
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            return None
        
        text = ""
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            
            # Extract text from each page
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None

def extract_text_from_txt(txt_path: str) -> Optional[str]:
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