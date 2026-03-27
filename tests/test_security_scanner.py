from pathlib import Path
from repomind.security_scanner import scan_security

RISKY_CODE = """\
import subprocess
import pickle
eval("rm -rf /")
password = "s3cr3t123"
API_KEY = "sk-abc123xyz"
import requests
requests.get("http://api.example.com/data")
open("/etc/passwd", "w")
"""

SAFE_CODE = """\
def add(a, b):
    return a + b
"""


def test_detects_risky_imports(tmp_path):
    f = tmp_path / "risky.py"
    f.write_text(RISKY_CODE)
    result = scan_security([f])
    assert "subprocess" in result.risky_imports or "pickle" in result.risky_imports


def test_detects_hardcoded_secrets(tmp_path):
    f = tmp_path / "risky.py"
    f.write_text(RISKY_CODE)
    result = scan_security([f])
    assert len(result.secret_patterns) > 0


def test_detects_insecure_http(tmp_path):
    f = tmp_path / "risky.py"
    f.write_text(RISKY_CODE)
    result = scan_security([f])
    descriptions = [i.get("description", "") for i in result.issues]
    assert any("http://" in d or "nsecure" in d for d in descriptions)


def test_safe_file_has_no_secrets(tmp_path):
    f = tmp_path / "safe.py"
    f.write_text(SAFE_CODE)
    result = scan_security([f])
    assert len(result.secret_patterns) == 0


def test_findings_have_severity_field(tmp_path):
    f = tmp_path / "risky.py"
    f.write_text(RISKY_CODE)
    result = scan_security([f])
    for issue in result.issues:
        assert "severity" in issue
        assert issue["severity"] in ("HIGH", "MEDIUM", "LOW")
