from NodeCV import NodeCV
import random

class BuscaCV:
    def __init__(self, dist):
        self.dist = dist
        self.n = len(dist)

    #--------------------------------------------------------------------------
    # CUSTO INICIAL
    #--------------------------------------------------------------------------
    def custo(self, rota):
        soma = 0
        for i in range(len(rota) - 1):
            a = rota[i]
            b = rota[i+1]
            soma += self.dist[a][b]
        return soma
    #--------------------------------------------------------------------------
    # GERAR SOLUÇÃO INICIAL
    #--------------------------------------------------------------------------
    def gerar_solucao_inicial(self):
        rota = []
        for i in range(self.n):
                rota.append(i)
        random.shuffle(rota)
        # rota.append(rota[0]) # coloca o nó/valor inicial no final para facilitar o calculo do custo
        return rota
    #--------------------------------------------------------------------------
    # GERAR VALOR INICIAL
    #--------------------------------------------------------------------------
    def gerar_valor_inicial(self):
        solucao_inicial = self.gerar_solucao_inicial()
        custo_inicial = self.custo(solucao_inicial)
        valor_inicial = NodeCV(solucao_inicial, custo_inicial)
        return valor_inicial
    #--------------------------------------------------------------------------
    # TROCA DE POSIÇÃO COM O VIZINHO
    #--------------------------------------------------------------------------
    def troca_com_vizinho(self, rota):
        aux_rota = rota.copy()
        i = random.randint(0, self.n - 1)
        j = random.randint(0, self.n - 1)
        aux_rota[i], aux_rota[j] = aux_rota[j], aux_rota[i]
        return aux_rota
    #--------------------------------------------------------------------------
    # GERAR SUCESSORES
    #--------------------------------------------------------------------------
    def sucessores(self, solucao_atual):
        sucessor = self.troca_com_vizinho(solucao_atual)
        novo_valor = self.custo(solucao_atual)
        return sucessor, novo_valor
    #--------------------------------------------------------------------------
    # SUBIDADE DE ENCOSTA
    #--------------------------------------------------------------------------
    def subida_encosta(self, solucao_inicial, valor_inicial):
        solucao_atual = solucao_inicial
        valor_atual = valor_inicial
        while True:
            nova_solucao, novo_valor = self.sucessores(solucao_atual)
            if (novo_valor < valor_atual):
                solucao_atual = nova_solucao
                valor_atual = novo_valor
            else:
                return solucao_atual, valor_atual
    #-------------------------------------------------------------------------
    # SUBIDA DE ENCOSTA COM TENTATIVA
    #-------------------------------------------------------------------------
    def subida_encosta_tentativas(self, si, vi, tmax):
        sa = si
        va = vi
        t = 0
        while t < tmax:
            ns, nv = self.sucessores(sa)
            if (nv < va):
                sa = ns
                va = nv
                t = 0
            else:
                t += 1
        return sa, va