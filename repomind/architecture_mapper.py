from dataclasses import dataclass, field
from pathlib import Path

LAYER_PATTERNS = {
    "models":     {"models", "model", "entities", "domain", "schemas", "schema"},
    "services":   {"services", "service", "business", "logic", "use_cases"},
    "routes":     {"routes", "route", "views", "controllers", "endpoints", "api"},
    "utils":      {"utils", "util", "helpers", "helper", "common", "shared"},
    "config":     {"config", "settings", "configuration"},
    "tests":      {"tests", "test", "spec", "specs"},
    "middleware": {"middleware", "middlewares"},
}
ENTRY_POINT_NAMES = {"main.py", "app.py", "run.py", "server.py", "manage.py", "__main__.py"}

# Directed edges representing typical layer call flow for the Mermaid diagram
LAYER_FLOW = [
    ("main_core", "services"),
    ("main_core", "routes"),
    ("routes", "services"),
    ("services", "models"),
    ("models", "database"),
    ("services", "utils"),
    ("routes", "utils"),
]


@dataclass
class ArchSummary:
    layers: dict[str, list[str]] = field(default_factory=dict)
    entry_points: list[str] = field(default_factory=list)
    mermaid_diagram: str = ""


def _build_mermaid(detected_layers: set[str], has_entry_points: bool) -> str:
    lines = ["graph TD"]
    if has_entry_points:
        lines.append('    main_core["main / core"]')
    for layer in sorted(detected_layers):
        lines.append(f'    {layer}["{layer}"]')
    for src, dst in LAYER_FLOW:
        src_present = (src == "main_core" and has_entry_points) or src in detected_layers
        dst_present = dst in detected_layers or dst == "database"
        if src_present and dst_present:
            lines.append(f"    {src} --> {dst}")
    return "\n".join(lines)


def map_architecture(root: Path) -> ArchSummary:
    """Infer architectural layers from directory/file naming and produce a Mermaid diagram."""
    layers: dict[str, list[str]] = {k: [] for k in LAYER_PATTERNS}
    layers["other"] = []
    entry_points: list[str] = []

    for path in Path(root).rglob("*.py"):
        # Skip hidden dirs and pycache
        if any(p.startswith(".") or p == "__pycache__" for p in path.parts):
            continue
        filename = path.name
        if filename in ENTRY_POINT_NAMES:
            entry_points.append(filename)

        parts_lower = {p.lower() for p in path.parts}
        assigned = False
        for layer, keywords in LAYER_PATTERNS.items():
            if parts_lower & keywords:
                layers[layer].append(filename)
                assigned = True
                break
        if not assigned:
            layers["other"].append(filename)

    non_empty = {k for k, v in layers.items() if v and k != "other"}
    mermaid = _build_mermaid(non_empty, bool(entry_points))

    return ArchSummary(
        layers={k: v for k, v in layers.items() if v},
        entry_points=entry_points,
        mermaid_diagram=mermaid,
    )
