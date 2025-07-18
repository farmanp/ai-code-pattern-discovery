"""Generate a service collaboration scan prompt.

This script loads the aggregated service collaboration spec and prints
out a basic prompt with placeholders for a target code path.
"""

import yaml
from pathlib import Path

SPEC_PATH = Path(__file__).resolve().parent.parent / "specs" / "service-collaboration-patterns.yaml"


def load_spec(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prompt(spec):
    patterns = [p["name"] for p in spec.get("service_collaboration_patterns", [])]
    pattern_list = ", ".join(patterns)
    return f"""# Service Collaboration Scan Prompt\n\n" \
           f"Supported patterns: {pattern_list}.\n" \
           "Provide CODE_PATH when invoking this script to fill in the target repository."""


if __name__ == "__main__":
    spec = load_spec(SPEC_PATH)
    prompt = build_prompt(spec)
    print(prompt)
