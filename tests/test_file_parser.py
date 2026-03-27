import textwrap
from pathlib import Path
from repomind.utils.file_parser import parse_file

SAMPLE_CODE = textwrap.dedent("""
    import os
    from pathlib import Path

    class MyClass:
        def method_one(self):
            pass

    def standalone_func(x, y):
        return x + y
""")


def test_parse_file_extracts_functions(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text(SAMPLE_CODE)
    result = parse_file(f)
    assert "standalone_func" in result["functions"]
    assert "method_one" in result["functions"]


def test_parse_file_extracts_classes(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text(SAMPLE_CODE)
    result = parse_file(f)
    assert "MyClass" in result["classes"]


def test_parse_file_extracts_imports(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text(SAMPLE_CODE)
    result = parse_file(f)
    assert "os" in result["imports"]
    assert "pathlib" in result["imports"]


def test_parse_file_counts_lines(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text(SAMPLE_CODE)
    result = parse_file(f)
    assert result["lines"] > 0
    assert result["file"] == "sample.py"


def test_parse_file_returns_empty_on_syntax_error(tmp_path):
    f = tmp_path / "bad.py"
    f.write_text("def (broken:")
    result = parse_file(f)
    assert result["functions"] == []
    assert result["classes"] == []
