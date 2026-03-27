from pathlib import Path
from repomind.repo_loader import filter_source_files


def test_filter_source_files_excludes_binaries(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "image.png").write_bytes(b"\x89PNG")
    result = filter_source_files(tmp_path)
    names = [p.name for p in result]
    assert "main.py" in names
    assert "image.png" not in names


def test_filter_source_files_excludes_large_files(tmp_path):
    big = tmp_path / "big.py"
    big.write_bytes(b"x" * (101 * 1024))
    small = tmp_path / "small.py"
    small.write_text("x = 1")
    result = filter_source_files(tmp_path)
    names = [p.name for p in result]
    assert "small.py" in names
    assert "big.py" not in names


def test_filter_source_files_excludes_hidden_dirs(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("data")
    (tmp_path / "app.py").write_text("pass")
    result = filter_source_files(tmp_path)
    assert all(".git" not in str(p) for p in result)
