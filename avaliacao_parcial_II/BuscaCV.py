import math
import random

class BuscaCV:
    def __init__(self, dist):
        self.dist = dist
        self.n = len(dist)

    #--------------------------------------------------------------------------
    # GERAR SOLUÇÃO INICIAL
    #--------------------------------------------------------------------------
    def gerar_solucao_inicial(self):
        solucao = []
        for i in range(self.n):
            solucao.append(i)
        random.shuffle(solucao)
        return solucao
    #--------------------------------------------------------------------------
    # valor INICIAL
    #--------------------------------------------------------------------------
    def valor_inicial(self, solucao):
        soma = 0
        for i in range(len(solucao) - 1):
            soma += self.dist[solucao[i]][solucao[i+1]]
        soma += self.dist[solucao[-1]][solucao[0]] # soma o último valor que é igual ao primeiro
        return soma
    #--------------------------------------------------------------------------
    # TROCA DE POSIÇÃO COM O VIZINHO
    #--------------------------------------------------------------------------
    def vizinho(self, solucao_atual):
        nova_solucao = solucao_atual[:]
        i = random.sample(range(len(nova_solucao)), 2)
        j = random.sample(range(len(nova_solucao)), 2)
        nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
        return nova_solucao
    #--------------------------------------------------------------------------
    # SUCESSOR
    #--------------------------------------------------------------------------
    def sucessor(self, solucao_atual):
        solucao_nova = self.vizinho(solucao_atual)
        valor_novo = self.valor_inicial(solucao_nova)
        return solucao_nova, valor_novo
    #--------------------------------------------------------------------------
    # SUBIDA DE ENCOSTA
    #--------------------------------------------------------------------------
    def subida_encosta(self, solucao_inicial, valor_inicial):
        solucao_atual = solucao_inicial
        valor_atual = valor_inicial
        while True:
            solucao_nova, valor_novo = self.sucessor(solucao_atual)
            if valor_novo < valor_atual:
                solucao_atual = solucao_nova
                valor_atual = valor_novo
            else:
                return solucao_atual, valor_atual
    #--------------------------------------------------------------------------
    # SUBIDA DE ENCOSTA COM TENTATIVAS
    #--------------------------------------------------------------------------
    def subida_encosta_tentativas(self, solucao_inicial, valor_inicial, tmax):
        solucao_atual = solucao_inicial
        valor_atual = valor_inicial
        tentativas = 0
        while tentativas < tmax:
            solucao_nova, valor_novo = self.sucessor(solucao_atual)
            if valor_novo < valor_atual:
                solucao_atual = solucao_nova
                valor_atual = valor_novo
                tentativas = 0
            else:
                tentativas += 1
        return solucao_atual, valor_atual
    #--------------------------------------------------------------------------
    # TÊMPERA SIMULADA
    #--------------------------------------------------------------------------
    def tempera_simulada(self, solucao_inicial, valor_inicial, temp_inicial, temp_final, fator_resfr):
        solucao_atual = solucao_inicial
        valor_atual = valor_inicial
        solucao_final = solucao_inicial
        valor_final = valor_inicial
        temp = temp_inicial
        while temp >= temp_final:
            solucao_nova, valor_novo = self.sucessor(solucao_atual)
            delta = valor_novo - valor_atual
            if delta < 0:
                solucao_atual = solucao_nova
                valor_atual = valor_novo
            else:
                ale = random.uniform(0, 1)
                aux = math.exp(-delta / temp)
                if ale <= aux:
                    solucao_atual = solucao_nova
                    valor_atual = valor_novo
            if valor_atual < valor_final:
                solucao_final = solucao_atual
                valor_final = valor_atual
            temp = temp * fator_resfr
        return solucao_final, valor_final