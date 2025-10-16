import subprocess

def post_pr_comment(pr_number, message):
    subprocess.run([
        "gh", "pr", "comment", str(pr_number),
        "--body", message
    ])
    print(f"Posted comment to PR #{pr_number}: {message}")
    return True