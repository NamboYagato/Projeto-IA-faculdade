import re
from collections import defaultdict

def grafoPonderado(nome_arquivo):
    nos = []
    grafo = []

    padrao = re.compile(r'^(.+?)(\d+(?:\.\d+)?)$')

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split()
            if not partes:
                continue
            no = partes[0].upper()
            nos.append(no)

            adj = []
            for i in partes[1:]:
                m = padrao.match(i)
                if not m:
                    raise ValueError(f"Nó inválido '{i}' na linha: {linha.strip()} (esperado ex.: B5)")
                destino = m.group(1).upper()
                pesoString = m.group(2)
                peso = int(pesoString)
                adj.append((destino, peso))
            grafo.append(adj)

    return nos, grafo

def carregar_grafo_txt(nome_arquivo):
    nos = []
    grafo = []

    corta_peso = re.compile(r'\d+(?:\.\d+)?$')

    with open(nome_arquivo, "r") as f:
        for linha in f:
            partes = linha.strip().split()
            if not partes:
                continue
            no = partes[0].upper()
            vizinhos = [corta_peso.sub("", i).upper() for i in partes[1:]]

            nos.append(no)
            grafo.append(vizinhos)

    return nos, grafo