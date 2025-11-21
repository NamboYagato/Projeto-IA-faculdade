import random
import math

def gerar_coordenadas_aleatorias(n, seed=None):
    if seed is not None:
        random.seed(seed)
    
    coordenadas = {}
    for i in range(n):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        coordenadas[i] = (x, y)
    
    return coordenadas

def calcular_distancia(coords):
    nos = sorted(coords.keys())
    n = len(nos)

    distancia = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                distancia[i][j] = 0
            else:
                x1, y1 = coords[nos[i]]
                x2, y2 = coords[nos[j]]
                dx = x1 - x2
                dy = y1 - y2
                distancia[i][j] = math.sqrt(dx * dx + dy * dy)
    return nos, distancia

def gerar_grafo(n, seed=None):
    coords = gerar_coordenadas_aleatorias(n, seed=seed)
    nos, distancia = calcular_distancia(coords)
    return nos, coords, distancia

def exportar_grafo_txt(list_nos, coords, distancia):
    with open("avaliacao_parcial_II/grafo.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(f"NOS: {len(list_nos)}\n")
        arquivo.write("COORDENADAS:\n")
        for no in list_nos:
            x, y = coords[no]
            arquivo.write(f"{no} {x:.2f} {y:.2f}\n")
        
        arquivo.write("DISTANCIAS:\n")
        n = len(list_nos)
        for i in range(n):
            valores = []
            for j in range(n):
                valores.append(str(distancia[i][j]))
            linha_str = " ".join(valores)
            arquivo.write(linha_str + "\n")

def print_grafo(list_nos, coords, distancia, max_linhas=None):
    print("NÓS: ", list_nos)
    print("COORDENADAS: ")
    for no in list_nos:
        x, y = coords[no]
        print(f"{no}: ({x}, {y})")

    print("DISTÂNCIAS: ")
    n = len(list_nos)
    if max_linhas is None:
        limite = n
    else:
        limite = min(n, max_linhas)
    for i in range(limite):
        linha = []
        for j in range(n):
            linha.append(distancia[i][j])
        print(linha)