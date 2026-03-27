import argparse
import sys
from pathlib import Path

from repomind.repo_loader import load_repository, load_local
from repomind.utils.file_parser import parse_file
from repomind.utils.github_client import get_repo_metadata
from repomind.dependency_analyzer import analyze_dependencies
from repomind.architecture_mapper import map_architecture
from repomind.complexity_analyzer import analyze_complexity
from repomind.security_scanner import scan_security
from repomind.ai_insights import generate_ai_insights
from repomind.report_generator import generate_report

TOTAL_STEPS = 7


def _step(n: int, msg: str) -> None:
    print(f"[{n}/{TOTAL_STEPS}] {msg}")


def run_pipeline(repo_url: str, output_path: Path, no_clone: bool = False) -> None:
    """Execute the full 7-step RepoMind analysis pipeline."""
    _step(1, f"Loading repository: {repo_url}")
    if no_clone:
        file_paths = load_local(repo_url)
        repo_meta = {
            "full_name": str(repo_url), "description": "",
            "language": "Unknown", "stars": 0, "forks": 0, "open_issues": 0,
        }
    else:
        file_paths = load_repository(repo_url)
        repo_meta = get_repo_metadata(repo_url)
    print(f"       {len(file_paths)} source files found")

    _step(2, "Parsing source files...")
    file_metas = [parse_file(p) for p in file_paths]

    _step(3, "Analyzing dependencies...")
    dependency_map = analyze_dependencies(file_metas)
    print(f"       {dependency_map.graph.number_of_nodes()} modules, "
          f"{len(dependency_map.circular_deps)} circular dependency cycles")

    _step(4, "Mapping architecture...")
    root = file_paths[0].parent if file_paths else Path(".")
    arch_summary = map_architecture(root)
    print(f"       Layers detected: {list(arch_summary.layers.keys())}")

    _step(5, "Computing complexity metrics...")
    complexity_report = analyze_complexity(file_paths)
    print(f"       {len(complexity_report.high_complexity_funcs)} high-complexity functions flagged")

    _step(6, "Scanning for security risks...")
    security_report = scan_security(file_paths)
    total_issues = len(security_report.issues) + len(security_report.secret_patterns)
    print(f"       {total_issues} issues found, "
          f"{len(security_report.risky_imports)} risky imports")

    _step(7, "Generating AI insights...")
    ai_insights = generate_ai_insights({
        "arch_summary": {
            "layers": arch_summary.layers,
            "entry_points": arch_summary.entry_points,
        },
        "complexity_report": {
            "high_complexity_funcs": complexity_report.high_complexity_funcs,
        },
        "dependency_map": {
            "circular_deps": dependency_map.circular_deps,
            "most_imported": dependency_map.most_imported,
        },
        "security_report": {
            "issues": security_report.issues,
            "risky_imports": security_report.risky_imports,
            "secret_patterns": security_report.secret_patterns,
        },
    })

    generate_report(
        {
            "repo_meta": repo_meta,
            "dependency_map": dependency_map,
            "arch_summary": arch_summary,
            "complexity_report": complexity_report,
            "security_report": security_report,
            "ai_insights": ai_insights,
        },
        output_path,
    )
    print(f"\n✅ Done! Open {output_path} to view your intelligence report.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="repomind",
        description="RepoMind — AI Codebase Intelligence System",
    )
    parser.add_argument("repo_url", help="GitHub repository URL or local path")
    parser.add_argument(
        "--output", default="analysis_report.md",
        help="Output file path (default: analysis_report.md)",
    )
    parser.add_argument(
        "--no-clone", action="store_true",
        help="Analyze a local directory without cloning",
    )
    args = parser.parse_args()
    run_pipeline(args.repo_url, Path(args.output), no_clone=args.no_clone)


if __name__ == "__main__":
    main()
