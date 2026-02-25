# ai-code-pattern-discovery

A comprehensive system for discovering, documenting, and understanding code patterns, algorithms, data structures, and architectural patterns using AI-powered analysis. This repository provides taxonomies, specifications, and prompt templates for analyzing software engineering patterns.

## Overview

This project helps developers and AI systems identify and understand:
- **Design Patterns**: Classic software design patterns (Creational, Structural, Behavioral)
- **Algorithms & Data Structures**: Common algorithms and data structures with complexity analysis
- **Cloud Architecture Patterns**: Modern cloud-native architectural patterns
- **Pattern Cross-References**: How different patterns relate to and complement each other

## Key Features

- 📚 **Comprehensive Taxonomies**: Detailed documentation of patterns across multiple domains
- 🔍 **AI-Ready Prompts**: Carefully crafted prompts for pattern recognition and analysis
- 📋 **Structured Specifications**: YAML-based specifications for consistent pattern documentation
- 🔗 **Cross-Reference Guide**: Understanding relationships between different pattern types
- 📊 **Complexity Analysis**: Big-O notation and performance considerations
- 🖥️ **CLI Tool**: Command-line interface for easy pattern analysis on any codebase
- 🧩 **Skills Registry**: Each analysis type is a named, self-describing `PatternSkill` with a prompt template and associated specs

## Usage

1. **Explore Pattern Taxonomies**: Browse the `docs/` directory to understand different pattern categories:
   - `Design-Patterns-Taxonomy.md`: Gang of Four and modern design patterns
   - `Algorithms-DS-Taxonomy.md`: Algorithms and data structures reference
   - `Cloud-Architecture-Taxonomy.md`: Cloud-native architectural patterns
   - `Pattern-Cross-Reference.md`: How patterns work together
   - `Complexity-Guide.md`: Performance and complexity analysis guide

2. **Use AI Prompts**: Leverage prompts in `prompts/` for pattern analysis:
   - `design-patterns-prompt.md`: For identifying design patterns in code
   - `algorithms-ds-prompt.md`: For algorithm and data structure analysis

3. **Work with Specifications**: Use YAML specs in `specs/` to structure pattern documentation:
   - `design-patterns-spec.yaml`: Design pattern specification template
   - `algorithms-data-structures-spec.yaml`: Algorithm/DS specification template
   - `cloud-architecture-spec.yaml`: Cloud architecture pattern template
   - `service-collaboration-patterns.yaml`: Collaboration pattern reference

4. **Generate Documentation**: Extend `scripts/generate_from_spec.py` to process specifications and generate pattern documentation.
   - `scripts/generate_service_collab_prompt.py` outputs a prompt listing supported collaboration patterns.

5. **CLI Tool Usage**: Use the command-line tool to analyze any codebase:
   ```bash
   # Install the CLI tool
   uv venv && source .venv/bin/activate && uv pip install -e .
   
   # Show prompts without executing (dry run)
   ai-code-pattern-discovery --dry-run algorithms
   
   # Execute prompts using Claude Code (requires Claude subscription)
   ai-code-pattern-discovery --execute algorithms          # Execute single analysis
   ai-code-pattern-discovery --execute all                # Execute all analyses
   
   # Analyze patterns in a codebase (placeholder mode)
   ai-code-pattern-discovery algorithms                    # Detect algorithms & data structures
   ai-code-pattern-discovery design-patterns              # Detect design patterns
   ai-code-pattern-discovery architectural                # Detect architectural patterns
   ai-code-pattern-discovery cloud                        # Detect cloud patterns
   ai-code-pattern-discovery service-collaboration        # Detect service collaboration patterns
   ai-code-pattern-discovery all                          # Run all analyses
   ai-code-pattern-discovery list-specs                   # List all skills and available specifications
   
   # Target a specific codebase
   ai-code-pattern-discovery --target-path /path/to/code --execute all
   
   # Run specific pattern analyses
   ai-code-pattern-discovery --execute all --patterns algorithms --patterns design-patterns
   
   # Chain prompts together in a single Claude Code session
   ai-code-pattern-discovery --execute all --chain
   
   # Use different Claude models and timeouts
   ai-code-pattern-discovery --execute --model opus --timeout 600 algorithms
   ai-code-pattern-discovery --execute --model haiku --timeout 120 all
   
   # Interactive mode - start a Claude Code session
   ai-code-pattern-discovery --execute --interactive session
   
   # Skip confirmation prompts and enable streaming
   ai-code-pattern-discovery --execute --no-confirm --stream all
   
   # Verbose mode with streaming for debugging
   ai-code-pattern-discovery --execute --verbose --stream algorithms
   
   # Check usage and rate limits
   ai-code-pattern-discovery usage
   ```

## Project Structure

