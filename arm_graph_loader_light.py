import json
from pathlib import Path
from typing import List, Tuple, Union

def load_ids_and_neighbors(src: Union[str, Path, dict]) -> Tuple[List[str], List[List[str]]]:
    """Carrega (nos, grafo) de um JSON contendo somente 'id' e 'neighbors'."""
    if isinstance(src, (str, Path)):
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = src  # já é um dict

    nodes = data.get("nodes", [])
    if not nodes:
        raise ValueError("JSON inválido: chave 'nodes' vazia ou ausente.")

    nos = [n["id"] for n in nodes]
    idset = set(nos)
    idx = {nid: i for i, nid in enumerate(nos)}

    grafo = [[] for _ in nos]
    for n in nodes:
        nid = n["id"]
        neigh = n.get("neighbors", [])
        # filtra vizinhos desconhecidos (não listados em 'nos')
        grafo[idx[nid]] = [v for v in neigh if v in idset]

    return nos, grafo

def print_graph(nos: List[str], grafo: List[List[str]]):
    print("\nGRAFO (lista de adjacência):")
    for i, n in enumerate(nos):
        print(f"{n} -> {grafo[i]}")
