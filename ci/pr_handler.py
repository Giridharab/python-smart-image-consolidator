import requests
import os

def post_pr_comment(pr_number, message):
    """
    Posts a comment to a GitHub PR using the GitHub REST API.
    """
    repo = os.getenv("GITHUB_REPOSITORY")  # e.g., Giridharab/python-smart-image-consolidator
    token = os.getenv("GH_PAT")

    if not token:
        print("❌ GH_PAT not found in environment.")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(url, headers=headers, json={"body": message})
    if response.status_code == 201:
        print(f"💬 Comment posted to PR #{pr_number}")
    else:
        print(f"❌ Failed to post comment: {response.status_code} - {response.text}")
