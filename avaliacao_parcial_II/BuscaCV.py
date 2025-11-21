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
    # SUCESSOR_T
    #--------------------------------------------------------------------------
    def sucessor_t(self, solucao_atual):
        solucao_nova = solucao_atual[:]
        i = random.randint(0, len(solucao_nova) - 1)
        j = random.randint(0, len(solucao_nova) - 1)
        solucao_nova[i], solucao_nova[j] = solucao_nova[j], solucao_nova[i]
        valor_novo = self.valor_inicial(solucao_nova)
        return solucao_nova, valor_novo
    #--------------------------------------------------------------------------
    # SUCESSORES
    #--------------------------------------------------------------------------
    def sucessores(self, solucao_atual, valor_atual):
        solucao_melhor = solucao_atual
        valor_melhor = valor_atual
        pos_fixa = random.randint(0, self.n - 1)

        for i in range(self.n):
            if i == pos_fixa:
                continue
            solucao_nova = solucao_atual[:]
            solucao_nova[i], solucao_nova[pos_fixa] = solucao_nova[pos_fixa], solucao_nova[i]
            valor_novo = self.valor_inicial(solucao_nova)

            if valor_novo < valor_melhor:
                solucao_melhor = solucao_nova
                valor_melhor = valor_novo
        return solucao_melhor, valor_melhor
    #--------------------------------------------------------------------------
    # SUBIDA DE ENCOSTA
    #--------------------------------------------------------------------------
    def subida_encosta(self, solucao_inicial, valor_inicial):
        solucao_atual = solucao_inicial
        valor_atual = valor_inicial
        while True:
            solucao_nova, valor_novo = self.sucessores(solucao_atual, valor_atual)
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
            solucao_nova, valor_novo = self.sucessores(solucao_atual, valor_atual)
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
            solucao_nova, valor_novo = self.sucessor_t(solucao_atual)
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