```
ai-code-pattern-discovery/
├── agents/                  # Agent markdown definitions for the interview prep tool
│   ├── repo_analyzer.md     # Analyzes repo structure, languages, patterns
│   ├── skills_extractor.md  # Maps patterns to interview-relevant skills
│   └── question_generator.md # Generates interview questions by difficulty
├── skills/                  # Shared skill vocabulary used by agents
│   ├── skills_db.md         # Canonical skill definitions, categories, difficulty
│   └── patterns.md          # Code pattern → skill mappings and difficulty rules
├── main.py                  # Interview prep tool orchestrator (three-agent pipeline)
├── docs/                    # Pattern taxonomies and guides
├── prompts/                 # AI prompts for pattern analysis
├── specs/                   # YAML specifications for patterns
├── src/                     # Python package source code
│   └── ai_code_pattern_discovery/
│       ├── __init__.py
│       ├── cli.py          # Main CLI interface
│       ├── skills.py       # PatternSkill registry (skills + agent definitions)
│       └── pattern_detector.py  # Pattern detection logic driven by skills registry
├── scripts/                 # Generation and processing scripts
├── examples/                # Example outputs
├── templates/               # Specification templates
├── tests/                   # Test suite
├── pyproject.toml          # Python package configuration
└── .venv/                  # Virtual environment (created by uv)
```

## Getting Started

### Quick Start with CLI Tool

1. **Install the package:**
   ```bash
   uv venv && source .venv/bin/activate && uv pip install -e .
   ```

2. **Preview analysis prompts (dry run):**
   ```bash
   ai-code-pattern-discovery --dry-run --target-path /path/to/your/code all
   ```

3. **Execute real analysis with Claude Code:**
   ```bash
   ai-code-pattern-discovery --execute --target-path /path/to/your/code all
   ```

4. **View available specifications:**
   ```bash
   ai-code-pattern-discovery list-specs
   ```

### Prerequisites for Execution Mode

