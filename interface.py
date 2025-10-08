import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox
from BuscaNP import buscaNP
from BuscaP import buscaP
from leitor_grafo import carregar_grafo_txt, grafoPonderado
 
 #armazena os nos
nos, grafo = carregar_grafo_txt("grafo.txt")
nosP, grafoP = grafoPonderado("grafo.txt")


class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.busca = buscaNP()
        self.buscaP = buscaP()

        self.setWindowTitle("Interface de busca")
        self.setGeometry(200, 200, 300, 200)

        #layout
        layout = QVBoxLayout()

        self.label = QLabel("Escolha uma opção", self)
        layout.addWidget(self.label)
        
        #combobox com as opções de busca
        self.combo = QComboBox(self)
        self.combo.addItems(["Amplitude", "Profundidade", "Profundidade Limitada", "Aprofundamento Iterativo", "Bidirecional", "Custo Uniforme"])
        layout.addWidget(self.combo)

        #conexões 
        self.combo.currentIndexChanged.connect(self.mudar_opcao)
   
        #adição futura do custo do precurso... 
        
        self.combo_inicio = QComboBox(self)
        self.combo_inicio.addItems(nos)

        self.combo_fim = QComboBox(self)
        self.combo_fim.addItems(nos)

        layout.addWidget(self.combo_inicio)
        layout.addWidget(self.combo_fim)

        self.botao_busca = QPushButton("Executar busca", self)
        layout.addWidget(self.botao_busca)
        self.botao_busca.clicked.connect(self.executar_busca)
        
        self.setLayout(layout)

    def mudar_opcao(self,index):
        opcao = self.combo.itemText(index)
        self.label.setText(f"Vc escolheu: {opcao}")
    
    def executar_busca(self):
        opcao = self.combo.currentText()
        inicio = self.combo_inicio.currentText()
        fim = self.combo_fim.currentText()

        resultado = None

        if opcao == "Amplitude":
            resultado = self.busca.amplitude(inicio, fim, nos, grafo)
        elif opcao == "Profundidade":
             resultado = self.busca.profundidade(inicio, fim, nos, grafo)
        elif opcao == "Profundidade Limitada":
            resultado = self.busca.prof_limitada(inicio, fim, nos, grafo, 4) #limite 
        elif opcao == "Aprofundamento Iterativo":
            resultado = self.busca.aprof_iterativo(inicio, fim, nos, grafo, 5) #limite máximo
        elif opcao == "Bidirecional":
            resultado = self.busca.bidirecional(inicio, fim, nos, grafo)
        elif opcao == "Custo Uniforme":
            resultado = self.buscaP.custo_uniforme(inicio, fim, nosP, grafoP) # custo uniforme

        if resultado:
            custo = len(resultado) - 1 
            self.label.setText(f"{opcao}: {resultado} (Custo: {custo})")
        else:
            self.label.setText(f"{opcao}: nenhum caminho encontrado")
        

app = QApplication(sys.argv)
janela = MinhaJanela()
janela.show()
sys.exit(app.exec_())
