from BuscaNP import buscaNP
from arm_graph_loader_light import load_ids_and_neighbors, print_graph

if __name__ == "__main__":
    nos, grafo = load_ids_and_neighbors("lista_adj.json")

    inicio, fim = "A", "H"  # IDs dos nós
    busca = buscaNP()
    caminho = busca.amplitude(inicio, fim, nos, grafo)

    if caminho is None:
        print("Nenhum caminho encontrado.")
    else:
        print_graph(nos, grafo)
        print("Caminho (BFS):", caminho)
