## Smart Image Consolidator (Python)

This tool automates Dockerfile analysis in GitHub PRs using Python. It provides:
	1.	Canonical base image suggestions
	2.	Real-time CPU/Memory/Storage/Cost metrics
	3.	Security scan with AnchoreCTL
	4.	PR comments with full results

When you open a PR containing Dockerfiles, the Python Smart Image Consolidator workflow will:
* Detect Dockerfiles in the PR
* Build temporary containers
* Measure CPU/Memory/Storage usage
* Suggest canonical base images (e.g., python:3.11-slim → artifactory.devhub-cloud.cisco.com/python:3.11-slim)
* Run AnchoreCTL for security scan
* Post a single comment in the PR with all results

  Setup
1. Clone the repository:
  
  ```
  git clone https://github.com/Giridharab/python-smart-image-consolidator.git
  cd python-smart-image-consolidator
  ```

2. Install dependencies:
 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3.	Ensure Docker CLI is installed and running locally.

4.	Install AnchoreCTL for security scanning (optional):

```
anchore --version
```

5.	For GitHub Actions, no manual token is needed; the workflow uses the default GITHUB_TOKEN to comment as a bot.

## Adding Canonical Base Images

Edit configs/canonical_bases.yaml:

```
CanonicalBases:
  - Original: "python:3.11-slim"
    Suggested: "artifactory.devhub-cloud.cisco.com/python:3.11-slim"
 ```

Running Locally

```
export PR_NUMBER=2
export GITHUB_REPOSITORY="owner/repo"
python main.py
```

* Builds Docker images for each Dockerfile in the PR
* Generates metrics: CPU, memory, storage, cost
* Suggests canonical base images
* Runs AnchoreCTL scan
* Posts results as a PR comment

## GitHub Actions Workflow

The workflow is defined in .github/workflows/smart-image-consolidator.yml:
```
name: Smart Image Consolidator

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Smart Image Consolidator
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: python main.py
```

## Output Example
```
### Dockerfile: Dockerfile.python

CPU: 120.00%
Memory: 150MiB
Storage: 50.12MiB
Estimated Cost: $0.01
Canonical Base Suggestion: artifactory.devhub-cloud.cisco.com/python:3.11-slim

#### Security Scan (AnchoreCTL)
Vulnerability Summary:
- CVE-2025-XXXX: High
- CVE-2025-YYYY: Medium
```

## Cleanup

Temporary containers and images are automatically removed.
Optionally, prune Docker images locally:

```
docker image prune -f

```

