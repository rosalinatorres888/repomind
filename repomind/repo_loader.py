import tempfile
from pathlib import Path
from git import Repo

SOURCE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go",
    ".rb", ".rs", ".cpp", ".c", ".h", ".cs", ".php",
    ".swift", ".kt", ".scala", ".r", ".sh",
    ".yaml", ".yml", ".toml", ".json", ".md",
}
MAX_FILE_SIZE_BYTES = 100 * 1024  # 100 KB
EXCLUDED_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build",
}


def filter_source_files(root: Path) -> list[Path]:
    """Walk a directory and return filtered source files."""
    results = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            continue
        results.append(path)
    return results


def load_repository(repo_url: str, clone_dir: Path | None = None) -> list[Path]:
    """Clone a GitHub repository (shallow) and return filtered source file paths."""
    target = clone_dir or Path(tempfile.mkdtemp(prefix="repomind_"))
    Repo.clone_from(repo_url, target, depth=1)
    return filter_source_files(target)


def load_local(path: str | Path) -> list[Path]:
    """Load source files from a local directory without cloning."""
    return filter_source_files(Path(path))
