"""Main CLI module for ai-code-pattern-discovery."""

import os
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table

from .pattern_detector import PatternDetector


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
@click.pass_context
def cli(ctx, target_path: Path):
    """AI Code Pattern Discovery CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["target_path"] = target_path.resolve()
    ctx.obj["repo_root"] = get_repo_root()


@cli.command()
@click.pass_context
def algorithms(ctx):
    """Detect algorithms and data structures in the codebase."""
    detector = PatternDetector(ctx.obj["repo_root"], ctx.obj["target_path"])
    results = detector.detect_algorithms()
    
    console.print("\n[bold green]Algorithms & Data Structures Analysis[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print("\n" + results)


@cli.command()
@click.pass_context
def design_patterns(ctx):
    """Detect design patterns in the codebase."""
    detector = PatternDetector(ctx.obj["repo_root"], ctx.obj["target_path"])
    results = detector.detect_design_patterns()
    
    console.print("\n[bold green]Design Patterns Analysis[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print("\n" + results)


@cli.command()
@click.pass_context
def architectural(ctx):
    """Detect architectural patterns in the codebase."""
    detector = PatternDetector(ctx.obj["repo_root"], ctx.obj["target_path"])
    results = detector.detect_architectural_patterns()
    
    console.print("\n[bold green]Architectural Patterns Analysis[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print("\n" + results)


@cli.command()
@click.pass_context
def cloud(ctx):
    """Detect cloud architecture patterns in the codebase."""
    detector = PatternDetector(ctx.obj["repo_root"], ctx.obj["target_path"])
    results = detector.detect_cloud_patterns()
    
    console.print("\n[bold green]Cloud Architecture Patterns Analysis[/bold green]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print("\n" + results)


@cli.command()
@click.option(
    "--patterns",
    "-p",
    multiple=True,
    type=click.Choice(["algorithms", "design_patterns", "architectural", "cloud"]),
    help="Specific patterns to analyze (can be used multiple times)",
)
@click.pass_context
def all(ctx, patterns: List[str]):
    """Run all pattern detection analyses or specific ones."""
    detector = PatternDetector(ctx.obj["repo_root"], ctx.obj["target_path"])
    
    # If no specific patterns specified, run all
    if not patterns:
        patterns = ["algorithms", "design_patterns", "architectural", "cloud"]
    
    console.print(f"\n[bold blue]Running Pattern Analysis[/bold blue]")
    console.print(f"Target: {ctx.obj['target_path']}")
    console.print(f"Patterns: {', '.join(patterns)}")
    
    results = {}
    
    for pattern in patterns:
        console.print(f"\n[yellow]Analyzing {pattern}...[/yellow]")
        
        if pattern == "algorithms":
            results[pattern] = detector.detect_algorithms()
        elif pattern == "design_patterns":
            results[pattern] = detector.detect_design_patterns()
        elif pattern == "architectural":
            results[pattern] = detector.detect_architectural_patterns()
        elif pattern == "cloud":
            results[pattern] = detector.detect_cloud_patterns()
    
    # Display results
    for pattern, result in results.items():
        console.print(f"\n[bold green]{pattern.replace('_', ' ').title()} Results[/bold green]")
        console.print(result)


@cli.command()
@click.pass_context
def list_specs(ctx):
    """List available pattern specifications."""
    repo_root = ctx.obj["repo_root"]
    specs_dir = repo_root / "specs"
    
    table = Table(title="Available Pattern Specifications")
    table.add_column("Category", style="cyan")
    table.add_column("File", style="magenta")
    table.add_column("Description", style="green")
    
    # Main specs
    main_specs = [
        ("algorithms-data-structures-spec.yaml", "Algorithms & Data Structures"),
        ("design-patterns-spec.yaml", "Design Patterns"),
        ("cloud-architecture-spec.yaml", "Cloud Architecture"),
    ]
    
    for spec_file, description in main_specs:
        if (specs_dir / spec_file).exists():
            table.add_row("Main", spec_file, description)
    
    # Subdirectory specs
    for subdir in specs_dir.iterdir():
        if subdir.is_dir():
            for spec_file in subdir.glob("*.yaml"):
                table.add_row(subdir.name.title(), spec_file.name, f"{subdir.name.title()} Pattern")
    
    console.print(table)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()