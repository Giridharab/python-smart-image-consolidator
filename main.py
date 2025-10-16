import os
import sys

# Add the repo root to sys.path so internal imports work
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scanner.dockerfile_scanner import find_dockerfiles
from analyzer.image_analyzer import load_canonical_bases, suggest_canonical_base
from metrics.perf_cost import estimate_cost
from security.anchore_scan import scan_with_anchore
from ai.llm_explainer import explain_suggestion
from ci.pr_handler import post_pr_comment

# Get PR number dynamically from environment variable
PR_NUMBER = os.getenv("PR_NUMBER")
PR_PATH = "./test_dockerfiles"

if not PR_NUMBER:
    print("No PR number provided. Exiting.")
    exit(1)

dockerfiles = find_dockerfiles(PR_PATH)
canonical_bases = load_canonical_bases()

for df in dockerfiles:
    with open(df) as f:
        content = f.read()

    suggested = suggest_canonical_base(content, canonical_bases)
    if suggested:
        explanation = explain_suggestion(content.split()[1], suggested)
        metrics = estimate_cost(suggested)
        #security_report = scan_with_anchore(suggested)

        message = (
            f"**Suggested Base:** {suggested}\n"
            f"**Explanation:** {explanation}\n"
            f"**Metrics:** {metrics}\n"

        )
        post_pr_comment(PR_NUMBER, message)