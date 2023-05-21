import json
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv


def create_graph(nodes: dict) -> nx.Graph:
    graph = nx.Graph()
    for node, edges in nodes.items():
        for edge, weight in edges.items():
            graph.add_edge(node, edge, weight=weight)
    return graph


def find_shortest_path(graph: nx.Graph, start: str, end: str) -> list[str]:
    return nx.shortest_path(graph, start, end)


def get_map(filepath: str) -> dict:
    with open(filepath) as file:
        return json.load(file)


def draw_graph(graph: nx.Graph) -> None:
    # graph = nx.petersen_graph()
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        font_weight="bold"
    )
    edge_weight = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weight)
    plt.show()


def draw_pygraph(nodes) -> None:
    graph = pgv.AGraph(nodes, name="wales_map")
    graph.graph_attr["label"] = "Wales to Wrexham"
    graph.node_attr["shape"] = "circle"
    graph.node_attr["fontsize"] = "5"
    graph.node_attr["fixedsize"] = "true"
    graph.node_attr["style"] = "filled"
    graph.graph_attr["outputorder"] = "edgesfirst"
    graph.graph_attr["ratio"] = "1.0"
    graph.edge_attr["color"] = "#1100FF"
    graph.edge_attr["style"] = "setlinewidth(2)"
    graph.layout(prog="dot")
    graph.layout(prog="neato", args="-n2")
    graph.draw("file.png")



if __name__ == '__main__':
    wales_graph = create_graph(
        get_map("resources/wales.json")
    )
    route = find_shortest_path(wales_graph, "Wrexham", "Cardiff")
    print(route)
    draw_graph(wales_graph)

    wales_graph = draw_pygraph(
        get_map("resources/wales.json")
    )

