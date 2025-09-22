from BuscaNP import buscaNP
from leitor_grafo import carregar_grafo_txt

nos, grafo = carregar_grafo_txt("grafo.txt")

busca = buscaNP()

inicio = "A".upper()
fim = "K".upper()
limite = 4
caminhoAmp = busca.amplitude(inicio, fim, nos, grafo)
caminhoPro = busca.profundidade(inicio, fim, nos, grafo)
caminhoProLim = busca.prof_limitada(inicio, fim, nos, grafo, limite)

print("            Amplitude: ", caminhoAmp)
print("         Profundidade: ", caminhoPro)
print("Profundidade Limitada: ", caminhoProLim)

