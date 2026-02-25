"""Generate analysis prompts from YAML specifications.

This script loads a pattern specification file and prints a ready-to-use
analysis prompt for the patterns it defines.  It works with any spec file
that follows the repository's YAML structure (a top-level key whose value
is a list of pattern objects each containing at least a ``name`` field).

Usage::

    python scripts/generate_from_spec.py specs/service-collaboration-patterns.yaml
    python scripts/generate_from_spec.py specs/reliability/circuit-breaker.yaml
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_spec(path: Path) -> dict:
    """Load and return the YAML document at *path*."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _iter_patterns(spec: dict):
    """Yield (category, pattern_dict) pairs from any spec structure."""
    for key, value in spec.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    yield key, item


def build_prompt(spec: dict, target_placeholder: str = "CODE_PATH") -> str:
    """Build a scan prompt from *spec*.

    Parameters
    ----------
    spec:
        Parsed YAML document.
    target_placeholder:
        String used as a stand-in for the actual repository path.

    Returns
    -------
    str
        A markdown prompt ready to be pasted into an agent or Claude Code session.
    """
    lines = [
        "# Pattern Analysis Prompt",
        "",
        f"Analyze the repository at `{target_placeholder}` for the following patterns:",
        "",
    ]

    for _category, pattern in _iter_patterns(spec):
        name = pattern["name"]
        hints = pattern.get("hints", [])
        report_fields = pattern.get("report_fields", [])

        lines.append(f"## {name}")
        if hints:
            lines.append("")
            lines.append("**Detection hints:** " + ", ".join(hints))
        if report_fields:
            lines.append("")
            lines.append("**Report fields:** " + ", ".join(report_fields))
        lines.append("")

    lines += [
        "For each detected pattern provide:",
        "- File path and line number of the key implementation",
        "- Evidence matched against the detection hints",
        "- Populated report fields",
        "- Improvement suggestions where applicable",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <spec-file.yaml>", file=sys.stderr)
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    if not spec_path.exists():
        print(f"File not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    spec = load_spec(spec_path)
    prompt = build_prompt(spec)
    print(prompt)