To use the `--execute` flag, you need:
- [Claude Code](https://claude.ai/code) installed and configured
- Active Claude subscription
- Claude Code CLI in your PATH

Install Claude Code:
```bash
npm install -g @anthropic-ai/claude-code
# or
curl -fsSL https://claude.ai/install.sh | sh
```

### Safety Features

The CLI includes several safety features to prevent overloading Claude:

- **Rate Limiting**: Tracks API usage per minute/hour/day
- **Confirmation Prompts**: Asks before executing expensive operations
- **Progress Indicators**: Shows real-time progress during analysis
- **Timeout Controls**: Configurable timeouts for long-running analyses
- **Usage Monitoring**: Track your API usage with `ai-code-pattern-discovery usage`
- **Interactive Mode**: Start a Claude Code session for exploratory analysis
- **Streaming Output**: See Claude's response in real-time with `--stream`
- **Verbose Mode**: Debug with `--verbose` to see exact commands executed
- **Graceful Cancellation**: Ctrl+C properly terminates Claude Code processes

### Execution Modes

1. **Placeholder Mode** (default): Shows analysis structure without execution
2. **Dry Run Mode** (`--dry-run`): Preview prompts that would be executed
3. **Print Mode** (`--execute`): Execute prompts and return results
4. **Interactive Mode** (`--execute --interactive`): Start interactive Claude Code session
5. **Chained Mode** (`--execute --chain`): Combine multiple analyses in one session
6. **Streaming Mode** (`--execute --stream`): See Claude's response in real-time
7. **Verbose Mode** (`--execute --verbose`): Debug mode with command details

### Observability Features

The CLI now provides excellent visibility into what's happening:

- **Real-time Streaming**: Use `--stream` to monitor process execution
- **Heartbeat Messages**: Shows process is alive with timing updates every 10 seconds
- **Progress Tracking**: Visual indicators show time elapsed and current status
- **Command Visibility**: `--verbose` shows exactly what commands are being executed
- **Rate Limit Monitoring**: Always shows current usage before execution
- **Graceful Cancellation**: Ctrl+C properly stops processes and cleans up
- **Error Handling**: Clear error messages with troubleshooting hints
- **Process Monitoring**: Shows start time, timeout, and total elapsed time
- **Diagnostic Commands**: `test-claude` to verify Claude Code connectivity

For more detailed information, check out `docs/getting-started.md` for a comprehensive introduction to using this pattern discovery system.

## Skills & Agents Architecture

The tool is structured around two core concepts from modern AI agent design:

### Skills

A **skill** (`PatternSkill`) is a named, self-describing analysis capability.  Each skill bundles:
- a unique `name` (CLI command identifier)
- a human-readable `title` and `description`
- a `prompt_file` (template in `prompts/`)
- one or more `spec_files` (YAML specs in `specs/`) the prompt should consult

The registry lives in `src/ai_code_pattern_discovery/skills.py` and is the single source-of-truth for all supported analyses.  To add a new skill, add a `PatternSkill` entry to the `SKILLS` list — the CLI and `PatternDetector` will pick it up automatically.

### Agent Orchestration

The CLI acts as a lightweight **agent** that:
1. Resolves the requested skill(s) from the registry
2. Checks rate limits and asks for confirmation before expensive operations
3. Dispatches each skill via `PatternDetector._run_skill()`, passing the compiled prompt to Claude Code
4. In **chained mode** (`--chain`), combines all skill prompts into a single Claude Code session for holistic analysis

---

## Interview Prep Tool

`main.py` is a standalone three-agent pipeline that analyzes **any** code repository and generates tailored technical interview questions using the Anthropic Claude API.

### What it does

1. **Repo Analyzer** — scans the repository structure, detects languages, architectural patterns, algorithms, data structures, and design patterns used.
2. **Skills Extractor** — maps every detected pattern to a curated set of interview-relevant skills (algorithms, data structures, design patterns, system design), each rated by difficulty and relevance.
3. **Question Generator** — produces interview questions at easy / medium / hard difficulty levels, tagged with skill, category, company patterns, answer hints, and follow-up questions.

Results are saved as both JSON (machine-readable, for curation tooling) and Markdown (human-readable, for study guides).

### How to use it

**Prerequisites**

```bash
pip install anthropic      # if not already in your environment
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Run on any repository**

```bash
# Analyze this repository itself and generate questions (saves to ./interview_prep_output/)
python main.py .

# Target a different repo and specify output location
python main.py /path/to/some/repo --output-dir ~/prep_sessions/my_repo

# Preview the agent prompts without making any API calls
python main.py /path/to/repo --dry-run

# Use a specific model and cap question count
python main.py /path/to/repo --model claude-3-5-sonnet-20241022 --max-questions 20

# Save only JSON (skip Markdown)
python main.py /path/to/repo --format json
```

**All options**

```
usage: main.py [-h] [--output-dir OUTPUT_DIR] [--format {json,markdown,both}]
               [--model MODEL] [--max-questions MAX_QUESTIONS] [--dry-run]
               repo_path

positional arguments:
  repo_path             Path to the repository to analyze.

optional arguments:
  --output-dir DIR      Directory to write results (default: ./interview_prep_output)
  --format {json,markdown,both}
                        Output format (default: both)
  --model MODEL         Claude model to use (default: claude-opus-4-5)
  --max-questions N     Maximum questions to generate (default: 30)
  --dry-run             Print agent prompts without calling the API
```

### Example output

After running `python main.py /path/to/repo`, you get two files in `interview_prep_output/`:

**`interview_prep_<timestamp>.md`** (study guide)
```markdown
# Interview Prep Questions

**Repository:** `/path/to/repo`
**Generated:** 2026-01-15T10:30:00Z

## Summary
- Total questions: 18
- By difficulty: easy: 6, medium: 8, hard: 4
- By category: algorithms: 7, data-structures: 4, design-patterns: 4, system-design: 3

---

## Algorithms

### Easy

#### How does binary search work?
**Skill:** Binary Search
**Context:** Found in the search module; used to locate pattern entries in the sorted skills registry.
**Answer hints:**
- Repeatedly halve the search space using two pointers
- Requires a sorted input; returns the index or -1 if not found
**Follow-ups:**
- What is its time complexity? When can you apply it to a non-array search space?
**Company patterns:** Google, Amazon, Meta
```

**`interview_prep_<timestamp>.json`** (machine-readable)
```json
{
  "repo_analysis": { ... },
  "extracted_skills": { ... },
  "questions": {
    "questions": [ ... ],
    "summary": { "total_questions": 18, ... }
  }
}
```

### How the agents work together

```
main.py
│
├─► agents/repo_analyzer.md ──────► Claude API ──► repo_analysis.json
│         (scan structure, detect patterns)
│
├─► agents/skills_extractor.md ───► Claude API ──► extracted_skills.json
│         (map patterns → skills using skills/skills_db.md + skills/patterns.md)
│
└─► agents/question_generator.md ─► Claude API ──► questions.json + questions.md
          (generate easy/medium/hard questions per skill)
```

Each agent is a self-contained Markdown file in `agents/`. You can iterate on any one independently — change the prompt, adjust output schema, add new skill categories — without touching the others.

The `skills/` directory provides the shared vocabulary:
- `skills/skills_db.md` — canonical list of all skills with IDs, categories, and default difficulty
- `skills/patterns.md` — lookup table mapping detected code patterns to skill IDs

## Installation

### Using uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-pattern-discovery.git
cd ai-code-pattern-discovery

# Create virtual environment and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-pattern-discovery.git
cd ai-code-pattern-discovery

# Create virtual environment and install
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Development

To set up for development:
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```
