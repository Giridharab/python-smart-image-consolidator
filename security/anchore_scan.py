import subprocess

def scan_with_anchore(image):
    result = subprocess.run(["anchore-cli", "image", "add", image], capture_output=True, text=True)
    subprocess.run(["anchore-cli", "image", "wait", image])
    report = subprocess.run(["anchore-cli", "image", "vuln", image, "all"], capture_output=True, text=True)
    return report.stdout