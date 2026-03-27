import os
from unittest.mock import patch, MagicMock
from repomind.ai_insights import generate_ai_insights

MOCK_CONTEXT = {
    "arch_summary": {"layers": {"services": ["auth.py"]}, "entry_points": ["main.py"]},
    "complexity_report": {"high_complexity_funcs": [{"function": "process", "cc_score": 15}]},
    "dependency_map": {"circular_deps": [], "most_imported": ["utils"]},
    "security_report": {
        "issues": [{"severity": "HIGH", "description": "eval() usage"}],
        "risky_imports": ["subprocess"],
        "secret_patterns": [],
    },
}

MOCK_AI_RESPONSE = """\
## Architecture Explanation
The codebase follows a service-oriented structure with clear separation of concerns.

## Technical Risks
- eval() usage poses injection risk.
- subprocess import may allow shell injection.

## Refactor Recommendations
- Extract process() into smaller focused functions.
- Add input validation before eval calls.

## Maintainability Score
72
"""


def test_generate_ai_insights_returns_dict():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=MOCK_AI_RESPONSE)]
    )
    with patch("repomind.ai_insights.anthropic.Anthropic", return_value=mock_client):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            result = generate_ai_insights(MOCK_CONTEXT)
    assert "architecture_explanation" in result
    assert "technical_risks" in result
    assert "refactor_recommendations" in result
    assert "maintainability_score" in result


def test_generate_ai_insights_parses_score():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=MOCK_AI_RESPONSE)]
    )
    with patch("repomind.ai_insights.anthropic.Anthropic", return_value=mock_client):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            result = generate_ai_insights(MOCK_CONTEXT)
    assert result["maintainability_score"] == 72


def test_generate_ai_insights_no_api_key_returns_placeholder():
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        result = generate_ai_insights(MOCK_CONTEXT)
    assert "ANTHROPIC_API_KEY" in result["architecture_explanation"]
    assert result["maintainability_score"] is None
