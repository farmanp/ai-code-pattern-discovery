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

4. **Generate Documentation**: Extend `scripts/generate_from_spec.py` to process specifications and generate pattern documentation.

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
   ai-code-pattern-discovery all                          # Run all analyses
   ai-code-pattern-discovery list-specs                   # List available specifications
   
   # Target a specific codebase
   ai-code-pattern-discovery --target-path /path/to/code --execute all
   
   # Run specific pattern analyses
   ai-code-pattern-discovery --execute all --patterns algorithms --patterns design_patterns
   
   # Chain prompts together in a single Claude Code session
   ai-code-pattern-discovery --execute all --chain
   
   # Use different Claude models
   ai-code-pattern-discovery --execute --model opus algorithms
   ai-code-pattern-discovery --execute --model haiku all
   ```

## Project Structure

```
ai-code-pattern-discovery/
├── docs/                    # Pattern taxonomies and guides
├── prompts/                 # AI prompts for pattern analysis
├── specs/                   # YAML specifications for patterns
├── src/                     # Python package source code
│   └── ai_code_pattern_discovery/
│       ├── __init__.py
│       ├── cli.py          # Main CLI interface
│       └── pattern_detector.py  # Pattern detection logic
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

For more detailed information, check out `docs/getting-started.md` for a comprehensive introduction to using this pattern discovery system.

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
