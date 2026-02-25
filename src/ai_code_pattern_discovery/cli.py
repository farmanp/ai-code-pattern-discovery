"""Main CLI module for ai-code-pattern-discovery."""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Confirm

from .pattern_detector import PatternDetector
from .rate_limiter import RateLimiter
from .skills import SKILLS, get_skill


console = Console()


def get_repo_root() -> Path:
    """Get the root directory of the ai-code-pattern-discovery repository."""
    return Path(__file__).parent.parent.parent


@click.group()
@click.version_option()
@click.option(
    "--target-path",
    "-t",
    default=".",
    help="Path to the codebase to analyze",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--execute",
    "-e",
    is_flag=True,
    default=False,
    help="Execute prompts using Claude Code (requires Claude subscription)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show prompts without executing them",
)
@click.option(
    "--model",
    default="sonnet",
    help="Claude model to use (sonnet, opus, haiku)",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    default=False,
    help="Start interactive Claude Code session instead of --print mode",
)
@click.option(
    "--timeout",
    default=300,
    help="Timeout for Claude Code execution in seconds (default: 300, use 600+ for large codebases)",
)
@click.option(
    "--confirm",
    is_flag=True,
    default=True,
    help="Ask for confirmation before executing (default: true)",
)
@click.option(
    "--no-confirm",
    is_flag=True,
    default=False,
    help="Skip confirmation prompts",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Show verbose output including Claude Code commands",
)
@click.option(
    "--stream",
    is_flag=True,
    default=False,
    help="Stream Claude Code output in real-time",
)
@click.pass_context
def cli(ctx, target_path: Path, execute: bool, dry_run: bool, model: str, interactive: bool, timeout: int, confirm: bool, no_confirm: bool, verbose: bool, stream: bool):
    """AI Code Pattern Discovery CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["target_path"] = target_path.resolve()
    ctx.obj["repo_root"] = get_repo_root()
    ctx.obj["execute"] = execute
    ctx.obj["dry_run"] = dry_run
    ctx.obj["model"] = model
    ctx.obj["interactive"] = interactive
    ctx.obj["timeout"] = timeout
    ctx.obj["confirm"] = confirm and not no_confirm
    ctx.obj["verbose"] = verbose
    ctx.obj["stream"] = stream


def _check_rate_limit_and_confirm(ctx, pattern_type: str, num_requests: int = 1) -> bool:
    """Check rate limits and ask user for confirmation before executing expensive operations."""
    rate_limiter = RateLimiter()
    
    # Check rate limits
    can_proceed, message = rate_limiter.check_rate_limit()
    if not can_proceed:
        console.print(f"[red]Rate limit exceeded: {message}[/red]")
        
        reset_times = rate_limiter.time_until_reset()
        if reset_times:
            console.print("[yellow]Rate limits will reset in:[/yellow]")
            for period, seconds in reset_times.items():
                if seconds > 0:
                    minutes = int(seconds // 60)
                    seconds = int(seconds % 60)
                    console.print(f"• {period}: {minutes}m {seconds}s")
        
        return False
    
    # Show usage stats
    stats = rate_limiter.get_usage_stats()
    console.print(f"[dim]Current usage: {stats['minute']['used']}/{stats['minute']['limit']} per minute, "
                  f"{stats['hour']['used']}/{stats['hour']['limit']} per hour, "
                  f"{stats['day']['used']}/{stats['day']['limit']} per day[/dim]")
    
    # Confirm execution
    if not ctx.obj["confirm"]:
        return True
    
    console.print(f"\n[yellow]About to execute {pattern_type} analysis ({num_requests} requests):[/yellow]")
    console.print(f"[cyan]Target: {ctx.obj['target_path']}[/cyan]")
    console.print(f"[cyan]Model: {ctx.obj['model']}[/cyan]")
    console.print(f"[cyan]Mode: {'Interactive' if ctx.obj['interactive'] else 'Print'}[/cyan]")
    console.print(f"[cyan]Timeout: {ctx.obj['timeout']} seconds[/cyan]")
    
    # Warn about potentially long processing times
    if ctx.obj['timeout'] <= 300:
        console.print("[yellow]💡 Tip: For large codebases, consider using --timeout 600 or --stream mode[/yellow]")
    
    return Confirm.ask("Continue with analysis?", default=True)

def _make_detector(ctx) -> PatternDetector:
    """Construct a :class:`PatternDetector` from the current Click context."""
    return PatternDetector(
        ctx.obj["repo_root"],
        ctx.obj["target_path"],
        execute=ctx.obj["execute"],
        dry_run=ctx.obj["dry_run"],
        model=ctx.obj["model"],
        interactive=ctx.obj["interactive"],
        timeout=ctx.obj["timeout"],
        verbose=ctx.obj["verbose"],
        stream=ctx.obj["stream"],
    )


def _run_analysis(ctx, skill_name: str) -> None:
    """Common entry point for single-skill analysis commands."""
    skill = get_skill(skill_name)

    if ctx.obj["execute"] and not _check_rate_limit_and_confirm(ctx, skill.title, 1):
        console.print("[yellow]Analysis cancelled.[/yellow]")
        return

    detector = _make_detector(ctx)

    console.print(f"\n[bold green]{skill.title} Analysis[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")

    if ctx.obj["execute"]:
        if ctx.obj["stream"]:
            console.print("[cyan]Streaming mode enabled - output will appear in real-time[/cyan]")
            results = detector._run_skill(skill)
        else:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Executing prompt via Claude Code...", total=None)
                results = detector._run_skill(skill)
                progress.update(task, description="Analysis complete!")
    elif ctx.obj["dry_run"]:
        console.print("[yellow]Dry run mode - showing prompt only[/yellow]")
        results = detector._run_skill(skill)
    else:
        results = detector._run_skill(skill)

    console.print("\n" + results)


@cli.command()
@click.pass_context
def algorithms(ctx):
    """Detect algorithms and data structures in the codebase."""
    _run_analysis(ctx, "algorithms")


@cli.command()
@click.pass_context
def design_patterns(ctx):
    """Detect design patterns in the codebase."""
    _run_analysis(ctx, "design-patterns")


@cli.command()
@click.pass_context
def architectural(ctx):
    """Detect architectural patterns in the codebase."""
    _run_analysis(ctx, "architectural")


@cli.command()
@click.pass_context
def cloud(ctx):
    """Detect cloud architecture patterns in the codebase."""
    _run_analysis(ctx, "cloud")


@cli.command(name="service-collaboration")
@click.pass_context
def service_collaboration(ctx):
    """Detect service collaboration patterns in the codebase."""
    _run_analysis(ctx, "service-collaboration")


@cli.command()
@click.option(
    "--patterns",
    "-p",
    multiple=True,
    type=click.Choice([s.name for s in SKILLS]),
    help="Specific skills to run (can be used multiple times; defaults to all)",
)
@click.option(
    "--chain",
    is_flag=True,
    default=False,
    help="Chain prompts together in a single Claude Code session",
)
@click.pass_context
def all(ctx, patterns: List[str], chain: bool):
    """Run all pattern detection analyses or specific ones."""
    # If no specific patterns specified, run all registered skills
    selected = list(patterns) if patterns else [s.name for s in SKILLS]

    # Show analysis overview
    console.print("\n[bold blue]Pattern Analysis Overview[/bold blue]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print(f"Skills: {', '.join(selected)}")
    console.print(f"Mode: {'Chained' if chain else 'Individual'}")

    if ctx.obj["execute"]:
        num_requests = 1 if chain else len(selected)
        pattern_desc = f"all patterns ({'chained' if chain else 'individual'})"

        if not _check_rate_limit_and_confirm(ctx, pattern_desc, num_requests):
            console.print("[yellow]Analysis cancelled.[/yellow]")
            return

        if not chain and len(selected) > 1:
            estimated_time = len(selected) * 30
            console.print(f"[cyan]Estimated time: ~{estimated_time} seconds[/cyan]")
            console.print("[yellow]This will make multiple separate requests to Claude Code.[/yellow]")

            if ctx.obj["confirm"] and not Confirm.ask("Proceed with multiple requests?", default=True):
                console.print("[yellow]Analysis cancelled.[/yellow]")
                return

    detector = _make_detector(ctx)

    if ctx.obj["execute"]:
        console.print("[yellow]Executing prompts via Claude Code...[/yellow]")
        if chain:
            console.print("[cyan]Using chained prompts in single session[/cyan]")
    elif ctx.obj["dry_run"]:
        console.print("[yellow]Dry run mode - showing prompts only[/yellow]")

    if chain and ctx.obj["execute"]:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Executing chained analysis...", total=None)
            result = detector.detect_all_patterns_chained(selected)
            progress.update(task, description="Chained analysis complete!")

        console.print("\n[bold green]Chained Analysis Results[/bold green]")
        console.print(result)
    else:
        results = {}

        if ctx.obj["execute"]:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                for i, skill_name in enumerate(selected):
                    skill = get_skill(skill_name)
                    task = progress.add_task(
                        f"Analyzing {skill.title}... ({i + 1}/{len(selected)})", total=None
                    )
                    results[skill_name] = detector._run_skill(skill)
                    progress.update(task, description=f"{skill.title} analysis complete!")
        else:
            for skill_name in selected:
                skill = get_skill(skill_name)
                console.print(f"\n[yellow]Analyzing {skill.title}...[/yellow]")
                results[skill_name] = detector._run_skill(skill)

        for skill_name, result in results.items():
            skill = get_skill(skill_name)
            console.print(f"\n[bold green]{skill.title} Results[/bold green]")
            console.print(result)


@cli.command()
@click.pass_context
def session(ctx):
    """Start an interactive Claude Code session for pattern analysis."""
    if not ctx.obj["execute"]:
        console.print("[red]Session command requires --execute flag[/red]")
        return
    
    console.print(f"\n[bold green]Starting Interactive Claude Code Session[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print(f"Model: {ctx.obj['model']}")
    console.print("\n[yellow]Tips:[/yellow]")
    console.print("• Use the prompts from --dry-run to guide your analysis")
    console.print("• Claude Code has access to your target directory")
    console.print("• You can ask for specific pattern analyses interactively")
    console.print("• Type 'exit' or press Ctrl+C to end the session")
    
    if ctx.obj["confirm"] and not Confirm.ask("Start interactive session?", default=True):
        console.print("[yellow]Session cancelled.[/yellow]")
        return
    
    try:
        # Change to target directory
        original_cwd = os.getcwd()
        os.chdir(ctx.obj["target_path"])
        
        # Start interactive Claude Code session
        console.print(f"\n[cyan]Starting Claude Code in {ctx.obj['target_path']}...[/cyan]")
        subprocess.run(["claude", "--model", ctx.obj["model"]], check=True)
        
        # Restore directory
        os.chdir(original_cwd)
        console.print("\n[green]Session ended.[/green]")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error starting Claude Code session: {e}[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted.[/yellow]")
    except FileNotFoundError:
        console.print("[red]Claude Code CLI not found. Please install Claude Code.[/red]")
    finally:
        try:
            os.chdir(original_cwd)
        except:
            pass

@cli.command()
@click.pass_context
def test_claude(ctx):
    """Test Claude Code connection and streaming."""
    console.print("\n[bold blue]Testing Claude Code Connection[/bold blue]")
    
    # Test basic Claude Code availability
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            console.print(f"[green]✓ Claude Code found: {result.stdout.strip()}[/green]")
        else:
            console.print(f"[red]✗ Claude Code version check failed: {result.stderr.strip()}[/red]")
            return
    except FileNotFoundError:
        console.print("[red]✗ Claude Code not found in PATH[/red]")
        return
    except subprocess.TimeoutExpired:
        console.print("[red]✗ Claude Code version check timed out[/red]")
        return
    
    # Test simple prompt
    console.print("\n[yellow]Testing simple prompt...[/yellow]")
    test_prompt = "Please respond with exactly: 'Claude Code test successful'"

    try:
        # Change to target directory
        original_cwd = os.getcwd()
        os.chdir(ctx.obj["target_path"])
        
        cmd = ["claude", "--model", ctx.obj["model"], "--print", test_prompt]
        
        if ctx.obj["verbose"]:
            console.print(f"[dim]Command: {' '.join(cmd)}[/dim]")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            console.print(f"[green]✓ Claude Code test successful[/green]")
            console.print(f"[dim]Response: {result.stdout.strip()}[/dim]")
        else:
            console.print(f"[red]✗ Claude Code test failed[/red]")
            console.print(f"[dim]Error: {result.stderr.strip()}[/dim]")
            
    except subprocess.TimeoutExpired:
        console.print("[red]✗ Claude Code test timed out[/red]")
        os.chdir(original_cwd)
    except Exception as e:
        console.print(f"[red]✗ Test failed: {str(e)}[/red]")
        os.chdir(original_cwd)

@cli.command()
@click.pass_context
def usage(ctx):
    """Show Claude Code API usage statistics."""
    rate_limiter = RateLimiter()
    stats = rate_limiter.get_usage_stats()
    
    console.print("\n[bold blue]Claude Code API Usage Statistics[/bold blue]")
    
    # Usage table
    table = Table(title="Current Usage")
    table.add_column("Period", style="cyan")
    table.add_column("Used", style="yellow")
    table.add_column("Limit", style="green")
    table.add_column("Remaining", style="magenta")
    table.add_column("Percentage", style="red")
    
    for period, data in [("Minute", stats['minute']), ("Hour", stats['hour']), ("Day", stats['day'])]:
        used = data['used']
        limit = data['limit']
        remaining = limit - used
        percentage = (used / limit) * 100 if limit > 0 else 0
        
        table.add_row(
            period,
            str(used),
            str(limit),
            str(remaining),
            f"{percentage:.1f}%"
        )
    
    console.print(table)
    
    # Check if any limits are close to being exceeded
    warnings = []
    if stats['minute']['used'] >= stats['minute']['limit'] * 0.8:
        warnings.append("minute")
    if stats['hour']['used'] >= stats['hour']['limit'] * 0.8:
        warnings.append("hour")
    if stats['day']['used'] >= stats['day']['limit'] * 0.8:
        warnings.append("day")
    
    if warnings:
        console.print(f"\n[yellow]Warning: Approaching rate limits for: {', '.join(warnings)}[/yellow]")
    
    # Show reset times if any limits are exceeded
    reset_times = rate_limiter.time_until_reset()
    if reset_times:
        console.print("\n[red]Rate limits will reset in:[/red]")
        for period, seconds in reset_times.items():
            if seconds > 0:
                minutes = int(seconds // 60)
                seconds = int(seconds % 60)
                console.print(f"• {period}: {minutes}m {seconds}s")
    
    console.print(f"\n[dim]Total requests tracked: {stats['total_requests']}[/dim]")

@cli.command()
@click.pass_context
def list_specs(ctx):
    """List available skills and their pattern specifications."""
    repo_root = ctx.obj["repo_root"]
    specs_dir = repo_root / "specs"

    # Skills table driven by the registry
    skills_table = Table(title="Registered Skills")
    skills_table.add_column("Name", style="cyan")
    skills_table.add_column("Title", style="yellow")
    skills_table.add_column("Description", style="green")
    skills_table.add_column("Prompt File", style="magenta")

    for skill in SKILLS:
        skills_table.add_row(skill.name, skill.title, skill.description, skill.prompt_file)

    console.print(skills_table)

    # Spec files on disk
    specs_table = Table(title="Available Spec Files")
    specs_table.add_column("Category", style="cyan")
    specs_table.add_column("File", style="magenta")

    for spec_file in sorted(specs_dir.glob("*.yaml")):
        specs_table.add_row("Main", spec_file.name)

    for subdir in sorted(p for p in specs_dir.iterdir() if p.is_dir()):
        for spec_file in sorted(subdir.glob("*.yaml")):
            specs_table.add_row(subdir.name.title(), spec_file.name)

    console.print(specs_table)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()