"""Pattern detection logic for analyzing codebases."""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

from .rate_limiter import RateLimiter


class PatternDetector:
    """Handles pattern detection across different categories."""
    
    def __init__(self, repo_root: Path, target_path: Path, execute: bool = False, dry_run: bool = False, model: str = "sonnet", interactive: bool = False, timeout: int = 300, verbose: bool = False, stream: bool = False):
        self.repo_root = repo_root
        self.target_path = target_path
        self.prompts_dir = repo_root / "prompts"
        self.specs_dir = repo_root / "specs"
        self.docs_dir = repo_root / "docs"
        self.execute = execute
        self.dry_run = dry_run
        self.model = model
        self.interactive = interactive
        self.timeout = timeout
        self.verbose = verbose
        self.stream = stream
        self.rate_limiter = RateLimiter()
    
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
            
            # Build command
            cmd = ["claude", "--model", self.model]
            
            if self.interactive:
                # Interactive mode - user can see and interact with Claude
                cmd.append(prompt)
            elif self.stream:
                # For streaming, we'll use regular print mode but with better monitoring
                cmd.extend(["--print", prompt])
            else:
                # Print mode - return output directly
                cmd.extend(["--print", prompt])
            
            if self.verbose:
                print(f"[DEBUG] Executing command: {' '.join(cmd)}")
                print(f"[DEBUG] Working directory: {self.target_path}")
                print(f"[DEBUG] Timeout: {self.timeout} seconds")
            
            if self.stream and not self.interactive:
                # Try streaming first, fall back to regular if it fails
                try:
                    return self._execute_claude_code_streaming(cmd)
                except Exception as e:
                    if self.verbose:
                        print(f"[WARNING] Streaming failed ({e}), falling back to regular execution")
                    # Fall through to regular execution
            
            if True:  # Always execute this block if streaming failed or not enabled
                # Execute claude command
                result = subprocess.run(
                    cmd,
                    capture_output=not self.interactive,
                    text=True,
                    timeout=self.timeout
                )
                
                # Restore original directory
                os.chdir(original_cwd)
                
                if result.returncode == 0:
                    # Record successful request
                    self.rate_limiter.record_request("pattern_analysis")
                    
                    if self.interactive:
                        return "Interactive Claude Code session completed. Check your terminal for results."
                    else:
                        return result.stdout.strip()
                else:
                    # Filter out Node.js experimental warnings from stderr
                    stderr_lines = result.stderr.strip().split('\n') if result.stderr else []
                    error_lines = [line for line in stderr_lines if 'ExperimentalWarning' not in line and 'node --trace-warnings' not in line and line.strip()]
                    error_message = '\n'.join(error_lines) if error_lines else "Unknown error"
                    return f"Error executing Claude Code: {error_message}"
                
        except subprocess.TimeoutExpired:
            os.chdir(original_cwd)
            timeout_msg = f"Error: Claude Code execution timed out after {self.timeout} seconds\n\n"
            timeout_msg += "💡 Try these solutions:\n"
            timeout_msg += f"  • Increase timeout: --timeout {self.timeout * 2}\n"
            timeout_msg += "  • Use streaming mode: --stream\n"
            timeout_msg += "  • Use interactive mode: --interactive\n"
            timeout_msg += "  • Analyze smaller code sections\n"
            timeout_msg += "  • Use session mode for exploratory analysis"
            return timeout_msg
        except FileNotFoundError:
            return "Error: Claude Code CLI not found. Please install Claude Code and ensure it's in your PATH."
        except Exception as e:
            os.chdir(original_cwd)
            return f"Error executing Claude Code: {str(e)}"
    
    def _execute_claude_code_streaming(self, cmd: List[str]) -> str:
        """Execute Claude Code with streaming output and better diagnostics."""
        import threading
        import queue
        import json
        
        output_queue = queue.Queue()
        error_queue = queue.Queue()
        
        def stream_output(pipe, queue_obj, prefix=""):
            """Stream output from subprocess pipe."""
            try:
                while True:
                    line = pipe.readline()
                    if not line:
                        break
                    queue_obj.put(f"{prefix}{line.rstrip()}")
            except Exception as e:
                queue_obj.put(f"Error reading stream: {e}")
        
        is_json_stream = False  # Disabled for now due to Claude Code requirements
        
        try:
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,  # Unbuffered
                universal_newlines=True
            )
            
            # Start streaming threads
            stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, output_queue))
            stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, error_queue, "[ERROR] "))
            
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            
            stdout_thread.start()
            stderr_thread.start()
            
            # Stream output in real-time
            output_lines = []
            error_lines = []
            content_buffer = ""
            
            print("[INFO] Claude Code is processing your request...")
            print("[INFO] Monitoring process output (press Ctrl+C to cancel):")
            print("=" * 60)
            print(f"[INFO] Process started at {time.strftime('%H:%M:%S')}")
            print(f"[INFO] Timeout: {self.timeout} seconds")
            
            last_heartbeat = time.time()
            start_time = time.time()
            heartbeat_interval = 10  # seconds
            no_output_count = 0
            
            while process.poll() is None:
                had_output = False
                
                # Check for new output
                try:
                    while True:
                        line = output_queue.get_nowait()
                        
                        if is_json_stream:
                            # Parse JSON streaming format
                            try:
                                data = json.loads(line)
                                if 'content' in data:
                                    content = data['content']
                                    print(content, end='', flush=True)
                                    content_buffer += content
                                    had_output = True
                                elif 'error' in data:
                                    print(f"\n[ERROR] {data['error']}")
                                    error_lines.append(data['error'])
                                    had_output = True
                            except json.JSONDecodeError:
                                # Not valid JSON, treat as regular output
                                print(line)
                                output_lines.append(line)
                                had_output = True
                        else:
                            # Regular line output
                            print(line)
                            output_lines.append(line)
                            had_output = True
                        
                        last_heartbeat = time.time()
                        no_output_count = 0
                except queue.Empty:
                    pass
                
                # Check for errors
                try:
                    while True:
                        line = error_queue.get_nowait()
                        if 'ExperimentalWarning' not in line and 'node --trace-warnings' not in line:
                            print(line)
                            error_lines.append(line)
                            had_output = True
                            last_heartbeat = time.time()
                except queue.Empty:
                    pass
                
                # Heartbeat mechanism
                current_time = time.time()
                if current_time - last_heartbeat >= heartbeat_interval:
                    no_output_count += 1
                    elapsed_since_output = int(current_time - last_heartbeat)
                    total_elapsed = int(current_time - start_time)
                    
                    if no_output_count <= 3:  # Show heartbeat for first 3 intervals
                        print(f"[INFO] Still processing... ({elapsed_since_output}s since last output, {total_elapsed}s total)")
                    elif no_output_count % 6 == 0:  # Show every minute after that
                        print(f"[INFO] Long-running analysis in progress... (total: {total_elapsed}s)")
                    last_heartbeat = current_time
                
                # Small delay to prevent busy waiting
                time.sleep(0.5)
            
            # Get any remaining output
            try:
                while True:
                    line = output_queue.get_nowait()
                    print(line)
                    output_lines.append(line)
            except queue.Empty:
                pass
            
            # Get any remaining errors
            try:
                while True:
                    line = error_queue.get_nowait()
                    if 'ExperimentalWarning' not in line and 'node --trace-warnings' not in line:
                        print(line)
                        error_lines.append(line)
            except queue.Empty:
                pass
            
            # Wait for threads to finish
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            
            print("=" * 60)
            
            # Check return code
            if process.returncode == 0:
                self.rate_limiter.record_request("pattern_analysis")
                
                # Use appropriate result based on format
                if is_json_stream and content_buffer.strip():
                    result = content_buffer
                else:
                    result = '\n'.join(output_lines)
                
                if result.strip():
                    print(f"\n[INFO] Claude Code completed successfully")
                    return result
                else:
                    print(f"\n[WARNING] Claude Code completed but produced no output")
                    return "Claude Code completed but produced no output. This may indicate an issue with the prompt or Claude Code configuration."
            else:
                error_msg = '\n'.join(error_lines) if error_lines else f"Process exited with code {process.returncode}"
                return f"Error executing Claude Code: {error_msg}"
                
        except KeyboardInterrupt:
            print("\n[INFO] Cancelling Claude Code execution...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("[WARNING] Process didn't terminate gracefully, forcing kill...")
                process.kill()
            return "Analysis cancelled by user"
        except Exception as e:
            return f"Error during streaming execution: {str(e)}"
    
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