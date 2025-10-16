# ci/pr_handler.py
import os
import json
import requests

def post_pr_comment(pr_number: str, message: str):
    """
    Post a comment to the given PR number in the repository.
    Expects the following environment variables:
        - GITHUB_TOKEN: GitHub personal access token
        - GITHUB_REPOSITORY: repository in 'owner/repo' format
    """
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")

    if not all([token, pr_number, repo]):
        print("Missing environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, or PR number")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": message}
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"✅ Successfully commented on PR #{pr_number}")
    else:
        print(f"❌ Failed to comment on PR #{pr_number}: {response.status_code} {response.text}")
