import textwrap
from pathlib import Path
from repomind.complexity_analyzer import analyze_complexity

SIMPLE_CODE = "def foo(x):\n    return x\n"

LONG_CODE = "\n".join(["def long_func():"] + ["    x = 1" for _ in range(105)])

NESTED_CODE = textwrap.dedent("""
    def nested(items):
        for i in items:
            for j in items:
                while j > 0:
                    j -= 1
""")


def test_simple_function_not_flagged(tmp_path):
    f = tmp_path / "simple.py"
    f.write_text(SIMPLE_CODE)
    result = analyze_complexity([f])
    assert len(result.high_complexity_funcs) == 0


def test_long_function_is_flagged(tmp_path):
    f = tmp_path / "long.py"
    f.write_text(LONG_CODE)
    result = analyze_complexity([f])
    assert any(r["reason"] == "length" for r in result.high_complexity_funcs)


def test_per_file_scores_populated(tmp_path):
    f = tmp_path / "simple.py"
    f.write_text(SIMPLE_CODE)
    result = analyze_complexity([f])
    assert "simple.py" in result.per_file


def test_function_details_captures_param_count(tmp_path):
    code = "def greet(name, greeting='Hello', punctuation='!'):\n    return f'{greeting} {name}{punctuation}'\n"
    f = tmp_path / "greet.py"
    f.write_text(code)
    result = analyze_complexity([f])
    assert len(result.function_details) > 0
    detail = result.function_details[0]
    assert detail["param_count"] == 3


def test_nested_loops_counted(tmp_path):
    f = tmp_path / "nested.py"
    f.write_text(NESTED_CODE)
    result = analyze_complexity([f])
    assert result.function_details[0]["nested_loops"] >= 2
