import networkx as nx

def build_graph(contract_id, filename, clauses):
    """
    Ek graph banata hai jisme Contract, uski Clauses,
    aur unke beech relationships hote hain.
    """
    G = nx.DiGraph()

    contract_node = f"Contract_{contract_id}"
    G.add_node(contract_node, type="Contract", label=filename)

    for clause in clauses:
        clause_node = clause["clause_type"]
        G.add_node(clause_node, type="Clause")
        G.add_edge(contract_node, clause_node, relation="HAS_CLAUSE")

    return G


def graph_to_json(G):
    """
    Graph ko JSON format mein convert karta hai taake
    API se bheja ja sake aur frontend pe dikhaya ja sake.
    """
    nodes = []
    for node, data in G.nodes(data=True):
        nodes.append({
            "id": node,
            "type": data.get("type", "Unknown"),
            "label": data.get("label", node)
        })

    edges = []
    for source, target, data in G.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "relation": data.get("relation", "RELATED_TO")
        })

    return {"nodes": nodes, "edges": edges}