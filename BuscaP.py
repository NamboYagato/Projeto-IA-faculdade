from collections import deque
from NodeP import NodeP

class buscaP(object):
#--------------------------------------------------------------------------
# SUCESSORES PARA GRAFO
#--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    
#--------------------------------------------------------------------------
# SUCESSORES PARA GRID
#--------------------------------------------------------------------------
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                custo = 5
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 7
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 29
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)        
        return f
#--------------------------------------------------------------------------    
# INSERE NA LISTA MANTENDO-A ORDENADA
#--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
#--------------------------------------------------------------------------    
# GERA H DE FORMA ALEATÓRIA
#--------------------------------------------------------------------------    
    def heuristica_grafo(self,nos,destino,n):
        i_destino = nos.index(destino)
        i_n = nos.index(n)
        h = [
             [89,97,59,100,53,71,66,72,91,70,74,58,62,88,70,77,67,50,93,70],
             [70,0,80,70,62,80,97,87,100,64,57,67,72,96,72,86,84,76,54,98],
             [78,92,0,66,50,99,71,99,56,77,52,55,64,96,96,97,72,86,91,95],
             [69,70,99,0,68,82,85,53,60,88,64,79,78,75,96,58,92,58,73,72],
             [83,64,83,100,0,84,99,82,86,98,56,84,83,70,76,57,51,62,95,91],
             [88,96,73,77,83,0,87,95,50,50,78,59,52,97,88,95,84,99,77,90],
             [56,52,73,64,97,70,0,58,69,58,95,94,89,72,53,70,96,89,75,83],
             [51,64,93,67,67,63,88,0,93,52,97,52,100,71,87,78,55,99,69,90],
             [84,75,90,89,62,95,91,81,0,88,60,55,71,70,82,55,90,85,63,100],
             [82,72,69,92,52,98,61,62,100,0,87,68,63,63,73,99,75,93,91,85],
             [94,55,100,57,77,59,62,92,86,98,0,85,67,75,87,75,84,64,79,74],
             [85,69,84,84,55,65,56,92,54,99,98,0,99,90,68,77,86,59,75,98],
             [92,76,77,85,51,76,88,55,75,73,60,92,0,85,80,93,82,96,66,98],
             [92,95,65,57,90,96,73,94,96,66,75,82,50,0,87,52,70,100,61,73],
             [88,95,76,56,72,86,59,100,85,88,58,100,98,74,0,77,91,75,79,89],
             [95,74,96,62,95,93,66,98,70,66,61,59,70,82,92,0,77,67,90,52],
             [63,68,83,99,61,96,81,59,83,76,86,77,94,51,74,100,0,100,85,65],
             [54,60,65,52,68,51,91,66,89,93,87,86,75,63,64,67,82,0,60,55],
             [51,93,100,96,57,83,50,55,59,79,81,71,76,56,93,70,93,78,0,76],
             [83,73,53,51,95,93,93,59,90,78,70,55,71,52,84,92,91,78,88,0]
             ]
        return h[i_destino][i_n]
# -----------------------------------------------------------------------------
# CUSTO UNIFORME
# -----------------------------------------------------------------------------
    #def custo_uniforme(self,inicio,fim,mapa,nx,ny):
    def custo_uniforme(self, inicio, fim, nos, grafo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        #t_inicio = tuple(inicio)   # grid
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
        #raiz = NodeP(None, t_inicio,0, None, None, 0)  # grid
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        #visitado = {tuple(inicio): raiz}    # grid
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos: # grafo
            #for novo in filhos: # grid
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 
    
                # Não visitado ou custo melhor
                #t_novo = tuple(novo[0])       # grid
                #if (t_novo not in visitado) or (v2<visitado[t_novo].v2): # grid
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    #filho = NodeP(atual,t_novo, v1, None, None, v2) # grid
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    #visitado[t_novo] = filho # grid
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, nos, grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Se já registramos um nó melhor para este estado, este está obsoleto
            #if visitado.get(atual.estado) is not atual:
            #    continue
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grafo(nos,novo[0],fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None  
# -----------------------------------------------------------------------------
# A ESTRELA
# -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,nos,grafo,):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grafo(nos,novo[0],fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# AI ESTRELA
# -----------------------------------------------------------------------------       
    def aia_estrela(self,inicio,fim,nos,grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        limite = self.heuristica_grafo(nos,inicio,fim) 
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        # Busca iterativa
        while True:
            lim_acima = []
            
            raiz = NodeP(None, inicio, 0, None, None, 0)       
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {inicio: raiz}

            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
                
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2, limite
                
                # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
                
                for novo in filhos:
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grafo(nos,novo[0],fim) 
                    
                    # Verifica se está dentro do limite
                    if v1<=limite:
                        # Não visitado ou custo melhor
                        if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                            filho = NodeP(atual, novo[0], v1, None, None, v2)
                            visitado[novo[0]] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(v1)
            
            limite = sum(lim_acima)/len(lim_acima)
            lista.clear()
            visitado.clear()
            filhos.clear()
                        
        return None
