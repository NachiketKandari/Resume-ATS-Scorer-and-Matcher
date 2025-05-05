import os
import subprocess
from typing import List

def run_command(command: List[str]) -> bool:
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        return False

def main():
    pipeline_steps = [
        ["python", "convert_resumes_to_txt.py"],
        ["python", "convert_to_csv.py"],
        ["python", "src/run_batch_analysis.py"],
        ["python", "src/run_extended_analysis.py"]
    ]
    
    for step in pipeline_steps:
        print(f"Running: {' '.join(step)}")
        if not run_command(step):
            print("Pipeline failed")
            return
    
    print("Pipeline completed successfully")

if __name__ == "__main__":
    main() 