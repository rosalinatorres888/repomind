import ast
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

RISKY_IMPORTS = {"subprocess", "pickle", "marshal", "ctypes", "shelve"}

# (pattern, severity, description)
SECRET_PATTERNS = [
    (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']',            "HIGH",   "Hardcoded password"),
    (r'(?i)(api_key|apikey|secret|token)\s*=\s*["\'][^"\']{8,}["\']',   "HIGH",   "Hardcoded API key/secret"),
    (r'(?i)(aws_access_key_id|aws_secret)\s*=\s*["\'][^"\']{10,}["\']', "HIGH",   "AWS credential"),
    (r'sk-[a-zA-Z0-9]{20,}',                                              "HIGH",   "OpenAI-style API key"),
]

_INSECURE_HTTP = re.compile(r'["\']http://[^"\']+["\']')
_OPEN_WRITE    = re.compile(r'\bopen\s*\([^)]+,\s*["\']w["\']')


@dataclass
class SecurityReport:
    issues: list[dict] = field(default_factory=list)
    risky_imports: list[str] = field(default_factory=list)
    secret_patterns: list[dict] = field(default_factory=list)


def _scan_secrets(source: str, filename: str) -> list[dict]:
    found = []
    for pattern, severity, description in SECRET_PATTERNS:
        for match in re.finditer(pattern, source):
            line_num = source[: match.start()].count("\n") + 1
            found.append({"file": filename, "line": line_num,
                          "severity": severity, "description": description})
    return found


def _scan_risky_imports(source: str) -> list[str]:
    found = []
    for risky in RISKY_IMPORTS:
        if re.search(rf"\b(import {risky}|from {risky})\b", source):
            found.append(risky)
    return found


def _scan_patterns(source: str, filename: str) -> list[dict]:
    issues = []
    # Insecure HTTP calls
    for match in _INSECURE_HTTP.finditer(source):
        line = source[: match.start()].count("\n") + 1
        issues.append({"file": filename, "line": line, "severity": "MEDIUM",
                       "description": f"Insecure HTTP call: {match.group()[:60]}"})
    # open() in write mode
    for match in _OPEN_WRITE.finditer(source):
        line = source[: match.start()].count("\n") + 1
        issues.append({"file": filename, "line": line, "severity": "LOW",
                       "description": "open() in write mode — verify file permissions"})
    # eval / exec via AST (catches dynamic names too)
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = (func.id if isinstance(func, ast.Name) else
                        func.attr if isinstance(func, ast.Attribute) else None)
                if name in ("eval", "exec"):
                    issues.append({"file": filename, "line": node.lineno,
                                   "severity": "HIGH",
                                   "description": f"Unsafe use of {name}()"})
    except SyntaxError:
        pass
    return issues


def _run_bandit(file_paths: list[Path]) -> list[dict]:
    if not file_paths:
        return []
    try:
        proc = subprocess.run(
            ["bandit", "-f", "json", "-q", *[str(p) for p in file_paths]],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(proc.stdout)
        return [
            {"file": r["filename"], "line": r["line_number"],
             "severity": r["issue_severity"], "description": r["issue_text"]}
            for r in data.get("results", [])
        ]
    except Exception:
        return []


def scan_security(file_paths: list[Path]) -> SecurityReport:
    """Scan for hardcoded secrets, eval/exec, insecure HTTP, open() perms, and run bandit."""
    all_issues: list[dict] = []
    all_risky: list[str] = []
    all_secrets: list[dict] = []

    py_files = [p for p in file_paths if p.suffix == ".py"]

    for path in py_files:
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            all_secrets.extend(_scan_secrets(source, path.name))
            all_risky.extend(_scan_risky_imports(source))
            all_issues.extend(_scan_patterns(source, path.name))
        except Exception:
            continue

    all_issues.extend(_run_bandit(py_files))

    return SecurityReport(
        issues=all_issues,
        risky_imports=list(set(all_risky)),
        secret_patterns=all_secrets,
    )
