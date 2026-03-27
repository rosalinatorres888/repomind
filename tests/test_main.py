from unittest.mock import patch, MagicMock
from pathlib import Path
from repomind.main import run_pipeline


def test_run_pipeline_calls_all_steps(tmp_path):
    fake_file = tmp_path / "app.py"
    fake_file.write_text("x = 1")

    with patch("repomind.main.load_repository", return_value=[fake_file]), \
         patch("repomind.main.get_repo_metadata", return_value={
             "full_name": "rosalinatorres888/repomind", "stars": 0,
             "language": "Python", "description": "", "forks": 0, "open_issues": 0,
         }), \
         patch("repomind.main.parse_file", return_value={
             "file": "app.py", "functions": [], "classes": [], "imports": [], "lines": 1,
         }), \
         patch("repomind.main.analyze_dependencies", return_value=MagicMock()) as mock_dep, \
         patch("repomind.main.map_architecture",     return_value=MagicMock()) as mock_arch, \
         patch("repomind.main.analyze_complexity",   return_value=MagicMock()) as mock_cc, \
         patch("repomind.main.scan_security",        return_value=MagicMock()) as mock_sec, \
         patch("repomind.main.generate_ai_insights", return_value={}) as mock_ai, \
         patch("repomind.main.generate_report")      as mock_report:

        run_pipeline("https://github.com/rosalinatorres888/repomind", tmp_path / "report.md")

    mock_dep.assert_called_once()
    mock_arch.assert_called_once()
    mock_cc.assert_called_once()
    mock_sec.assert_called_once()
    mock_ai.assert_called_once()
    mock_report.assert_called_once()


def test_run_pipeline_no_clone_uses_load_local(tmp_path):
    fake_file = tmp_path / "app.py"
    fake_file.write_text("x = 1")

    with patch("repomind.main.load_local", return_value=[fake_file]) as mock_local, \
         patch("repomind.main.parse_file", return_value={
             "file": "app.py", "functions": [], "classes": [], "imports": [], "lines": 1,
         }), \
         patch("repomind.main.analyze_dependencies", return_value=MagicMock()), \
         patch("repomind.main.map_architecture",     return_value=MagicMock()), \
         patch("repomind.main.analyze_complexity",   return_value=MagicMock()), \
         patch("repomind.main.scan_security",        return_value=MagicMock()), \
         patch("repomind.main.generate_ai_insights", return_value={}), \
         patch("repomind.main.generate_report"):

        run_pipeline(str(tmp_path), tmp_path / "report.md", no_clone=True)

    mock_local.assert_called_once()
