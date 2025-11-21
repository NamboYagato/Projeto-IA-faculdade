from NovoGrafo import gerar_grafo, exportar_grafo_txt, print_grafo

def main():
    lista_nos, coords, dist = gerar_grafo(6)
    print("===print do grafo===")
    print_grafo(lista_nos, coords, dist)
    exportar_grafo_txt(lista_nos, coords, dist)
    
main()