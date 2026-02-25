"""Tests for the interview prep tool (main.py).

These tests exercise all logic paths that do NOT require a live Claude API call.
The Claude-calling path is tested with a simple mock.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Make main.py importable from the tests directory
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import main as m


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def repo_root(tmp_path):
    """A minimal fake repository directory."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    (tmp_path / "tests").mkdir()
    (tmp_path / "README.md").write_text("# Fake repo")
    return tmp_path


@pytest.fixture()
def output_dir(tmp_path):
    out = tmp_path / "output"
    out.mkdir()
    return out


# ---------------------------------------------------------------------------
# File-loading helpers
# ---------------------------------------------------------------------------


def test_load_agent_repo_analyzer():
    content = m._load_agent("repo_analyzer")
    assert "Repo Analyzer" in content


def test_load_agent_skills_extractor():
    content = m._load_agent("skills_extractor")
    assert "Skills Extractor" in content


def test_load_agent_question_generator():
    content = m._load_agent("question_generator")
    assert "Question Generator" in content


def test_load_skill_doc_skills_db():
    content = m._load_skill_doc("skills_db")
    assert "binary-search" in content


def test_load_skill_doc_patterns():
    content = m._load_skill_doc("patterns")
    assert "Detected Pattern" in content


def test_load_agent_missing_raises():
    with pytest.raises(FileNotFoundError):
        m._load_agent("nonexistent_agent")


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------


def test_build_repo_analyzer_prompt_contains_path(repo_root):
    agent_def = "# Repo Analyzer Agent\nInstructions here."
    prompt = m._build_repo_analyzer_prompt(agent_def, repo_root)
    assert str(repo_root) in prompt
    assert "Directory Tree" in prompt
    assert "README.md" in prompt


def test_build_repo_analyzer_prompt_depth_limit(repo_root):
    # Create a dir deeper than 3 levels
    deep = repo_root / "a" / "b" / "c" / "d"
    deep.mkdir(parents=True)
    (deep / "deep_file.py").write_text("")
    agent_def = "Instructions."
    prompt = m._build_repo_analyzer_prompt(agent_def, repo_root)
    # deep_file.py should NOT appear in the prompt (depth 4)
    assert "deep_file.py" not in prompt


def test_build_skills_extractor_prompt_embeds_analysis():
    agent_def = "# Skills Extractor\nInstructions."
    skills_db = "skill: binary-search"
    patterns_doc = "pattern: BFS"
    analysis = {"repo_path": "/tmp/repo", "algorithms_detected": [{"name": "BFS"}]}
    prompt = m._build_skills_extractor_prompt(agent_def, skills_db, patterns_doc, analysis)
    assert "binary-search" in prompt
    assert "BFS" in prompt
    assert "/tmp/repo" in prompt


def test_build_question_generator_prompt_respects_max():
    agent_def = "# Question Generator\nInstructions."
    skills = {"extracted_skills": [], "skill_summary": {"total": 0}}
    prompt = m._build_question_generator_prompt(agent_def, skills, max_questions=15)
    assert "15" in prompt


# ---------------------------------------------------------------------------
# _call_claude — test JSON stripping and parse
# ---------------------------------------------------------------------------


def _make_mock_client(response_text: str):
    """Build a mock Anthropic client that returns *response_text*."""
    mock_content = MagicMock()
    mock_content.text = response_text

    mock_message = MagicMock()
    mock_message.content = [mock_content]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


def test_call_claude_plain_json():
    client = _make_mock_client('{"key": "value"}')
    result = m._call_claude(client, "claude-3-sonnet-20240229", "prompt", "test")
    assert result == {"key": "value"}


def test_call_claude_strips_code_fences():
    client = _make_mock_client('```json\n{"key": "value"}\n```')
    result = m._call_claude(client, "claude-3-sonnet-20240229", "prompt", "test")
    assert result == {"key": "value"}


def test_call_claude_strips_plain_fences():
    client = _make_mock_client('```\n{"a": 1}\n```')
    result = m._call_claude(client, "claude-3-sonnet-20240229", "prompt", "test")
    assert result == {"a": 1}


def test_call_claude_bad_json_returns_raw():
    client = _make_mock_client("not json at all")
    result = m._call_claude(client, "claude-3-sonnet-20240229", "prompt", "test")
    assert "_raw_response" in result
    assert "_parse_error" in result


# ---------------------------------------------------------------------------
# _save_json
# ---------------------------------------------------------------------------


def test_save_json_creates_file(tmp_path):
    data = {"questions": [{"id": "q1"}]}
    out = tmp_path / "sub" / "out.json"
    m._save_json(data, out)
    assert out.exists()
    loaded = json.loads(out.read_text())
    assert loaded["questions"][0]["id"] == "q1"


def test_save_json_pretty_printed(tmp_path):
    data = {"a": 1, "b": 2}
    out = tmp_path / "out.json"
    m._save_json(data, out)
    text = out.read_text()
    assert "\n" in text  # pretty-printed has newlines


# ---------------------------------------------------------------------------
# _save_markdown
# ---------------------------------------------------------------------------


