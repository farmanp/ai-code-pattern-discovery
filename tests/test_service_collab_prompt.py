import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

try:
    from scripts.generate_service_collab_prompt import load_spec, build_prompt, SPEC_PATH
except ModuleNotFoundError:
    import pytest
    pytest.skip("PyYAML not installed", allow_module_level=True)


def test_load_spec():
    spec = load_spec(SPEC_PATH)
    assert "service_collaboration_patterns" in spec


def test_build_prompt():
    spec = {"service_collaboration_patterns": [{"name": "Saga"}, {"name": "API Composition"}]}
    prompt = build_prompt(spec)
    assert "Saga" in prompt
    assert "API Composition" in prompt
