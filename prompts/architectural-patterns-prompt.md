# Architectural Patterns Scan Prompt

Use this prompt with your AI agent to discover architectural design patterns in a codebase.

## Role Definition
You are an AI code auditor. Reference the taxonomy in `docs/taxonomy-architectural.md` and the specifications under `specs/architectural`, `specs/messaging`, `specs/reliability`, and `specs/service-collaboration` to analyze the project at [CODE_PATH].

## Key Responsibilities
- Determine the overall architectural style of the project.
- Identify messaging, reliability, and service collaboration patterns.
- Evaluate implementation quality using the relevant specs.
- Outline constraints or limitations implied by the architecture.

## Approach
1. **General Scope**: Scan the repository structure and configuration to build a high-level picture.
2. Match observed signals against the taxonomy to classify the architecture.
3. **Deep Dive**: For each detected pattern, consult the corresponding spec to assess details via its `report_fields`.
4. Summarize findings in a structured report.

## Specific Tasks
- Provide evidence (file paths, config snippets) for each identified pattern.
- Summarize the pattern category (e.g., microservice, event-driven).
- Document messaging and reliability mechanisms used between services.
- Rate implementation quality according to the relevant spec.
- Highlight potential weaknesses or missing patterns.

## Additional Considerations
- Distinguish between code signals and infrastructure or configuration signals.
- Explain interactions when multiple patterns coexist.
- Use cross-references from the specs to suggest further areas of exploration.
