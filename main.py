import os
import sys

# Add the repo root to sys.path so internal imports work
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scanner.dockerfile_scanner import find_dockerfiles
from analyzer.image_analyzer import load_canonical_bases, suggest_canonical_base
from metrics.perf_cost import estimate_cost
# from security.anchore_scan import scan_with_anchore   # Optional
from ai.llm_explainer import explain_suggestion
from ci.pr_handler import post_pr_comment

# === Configuration ===
PR_NUMBER = os.getenv("PR_NUMBER")
PR_PATH = "./test_dockerfiles"

if not PR_NUMBER:
    print("❌ No PR number provided. Exiting.")
    sys.exit(1)

print(f"🔍 Processing PR #{PR_NUMBER}...")
dockerfiles = find_dockerfiles(PR_PATH)
canonical_bases = load_canonical_bases()

for df in dockerfiles:
    print(f"🧩 Analyzing Dockerfile: {df}")
    with open(df) as f:
        content = f.read()

    suggested = suggest_canonical_base(content, canonical_bases)
    if suggested:
        base_image = content.split()[1] if "FROM" in content else "unknown"
        explanation = explain_suggestion(base_image, suggested)
        metrics = estimate_cost(suggested)
        # security_report = scan_with_anchore(suggested)

        message = (
            f"### 🐳 Smart Image Consolidator Results\n\n"
            f"**Dockerfile:** `{df}`\n"
            f"**Original Base:** `{base_image}`\n"
            f"**Suggested Base:** `{suggested}`\n\n"
            f"**AI Explanation:**\n{explanation}\n\n"
            f"**Metrics:** {metrics}\n"
            # f"**Security Report:** {security_report}\n"
        )

        post_pr_comment(PR_NUMBER, message)

print("✅ Smart Image Consolidator completed successfully!")
