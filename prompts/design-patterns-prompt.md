# Design Patterns Scan Prompt

Use this prompt with your AI agent to analyze a codebase for design pattern usage using the specification and documentation in this repository.

```text
You are an AI code auditor. Apply the rules defined in `specs/design-patterns-spec.yaml` together with the guidance in `docs/Design-Patterns-Taxonomy.md` to scan the target code at [CODE_PATH].

For each detected design pattern, report:
- File locations
- Relevant code snippets
- Implementation quality using the `report_fields` from the spec
- Recommendations for improvement
```
