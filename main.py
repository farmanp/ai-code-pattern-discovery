"""Interview Prep Tool — main orchestrator.

Usage
-----
    python main.py /path/to/repo [options]

Options
-------
    --output-dir   Directory to save results (default: ./interview_prep_output)
    --format       Output format: json, markdown, or both (default: both)
    --model        Claude model to use (default: claude-opus-4-5)
    --max-questions  Maximum questions to generate (default: 30)
    --dry-run      Print agent prompts without calling the API

Environment
-----------
    ANTHROPIC_API_KEY   Required when not using --dry-run.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Optional Anthropic import — fail gracefully if not installed
# ---------------------------------------------------------------------------
try:
    import anthropic  # type: ignore

    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False

# ---------------------------------------------------------------------------
# Repository root — agents/ and skills/ live next to main.py
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent
AGENTS_DIR = REPO_ROOT / "agents"
SKILLS_DIR = REPO_ROOT / "skills"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_file(path: Path) -> str:
    """Return the text content of *path*, or raise a clear error."""
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def _load_agent(name: str) -> str:
    """Load an agent markdown definition from agents/<name>.md."""
    return _read_file(AGENTS_DIR / f"{name}.md")


def _load_skill_doc(name: str) -> str:
    """Load a skills document from skills/<name>.md."""
    return _read_file(SKILLS_DIR / f"{name}.md")


def _build_repo_analyzer_prompt(agent_def: str, repo_path: Path) -> str:
    """Construct the full prompt for the Repo Analyzer Agent."""
    tree_lines: list = []
    try:
        for root, dirs, files in os.walk(repo_path):
            # Prune hidden and common noise directories
            dirs[:] = [
                d
                for d in sorted(dirs)
                if not d.startswith(".")
                and d not in {"node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".git"}
            ]
            depth = len(Path(root).relative_to(repo_path).parts)
            if depth > 3:
                dirs.clear()
                continue
            indent = "  " * depth
            rel_root = Path(root).relative_to(repo_path)
            tree_lines.append(f"{indent}{rel_root}/")
            for fname in sorted(files)[:20]:  # cap files per dir
                tree_lines.append(f"{indent}  {fname}")
    except Exception:
        tree_lines = ["<could not walk directory>"]

    tree_text = "\n".join(tree_lines) if tree_lines else "<empty directory>"

    return f"""{agent_def}

---

## Repository to Analyze

**Path:** `{repo_path}`

**Directory Tree (depth ≤ 3):**
```
{tree_text}
```

Please analyze the repository according to your instructions and return **only** valid JSON matching the schema defined above. Do not include any prose outside the JSON object.
"""


def _build_skills_extractor_prompt(
    agent_def: str,
    skills_db: str,
    patterns_doc: str,
    repo_analysis: Dict[str, Any],
) -> str:
    """Construct the full prompt for the Skills Extractor Agent."""
    analysis_json = json.dumps(repo_analysis, indent=2)
    return f"""{agent_def}

---

## Skills Database Reference

{skills_db}

## Pattern-to-Skill Mapping Reference

{patterns_doc}

---

## Repo Analysis Input

```json
{analysis_json}
```

Please extract skills according to your instructions and return **only** valid JSON matching the schema defined above. Do not include any prose outside the JSON object.
"""


def _build_question_generator_prompt(
    agent_def: str,
    extracted_skills: Dict[str, Any],
    max_questions: int,
) -> str:
    """Construct the full prompt for the Question Generator Agent."""
    skills_json = json.dumps(extracted_skills, indent=2)
    return f"""{agent_def}

---

## Extracted Skills Input

```json
{skills_json}
```

**Constraint:** Generate at most {max_questions} questions in total.

Please generate interview questions according to your instructions and return **only** valid JSON matching the schema defined above. Do not include any prose outside the JSON object.
"""


def _call_claude(client: Any, model: str, prompt: str, description: str) -> Dict[str, Any]:
    """Call the Claude API with *prompt* and return parsed JSON."""
    print(f"  → Calling Claude ({model}) for: {description} ...", flush=True)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        lines = raw.splitlines()
        # Remove opening fence (```json or ```)
        start = 1 if len(lines) > 1 else 0
        # Remove closing fence
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        raw = "\n".join(lines[start:end]).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"  [WARNING] Could not parse JSON from {description}: {exc}", file=sys.stderr)
        print(f"  Raw response (first 500 chars): {raw[:500]}", file=sys.stderr)
        return {"_raw_response": raw, "_parse_error": str(exc)}


def _dry_run_print(label: str, prompt: str) -> None:
    """Print a prompt in dry-run mode."""
    separator = "=" * 70
    print(f"\n{separator}")
    print(f"  AGENT PROMPT: {label}")
    print(separator)
    print(prompt[:3000])
    if len(prompt) > 3000:
        print(f"\n  ... [{len(prompt) - 3000} more characters truncated]")
    print(separator)


def _save_json(data: Dict[str, Any], path: Path) -> None:
    """Write *data* as pretty-printed JSON to *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved JSON  → {path}")


