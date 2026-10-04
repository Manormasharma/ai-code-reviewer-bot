import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_pr_diff(diff_url: str) -> str:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(diff_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return f"Error fetching diff: {response.text}"

def post_github_comment(repo_full_name: str, pr_number: int, comment_body: str):
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"body": comment_body}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()