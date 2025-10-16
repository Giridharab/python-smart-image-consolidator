import yaml

def load_canonical_bases(path="configs/canonical_bases.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)["canonical_bases"]

def suggest_canonical_base(dockerfile_content, canonical_bases):
    for base in canonical_bases:
        if base["original"] in dockerfile_content:
            return base["suggested"]
    return None