def _save_markdown(questions_data: Dict[str, Any], path: Path) -> None:
    """Write a human-readable Markdown report from *questions_data* to *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)

    questions = questions_data.get("questions", [])
    summary = questions_data.get("summary", {})
    repo_path = questions_data.get("repo_path", "unknown")
    generated_at = questions_data.get("generated_at", "")

    lines = [
        "# Interview Prep Questions",
        "",
        f"**Repository:** `{repo_path}`",
        f"**Generated:** {generated_at}",
        "",
        "## Summary",
        "",
        f"- **Total questions:** {summary.get('total_questions', len(questions))}",
    ]

    by_difficulty = summary.get("by_difficulty", {})
    if by_difficulty:
        lines.append(
            f"- **By difficulty:** "
            + ", ".join(f"{k}: {v}" for k, v in by_difficulty.items())
        )

    by_category = summary.get("by_category", {})
    if by_category:
        lines.append(
            f"- **By category:** "
            + ", ".join(f"{k}: {v}" for k, v in by_category.items())
        )

    lines += ["", "---", ""]

    # Group by category then difficulty
    categories = ["algorithms", "data-structures", "design-patterns", "system-design"]
    difficulties = ["easy", "medium", "hard"]

    for cat in categories:
        cat_questions = [q for q in questions if q.get("category") == cat]
        if not cat_questions:
            continue
        lines.append(f"## {cat.replace('-', ' ').title()}")
        lines.append("")

        for diff in difficulties:
            diff_questions = [q for q in cat_questions if q.get("difficulty") == diff]
            if not diff_questions:
                continue
            lines.append(f"### {diff.title()}")
            lines.append("")

            for q in diff_questions:
                lines.append(f"#### {q.get('question', '(no question text)')}")
                lines.append("")

                skill_name = q.get("skill_name", "")
                if skill_name:
                    lines.append(f"**Skill:** {skill_name}")

                context = q.get("context", "")
                if context:
                    lines.append(f"**Context:** {context}")

                answer_hint = q.get("answer_hint", "")
                if answer_hint:
                    lines.append(f"**Answer hints:**")
                    if isinstance(answer_hint, list):
                        for hint in answer_hint:
                            lines.append(f"- {hint}")
                    else:
                        lines.append(f"- {answer_hint}")

                follow_ups = q.get("follow_ups", [])
                if follow_ups:
                    lines.append("**Follow-ups:**")
                    for fu in follow_ups:
                        lines.append(f"- {fu}")

                company_patterns = q.get("company_patterns", [])
                if company_patterns:
                    lines.append(f"**Company patterns:** {', '.join(company_patterns)}")

                lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved Markdown → {path}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run_pipeline(
    repo_path: Path,
    output_dir: Path,
    fmt: str,
    model: str,
    max_questions: int,
    dry_run: bool,
) -> Dict[str, Any]:
    """Execute the three-agent pipeline and return the final questions data."""

    print("\n=== Interview Prep Tool ===")
    print(f"Repository : {repo_path}")
    print(f"Output dir : {output_dir}")
    print(f"Model      : {model}")
    print(f"Dry run    : {dry_run}")
    print()

    # ------------------------------------------------------------------
    # Load agent definitions and skill docs
    # ------------------------------------------------------------------
    print("[1/3] Loading agent definitions and skill references …")
    repo_analyzer_def = _load_agent("repo_analyzer")
    skills_extractor_def = _load_agent("skills_extractor")
    question_generator_def = _load_agent("question_generator")
    skills_db = _load_skill_doc("skills_db")
    patterns_doc = _load_skill_doc("patterns")

    # ------------------------------------------------------------------
    # Stage 1: Repo Analyzer
    # ------------------------------------------------------------------
    print("[2/3] Stage 1 — Repo Analyzer …")
    analyzer_prompt = _build_repo_analyzer_prompt(repo_analyzer_def, repo_path)

    if dry_run:
        _dry_run_print("Repo Analyzer", analyzer_prompt)
        # Return a stub so we can still show the downstream prompts
        repo_analysis: Dict[str, Any] = {
            "repo_path": str(repo_path),
            "languages": ["Python"],
            "architecture_style": "modular CLI tool",
            "algorithms_detected": [],
            "data_structures_detected": [],
            "design_patterns_detected": [{"name": "Registry", "category": "creational", "location": "src/ai_code_pattern_discovery/skills.py", "description": "SKILLS list acts as a registry of pattern skills"}],
            "system_design_concepts": [],
            "notable_patterns": ["Stub data for dry-run mode"],
        }
    else:
        if not _ANTHROPIC_AVAILABLE:
            print("ERROR: 'anthropic' package not installed. Run: pip install anthropic", file=sys.stderr)
            sys.exit(1)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
            sys.exit(1)
        client = anthropic.Anthropic(api_key=api_key)
        repo_analysis = _call_claude(client, model, analyzer_prompt, "Repo Analyzer")

    # ------------------------------------------------------------------
    # Stage 2: Skills Extractor
    # ------------------------------------------------------------------
    print("[3/3] Stage 2 — Skills Extractor …")
    extractor_prompt = _build_skills_extractor_prompt(
        skills_extractor_def, skills_db, patterns_doc, repo_analysis
    )

    if dry_run:
        _dry_run_print("Skills Extractor", extractor_prompt)
        extracted_skills: Dict[str, Any] = {
            "repo_path": str(repo_path),
            "extracted_skills": [
                {
                    "skill_id": "registry-pattern",
                    "skill_name": "Registry Pattern",
                    "category": "design-patterns",
                    "difficulty": "easy",
                    "relevance_rank": 1,
                    "source_patterns": ["Registry"],
                    "company_patterns": ["Google", "Meta"],
                    "description": "Stub skill for dry-run mode",
                }
            ],
            "skill_summary": {
                "total": 1,
                "by_category": {"design-patterns": 1},
                "by_difficulty": {"easy": 1},
            },
        }
    else:
        extracted_skills = _call_claude(client, model, extractor_prompt, "Skills Extractor")

    # ------------------------------------------------------------------
    # Stage 3: Question Generator
    # ------------------------------------------------------------------
    print("[4/4] Stage 3 — Question Generator …")
    generator_prompt = _build_question_generator_prompt(
        question_generator_def, extracted_skills, max_questions
    )

    if dry_run:
        _dry_run_print("Question Generator", generator_prompt)
        questions_data: Dict[str, Any] = {
            "repo_path": str(repo_path),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "questions": [
                {
                    "id": "registry-pattern-easy-01",
                    "skill_id": "registry-pattern",
                    "skill_name": "Registry Pattern",
                    "category": "design-patterns",
                    "difficulty": "easy",
                    "question": "What is the Registry pattern and when would you use it? (dry-run stub)",
                    "context": "Stub question for dry-run mode",
                    "answer_hint": "Centralized lookup for named objects; used to avoid globals while enabling named access.",
                    "follow_ups": ["How does Registry differ from Singleton?"],
                    "company_patterns": ["Google"],
                }
            ],
            "summary": {
                "total_questions": 1,
                "by_difficulty": {"easy": 1, "medium": 0, "hard": 0},
                "by_category": {"design-patterns": 1},
            },
        }
    else:
        questions_data = _call_claude(client, model, generator_prompt, "Question Generator")
        # Ensure generated_at is present
        if "generated_at" not in questions_data:
            questions_data["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    # ------------------------------------------------------------------
    # Save outputs
    # ------------------------------------------------------------------
    print("\nSaving results …")
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S")
    base_name = f"interview_prep_{timestamp}"

    if fmt in ("json", "both"):
        _save_json(
            {
                "repo_analysis": repo_analysis,
                "extracted_skills": extracted_skills,
                "questions": questions_data,
            },
            output_dir / f"{base_name}.json",
        )

    if fmt in ("markdown", "both"):
        _save_markdown(questions_data, output_dir / f"{base_name}.md")

    print("\nDone!")
    return questions_data


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate interview prep questions from a code repository using Claude AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "repo_path",
        type=Path,
        help="Path to the repository to analyze.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("interview_prep_output"),
        help="Directory to write results (default: ./interview_prep_output).",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Output format (default: both).",
    )
    parser.add_argument(
        "--model",
        default="claude-opus-4-5",
        help="Claude model to use (default: claude-opus-4-5).",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=30,
        help="Maximum number of questions to generate (default: 30).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print agent prompts without calling the API.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> None:
    args = _parse_args(argv)

    repo_path = args.repo_path.resolve()
    if not repo_path.exists():
        print(f"ERROR: Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)
    if not repo_path.is_dir():
        print(f"ERROR: Repository path is not a directory: {repo_path}", file=sys.stderr)
        sys.exit(1)

    run_pipeline(
        repo_path=repo_path,
        output_dir=args.output_dir.resolve(),
        fmt=args.format,
        model=args.model,
        max_questions=args.max_questions,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
