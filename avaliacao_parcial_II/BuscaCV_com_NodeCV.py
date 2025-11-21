import math
from NodeCV import NodeCV
import random

from avaliacao_parcial_II import NodeCV

class BuscaCV:
    def __init__(self, dist):
        self.dist = dist
        self.n = len(dist)

    #--------------------------------------------------------------------------
    # GERAR SOLUÇÃO INICIAL para depois usar no node inicial
    #--------------------------------------------------------------------------
    def gerar_solucao_inicial(self):
        rota = []
        for i in range(self.n):
            rota.append(i)
        random.shuffle(rota)
        # rota.append(rota[0]) # coloca o nó/valor inicial no final para facilitar o calculo do custo
        return rota

    #--------------------------------------------------------------------------
    # CUSTO INICIAL para depois usar no node inicial
    #--------------------------------------------------------------------------
    def custo(self, rota):
        soma = 0
        for i in range(len(rota) - 1):
            a = rota[i]
            b = rota[i+1]
            soma += self.dist[a][b]
        soma += self.dist[rota[-1]][rota[0]] # soma a volta ao ponto inicial
        return soma
    #--------------------------------------------------------------------------
    # GERAR NODE INICIAL
    #--------------------------------------------------------------------------
    def gerar_node_inicial(self):
        solucao_inicial = self.gerar_solucao_inicial()
        custo_inicial = self.custo(solucao_inicial)
        node_inicial = NodeCV(solucao_inicial, custo_inicial)
        return node_inicial
    #--------------------------------------------------------------------------
    # GERAR NODE SUCESSOR
    #--------------------------------------------------------------------------
    def node_sucessor(self, node_atual):
        solucao_atual = node_atual.rota
        sucessor_novo = self.troca_com_vizinho(solucao_atual)
        valor_novo = self.custo(sucessor_novo)
        node_novo = NodeCV(sucessor_novo, valor_novo, node_atual)
        return node_novo
    #--------------------------------------------------------------------------
    # TROCA DE POSIÇÃO COM O VIZINHO
    #--------------------------------------------------------------------------
    def troca_com_vizinho(self, rota):
        nova_rota = rota.copy()
        i = random.sample(0, len(nova_rota) - 1)
        j = random.randint(0, len(nova_rota) - 1)
        nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
        return nova_rota
    #--------------------------------------------------------------------------
    # SUBIDADE DE ENCOSTA
    #--------------------------------------------------------------------------
    def subida_encosta(self, node_inicial):
        node_atual = node_inicial
        while True:
            node_novo = self.node_sucessor(node_atual)
            if (node_novo.custo < node_atual.custo):
                node_atual = node_novo
            else:
                return node_atual
    #-------------------------------------------------------------------------
    # SUBIDA DE ENCOSTA COM TENTATIVA
    #-------------------------------------------------------------------------
    def subida_encosta_tentativas(self, node_inicial, tmax):
        node_atual = node_inicial
        tentativas = 0
        while tentativas < tmax:
            node_novo = self.node_sucessor(node_atual)
            if (node_novo.custo < node_atual.custo):
                node_atual = node_novo
                tentativas = 0
            else:
                tentativas += 1
        return node_atual
    #--------------------------------------------------------------------------
    # TÊMPERA SIMULADA
    #--------------------------------------------------------------------------
    def tempera_simulada(self, node_inicial, temp_inicial, temp_final, fator_resfr):
        node_atual = node_inicial
        temp = temp_inicial
        while temp > temp_final:
            node_novo = self.node_sucessor(node_atual)
            delta = node_novo.custo - node_atual.custo
            if delta < 0:
                node_atual = node_novo
            else:
                ale = random.uniform(0, 1)
                aux = math.exp(-delta / temp)
                if ale < aux:
                    node_atual = node_novo
            temp = temp * fator_resfr
        return node_atual