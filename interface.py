import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox


class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minha Interface PyQt5")
        self.setGeometry(200, 200, 300, 200)

        #layout
        layout = QVBoxLayout()

        self.label = QLabel("Escolha uma opção", self)
        layout.addWidget(self.label)
        
        #combobox com as opções de busca
        self.combo = QComboBox(self)
        self.combo.addItems(["Opção 1","opção2","opção3","opção4"])
        layout.addWidget(self.combo)

        #conexões 
        self.combo.currentIndexChanged.connect(self.mudar_opcao)
       
        #armazem temporario dos nos
        self.nos = ['A','B','C','D']
        #adição futura do custo do precurso... 
        self.custo 

        self.combo_inicio = QComboBox(self)
        self.combo_inicio.addItems(self.nos)

        self.combo_fim = QComboBox(self)
        self.combo_fim.addItems(self.nos)

        layout.addWidget(self.combo_inicio)
        layout.addWidget(self.combo_fim)

        self.busca = QPushButton("Executar busca", self)
        layout.addWidget(self.busca)
        self.busca.clicked.connect(self.executar_busca)
        
        self.setLayout(layout)

    def mudar_opcao(self,index):
        opcao = self.combo.itemText(index)
        self.label.setText(f"Vc escolheu: {opcao}")
    
    def executar_busca(self):
        opcao = self.combo.currentText()
        inicio = self.combo_inicio.currentText()
        fim = self.combo_fim.currentText()
        self.label.setText(f"Buscando no caminho: {inicio} para {fim} utilizando o {opcao}" )
        

app = QApplication(sys.argv)
janela = MinhaJanela()
janela.show()
sys.exit(app.exec_())
