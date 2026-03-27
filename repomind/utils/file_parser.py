import ast
from pathlib import Path


def parse_file(file_path: Path) -> dict:
    """Parse a Python source file and extract structural metadata."""
    path = Path(file_path)
    source = ""
    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except SyntaxError:
        return {
            "file": path.name,
            "functions": [],
            "classes": [],
            "imports": [],
            "lines": len(source.splitlines()),
        }

    functions = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    classes = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])

    return {
        "file": path.name,
        "functions": functions,
        "classes": classes,
        "imports": list(set(imports)),
        "lines": len(source.splitlines()),
    }
