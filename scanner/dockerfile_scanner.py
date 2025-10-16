import os

def find_dockerfiles(pr_path):
    dockerfiles = []
    for root, _, files in os.walk(pr_path):
        for file in files:
            if file.startswith("Dockerfile"):
                dockerfiles.append(os.path.join(root, file))
    return dockerfiles
