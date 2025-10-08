import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox, QSpinBox, QFormLayout
from PyQt5.QtWidgets import QSizePolicy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from BuscaNP import buscaNP
from BuscaP import buscaP
from leitor_grafo import carregar_grafo_txt, grafoPonderado

try:
    nos, grafo = carregar_grafo_txt("grafo.txt")
    nosP, grafoP = grafoPonderado("grafo.txt")
except FileNotFoundError:
    print("Erro: O arquivo 'grafo.txt' não foi encontrado.")
    sys.exit(1) 


class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()
        self.busca = buscaNP()
        self.buscaP = buscaP()

        self.init_ui()
        self.desenha_grafo()

    def init_ui(self):
        """Inicializa e organiza todos os widgets da interface."""
        self.G = nx.Graph()
        for i, no in enumerate(nos):
            for viz in grafo[i]:
                self.G.add_edge(no, viz)

        self.setWindowTitle("Interface de Busca em Grafos")
        self.setGeometry(200, 200, 500, 600) 
        
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()

        self.label_resultado = QLabel("Escolha um algoritmo e os nós de início/fim.", self)
        main_layout.addWidget(self.label_resultado)
        
        self.combo_algoritmo = QComboBox(self)
        self.combo_algoritmo.addItems(["Amplitude", "Profundidade", "Profundidade Limitada", "Aprofundamento Iterativo", "Bidirecional", "Custo Uniforme"])
        
        self.combo_algoritmo.currentIndexChanged.connect(self.mostra_limite)
        form_layout.addRow("Algoritmo:", self.combo_algoritmo)
    
        self.input_limite = QSpinBox(self)
        self.input_limite.setMinimum(1)
        self.input_limite.setValue(3)
        self.label_limite = QLabel("Limite de Profundidade:", self)
        form_layout.addRow(self.label_limite, self.input_limite)
        
        self.combo_inicio = QComboBox(self)
        self.combo_inicio.addItems(nos)
        self.combo_fim = QComboBox(self)
        self.combo_fim.addItems(nos)
        form_layout.addRow("Nó de Início:", self.combo_inicio)
        form_layout.addRow("Nó de Fim:", self.combo_fim)

        main_layout.addLayout(form_layout)
        
        self.botao_busca = QPushButton("Executar Busca", self)
        self.botao_busca.clicked.connect(self.executar_busca)
        main_layout.addWidget(self.botao_busca)
        
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.mostra_limite() 

   
    def mostra_limite(self):
        """Mostra ou esconde o input de limite baseado no algoritmo selecionado."""
        algoritmo_selecionado = self.combo_algoritmo.currentText()
        is_visible = algoritmo_selecionado in ["Profundidade Limitada", "Aprofundamento Iterativo"]
        self.input_limite.setVisible(is_visible)
        self.label_limite.setVisible(is_visible)

    def desenha_grafo(self, caminho=None):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10, ax=self.ax)

        if caminho: 

            if len(caminho) > 1:
                edges = [(caminho[i], caminho[i+1]) for i in range(len(caminho) - 1)]
                nx.draw_networkx_edges(self.G, pos, edgelist=edges, edge_color="red", width=2, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos, nodelist=caminho, node_color="red", ax=self.ax) 
        self.canvas.draw()

    def executar_busca(self):
        opcao = self.combo_algoritmo.currentText()
        inicio = self.combo_inicio.currentText()
        fim = self.combo_fim.currentText()
        limite = self.input_limite.value() 

        caminho = None
        
        buscas = {
            "Amplitude": lambda: self.busca.amplitude(inicio, fim, nos, grafo),
            "Profundidade": lambda: self.busca.profundidade(inicio, fim, nos, grafo),
            "Profundidade Limitada": lambda: self.busca.prof_limitada(inicio, fim, nos, grafo, limite),
            "Aprofundamento Iterativo": lambda: self.busca.aprof_iterativo(inicio, fim, nos, grafo, limite),
            "Bidirecional": lambda: self.busca.bidirecional(inicio, fim, nos, grafo),
            "Custo Uniforme": lambda: self.buscaP.custo_uniforme(inicio, fim, nosP, grafoP)
        }
        
        if opcao in buscas:
            caminho = buscas[opcao]()

        if caminho:
            custo = len(caminho) - 1 
            self.label_resultado.setText(f"{opcao}: {' -> '.join(caminho)} (Custo: {custo})")
            self.desenha_grafo(caminho)
        else:
            self.label_resultado.setText(f"{opcao}: Nenhum caminho encontrado.")
            self.desenha_grafo()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())