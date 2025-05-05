import os
import pandas as pd
from typing import List, Dict, Any

def convert_json_to_csv(json_dir: str, output_file: str) -> None:
    all_data = []
    
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(json_dir, filename)
            try:
                df = pd.read_json(json_path)
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Successfully converted JSON files to {output_file}")
    else:
        print("No data found to convert")

def main():
    json_dir = "data/raw/jobs"
    output_file = "data/raw/jobs/sample_jobs.csv"
    convert_json_to_csv(json_dir, output_file)

if __name__ == "__main__":
    main() 