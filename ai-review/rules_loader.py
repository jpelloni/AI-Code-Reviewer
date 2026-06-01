import os
import yaml

def load_rules(path=".api-review-rules.yml"):
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    # Flatten nested categories into a single list of rule strings
    rules = []
    for category, items in data.items():
        for rule in items:
            rules.append(rule)

    return rules