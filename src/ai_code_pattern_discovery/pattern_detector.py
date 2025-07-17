"""Pattern detection logic for analyzing codebases."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


class PatternDetector:
    """Handles pattern detection across different categories."""
    
    def __init__(self, repo_root: Path, target_path: Path, execute: bool = False, dry_run: bool = False, model: str = "sonnet"):
        self.repo_root = repo_root
        self.target_path = target_path
        self.prompts_dir = repo_root / "prompts"
        self.specs_dir = repo_root / "specs"
        self.docs_dir = repo_root / "docs"
        self.execute = execute
        self.dry_run = dry_run
        self.model = model
    
    def _load_spec(self, spec_filename: str) -> Dict[str, Any]:
        """Load a YAML specification file."""
        spec_path = self.specs_dir / spec_filename
        if not spec_path.exists():
            return {}
        
        with open(spec_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_prompt_template(self, prompt_filename: str) -> str:
        """Load a prompt template file."""
        prompt_path = self.prompts_dir / prompt_filename
        if not prompt_path.exists():
            return "Prompt template not found."
        
        with open(prompt_path, 'r') as f:
            content = f.read()
        
        # Replace [CODE_PATH] placeholder with actual target path
        return content.replace("[CODE_PATH]", str(self.target_path))
    
    def _get_file_tree(self, max_depth: int = 3) -> str:
        """Get a tree view of the target directory structure."""
        try:
            result = subprocess.run(
                ["find", str(self.target_path), "-type", "f", "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.java", "-o", "-name", "*.cpp", "-o", "-name", "*.c", "-o", "-name", "*.go", "-o", "-name", "*.rs"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            files = result.stdout.strip().split('\n')[:50]  # Limit to first 50 files
            return '\n'.join(files) if files and files[0] else "No source files found."
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return "Could not generate file tree."
    
    def _execute_claude_code(self, prompt: str) -> str:
        """Execute a prompt using Claude Code CLI."""
        try:
            # Change to target directory for context
            original_cwd = os.getcwd()
            os.chdir(self.target_path)
            
            # Execute claude command
            result = subprocess.run(
                ["claude", "--print", "--model", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Restore original directory
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                # Filter out Node.js experimental warnings from stderr
                stderr_lines = result.stderr.strip().split('\n')
                error_lines = [line for line in stderr_lines if 'ExperimentalWarning' not in line and 'node --trace-warnings' not in line and line.strip()]
                error_message = '\n'.join(error_lines) if error_lines else "Unknown error"
                return f"Error executing Claude Code: {error_message}"
                
        except subprocess.TimeoutExpired:
            os.chdir(original_cwd)
            return "Error: Claude Code execution timed out after 5 minutes"
        except FileNotFoundError:
            return "Error: Claude Code CLI not found. Please install Claude Code and ensure it's in your PATH."
        except Exception as e:
            os.chdir(original_cwd)
            return f"Error executing Claude Code: {str(e)}"
    
    def _analyze_with_ai_prompt(self, prompt: str, pattern_type: str) -> str:
        """
        Analyze codebase using AI prompt, either via Claude Code or as placeholder.
        """
        if self.dry_run:
            return f"""
=== {pattern_type.upper()} ANALYSIS - DRY RUN ===

Target Directory: {self.target_path}
Model: {self.model}

Prompt to be executed:
{prompt}

[This is a dry run - no actual analysis performed]
"""
        
        if self.execute:
            return self._execute_claude_code(prompt)
        
        # Fallback to placeholder
        file_tree = self._get_file_tree()
        
        analysis_result = f"""
=== {pattern_type.upper()} ANALYSIS ===

Target Directory: {self.target_path}

File Structure:
{file_tree}

Analysis Prompt:
{prompt}

=== ANALYSIS PLACEHOLDER ===
This is a placeholder for AI-powered analysis. To execute actual analysis:

Use the --execute flag: ai-code-pattern-discovery --execute {pattern_type.lower().replace(' ', '_')}

The prompt template contains specific instructions for:
- Pattern identification
- Quality metrics
- Code locations
- Recommendations

=== SAMPLE OUTPUT FORMAT ===
Based on the specification, the output should include:
- Pattern name and type
- File locations (file:line)
- Implementation quality score
- Complexity analysis
- Improvement suggestions
"""
        
        return analysis_result
    
    def detect_algorithms(self) -> str:
        """Detect algorithms and data structures."""
        prompt = self._load_prompt_template("algorithms-ds-prompt.md")
        spec = self._load_spec("algorithms-data-structures-spec.yaml")
        
        return self._analyze_with_ai_prompt(prompt, "algorithms & data structures")
    
    def detect_design_patterns(self) -> str:
        """Detect design patterns."""
        prompt = self._load_prompt_template("design-patterns-prompt.md")
        spec = self._load_spec("design-patterns-spec.yaml")
        
        return self._analyze_with_ai_prompt(prompt, "design patterns")
    
    def detect_architectural_patterns(self) -> str:
        """Detect architectural patterns."""
        # Use cloud architecture spec as a starting point for architectural patterns
        spec = self._load_spec("cloud-architecture-spec.yaml")
        
        prompt = f"""
