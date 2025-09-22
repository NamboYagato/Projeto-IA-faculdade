from collections import deque
from Node import Node

class buscaNP(object):
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
    # SUCESSORES PARA GRID (LISTA DE ADJACENCIAS)
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                f.append(suc)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                f.append(suc)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                f.append(suc)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                f.append(suc)
        
        return f
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
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibirCaminho1(self,encontro,visitado1, visitado2):
        # nó do lado do início
        encontro1 = visitado1[encontro]  
        # nó do lado do objetivo
        encontro2 = visitado2[encontro]
    
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
    
        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))
    
        return caminho1 + caminho2
    #--------------------------------------------------------------------------
    # BUSCA EM AMPLITUDE
    #--------------------------------------------------------------------------
    #def amplitude(self,inicio,fim,nx,ny,mapa):  # grid
    def amplitude(self,inicio,fim,nos,grafo):   # grafo
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        #t_inicio = tuple(inicio)   # grid
        #t_fim = tuple(fim)         # grid
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        #raiz = Node(None,t_inicio,0,None,None)  # grid
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {inicio: raiz}           # grafo
        #visitado = {tuple(inicio): raiz}    # grid
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.popleft()
    
            # Gera sucessores a partir do grafo
            ind = nos.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind, grafo, 1) # grafo
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos:
                #t_novo = tuple(novo)       # grid
                #if t_novo not in visitado: # grid
                if novo not in visitado:   # grafo
                    #filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    #visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if novo == fim:        # grafo
                    #if t_novo == t_fim:    # grid
                        return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE
    #--------------------------------------------------------------------------
    def profundidade(self, inicio, fim, nos, grafo):
    #def profundidade(self,inicio,fim,nx,ny,mapa):
        # Finaliza se início for igual a objetivo
        if inicio == fim:
            return [inicio]
        
        # GRID: transforma em tupla
        #t_inicio = tuple(inicio)   # grid
        #t_fim = tuple(fim)         # grid
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,inicio,0,None,None)    # grafo
        #raiz = Node(None,t_inicio,0,None,None)  # grid
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {inicio: raiz}           # grafo
        #visitado = {tuple(inicio): raiz}    # grid
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.pop()
    
            # Gera sucessores a partir do grafo
            ind = nos.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind,grafo,1) # grafo
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos:
                #t_novo = tuple(novo)       # grid
                #if t_novo not in visitado: # grid
                if novo not in visitado:   # grafo
                    #filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    #visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if novo == fim:        # grafo
                    #if t_novo == t_fim:    # grid
                        return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE LIMITADA
    #--------------------------------------------------------------------------
    def prof_limitada(self,inicio,fim,nos,grafo,lim):
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - PILHA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        pilha.append(Node(None,inicio,0,None,None))
    
        # Marca início como visitado
        visitado = {inicio: 0}
    
        while pilha:
            # Remove o último da PILHA
            atual = pilha.pop()
            
            if atual.v1<lim:
                # Obtem o índice do estado atual na lista 'nos'
                ind = nos.index(atual.estado)
        
                # Gera sucessores a partir do grafo
                filhos = self.sucessores_grafo(ind, grafo,-1)
        
                for novo in filhos:
                    if novo not in visitado:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        pilha.append(filho)
                        visitado[novo] = filho.v1
        
                        # Verifica se encontrou o objetivo
                        if novo == fim:
                            return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM APROFUNDAMENTO ITERATIVO
    #--------------------------------------------------------------------------
    def aprof_iterativo(self,inicio,fim,nos,grafo,lim_max):
        if inicio == fim:
            return [inicio]
        
        for lim in range(1,lim_max+1):
            # Lista para árvore de busca - PILHA
            pilha = deque()
        
            # Inclui início como nó raíz da árvore de busca
            pilha.append(Node(None,inicio,0,None,None))
        
            # Marca início como visitado
            visitado = {inicio: 0}
        
            while pilha:
                # Remove o último da PILHA
                atual = pilha.pop()
                
                if atual.v1<lim:
                    # Obtem o índice do estado atual na lista 'nos'
                    ind = nos.index(atual.estado)
            
                    # Gera sucessores a partir do grafo
                    filhos = self.sucessores_grafo(ind, grafo,-1)
            
                    for novo in filhos:
                        if novo not in visitado:
                            filho = Node(atual,novo,atual.v1 + 1,None,None)
                            pilha.append(filho)
                            visitado[novo] = filho.v1
            
                            # Verifica se encontrou o objetivo
                            if novo == fim:
                                return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA BIDIRECIONAL
    #--------------------------------------------------------------------------
    def bidirecional(self, inicio, fim, nos, grafo):
        if inicio == fim:
            return [inicio]

        # Lista para árvore de busca a partir da origem - FILA
        fila1 = deque()
        
        # Lista para árvore de busca a partir do destino - FILA
        fila2 = deque()  
        
        # Inclui início e fim como nó raíz da árvore de busca
        fila1.append(Node(None,inicio,0,None,None))
        fila2.append(Node(None,fim,0,None,None))
    
        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {inicio: fila1[0]}
        visitado2 = {fim:    fila2[0]}
        
        nivel = 0
    
        while fila1 and fila2:
            
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(fila1)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila1.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado1:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado1[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado2:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila1.append(filho)
            
            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(fila2)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila2.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila2.append(filho)
        return None
