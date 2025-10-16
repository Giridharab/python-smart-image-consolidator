import subprocess

def PostPrComment(pr_number, message):
    subprocess.run([
        "gh", "pr", "comment", str(pr_number),
        "--body", message
    ])
    print(f"Posted comment to PR #{pr_number}: {message}")
    return True