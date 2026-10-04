from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from app.github_service import fetch_pr_diff, post_github_comment
from app.tasks import run_code_review_pipeline

app = FastAPI(title="Autonomous AI Code Reviewer Bot", version="1.0.0")

def process_pr_background(repo_full_name: str, pr_number: int, diff_url: str):
    # 1. Fetch diff from GitHub
    diff_text = fetch_pr_diff(diff_url)
    
    if "Error fetching diff" in diff_text:
        return

    # 2. Run multi-agent AI review crew
    review_output = run_code_review_pipeline(diff_text)
    
    formatted_comment = f"## 🤖 Autonomous Multi-Agent Code Review\n\n{review_output}\n\n*Reviewed by Gemini AI Agents (Security, Performance, Clean Code)*"

    # 3. Post comment back to GitHub PR
    post_github_comment(repo_full_name, pr_number, formatted_comment)

@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    action = payload.get("action")
    # Trigger on pull request opened or new commits pushed (synchronize)
    if action in ["opened", "synchronize"]:
        pr_data = payload.get("pull_request", {})
        repo_data = payload.get("repository", {})
        
        pr_number = pr_data.get("number")
        diff_url = pr_data.get("diff_url")
        repo_full_name = repo_data.get("full_name")
        
        if pr_number and diff_url and repo_full_name:
            # Run review asynchronously so webhook doesn't timeout
            background_tasks.add_task(process_pr_background, repo_full_name, pr_number, diff_url)
            return {"status": "success", "message": f"Review triggered for PR #{pr_number}"}

    return {"status": "ignored", "reason": "Event action not handled"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Code Reviewer Bot Active"}