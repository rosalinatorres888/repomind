"""
RepoMind Gradio Web UI
Run: python -m repomind.app
"""

import os
import tempfile
from pathlib import Path

import gradio as gr

from repomind.repo_loader import load_repository, load_local
from repomind.utils.file_parser import parse_file
from repomind.utils.github_client import get_repo_metadata
from repomind.dependency_analyzer import analyze_dependencies
from repomind.architecture_mapper import map_architecture
from repomind.complexity_analyzer import analyze_complexity
from repomind.security_scanner import scan_security
from repomind.ai_insights import generate_ai_insights
from repomind.report_generator import generate_report

# ── Mermaid renderer via CDN ──────────────────────────────────────────────────

def _mermaid_html(diagram: str) -> str:
    escaped = diagram.replace("`", "\\`")
    return f"""
<div id="mermaid-box" style="background:#1e1e2e;border-radius:10px;padding:1.2rem;">
  <div class="mermaid" style="color:#cdd6f4;">{diagram}</div>
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{startOnLoad:true, theme:'dark'}});
</script>
"""


# ── Pipeline ─────────────────────────────────────────────────────────────────

def run_analysis(repo_url: str, no_clone: bool, api_key: str):
    """Generator — yields (log, overview_md, arch_md, arch_html, dep_md, cc_md, sec_md, ai_md, dl_path)"""

    if api_key and api_key.strip():
        os.environ["ANTHROPIC_API_KEY"] = api_key.strip()

    blank = ("", "", "", "", "", "", "", "", None)

    if not repo_url.strip():
        yield ("⚠️ Please enter a GitHub URL or local path.", *blank[1:])
        return

    log = ""

    def step(msg):
        nonlocal log
        log += f"\n{msg}"
        return log

    try:
        yield (step("**[1/7]** Loading repository…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        if no_clone:
            file_paths = load_local(repo_url)
            repo_meta  = {"full_name": repo_url, "description": "", "language": "Local",
                          "stars": 0, "forks": 0, "open_issues": 0}
        else:
            file_paths = load_repository(repo_url)
            repo_meta  = get_repo_metadata(repo_url)
        yield (step(f"  ✅ {len(file_paths)} source files found"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[2/7]** Parsing source files…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        file_metas = [parse_file(p) for p in file_paths]
        yield (step(f"  ✅ {len(file_metas)} files parsed"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[3/7]** Analyzing dependencies…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        dep_map = analyze_dependencies(file_metas)
        yield (step(f"  ✅ {dep_map.graph.number_of_nodes()} modules, {len(dep_map.circular_deps)} cycles"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[4/7]** Mapping architecture…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        root         = file_paths[0].parent if file_paths else Path(".")
        arch_summary = map_architecture(root)
        yield (step(f"  ✅ Layers: {list(arch_summary.layers.keys())}"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[5/7]** Computing complexity…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        cc_report = analyze_complexity(file_paths)
        yield (step(f"  ✅ {len(cc_report.high_complexity_funcs)} high-complexity functions flagged"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[6/7]** Scanning security…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        sec_report = scan_security(file_paths)
        total_sec  = len(sec_report.issues) + len(sec_report.secret_patterns)
        yield (step(f"  ✅ {total_sec} issues, {len(sec_report.risky_imports)} risky imports"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        yield (step("**[7/7]** Generating AI insights…"), "", "", "<p>Waiting…</p>", "", "", "", "", None)
        ai = generate_ai_insights({
            "arch_summary":     {"layers": arch_summary.layers, "entry_points": arch_summary.entry_points},
            "complexity_report": {"high_complexity_funcs": cc_report.high_complexity_funcs},
            "dependency_map":   {"circular_deps": dep_map.circular_deps, "most_imported": dep_map.most_imported},
            "security_report":  {"issues": sec_report.issues, "risky_imports": sec_report.risky_imports,
                                 "secret_patterns": sec_report.secret_patterns},
        })
        yield (step("  ✅ AI insights ready"), "", "", "<p>Waiting…</p>", "", "", "", "", None)

        # ── Build tab content ─────────────────────────────────────────────────

        overview_md = f"""
## {repo_meta.get('full_name', repo_url)}
{repo_meta.get('description', '')}

| | |
|---|---|
| **Language** | {repo_meta.get('language', '—')} |
| **Stars** | ⭐ {repo_meta.get('stars', 0)} |
| **Forks** | 🍴 {repo_meta.get('forks', 0)} |
| **Open Issues** | 🐛 {repo_meta.get('open_issues', 0)} |
| **Files Analysed** | 📄 {len(file_paths)} |
"""

        layers_rows = "\n".join(
            f"| **{layer}** | {', '.join(f'`{f}`' for f in files[:5])}{'…' if len(files) > 5 else ''} |"
            for layer, files in arch_summary.layers.items()
        )
        arch_md = f"""
## Architecture Layers

| Layer | Files |
|-------|-------|
{layers_rows}

**Entry Points:** {', '.join(f'`{e}`' for e in arch_summary.entry_points) or '—'}
"""
        if ai.get("architecture_explanation"):
            arch_md += f"\n**AI Summary:** {ai['architecture_explanation']}"

        arch_html = _mermaid_html(arch_summary.mermaid_diagram)

        # Dependency tab
        dep_rows = "\n".join(
            f"| `{src}` | {', '.join(f'`{t}`' for t in targets) or '—'} |"
            for src, targets in list(dep_map.adjacency_list.items())[:20] if targets
        ) or "| — | No internal dependencies detected |"
        cycles_md = (
            "\n### ⚠️ Circular Dependencies\n" +
            "\n".join(f"- `{' → '.join(c)}`" for c in dep_map.circular_deps[:10])
        ) if dep_map.circular_deps else "\n✅ No circular dependencies."
        dep_md = f"""
## Dependency Graph
- **Modules:** {dep_map.graph.number_of_nodes()}
- **Edges:** {dep_map.graph.number_of_edges()}
{cycles_md}

### Adjacency List
| Module | Imports |
|--------|---------|
{dep_rows}
"""

        # Complexity tab
        if cc_report.high_complexity_funcs:
            cc_rows = "\n".join(
                f"| `{f['file']}` | `{f['function']}` | {f.get('cc_score','—')} "
                f"| {f.get('length','—')} | {f.get('nested_loops','—')} | {f.get('param_count','—')} |"
                for f in sorted(cc_report.high_complexity_funcs, key=lambda x: x.get("cc_score", 0), reverse=True)
            )
            cc_table = f"""
### 🚨 Flagged Functions
| File | Function | CC | Lines | Nested Loops | Params |
|------|----------|----|-------|--------------|--------|
{cc_rows}
"""
        else:
            cc_table = "\n✅ No high-complexity functions detected."

        mi_rows = "\n".join(
            f"| `{fname}` | {score} {'⚠️' if score < 20 else '✅' if score > 65 else ''} |"
            for fname, score in sorted(cc_report.per_file.items(), key=lambda x: x[1])[:20]
        )
        cc_md = f"""
## Complexity Metrics
- **Files analysed:** {len(cc_report.per_file)}
- **High-complexity functions:** {len(cc_report.high_complexity_funcs)}
{cc_table}

### Maintainability Index (MI)
> Higher = more maintainable. ⚠️ below 20, ✅ above 65.

| File | MI Score |
|------|----------|
{mi_rows}
"""

        # Security tab
        sec_parts = []
        if sec_report.risky_imports:
            sec_parts.append(f"### Risky Imports\n{', '.join(f'`{i}`' for i in sec_report.risky_imports)}")
        if sec_report.secret_patterns:
            rows = "\n".join(
                f"| `{s['file']}` | {s['line']} | 🔴 {s['severity']} | {s['description']} |"
                for s in sec_report.secret_patterns
            )
            sec_parts.append(f"### 🔴 Hardcoded Secrets\n| File | Line | Severity | Issue |\n|------|------|----------|-------|\n{rows}")
        if sec_report.issues:
            icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            rows = "\n".join(
                f"| `{i.get('file','—')}` | {i.get('line','—')} | {icons.get(i.get('severity','LOW'),'⚪')} {i.get('severity','—')} | {i.get('description','—')} |"
                for i in sec_report.issues[:30]
            )
            sec_parts.append(f"### Findings\n| File | Line | Severity | Description |\n|------|------|----------|-------------|\n{rows}")
        sec_md = "## Security Scan\n\n" + (
            "\n\n".join(sec_parts) if sec_parts else "✅ No security issues detected."
        )

        # AI Insights tab
        if ai.get("maintainability_score") is not None:
            score = ai["maintainability_score"]
            bar   = "█" * (score // 10) + "░" * (10 - score // 10)
            score_line = f"\n### Maintainability Score\n**`{score}/100`** `{bar}`"
        else:
            score_line = ""

        risks = "\n".join(f"- ⚠️ {r}" for r in ai.get("technical_risks", [])) or "_None identified._"
        recs  = "\n".join(f"- 💡 {r}" for r in ai.get("refactor_recommendations", [])) or "_None identified._"
        ai_md = f"""
## AI-Powered Insights
{score_line}

### Architecture Explanation
{ai.get('architecture_explanation', '_Set ANTHROPIC_API_KEY to enable._')}

### Technical Risks
{risks}

### Refactor Recommendations
{recs}
"""

        # Write report file for download
        tmp = Path(tempfile.mktemp(suffix=".md"))
        generate_report({
            "repo_meta": repo_meta, "dependency_map": dep_map,
            "arch_summary": arch_summary, "complexity_report": cc_report,
            "security_report": sec_report, "ai_insights": ai,
        }, tmp)

        yield (
            step("\n\n✅ **Analysis complete!**"),
            overview_md, arch_md, arch_html, dep_md, cc_md, sec_md, ai_md,
            str(tmp),
        )

    except Exception as exc:
        yield (step(f"\n❌ **Error:** {exc}"), "", "", "<p>Error.</p>", "", "", "", "", None)


# ── UI ────────────────────────────────────────────────────────────────────────

CSS = """
#logo { font-size: 1.6rem; font-weight: 700; color: #2563eb; }
.tab-nav button { font-size: 0.9rem; }
#run-btn { background: linear-gradient(135deg, #2563eb, #7c3aed) !important; color: #ffffff !important; font-weight: 700; }
#log-box { font-family: monospace; font-size: 0.82rem; background: #f1f5f9 !important; color: #1e293b !important; border-radius: 8px; padding: 0.8rem; border: 1px solid #e2e8f0; }
"""

with gr.Blocks(title="RepoMind") as demo:

    gr.HTML('<div id="logo">🔍 RepoMind — AI Codebase Intelligence</div>')
    gr.Markdown("Paste any public GitHub URL and get an instant architecture, dependency, complexity, security, and AI insights report.")

    with gr.Row():
        with gr.Column(scale=4):
            url_input = gr.Textbox(
                label="GitHub Repository URL",
                placeholder="https://github.com/owner/repo",
                autofocus=True,
            )
        with gr.Column(scale=1):
            no_clone_cb = gr.Checkbox(label="Local path (no clone)", value=False)

    with gr.Accordion("🔑 AI Insights (optional)", open=False):
        api_key_input = gr.Textbox(
            label="Anthropic API Key",
            type="password",
            placeholder="sk-ant-… (leave blank to skip AI insights)",
        )

    run_btn  = gr.Button("🚀 Analyze Repository", variant="primary", elem_id="run-btn")
    log_box  = gr.Markdown(value="_Progress will appear here…_", elem_id="log-box")

    with gr.Tabs():
        with gr.Tab("📋 Overview"):
            overview_out = gr.Markdown()
        with gr.Tab("🏗️ Architecture"):
            arch_text_out = gr.Markdown()
            arch_html_out = gr.HTML("<p style='color:#888'>Run analysis to see diagram.</p>")
        with gr.Tab("🔗 Dependencies"):
            dep_out = gr.Markdown()
        with gr.Tab("📊 Complexity"):
            cc_out = gr.Markdown()
        with gr.Tab("🔒 Security"):
            sec_out = gr.Markdown()
        with gr.Tab("🤖 AI Insights"):
            ai_out = gr.Markdown()

    dl_btn = gr.File(label="⬇️ Download analysis_report.md", visible=False)

    run_btn.click(
        fn=run_analysis,
        inputs=[url_input, no_clone_cb, api_key_input],
        outputs=[log_box, overview_out, arch_text_out, arch_html_out,
                 dep_out, cc_out, sec_out, ai_out, dl_btn],
    )

    # Show download button once a file path is set
    dl_btn.change(fn=lambda p: gr.File(visible=bool(p)), inputs=dl_btn, outputs=dl_btn)


if __name__ == "__main__":
    demo.launch(
        server_port=7860,
        theme=gr.themes.Default(primary_hue="blue"),
        css=CSS,
    )
