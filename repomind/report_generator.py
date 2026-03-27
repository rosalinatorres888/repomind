from pathlib import Path

from repomind.dependency_analyzer import DependencyMap
from repomind.architecture_mapper import ArchSummary
from repomind.complexity_analyzer import ComplexityReport
from repomind.security_scanner import SecurityReport


def _icon(severity: str) -> str:
    return {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(severity.upper(), "⚪")


def generate_report(results: dict, output_path: Path) -> None:
    """Assemble and write the Markdown intelligence report (analysis_report.md)."""
    meta: dict          = results["repo_meta"]
    dep: DependencyMap  = results["dependency_map"]
    arch: ArchSummary   = results["arch_summary"]
    cc: ComplexityReport = results["complexity_report"]
    sec: SecurityReport = results["security_report"]
    ai: dict            = results.get("ai_insights", {})

    lines: list[str] = []

    # ── 1. Repository Overview ────────────────────────────────────────────────
    lines += [
        f"# RepoMind Analysis: {meta.get('full_name', 'Unknown')}",
        "",
        "## 1. Repository Overview",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Repository** | {meta.get('full_name', '-')} |",
        f"| **Language**   | {meta.get('language', '-')} |",
        f"| **Stars**      | {meta.get('stars', 0)} |",
        f"| **Forks**      | {meta.get('forks', 0)} |",
        f"| **Open Issues**| {meta.get('open_issues', 0)} |",
        f"| **Description**| {meta.get('description', '-')} |",
        "",
    ]

    # ── 2. Architecture Diagram ───────────────────────────────────────────────
    lines += [
        "## 2. Architecture Diagram",
        "",
        "```mermaid",
        arch.mermaid_diagram,
        "```",
        "",
        "**Detected Layers:**",
        "",
    ]
    for layer, files in arch.layers.items():
        preview = ", ".join(files[:5])
        suffix  = "..." if len(files) > 5 else ""
        lines.append(f"- **{layer}**: {preview}{suffix}")
    if arch.entry_points:
        lines += ["", f"**Entry Points:** {', '.join(arch.entry_points)}"]
    lines.append("")

    if ai.get("architecture_explanation"):
        lines += ["**AI Architecture Summary:**", "", ai["architecture_explanation"], ""]

    # ── 3. Dependency Analysis ────────────────────────────────────────────────
    lines += [
        "## 3. Dependency Analysis",
        "",
        f"- **Total modules:** {dep.graph.number_of_nodes()}",
        f"- **Dependency edges:** {dep.graph.number_of_edges()}",
        f"- **Circular dependency cycles:** {len(dep.circular_deps)}",
        "",
    ]
    if dep.circular_deps:
        lines += ["### ⚠️ Circular Dependencies", ""]
        for cycle in dep.circular_deps[:10]:
            lines.append(f"- `{' → '.join(cycle)}`")
        lines.append("")

    if dep.most_imported:
        lines += [
            "### Most Imported Modules",
            "",
            "| Module | In-Degree |",
            "|--------|-----------|",
        ]
        for mod in dep.most_imported[:10]:
            lines.append(f"| `{mod}` | {dep.graph.in_degree(mod)} |")
        lines.append("")

    if dep.adjacency_list:
        lines += ["### Dependency Adjacency List", ""]
        for src, targets in list(dep.adjacency_list.items())[:15]:
            if targets:
                lines.append(f"- `{src}` → {', '.join(f'`{t}`' for t in targets)}")
        lines.append("")

    # ── 4. Complexity Metrics ─────────────────────────────────────────────────
    lines += [
        "## 4. Complexity Metrics",
        "",
        f"- **Files analyzed:** {len(cc.per_file)}",
        f"- **High-complexity functions flagged:** {len(cc.high_complexity_funcs)}",
        "",
    ]
    if cc.per_file:
        lines += [
            "### Maintainability Index (per file)",
            "",
            "| File | MI Score |",
            "|------|----------|",
        ]
        for fname, score in sorted(cc.per_file.items(), key=lambda x: x[1]):
            flag = " ⚠️" if score < 20 else ""
            lines.append(f"| `{fname}` | {score}{flag} |")
        lines.append("")

    if cc.high_complexity_funcs:
        lines += [
            "### Flagged Functions",
            "",
            "| File | Function | CC | Length | Nested Loops | Params | Reason |",
            "|------|----------|----|--------|--------------|--------|--------|",
        ]
        for f in sorted(cc.high_complexity_funcs, key=lambda x: x.get("cc_score", 0), reverse=True):
            lines.append(
                f"| `{f['file']}` | `{f['function']}` | {f.get('cc_score', '-')} "
                f"| {f.get('length', '-')} | {f.get('nested_loops', '-')} "
                f"| {f.get('param_count', '-')} | {f.get('reason', '-')} |"
            )
        lines.append("")

    # ── 5. Security Risks ─────────────────────────────────────────────────────
    lines += ["## 5. Security Risks", ""]

    if not any([sec.risky_imports, sec.secret_patterns, sec.issues]):
        lines += ["✅ No security issues detected.", ""]
    else:
        if sec.risky_imports:
            lines += [
                "### Risky Imports",
                "",
                f"{', '.join(f'`{i}`' for i in sec.risky_imports)}",
                "",
            ]
        if sec.secret_patterns:
            lines += [
                "### 🔴 Hardcoded Secrets",
                "",
                "| File | Line | Severity | Description |",
                "|------|------|----------|-------------|",
            ]
            for s in sec.secret_patterns:
                lines.append(
                    f"| `{s['file']}` | {s['line']} "
                    f"| {_icon(s['severity'])} {s['severity']} | {s['description']} |"
                )
            lines.append("")
        if sec.issues:
            lines += [
                "### Additional Findings",
                "",
                "| File | Line | Severity | Description |",
                "|------|------|----------|-------------|",
            ]
            for i in sec.issues[:30]:
                lines.append(
                    f"| `{i.get('file', '-')}` | {i.get('line', '-')} "
                    f"| {_icon(i.get('severity', 'LOW'))} {i.get('severity', '-')} "
                    f"| {i.get('description', '-')} |"
                )
            lines.append("")

    # ── 6. Refactoring Suggestions ────────────────────────────────────────────
    lines += ["## 6. Refactoring Suggestions", ""]

    if ai.get("technical_risks"):
        lines += ["### ⚠️ Technical Risks", ""]
        for risk in ai["technical_risks"]:
            lines.append(f"- {risk}")
        lines.append("")

    if ai.get("refactor_recommendations"):
        lines += ["### 💡 Recommendations", ""]
        for rec in ai["refactor_recommendations"]:
            lines.append(f"- {rec}")
        lines.append("")

    if ai.get("maintainability_score") is not None:
        score = ai["maintainability_score"]
        bar   = "█" * (score // 10) + "░" * (10 - score // 10)
        lines += [f"**Maintainability Score: `{score}/100`**  `{bar}`", ""]

    if not any([ai.get("technical_risks"), ai.get("refactor_recommendations")]):
        lines += ["_Set `ANTHROPIC_API_KEY` to enable AI-powered refactor suggestions._", ""]

    lines += ["---", "_Generated by [RepoMind](https://github.com/rosalinatorres888/repomind)_"]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → Report saved: {output_path}")
