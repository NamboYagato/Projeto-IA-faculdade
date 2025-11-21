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

        self.botao_anaise = QPushButton("ANÁLISE", self)
        self.botao_anaise.clicked.connect(self.gerar_pdf)
        
        

        # ÁREA DE TEXTO PARA OS RESULTADOS
        self.label_resultado = QLabel("", self)
        self.label_resultado.setWordWrap(True)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.botao_executar)
        main_layout.addWidget(self.botao_anaise)
        main_layout.addWidget(self.label_resultado)
        self.resize(400, 300)

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
        
        # self.busca_local_com_node = BuscaCVN(self.dist) # cria o objeto da classe BuscaCV_com_NodeCV com o matriz gerada
        self.busca_local = BuscaCV(self.dist) # cria o objeto da classe BuscaCV com o matriz gerada
        
        # node_inicial = self.busca_local_com_node.gerar_node_inicial() # gera a node inicial para os métodos de busca local / o node carrega a solução, o valor/custo e o pai/anterior da solução

        # sin = node_inicial.rota # pega a solução inicial do node
        # vin = node_inicial.custo # pega o valor/custo da solução inicial do node
        si = self.busca_local.gerar_solucao_inicial() # gera a solução inicial sem usar node
        vi = self.busca_local.valor_inicial(si) # gera o valor/custo da solução inicial sem usar node

        metodo = self.combo_metodo.currentText()
        if metodo.startswith("SUBIDA DE ENCOSTA"):
            # node_final = self.busca_local_com_node.subida_encosta(node_inicial) # executa o encosta usando o node
            sa, va = self.busca_local.subida_encosta(si, vi) # executa o encosta usando o node
            # sfn = node_final.rota
            # vfn = node_final.custo
            sf = sa
            vf = va
        elif metodo.startswith("SUBIDA DE ENCOSTA COM TENTATIVAS"):
            tmax = self.spin_tentativas.value()
            # node_final = self.busca_local_com_node.subida_encosta_tentativas(node_inicial, tmax)
            sa, va = self.busca_local.subida_encosta_tentativas(si, vi, tmax)
            # sfn = node_final.rota
            # vfn = node_final.custo
            sf = sa
            vf = va
        elif metodo.startswith("TÊMPERA SIMULADA"):
            TI = 400
            TF = 0.1
            FR = 0.8
            # node_final = self.busca_local_com_node.tempera_simulada(node_inicial, TI, TF, FR)
            sa, va = self.busca_local.tempera_simulada(si, vi, TI, TF, FR)
            # sf = node_final.rota
            # vf = node_final.custo
            sf = sa
            vf = va
        elif metodo.startswith("ALGORITMO GENÉTICO"):
            # ainda precisa mudar para funcionar com NovoGrafo
            TP   = 30    # tamanho da população
            NG   = 300    # número de gerações
            TC   = 0.9  # taxa de cruzamento
            TM   = 0.1  # taxa de mutação
            IG   = 0.2  # intervalo de geração
            si, sa, vi, va = AlgoritmoGenetico(n, self.dist, TP, NG, TC, TM, IG)
            sf = sa
            vf = va
        else:
            return
        
        ganho = 100 * abs(vi - vf) / vi

        texto = []
        texto.append(f"Método: {metodo}")
        texto.append(f"SI = {si}")
        texto.append(f"VI = {vi:.2f}")
        texto.append(f"SF = {sf}")
        texto.append(f"VF = {vf:.2f}")
        # texto.append(f"SIN = {sin}")
        # texto.append(f"VIN = {vin:.2f}")
        # texto.append(f"SFN = {sfn}")
        # texto.append(f"VFN = {vfn:.2f}")
        texto.append(f"Ganho = {ganho:.2f} %")
        self.label_resultado.setText("\n".join(texto))

    def gerar_pdf(self):
      
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        n = self.spin_tamanho.value()

        nome_pdf = f"Relatorio_Todos_Metodos_N{n}.pdf"
        c = canvas.Canvas(nome_pdf, pagesize=letter)

        # ===========================================================
        # Função interna para executar um caso e calcular o ganho
        # ===========================================================
        def executar(busca, params, metodo_nome, config_texto):
        # SUBIDA DE ENCOSTA NORMAL
                if metodo_nome == "SE":
                    si = busca.gerar_solucao_inicial()
                    vi = busca.valor_inicial(si)
                    sf, vf = busca.subida_encosta(si, vi)

                # SUBIDA DE ENCOSTA COM TENTATIVAS
                elif metodo_nome == "SET":
                    si = busca.gerar_solucao_inicial()
                    vi = busca.valor_inicial(si)
                    sf, vf = busca.subida_encosta_tentativas(si, vi, params["TMAX"])

                # TÊMPERA SIMULADA
                elif metodo_nome == "TS":
                    si = busca.gerar_solucao_inicial()
                    vi = busca.valor_inicial(si)
                    sf, vf = busca.tempera_simulada(si, vi,
                                                    params["TI"], params["TF"], params["FR"])

                # ALGORITMO GENÉTICO (NÃO USA busca)
                elif metodo_nome == "AG":
                    si, sf, vi, vf = AlgoritmoGenetico(
                        params["N"],
                        params["dist"],
                        params["TP"],
                        params["NG"],
                        params["TC"],
                        params["TM"],
                        params["IG"]
                    )

                # CALCULAR GANHO
                ganho = 100 * abs(vi - vf) / vi
                return ganho
        # ===========================================================
        # Escrever título no PDF
        # ===========================================================
        y = 760
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, y, "RELATÓRIO (PDF)")
        y -= 40

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, f"N = {n}")
        y -= 40

        # ===========================================================
        # BLOCO: Subida de Encosta (1 vez)
        # ===========================================================
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, "Método: Subida de Encosta (1 execução)")
        y -= 25

        nos, coords, dist = gerar_grafo(n)
        busca = BuscaCV(dist)

        ganho = executar(busca, {}, "SE", "")
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Ganho: {ganho:.2f}%")
        y -= 40

        # ===========================================================
        # BLOCO: Subida de Encosta com Tentativas (3 execuções)
        # ===========================================================
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, "Método: Subida de Encosta com Tentativas")
        y -= 25

        configs_set = [
            ("TMAX = N",        n),
            ("TMAX = N/2",      n/2),
            ("TMAX = N/4",      n/4)
        ]

        for texto, tmax in configs_set:
            nos, coords, dist = gerar_grafo(n)
            busca = BuscaCV(dist)

            ganho = executar(busca, {"TMAX": tmax}, "SET", texto)

            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"{texto}  →  Ganho: {ganho:.2f}%")
            y -= 25

            if y < 80:
                c.showPage()
                y = 760

        y -= 15

        # ===========================================================
        # BLOCO: Têmpera Simulada (4 execuções)
        # ===========================================================
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, "Método: Têmpera Simulada")
        y -= 25

        configs_ts = [
            ("TI=400 TF=0.1 FR=0.8",   400, 0.1, 0.8),
            ("TI=400 TF=0.01 FR=0.8",  400, 0.01, 0.8),
            ("TI=200 TF=0.1 FR=0.8",   200, 0.1, 0.8),
            ("TI=200 TF=0.01 FR=0.8",  200, 0.01, 0.8),
        ]

        for texto, TI, TF, FR in configs_ts:
            nos, coords, dist = gerar_grafo(n)
            busca = BuscaCV(dist)

            ganho = executar(busca,
                            {"TI": TI, "TF": TF, "FR": FR},
                            "TS",
                            texto)

            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"{texto}  →  Ganho: {ganho:.2f}%")
            y -= 25

            if y < 80:
                c.showPage()
                y = 760

        y -= 15

        # ===========================================================
        # BLOCO: Algoritmo Genético (4 execuções)
        # ===========================================================
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, "Método: Algoritmo Genético")
        y -= 25

        configs_ag = [
            ("TC=0.8 TM=0.1 IG=0.2", 0.8, 0.1, 0.2),
            ("TC=0.4 TM=0.1 IG=0.2", 0.4, 0.1, 0.2),
            ("TC=0.8 TM=0.6 IG=0.2", 0.8, 0.6, 0.2),
            ("TC=0.8 TM=0.1 IG=0.0", 0.8, 0.1, 0.0),
        ]

        for texto, TC, TM, IG in configs_ag:
            nos, coords, dist = gerar_grafo(n)

            ganho = executar(
                None,
                {"N": n, "TP": n, "NG": 2*n, "TC": TC, "TM": TM, "IG": IG, "dist": dist},
                "AG",
                texto
)

            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"{texto}  →  Ganho: {ganho:.2f}%")
            y -= 25

            if y < 80:
                c.showPage()
                y = 760

        c.save()

        self.label_resultado.setText(f"Relatório gerado: {nome_pdf}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())