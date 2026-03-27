import os
import re
import anthropic

MODEL = "claude-sonnet-4-6"

_PLACEHOLDER = {
    "architecture_explanation": "ANTHROPIC_API_KEY not set — skipping AI insights.",
    "technical_risks": [],
    "refactor_recommendations": [],
    "maintainability_score": None,
}


def _build_prompt(context: dict) -> str:
    arch = context.get("arch_summary", {})
    cc   = context.get("complexity_report", {})
    deps = context.get("dependency_map", {})
    sec  = context.get("security_report", {})

    return f"""You are a senior software architect. Analyze this codebase profile and provide a structured report.

## Codebase Profile

**Architecture Layers:** {list(arch.get("layers", {}).keys())}
**Entry Points:** {arch.get("entry_points", [])}
**Circular Dependencies:** {deps.get("circular_deps", [])}
**Most Imported Modules:** {deps.get("most_imported", [])}
**High Complexity Functions:** {cc.get("high_complexity_funcs", [])}
**Security Issues:** {sec.get("issues", [])}
**Risky Imports:** {sec.get("risky_imports", [])}
**Hardcoded Secrets Found:** {len(sec.get("secret_patterns", []))}

## Required Output (use these exact headings)

## Architecture Explanation
[2-3 paragraphs describing the overall architecture and design patterns]

## Technical Risks
- [risk 1]
- [risk 2]

## Refactor Recommendations
- [recommendation 1]
- [recommendation 2]

## Maintainability Score
[integer 0-100]
"""


def _extract_section(text: str, header: str) -> str:
    match = re.search(rf"## {header}\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def _parse_response(text: str) -> dict:
    risks_raw    = _extract_section(text, "Technical Risks")
    refactor_raw = _extract_section(text, "Refactor Recommendations")
    score_raw    = _extract_section(text, "Maintainability Score")

    score = None
    m = re.search(r"\d+", score_raw)
    if m:
        score = min(100, max(0, int(m.group())))

    return {
        "architecture_explanation": _extract_section(text, "Architecture Explanation"),
        "technical_risks":          [l.lstrip("- ").strip() for l in risks_raw.splitlines() if l.strip()],
        "refactor_recommendations": [l.lstrip("- ").strip() for l in refactor_raw.splitlines() if l.strip()],
        "maintainability_score":    score,
    }


def generate_ai_insights(context: dict) -> dict:
    """Call Claude to synthesize codebase findings into actionable insights.

    Returns a placeholder dict gracefully if ANTHROPIC_API_KEY is not set.
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        return _PLACEHOLDER.copy()

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": _build_prompt(context)}],
    )
    return _parse_response(message.content[0].text)
