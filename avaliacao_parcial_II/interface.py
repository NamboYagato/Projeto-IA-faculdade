import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox, QSpinBox, QFormLayout, QDoubleSpinBox
from PyQt5.QtWidgets import QSizePolicy
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from BuscaCV_com_NodeCV import BuscaCVNodeCV as BuscaCVN
from BuscaCV import BuscaCV
from ag_pcv import AlgoritmoGenetico
from NovoGrafo import gerar_grafo

class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()
        self.nos = None
        self.coords = None
        self.dist = None
        self.busca_local = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # CAMPO TAMANHO DO PROBLEMA
        self.spin_tamanho = QSpinBox(self)
        self.spin_tamanho.setMinimum(3)
        self.spin_tamanho.setMaximum(30)
        self.spin_tamanho.setValue(30)
        form_layout.addRow("Tamanho do problema:", self.spin_tamanho)

        # COMBOBOX PARA A ESCOLHA DO MÉTODO
        self.combo_metodo = QComboBox(self)
        self.combo_metodo.addItems([
            "SUBIDA DE ENCOSTA",
            "SUBIDA DE ENCOSTA COM TENTATIVAS",
            "TÊMPERA SIMULADA",
            "ALGORITMO GENÉTICO"
        ])
        form_layout.addRow("Algoritmo:", self.combo_metodo)

        self.label_tentativas = QLabel("Tentativas:", self)
        self.spin_tentativas = QDoubleSpinBox(self)
        self.spin_tentativas.setMinimum(1)
        self.spin_tentativas.setMaximum(10000)
        self.spin_tentativas.setValue(30)
        form_layout.addRow(self.label_tentativas, self.spin_tentativas)

        self.label_tempI = QLabel("Temperatura Inicial:", self)
        self.spin_tempI = QDoubleSpinBox(self)
        self.spin_tempI.setMaximum(10000)
        self.spin_tempI.setValue(400)

        self.label_tempF = QLabel("Temperatura Final:", self)
        self.spin_tempF = QDoubleSpinBox(self)
        self.spin_tempF.setMaximum(10000)
        self.spin_tempF.setValue(0.1)

        self.label_fatorResf = QLabel("Fator de Resfriamento:", self)
        self.spin_fatorResf = QDoubleSpinBox(self)
        self.spin_fatorResf.setMinimum(0)
        self.spin_fatorResf.setMaximum(1)
        self.spin_fatorResf.setValue(0.8)

        form_layout.addRow(self.label_tempI, self.spin_tempI)
        form_layout.addRow(self.label_tempF, self.spin_tempF)
        form_layout.addRow(self.label_fatorResf, self.spin_fatorResf)

        self.label_tentativas.hide()
        self.label_tempI.hide()
        self.label_tempF.hide()
        self.label_fatorResf.hide()
        self.spin_tentativas.hide()
        self.spin_tempI.hide()
        self.spin_tempF.hide()
        self.spin_fatorResf.hide()

        self.combo_metodo.currentIndexChanged.connect(self.on_metodo_changed)

        # BOTÃO PARA EXECUTAR O ALGORITMO
        self.botao_executar = QPushButton("EXECUTAR", self)
        self.botao_executar.clicked.connect(self.on_executar)

        # ÁREA DE TEXTO PARA OS RESULTADOS
        self.label_resultado = QLabel("", self)
        self.label_resultado.setWordWrap(True)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.botao_executar)
        main_layout.addWidget(self.label_resultado)

        self.setLayout(main_layout)
        self.setWindowTitle("Avaliação Parcial II - IA / Problema do Caixeiro Viajante - Algoritmos de Busca Local e Genéticos")

    def on_metodo_changed(self, index):
        metodo = self.combo_metodo.currentText()
        self.label_tentativas.hide()
        self.label_tempI.hide()
        self.label_tempF.hide()
        self.label_fatorResf.hide()
        self.spin_tentativas.hide()
        self.spin_tempI.hide()
        self.spin_tempF.hide()
        self.spin_fatorResf.hide()

        if metodo.startswith("SUBIDA DE ENCOSTA COM TENTATIVAS"):
            self.label_tentativas.show()
            self.spin_tentativas.show()
        elif metodo.startswith("TÊMPERA SIMULADA"):
            self.label_tempI.show()
            self.label_tempF.show()
            self.label_fatorResf.show()
            self.spin_tempI.show()
            self.spin_tempF.show()
            self.spin_fatorResf.show()

    def on_executar(self):
        n = self.spin_tamanho.value() # lé o campo que informa o tamanho do problema
        
        self.nos, self.coords, self.dist = gerar_grafo(n) # gera o grafo/matriz com o tamanho do problema
        
        self.busca_local = BuscaCVN(self.dist) # cria o objeto de busca local com o matriz gerada
        
        node_inicial = self.busca_local.gerar_node_inicial() # gera a node inicial para os métodos de busca local / o node carrega a solução, o valor/custo e o pai/anterior da solução
        si = node_inicial.rota
        vi = node_inicial.custo

        metodo = self.combo_metodo.currentText()
        if metodo.startswith("SUBIDA DE ENCOSTA"):
            node_final = self.busca_local.subida_encosta(node_inicial)
            sf = node_final.rota
            vf = node_final.custo
        elif metodo.startswith("SUBIDA DE ENCOSTA COM TENTATIVAS"):
            tmax = self.spin_tentativas.value()
            node_final = self.busca_local.subida_encosta_tentativas(node_inicial, tmax)
            sf = node_final.rota
            vf = node_final.custo
        elif metodo.startswith("TÊMPERA SIMULADA"):
            TI = 400
            TF = 0.1
            FR = 0.8
            node_final = self.busca_local.tempera_simulada(node_inicial, TI, TF, FR)
            sf = node_final.rota
            vf = node_final.custo
        elif metodo.startswith("ALGORITMO GENÉTICO"):
            # ainda precisa mudar para funcionar com NovoGrafo
            pass
        else:
            return
        
        ganho = 100 * abs(vi - vf) / vi

        texto = []
        texto.append(f"Método: {metodo}")
        texto.append(f"SI = {si}")
        texto.append(f"VI = {vi:.2f}")
        texto.append(f"SF = {sf}")
        texto.append(f"VF = {vf:.2f}")
        texto.append(f"Ganho = {ganho:.2f} %")
        self.label_resultado.setText("\n".join(texto))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())