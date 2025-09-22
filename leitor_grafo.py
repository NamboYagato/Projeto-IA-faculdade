def carregar_grafo_txt(nome_arquivo):
    nos = []
    grafo = []

    with open(nome_arquivo, "r") as f:
        for linha in f:
            partes = linha.strip().split()
            if not partes:
                continue
            no = partes[0].upper()
            vizinhos = [viz.upper() for viz in partes[1:]]

            nos.append(no)
            grafo.append(vizinhos)

    return [n.upper() for n in nos], [[v.upper() for v in viz] for viz in grafo]