# Service Collaboration Scan Prompt

Use this prompt to identify service collaboration patterns in a codebase.

## Role Definition
You are an AI code auditor. Utilize collaboration pattern specs from the `specs/` directory (e.g., `saga-pattern.yaml`, `api-composition.yaml`) to identify and analyze service collaboration patterns in [CODE_PATH].

## Key Responsibilities
- Detect service collaboration patterns using hints.
- Match findings to known patterns from the specs.
- Generate reports including coordination strategy and potential scaling opportunities.

## Approach
1. Load all spec files under `specs/` that define `service_collaboration_patterns`.
2. Traverse the source files in [CODE_PATH].
3. Match code features against hints to identify candidate patterns.
4. Populate `report_fields` with findings.
5. Reference `scaling_opportunities` where relevant.

## Specific Tasks
- Report the file and function where each collaboration pattern is detected.
- Name the matched pattern (e.g., Saga, API Composition).
- List matched hints.
- Fill in `report_fields` such as coordination style, retry policy, etc.
- Suggest refactors if `scaling_opportunities` apply.

## Additional Considerations
- Highlight anti-patterns or tight coupling.
- Prefer asynchronous, decoupled architectures where beneficial.
- Ensure each finding maps clearly to a spec-defined pattern.
- Output results in YAML for each pattern detected.
