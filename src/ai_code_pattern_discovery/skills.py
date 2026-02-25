"""Skill definitions for AI code pattern analysis.

Each PatternSkill represents a reusable, named analysis capability that pairs a
prompt template with one or more YAML specifications.  The registry at the
bottom of this module is the single source-of-truth for all supported skills.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PatternSkill:
    """A named, self-describing analysis skill.

    Attributes:
        name: Machine-friendly identifier (e.g. ``"algorithms"``).
        title: Human-readable label (e.g. ``"Algorithms & Data Structures"``).
        description: One-line summary surfaced in help text and reports.
        prompt_file: Filename (relative to ``prompts/``) containing the
            prompt template for this skill.
        spec_files: One or more spec filenames (relative to ``specs/``)
            that the prompt should consult.
    """

    name: str
    title: str
    description: str
    prompt_file: str
    spec_files: List[str] = field(default_factory=list)


#: Registry of all built-in pattern skills.
SKILLS: List[PatternSkill] = [
    PatternSkill(
        name="algorithms",
        title="Algorithms & Data Structures",
        description="Identify sorting, searching, graph, and other algorithmic patterns.",
        prompt_file="algorithms-ds-prompt.md",
        spec_files=["algorithms-data-structures-spec.yaml"],
    ),
    PatternSkill(
        name="design-patterns",
        title="Design Patterns",
        description="Detect Gang-of-Four and modern design patterns.",
        prompt_file="design-patterns-prompt.md",
        spec_files=["design-patterns-spec.yaml"],
    ),
    PatternSkill(
        name="architectural",
        title="Architectural Patterns",
        description="Classify the overall architectural style and sub-patterns.",
        prompt_file="architectural-patterns-prompt.md",
        spec_files=[
            "architectural/microservice-architecture.yaml",
            "messaging/event-sourcing.yaml",
            "messaging/transactional-outbox.yaml",
            "reliability/circuit-breaker.yaml",
            "service-boundaries/business-capability.yaml",
            "service-collaboration/saga-pattern.yaml",
            "service-collaboration/api-composition.yaml",
        ],
    ),
    PatternSkill(
        name="cloud",
        title="Cloud Architecture Patterns",
        description="Assess cloud-native readiness, container and serverless patterns.",
        prompt_file="architectural-patterns-prompt.md",
        spec_files=["cloud-architecture-spec.yaml"],
    ),
    PatternSkill(
        name="service-collaboration",
        title="Service Collaboration Patterns",
        description="Detect orchestration, choreography, saga, CQRS and other inter-service patterns.",
        prompt_file="service-collaboration-prompt.md",
        spec_files=[
            "service-collaboration-patterns.yaml",
            "service-collaboration/saga-pattern.yaml",
            "service-collaboration/api-composition.yaml",
        ],
    ),
]


def get_skill(name: str) -> PatternSkill:
    """Return the skill with the given name, or raise ``KeyError``."""
    for skill in SKILLS:
        if skill.name == name:
            return skill
    raise KeyError(f"Unknown skill: {name!r}")