You are an AI code auditor analyzing architectural patterns in the codebase at {self.target_path}.

Using the architectural specifications and patterns found in the specs/ directory,
identify implementations of architectural patterns such as:

- Microservices architecture
- Layered architecture
- MVC/MVP/MVVM patterns
- Event-driven architecture
- Domain-driven design patterns
- CQRS (Command Query Responsibility Segregation)
- Event sourcing
- Saga patterns
- Circuit breaker patterns
- API Gateway patterns

For each detected pattern, provide:
- File locations and relevant code snippets
- Pattern implementation quality
- Adherence to architectural principles
- Suggestions for improvement
- Relationships to other patterns
"""
        
        return self._analyze_with_ai_prompt(prompt, "architectural patterns")
    
    def detect_cloud_patterns(self) -> str:
        """Detect cloud architecture patterns."""
        spec = self._load_spec("cloud-architecture-spec.yaml")
        
        prompt = f"""
You are an AI code auditor analyzing cloud architecture patterns in the codebase at {self.target_path}.

Using the cloud architecture specification, identify implementations of cloud patterns such as:

- Microservices and service mesh
- Container orchestration patterns
- Serverless patterns
- Event-driven architectures
- Cloud-native data patterns
- Resilience patterns (circuit breaker, retry, timeout)
- Observability patterns
- Security patterns
- Deployment patterns

For each detected pattern, provide:
- File locations and implementation details
- Cloud-readiness assessment
- Scalability considerations
- Resilience and fault tolerance
- Security implications
- Performance characteristics
- Recommendations for cloud optimization
"""
        
        return self._analyze_with_ai_prompt(prompt, "cloud architecture patterns")
    
    def get_available_patterns(self) -> List[str]:
        """Get list of available pattern detection categories."""
        return ["algorithms", "design_patterns", "architectural", "cloud"]
    
    def detect_all_patterns_chained(self, patterns: List[str]) -> str:
        """Execute all pattern analyses in a single chained Claude Code session."""
        if not self.execute:
            return "Error: Chained analysis requires --execute flag"
        
        # Build comprehensive chained prompt
        chain_prompt = f"""
I want you to analyze the codebase at {self.target_path} for multiple pattern types in sequence. 
Please provide a comprehensive analysis covering all requested patterns.

Target Directory: {self.target_path}

Please analyze the following patterns in order:
"""
        
        for i, pattern in enumerate(patterns, 1):
            if pattern == "algorithms":
                template = self._load_prompt_template("algorithms-ds-prompt.md")
            elif pattern == "design_patterns":
                template = self._load_prompt_template("design-patterns-prompt.md")
            elif pattern == "architectural":
                template = f"""
Analyze architectural patterns in this codebase. Look for:
- Microservices architecture
- Layered architecture
- MVC/MVP/MVVM patterns
- Event-driven architecture
- Domain-driven design patterns
- CQRS and Event sourcing
- Circuit breaker and other resilience patterns

For each pattern found, provide:
- File locations and code examples
- Implementation quality assessment
- Architectural compliance
- Recommendations for improvement
"""
            elif pattern == "cloud":
                template = f"""
Analyze cloud architecture patterns in this codebase. Look for:
- Cloud-native patterns (12-factor app principles)
- Containerization patterns
- Service mesh patterns
- Event-driven cloud patterns
- Serverless patterns
- Cloud security patterns
- Observability patterns

For each pattern found, provide:
- File locations and implementation details
- Cloud-readiness assessment
- Scalability considerations
- Best practices compliance
- Recommendations for cloud optimization
"""
            else:
                template = f"Analyze {pattern} patterns in the codebase."
            
            chain_prompt += f"""

{i}. {pattern.replace('_', ' ').title()} Analysis:
{template}

---
"""
        
        chain_prompt += """

Please provide a comprehensive report with:
1. Executive summary of all patterns found
2. Detailed analysis for each pattern type
3. Cross-pattern relationships and interactions
4. Overall architecture assessment
5. Prioritized recommendations for improvement

Format the response with clear sections and use markdown for better readability.
"""
        
        return self._execute_claude_code(chain_prompt)
    
    def get_spec_info(self, pattern_type: str) -> Dict[str, Any]:
        """Get specification information for a pattern type."""
        spec_mapping = {
            "algorithms": "algorithms-data-structures-spec.yaml",
            "design_patterns": "design-patterns-spec.yaml",
            "architectural": "cloud-architecture-spec.yaml",  # Using cloud spec as base
            "cloud": "cloud-architecture-spec.yaml"
        }
        
        spec_file = spec_mapping.get(pattern_type)
        if spec_file:
            return self._load_spec(spec_file)
        return {}