from dataclasses import dataclass, field
import networkx as nx


@dataclass
class DependencyMap:
    graph: nx.DiGraph
    adjacency_list: dict[str, list[str]]  # module → [imported internal modules]
    circular_deps: list[tuple]
    most_imported: list[str]              # highest in-degree (most depended upon)


def analyze_dependencies(file_metas: list[dict]) -> DependencyMap:
    """Build a directed dependency graph from parsed file metadata."""
    graph = nx.DiGraph()
    module_to_file = {m["file"].replace(".py", ""): m["file"] for m in file_metas}
    adjacency_list: dict[str, list[str]] = {}

    for meta in file_metas:
        graph.add_node(meta["file"])
        edges = []
        for imp in meta["imports"]:
            target = module_to_file.get(imp)
            if target and target != meta["file"]:
                graph.add_edge(meta["file"], target)
                edges.append(target)
        adjacency_list[meta["file"]] = edges

    circular = list(nx.simple_cycles(graph))
    in_degree = dict(graph.in_degree())
    most_imported = sorted(in_degree, key=lambda n: in_degree[n], reverse=True)[:10]

    return DependencyMap(
        graph=graph,
        adjacency_list=adjacency_list,
        circular_deps=circular,
        most_imported=most_imported,
    )
