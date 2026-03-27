from pathlib import Path
from repomind.architecture_mapper import map_architecture


def test_detects_service_layer(tmp_path):
    (tmp_path / "services").mkdir()
    (tmp_path / "services" / "user_service.py").write_text("")
    result = map_architecture(tmp_path)
    assert "services" in result.layers


def test_detects_data_layer(tmp_path):
    (tmp_path / "models").mkdir()
    (tmp_path / "models" / "user.py").write_text("")
    result = map_architecture(tmp_path)
    assert "models" in result.layers


def test_detects_utility_modules(tmp_path):
    (tmp_path / "utils").mkdir()
    (tmp_path / "utils" / "helpers.py").write_text("")
    result = map_architecture(tmp_path)
    assert "utils" in result.layers


def test_detects_core_entry_points(tmp_path):
    (tmp_path / "main.py").write_text("")
    result = map_architecture(tmp_path)
    assert "main.py" in result.entry_points


def test_mermaid_diagram_is_generated(tmp_path):
    (tmp_path / "main.py").write_text("")
    (tmp_path / "services").mkdir()
    (tmp_path / "services" / "auth.py").write_text("")
    result = map_architecture(tmp_path)
    assert "graph TD" in result.mermaid_diagram
    assert "-->" in result.mermaid_diagram
