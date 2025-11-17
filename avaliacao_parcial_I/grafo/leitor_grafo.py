import re

def carregar_dados_completos(nome_arquivo):

    linhas_buffer = []
    nos_set = set()
    coordenadas = {}

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue
            
            linhas_buffer.append(linha_limpa) 
            
            partes = linha_limpa.split(':')
            info_no = partes[0].strip().split()
            no_principal = info_no[0]
            
            nos_set.add(no_principal)
            if len(info_no) == 3:
                coordenadas[no_principal] = (float(info_no[1]), float(info_no[2]))

    nos = sorted(list(nos_set))
    node_to_index = {node: i for i, node in enumerate(nos)}

 
    grafo = [[] for _ in nos]
    grafoP = [[] for _ in nos]

  
    corta_peso_regex = re.compile(r'\d+$')
    vizinho_peso_regex = re.compile(r"([a-zA-Z]+)(\d+)$")

    for linha in linhas_buffer:
        partes = linha.split(':')
        no_principal = partes[0].strip().split()[0]
        idx = node_to_index[no_principal]

        if len(partes) > 1:
            vizinhos_str = partes[1].strip().split()
            for vizinho_com_peso in vizinhos_str:

                # Grafo Não Ponderado
                vizinho_np = corta_peso_regex.sub("", vizinho_com_peso)
                grafo[idx].append(vizinho_np)

                # Grafo Ponderado
                match = vizinho_peso_regex.match(vizinho_com_peso)
                if match:
                    vizinho, peso_str = match.groups()
                    grafoP[idx].append((vizinho, int(peso_str)))
    

    return nos, grafo, grafoP, coordenadas