import requests
import time
import math
import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm

def fetch_issues(
    owner='huggingface',
    repo='datasets',
    num_issues=10_000,
    rate_limit=100_000,
    per_page=100,
    issues_path=Path('.')):

    if not issues_path.is_dir():
      issues_path.mkdir(exist_ok=True)

    batch=[]
    all_issues=[]
    per_page=per_page
    num_pages = math.ceil(num_issues / per_page)
    base_url = "https://api.github.com/repos"

    for page in tqdm(range(num_pages)):
      query = f"issues?page={page}&per_page={per_page}&state=all"
      issues = requests.get(f"{base_url}/{owner}/{repo}/{query}", headers=headers)
      batch.extend(issues.json())

      if len(batch) > rate_limit and len(all_issues) < num_issues:
        all_issues.extend(batch)
        batch=[]
        print("Reatch the GitHub rate limit. Sleeping for one Hour...")
        time.sleep(60*60+1)

    all_issues.extend(batch)
    df = pd.DataFrame(all_issues)
    df.to_json(f'{issues_path}/{repo}-issues.jsonl', orient='records', lines=True)
    print(f"Download the dataset for {repo}! Dataset stored in {issues_path}/{repo}-issues.jsonl.")
