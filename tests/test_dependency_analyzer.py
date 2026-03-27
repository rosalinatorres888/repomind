from repomind.dependency_analyzer import analyze_dependencies

MOCK_FILE_METAS = [
    {"file": "app.py",    "imports": ["flask", "models"], "functions": [], "classes": [], "lines": 10},
    {"file": "models.py", "imports": ["sqlalchemy"],       "functions": [], "classes": [], "lines": 20},
    {"file": "utils.py",  "imports": ["app"],              "functions": [], "classes": [], "lines": 5},
]


def test_dependency_map_contains_nodes():
    result = analyze_dependencies(MOCK_FILE_METAS)
    assert "app.py" in result.graph.nodes


def test_dependency_map_detects_edges():
    result = analyze_dependencies(MOCK_FILE_METAS)
    assert result.graph.has_edge("app.py", "models.py")


def test_circular_dependency_detection():
    circular_metas = [
        {"file": "a.py", "imports": ["b"], "functions": [], "classes": [], "lines": 5},
        {"file": "b.py", "imports": ["a"], "functions": [], "classes": [], "lines": 5},
    ]
    result = analyze_dependencies(circular_metas)
    assert len(result.circular_deps) > 0


def test_adjacency_list_populated():
    result = analyze_dependencies(MOCK_FILE_METAS)
    assert isinstance(result.adjacency_list, dict)
    assert "app.py" in result.adjacency_list


def test_most_imported_is_populated():
    result = analyze_dependencies(MOCK_FILE_METAS)
    assert isinstance(result.most_imported, list)
