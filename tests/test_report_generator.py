import networkx as nx
from pathlib import Path
from repomind.report_generator import generate_report
from repomind.dependency_analyzer import DependencyMap
from repomind.architecture_mapper import ArchSummary
from repomind.complexity_analyzer import ComplexityReport
from repomind.security_scanner import SecurityReport


def _mock_results():
    return {
        "repo_meta": {
            "full_name": "rosalinatorres888/repomind",
            "stars": 10, "language": "Python",
            "description": "AI Codebase Intelligence System",
            "forks": 5, "open_issues": 2,
        },
        "dependency_map": DependencyMap(
            graph=nx.DiGraph(), adjacency_list={}, circular_deps=[], most_imported=[]
        ),
        "arch_summary": ArchSummary(
            layers={"models": ["user.py"], "services": ["auth.py"]},
            entry_points=["main.py"],
            mermaid_diagram="graph TD\n    main_core --> services\n    services --> models",
        ),
        "complexity_report": ComplexityReport(
            per_file={"app.py": 85.0},
            high_complexity_funcs=[],
            function_details=[],
        ),
        "security_report": SecurityReport(issues=[], risky_imports=[], secret_patterns=[]),
        "ai_insights": {
            "architecture_explanation": "Clean service-oriented architecture.",
            "technical_risks": ["Risk A: no input validation"],
            "refactor_recommendations": ["Extract helper functions"],
            "maintainability_score": 78,
        },
    }


def test_generate_report_creates_markdown_file(tmp_path):
    output = tmp_path / "analysis_report.md"
    generate_report(_mock_results(), output)
    assert output.exists()


def test_report_contains_all_six_sections(tmp_path):
    output = tmp_path / "analysis_report.md"
    generate_report(_mock_results(), output)
    content = output.read_text()
    for section in [
        "Repository Overview", "Architecture Diagram",
        "Dependency Analysis", "Complexity Metrics",
        "Security Risks", "Refactoring Suggestions",
    ]:
        assert section in content, f"Missing section: {section}"


def test_report_contains_repo_name(tmp_path):
    output = tmp_path / "analysis_report.md"
    generate_report(_mock_results(), output)
    assert "rosalinatorres888/repomind" in output.read_text()


def test_report_contains_mermaid_block(tmp_path):
    output = tmp_path / "analysis_report.md"
    generate_report(_mock_results(), output)
    content = output.read_text()
    assert "```mermaid" in content
    assert "graph TD" in content


def test_report_contains_ai_insights(tmp_path):
    output = tmp_path / "analysis_report.md"
    generate_report(_mock_results(), output)
    content = output.read_text()
    assert "Risk A" in content
    assert "Extract helper" in content
    assert "78" in content
