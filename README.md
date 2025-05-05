# Resume ATS Scorer and Matcher

This project implements an intelligent Resume ATS (Applicant Tracking System) scorer and matcher that analyzes resumes against job descriptions using advanced NLP techniques.

## Features

- PDF Resume parsing and text extraction
- Semantic analysis using BERT embeddings
- Keyword matching using TF-IDF
- Resume-Job Description matching score
- Gap analysis for resume improvement
- Support for CSV-based job description dataset

## Project Structure

```
resume_ats_scorer/
├── data/                   # Directory for storing datasets
│   ├── raw/               # Raw job descriptions and resumes
│   └── processed/         # Processed data
├── src/                   # Source code
│   ├── preprocessing/     # Data preprocessing modules
│   ├── models/           # BERT and TF-IDF model implementations
│   ├── scoring/          # Scoring and matching logic
│   └── utils/            # Utility functions
├── notebooks/            # Jupyter notebooks for analysis
├── tests/               # Unit tests
└── requirements.txt     # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage

1. Place your resume in PDF format in the `data/raw/resumes` directory
2. Add your job descriptions dataset in CSV format in the `data/raw/jobs` directory
3. Run the main script:
```bash
python src/main.py
```

## Output

The system will generate:
- A matching score between the resume and job description
- Keyword analysis
- Semantic similarity score
- Recommendations for resume improvement
- Identified skill gaps

## License

MIT License 