import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QSizePolicy

from BuscaNP import buscaNP
from leitor_grafo import carregar_grafo_txt

#bibliotecas para desenho do grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
 
 #armazena os nos
nos, grafo = carregar_grafo_txt("grafo.txt")


class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.busca = buscaNP()

        self.G = nx.Graph()
        for i, no in enumerate(nos):
            for viz in grafo[i]:
                self.G.add_edge(no,viz)

        self.setWindowTitle("Interface de busca")
        self.setGeometry(200, 200, 300, 200)
        #layout
        layout = QVBoxLayout()

        self.label = QLabel("Escolha uma opção", self)
        layout.addWidget(self.label)
        
        #combobox com as opções de busca
        self.combo = QComboBox(self)
        self.combo.addItems(["Amplitude", "Profundidade", "Profundidade Limitada", "Aprofundamento Iterativo", "Bidirecional"])
        layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.mudar_opcao)
   
        #combobox inicio e fim
        self.combo_inicio = QComboBox(self)
        self.combo_inicio.addItems(nos)
        self.combo_fim = QComboBox(self)
        self.combo_fim.addItems(nos)
        layout.addWidget(self.combo_inicio)
        layout.addWidget(self.combo_fim)

        #botao executar busca 
        self.botao_busca = QPushButton("Executar busca", self)
        layout.addWidget(self.botao_busca)
        self.botao_busca.clicked.connect(self.executar_busca)
        
        self.figure, self.ax = plt.subplots(figsize = (5,4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.desenha_grafo()

    def mudar_opcao(self,index):
        opcao = self.combo.itemText(index)
        self.label.setText(f"Vc escolheu: {opcao}")

    def desenha_grafo(self, caminho = None):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed = 42)

        nx.draw(self.G, pos, with_labels = True, node_color = "lightblue", node_size = 800, font_size = 10, ax = self.ax)
    

        if caminho: 
            edges = [(caminho[i], caminho[i+1]) for i in range(len(caminho) -1)]
            nx.draw_networkx_nodes(self.G, pos, nodelist = caminho, node_color = "red", ax = self.ax) 
            nx.draw_networkx_edges(self.G, pos, edgelist = edges, edge_color= "red", width = 2, ax = self.ax)
            
        self.canvas.draw()

    def executar_busca(self):
        opcao = self.combo.currentText()
        inicio = self.combo_inicio.currentText()
        fim = self.combo_fim.currentText()

        caminho = None 

        if opcao == "Amplitude":
            caminho = self.busca.amplitude(inicio, fim, nos, grafo)
        
        elif opcao == "Profundidade":
            caminho = self.busca.profundidade(inicio, fim, nos, grafo)

        elif opcao == "Profundidade Limitada":
            caminho = self.busca.prof_limitada(inicio, fim, nos, grafo, 4) 
            
        elif opcao == "Aprofundamento Iterativo":
            caminho = self.busca.aprof_iterativo(inicio, fim, nos, grafo, 5)
            
        elif opcao == "Bidirecional":
            caminho = self.busca.bidirecional(inicio, fim, nos, grafo)

        if caminho:
            custo = len(caminho) - 1 
            self.label.setText(f"{opcao}: {' -> '.join(caminho)} (Custo: {custo})")
            self.desenha_grafo(caminho)
        else:
            self.label.setText(f"{opcao}: Nenhum caminho encontrado.")
            self.desenha_grafo()
        
        # na tentativa de fazer uma busca de A a E utilizando profudidade o programa fecha e da erro 

app = QApplication(sys.argv)
janela = MinhaJanela()
janela.show()
sys.exit(app.exec_())