SAMPLE_QUESTIONS_DATA = {
    "repo_path": "/tmp/repo",
    "generated_at": "2026-01-01T00:00:00Z",
    "questions": [
        {
            "id": "binary-search-easy-01",
            "skill_id": "binary-search",
            "skill_name": "Binary Search",
            "category": "algorithms",
            "difficulty": "easy",
            "question": "How does binary search work?",
            "context": "Found in search module.",
            "answer_hint": "Repeatedly halve the search space.",
            "follow_ups": ["What is its time complexity?"],
            "company_patterns": ["Google"],
        },
        {
            "id": "heap-medium-01",
            "skill_id": "heap",
            "skill_name": "Heap",
            "category": "data-structures",
            "difficulty": "medium",
            "question": "Implement a min-heap.",
            "context": "Used in task scheduler.",
            "answer_hint": ["Maintain heap property", "sift-up on insert"],
            "follow_ups": [],
            "company_patterns": ["Amazon"],
        },
    ],
    "summary": {
        "total_questions": 2,
        "by_difficulty": {"easy": 1, "medium": 1, "hard": 0},
        "by_category": {"algorithms": 1, "data-structures": 1},
    },
}


def test_save_markdown_creates_file(tmp_path):
    out = tmp_path / "report.md"
    m._save_markdown(SAMPLE_QUESTIONS_DATA, out)
    assert out.exists()


def test_save_markdown_contains_questions(tmp_path):
    out = tmp_path / "report.md"
    m._save_markdown(SAMPLE_QUESTIONS_DATA, out)
    text = out.read_text()
    assert "How does binary search work?" in text
    assert "Implement a min-heap." in text


def test_save_markdown_structure(tmp_path):
    out = tmp_path / "report.md"
    m._save_markdown(SAMPLE_QUESTIONS_DATA, out)
    text = out.read_text()
    assert "# Interview Prep Questions" in text
    assert "## Algorithms" in text
    assert "## Data Structures" in text
    assert "### Easy" in text
    assert "### Medium" in text


def test_save_markdown_answer_hint_list(tmp_path):
    out = tmp_path / "report.md"
    m._save_markdown(SAMPLE_QUESTIONS_DATA, out)
    text = out.read_text()
    # Heap question has list answer hints
    assert "Maintain heap property" in text
    assert "sift-up on insert" in text


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------


def test_parse_args_defaults(repo_root):
    args = m._parse_args([str(repo_root)])
    assert args.repo_path == repo_root
    assert args.format == "both"
    assert args.max_questions == 30
    assert args.dry_run is False
    assert args.model == "claude-opus-4-5"


def test_parse_args_overrides(repo_root):
    args = m._parse_args([
        str(repo_root),
        "--format", "json",
        "--max-questions", "10",
        "--dry-run",
        "--model", "claude-3-5-sonnet-20241022",
    ])
    assert args.format == "json"
    assert args.max_questions == 10
    assert args.dry_run is True
    assert args.model == "claude-3-5-sonnet-20241022"


# ---------------------------------------------------------------------------
# Dry-run pipeline integration test (no API calls)
# ---------------------------------------------------------------------------


def test_dry_run_pipeline_produces_output(repo_root, output_dir, capsys):
    result = m.run_pipeline(
        repo_path=repo_root,
        output_dir=output_dir,
        fmt="both",
        model="claude-opus-4-5",
        max_questions=5,
        dry_run=True,
    )
    assert "questions" in result
    assert len(result["questions"]) >= 1

    # Both output files should have been created
    json_files = list(output_dir.glob("*.json"))
    md_files = list(output_dir.glob("*.md"))
    assert len(json_files) == 1
    assert len(md_files) == 1

    # JSON file should have three keys
    loaded = json.loads(json_files[0].read_text())
    assert "repo_analysis" in loaded
    assert "extracted_skills" in loaded
    assert "questions" in loaded


def test_dry_run_pipeline_json_only(repo_root, output_dir):
    m.run_pipeline(
        repo_path=repo_root,
        output_dir=output_dir,
        fmt="json",
        model="claude-opus-4-5",
        max_questions=5,
        dry_run=True,
    )
    assert len(list(output_dir.glob("*.json"))) == 1
    assert len(list(output_dir.glob("*.md"))) == 0


def test_dry_run_pipeline_markdown_only(repo_root, output_dir):
    m.run_pipeline(
        repo_path=repo_root,
        output_dir=output_dir,
        fmt="markdown",
        model="claude-opus-4-5",
        max_questions=5,
        dry_run=True,
    )
    assert len(list(output_dir.glob("*.md"))) == 1
    assert len(list(output_dir.glob("*.json"))) == 0


# ---------------------------------------------------------------------------
# main() error handling
# ---------------------------------------------------------------------------


def test_main_exits_on_missing_repo(tmp_path):
    missing = tmp_path / "does_not_exist"
    with pytest.raises(SystemExit) as exc_info:
        m.main([str(missing)])
    assert exc_info.value.code != 0


def test_main_exits_on_file_not_dir(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("content")
    with pytest.raises(SystemExit) as exc_info:
        m.main([str(f)])
    assert exc_info.value.code != 0
