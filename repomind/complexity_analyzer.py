import ast
from dataclasses import dataclass, field
from pathlib import Path
from radon.complexity import cc_visit
from radon.metrics import mi_visit

CC_THRESHOLD = 10
LENGTH_THRESHOLD = 100


def _count_nested_loops(func_node: ast.FunctionDef) -> int:
    """Return the maximum loop nesting depth inside a function."""
    max_depth = [0]

    def walk(node: ast.AST, depth: int) -> None:
        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            max_depth[0] = max(max_depth[0], depth)
        for child in ast.iter_child_nodes(node):
            walk(child, depth)

    walk(func_node, 0)
    return max_depth[0]


def _count_params(func_node: ast.FunctionDef) -> int:
    args = func_node.args
    return (
        len(args.args)
        + len(args.posonlyargs)
        + len(args.kwonlyargs)
        + (1 if args.vararg else 0)
        + (1 if args.kwarg else 0)
    )


@dataclass
class ComplexityReport:
    per_file: dict[str, float] = field(default_factory=dict)
    high_complexity_funcs: list[dict] = field(default_factory=list)
    function_details: list[dict] = field(default_factory=list)


def analyze_complexity(file_paths: list[Path]) -> ComplexityReport:
    """Compute CC, MI, function length, loop nesting, and param counts per file."""
    per_file: dict[str, float] = {}
    high_complexity_funcs: list[dict] = []
    function_details: list[dict] = []

    for path in file_paths:
        if path.suffix != ".py":
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            per_file[path.name] = round(mi_visit(source, multi=True), 2)
            cc_map = {b.name: b.complexity for b in cc_visit(source)}

            tree = ast.parse(source)
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                end_line = getattr(node, "end_lineno", node.lineno)
                func_length = end_line - node.lineno + 1
                cc_score = cc_map.get(node.name, 1)
                detail = {
                    "file": path.name,
                    "function": node.name,
                    "line": node.lineno,
                    "cc_score": cc_score,
                    "length": func_length,
                    "nested_loops": _count_nested_loops(node),
                    "param_count": _count_params(node),
                }
                function_details.append(detail)

                if cc_score > CC_THRESHOLD:
                    high_complexity_funcs.append({**detail, "reason": "cyclomatic_complexity"})
                elif func_length > LENGTH_THRESHOLD:
                    high_complexity_funcs.append({**detail, "reason": "length"})

        except Exception:
            continue

    return ComplexityReport(
        per_file=per_file,
        high_complexity_funcs=high_complexity_funcs,
        function_details=function_details,
    )
