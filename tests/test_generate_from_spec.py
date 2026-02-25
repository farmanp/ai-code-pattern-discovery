"""Tests for the generate_from_spec script."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

try:
    from scripts.generate_from_spec import load_spec, build_prompt
except ModuleNotFoundError:
    import pytest
    pytest.skip("PyYAML not installed", allow_module_level=True)

SPEC_PATH = ROOT / "specs" / "service-collaboration-patterns.yaml"


def test_load_spec():
    spec = load_spec(SPEC_PATH)
    assert "service_collaboration_patterns" in spec


def test_build_prompt_contains_pattern_names():
    spec = load_spec(SPEC_PATH)
    prompt = build_prompt(spec)
    assert "Saga" in prompt
    assert "CQRS" in prompt


def test_build_prompt_custom_placeholder():
    spec = {"patterns": [{"name": "MyPattern", "hints": ["foo"]}]}
    prompt = build_prompt(spec, target_placeholder="/my/repo")
    assert "/my/repo" in prompt
    assert "MyPattern" in prompt
    assert "foo" in prompt


def test_build_prompt_empty_spec():
    prompt = build_prompt({})
    assert "Pattern Analysis Prompt" in prompt
