import os
import random
from faker import Faker
import json
from typing import List, Dict, Any

fake = Faker()

# Job titles and their corresponding skills
JOB_TITLES = {
    "Software Engineer": ["Python", "Java", "JavaScript", "SQL", "Git", "Docker", "AWS", "REST APIs"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "TensorFlow", "PyTorch", "Data Analysis"],
    "Product Manager": ["Agile", "Scrum", "Product Strategy", "User Research", "Data Analysis", "Communication"],
    "UX Designer": ["Figma", "Adobe XD", "User Research", "Wireframing", "Prototyping", "UI Design"],
    "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Jenkins", "Terraform"],
    "Frontend Developer": ["React", "JavaScript", "HTML", "CSS", "TypeScript", "Redux", "Webpack"],
    "Backend Developer": ["Python", "Java", "Node.js", "SQL", "MongoDB", "Redis", "Microservices"],
    "Data Engineer": ["Python", "SQL", "Spark", "Hadoop", "ETL", "Data Warehousing", "Airflow"],
    "QA Engineer": ["Python", "Selenium", "JUnit", "TestNG", "API Testing", "Automation", "CI/CD"],
    "Security Engineer": ["Security", "Cryptography", "Network Security", "Python", "Linux", "AWS"],
    "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Deep Learning", "NLP", "Computer Vision"],
    "Cloud Architect": ["AWS", "Azure", "GCP", "Cloud Architecture", "Terraform", "Kubernetes"],
    "Full Stack Developer": ["JavaScript", "Python", "React", "Node.js", "SQL", "MongoDB", "Docker"],
    "Business Analyst": ["SQL", "Data Analysis", "Business Intelligence", "Tableau", "Excel", "Requirements"],
    "Technical Lead": ["Leadership", "Architecture", "Code Review", "Mentoring", "System Design"],
    "Mobile Developer": ["Swift", "Kotlin", "React Native", "Flutter", "iOS", "Android", "Mobile Apps"],
    "Database Administrator": ["SQL", "MongoDB", "PostgreSQL", "MySQL", "Database Design", "Performance"],
    "System Administrator": ["Linux", "Windows Server", "Networking", "Security", "Automation", "Monitoring"],
    "Technical Writer": ["Documentation", "Technical Writing", "API Documentation", "Git", "Markdown"],
    "Research Scientist": ["Python", "R", "Machine Learning", "Statistics", "Research", "Data Analysis"]
}

def generate_job_description():
    title = random.choice(list(JOB_TITLES.keys()))
    skills = JOB_TITLES[title]
    required_skills = random.sample(skills, min(5, len(skills)))
    remaining_skills = [s for s in skills if s not in required_skills]
    preferred_skills = random.sample(remaining_skills, min(3, len(remaining_skills)))
    
    description = {
        "title": title,
        "company": fake.company(),
        "location": fake.city() + ", " + fake.country(),
        "salary_range": f"${random.randint(50, 150)}k - ${random.randint(150, 250)}k",
        "job_type": random.choice(["Full-time", "Contract", "Remote", "Hybrid"]),
        "experience_level": random.choice(["Entry Level", "Mid Level", "Senior Level", "Lead"]),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "description": fake.paragraph(nb_sentences=5),
        "responsibilities": [fake.sentence() for _ in range(random.randint(5, 8))],
        "requirements": [fake.sentence() for _ in range(random.randint(3, 6))]
    }
    return description

def generate_resume():
    title = random.choice(list(JOB_TITLES.keys()))
    skills = JOB_TITLES[title]
    candidate_skills = random.sample(skills, min(7, len(skills)))
    
    resume = {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "location": fake.city() + ", " + fake.country(),
        "summary": fake.paragraph(nb_sentences=3),
        "skills": candidate_skills,
        "experience": [
            {
                "title": random.choice(list(JOB_TITLES.keys())),
                "company": fake.company(),
                "duration": f"{random.randint(1, 5)} years",
                "description": [fake.sentence() for _ in range(random.randint(3, 5))]
            }
            for _ in range(random.randint(2, 4))
        ],
        "education": [
            {
                "degree": random.choice(["Bachelor's", "Master's", "PhD"]),
                "field": random.choice(["Computer Science", "Engineering", "Data Science", "Mathematics"]),
                "university": fake.company() + " University",
                "year": random.randint(2010, 2023)
            }
            for _ in range(random.randint(1, 2))
        ]
    }
    return resume

def generate_sample_jobs(num_jobs: int = 10) -> List[Dict[str, Any]]:
    job_titles = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "Cloud Architect",
        "Security Engineer"
    ]
    
    required_skills = [
        ["Python", "Java", "Git", "SQL"],
        ["Python", "R", "Machine Learning", "Statistics"],
        ["Product Strategy", "Agile", "User Research", "Data Analysis"],
        ["Linux", "Docker", "Kubernetes", "CI/CD"],
        ["JavaScript", "React", "HTML", "CSS"],
        ["Java", "Spring", "SQL", "REST APIs"],
        ["JavaScript", "Python", "React", "Node.js"],
        ["Python", "TensorFlow", "PyTorch", "Deep Learning"],
        ["AWS", "Azure", "Terraform", "Kubernetes"],
        ["Network Security", "Cryptography", "Security Tools", "Incident Response"]
    ]
    
    jobs = []
    for i in range(num_jobs):
        job = {
            "title": job_titles[i],
            "description": f"Sample job description for {job_titles[i]}",
            "required_skills": required_skills[i],
            "preferred_skills": ["Communication", "Teamwork", "Problem Solving"]
        }
        jobs.append(job)
    
    return jobs

def save_jobs(jobs: List[Dict[str, Any]], output_dir: str) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, job in enumerate(jobs, 1):
        output_file = os.path.join(output_dir, f"job_{i}.json")
        with open(output_file, 'w') as f:
            json.dump(job, f, indent=4)

def main():
    # Create directories if they don't exist
    os.makedirs("data/raw/jobs", exist_ok=True)
    os.makedirs("data/raw/resumes", exist_ok=True)
    
    # Generate job descriptions
    for i in range(20):
        job = generate_job_description()
        with open(f"data/raw/jobs/job_{i+1}.json", "w") as f:
            json.dump(job, f, indent=2)
    
    # Generate resumes
    for i in range(100):
        resume = generate_resume()
        with open(f"data/raw/resumes/resume_{i+1}.json", "w") as f:
            json.dump(resume, f, indent=2)

    output_dir = "data/raw/jobs"
    jobs = generate_sample_jobs()
    save_jobs(jobs, output_dir)
    print(f"Generated {len(jobs)} sample job descriptions")

if __name__ == "__main__":
    main() 