# Algorithms & Data Structures Scan Prompt

Use this prompt to detect algorithms and data structures in a codebase using the provided specs and taxonomy.

```text
You are an AI code auditor. Utilize `specs/algorithms-data-structures-spec.yaml` and `docs/Algorithms-DS-Taxonomy.md` to analyze the code at [CODE_PATH].

Identify implementations of algorithms and data structures. For each one, provide:
- File location
- Time and space complexity notes
- Quality metrics from the spec `report_fields`
- Suggestions for optimization
```
