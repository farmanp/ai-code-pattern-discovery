"""Tests for the PatternSkill registry and PatternDetector integration."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_code_pattern_discovery.skills import SKILLS, PatternSkill, get_skill
from ai_code_pattern_discovery.pattern_detector import PatternDetector


# ---------------------------------------------------------------------------
# PatternSkill / registry tests
# ---------------------------------------------------------------------------

def test_skills_registry_not_empty():
    assert len(SKILLS) > 0


def test_all_skills_have_required_fields():
    for skill in SKILLS:
        assert skill.name, f"Skill missing name: {skill}"
        assert skill.title, f"Skill missing title: {skill}"
        assert skill.description, f"Skill missing description: {skill}"
        assert skill.prompt_file, f"Skill missing prompt_file: {skill}"


def test_known_skills_present():
    names = [s.name for s in SKILLS]
    for expected in ["algorithms", "design-patterns", "architectural", "cloud", "service-collaboration"]:
        assert expected in names, f"Expected skill {expected!r} not found in registry"


def test_get_skill_returns_correct_skill():
    skill = get_skill("algorithms")
    assert isinstance(skill, PatternSkill)
    assert skill.name == "algorithms"


def test_get_skill_raises_for_unknown():
    import pytest
    with pytest.raises(KeyError):
        get_skill("nonexistent-skill")


def test_skill_prompt_files_exist():
    prompts_dir = ROOT / "prompts"
    for skill in SKILLS:
        prompt_path = prompts_dir / skill.prompt_file
        assert prompt_path.exists(), f"Prompt file missing for skill {skill.name!r}: {prompt_path}"


def test_skill_spec_files_exist():
    specs_dir = ROOT / "specs"
    for skill in SKILLS:
        for spec_file in skill.spec_files:
            spec_path = specs_dir / spec_file
            assert spec_path.exists(), (
                f"Spec file missing for skill {skill.name!r}: {spec_path}"
            )


# ---------------------------------------------------------------------------
# PatternDetector tests
# ---------------------------------------------------------------------------

def test_detector_get_available_patterns():
    detector = PatternDetector(ROOT, ROOT)
    patterns = detector.get_available_patterns()
    assert "algorithms" in patterns
    assert "service-collaboration" in patterns


def test_detector_get_available_skills():
    detector = PatternDetector(ROOT, ROOT)
    skills = detector.get_available_skills()
    assert all(isinstance(s, PatternSkill) for s in skills)


def test_detector_placeholder_output_contains_title():
    """In placeholder mode, the output should mention the skill title."""
    detector = PatternDetector(ROOT, ROOT, execute=False, dry_run=False)
    result = detector.detect_algorithms()
    assert "ALGORITHMS" in result.upper()


def test_detector_dry_run_shows_prompt():
    detector = PatternDetector(ROOT, ROOT, execute=False, dry_run=True)
    result = detector.detect_algorithms()
    assert "DRY RUN" in result.upper()


def test_detector_service_collaboration_placeholder():
    detector = PatternDetector(ROOT, ROOT, execute=False, dry_run=False)
    result = detector.detect_service_collaboration()
    assert result  # non-empty


def test_detector_architectural_uses_prompt_file():
    """architectural skill should load the dedicated prompt file, not an inline prompt."""
    detector = PatternDetector(ROOT, ROOT, execute=False, dry_run=True)
    result = detector.detect_architectural_patterns()
    # The architectural-patterns-prompt.md references the taxonomy doc
    assert "taxonomy" in result.lower() or "architectural" in result.lower()


def test_detector_chained_requires_execute():
    detector = PatternDetector(ROOT, ROOT, execute=False)
    result = detector.detect_all_patterns_chained(["algorithms"])
    assert "Error" in result


def test_get_spec_info_returns_dict():
    detector = PatternDetector(ROOT, ROOT)
    info = detector.get_spec_info("algorithms")
    assert isinstance(info, dict)


def test_get_spec_info_unknown_returns_empty():
    detector = PatternDetector(ROOT, ROOT)
    info = detector.get_spec_info("nonexistent")
    assert info == {}
