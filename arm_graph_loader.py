from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
import json
import csv
import pathlib

Number = Union[int, float]

@dataclass(frozen=True)
class Pose:
    """
    Metadados de um nó do grafo do braço robótico.
    position: (x, y, z)
    angles:   tuple com N ângulos (em graus ou radianos — você decide)
    rotation: rotação do atuador/ferramenta (ex.: yaw do punho)
    """
    position: Tuple[Number, Number, Number]
    angles: Tuple[Number, ...]
    rotation: Number


def _normalize_angles(text: str) -> Tuple[Number, ...]:
    """
    Converte uma string de ângulos em tuple de floats.
    Aceita separador ';' ou ',' (ex.: '0;45;90' ou '0,45,90').
    """
    if text is None:
        return tuple()
    text = text.strip()
    if not text:
        return tuple()
    # aceita ; ou ,
    chunks = text.replace(",", ";").split(";")
    return tuple(float(a.strip()) for a in chunks if a.strip())


def load_graph_from_json(src: Union[str, pathlib.Path, dict]):
    """
    Lê um grafo no formato JSON:

    {
      "nodes": [
        {
          "id": "A",
          "position": [0, 0, 0],
          "angles":   [0, 45, 90],
          "rotation": 0,
          "neighbors": ["B", "C"]
        },
        ...
      ]
    }

    Retorna: (nos, grafo, poses)
      - nos:   List[str]              -> ex.: ["A", "B", "C", ...]
      - grafo: List[List[str]]        -> adjacências por índice de 'nos'
      - poses: Dict[str, Pose]        -> metadados por id
    """
    if isinstance(src, (str, pathlib.Path)):
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = src  # já é o dict

    nodes = data.get("nodes", [])
    if not nodes:
        raise ValueError("JSON inválido: não há 'nodes'.")

    nos: List[str] = [n["id"] for n in nodes]
    id_to_idx = {nid: i for i, nid in enumerate(nos)}

    grafo: List[List[str]] = [[] for _ in nos]
    poses: Dict[str, Pose] = {}

    for n in nodes:
        nid = n["id"]
        pos = tuple(n.get("position", (0, 0, 0)))
        if len(pos) != 3:
            raise ValueError(f"Node {nid}: 'position' deve ter 3 valores (x,y,z).")
        ang = tuple(n.get("angles", ()))
        rot = float(n.get("rotation", 0.0))
        neigh = n.get("neighbors", [])

        poses[nid] = Pose(
            position=(float(pos[0]), float(pos[1]), float(pos[2])),
            angles=tuple(float(a) for a in ang),
            rotation=rot,
        )

        # Mantemos vizinhos como IDs (strings), como seus sucessores já esperam.
        grafo[id_to_idx[nid]] = [v for v in neigh if v in id_to_idx]

    return nos, grafo, poses


def load_graph_from_csv(csv_path: Union[str, pathlib.Path]):
    """
    Lê um grafo a partir de CSV com cabeçalho:
      id,x,y,z,rotation,angles,neighbors

    - angles:    '0;45;90' ou '0,45,90'
    - neighbors: 'B;C;D'   ou 'B,C,D'

    Retorna: (nos, grafo, poses) como em load_graph_from_json.
    """
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV vazio.")

    nos: List[str] = [r["id"].strip() for r in rows]
    id_to_idx = {nid: i for i, nid in enumerate(nos)}

    grafo: List[List[str]] = [[] for _ in nos]
    poses: Dict[str, Pose] = {}

    for r in rows:
        nid = r["id"].strip()
        x = float(r.get("x", 0))
        y = float(r.get("y", 0))
        z = float(r.get("z", 0))
        rotation = float(r.get("rotation", 0))
        angles = _normalize_angles(r.get("angles", ""))

        # vizinhos
        raw_nei = (r.get("neighbors") or "").strip()
        neigh = []
        if raw_nei:
            neigh = [n.strip() for n in raw_nei.replace(",", ";").split(";") if n.strip()]

        poses[nid] = Pose(position=(x, y, z), angles=angles, rotation=rotation)
        grafo[id_to_idx[nid]] = [v for v in neigh if v in id_to_idx]

    return nos, grafo, poses


def pretty_print_path(path: List[str], poses: Dict[str, Pose]) -> str:
    """
    Gera um texto bonitinho mostrando o caminho e os metadados de cada nó.
    """
    lines = []
    for step, nid in enumerate(path):
        pose = poses.get(nid)
        if pose:
            lines.append(
                f"{step:02d}. {nid} | pos={pose.position} | "
                f"angles={pose.angles} | rot={pose.rotation}"
            )
        else:
            lines.append(f"{step:02d}. {nid}")
    return "\n".join(lines)
