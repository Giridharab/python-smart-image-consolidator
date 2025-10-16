# ci/github_comment.py
import os
import requests
import json

def post_pr_comment(report: str):
    token = os.getenv("GITHUB_TOKEN")
    pr_number = os.getenv("GITHUB_PR_NUMBER")
    repo = os.getenv("GITHUB_REPOSITORY")
    commit_sha = os.getenv("COMMIT_SHA")

    if not all([token, pr_number, repo, commit_sha]):
        print("Missing environment variables")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    # 1️⃣ Comment on the PR
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": report}
    response = requests.post(comment_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"Commented on PR #{pr_number}")
    else:
        print(f"Failed to comment on PR: {response.status_code}, {response.text}")

    # 2️⃣ Update commit status
    status_url = f"https://api.github.com/repos/{repo}/statuses/{commit_sha}"
    status_payload = {
        "state": "success",
        "description": "Smart Image Consolidator: Analysis complete",
        "context": "Smart Image Consolidator"
    }
    status_response = requests.post(status_url, headers=headers, data=json.dumps(status_payload))
    if status_response.status_code == 201:
        print(f"Status updated for commit {commit_sha}")
    else:
        print(f"Failed to update status: {status_response.status_code}, {status_response.text}")


if __name__ == "__main__":
    test_report = "Smart Image Consolidator analysis completed successfully ✅"
    comment_on_pr(test_report)
