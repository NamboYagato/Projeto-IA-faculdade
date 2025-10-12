# 🤖 Projeto de busca em grafo — Robótica (Braços, Solda e Pintura)
Este trabalho, desenvolvido para a disciplina de Inteligência Artificial, apresenta a implementação de uma ferramenta gráfica para a visualização e comparação de algoritmos de busca em grafos. O sistema foi aplicado ao problema de planejamento de rotas para braços robóticos, demonstrando a funcionalidade de métodos de busca com e sem informação em um cenário prático.

### Sumário
- [Descrição da atividade](#-descrição-da-atividade)
- [Como executar o projeto](#-como-executar-o-projeto)
- [Estrutura do grafo](#-estrutura-do-grafo)
- [Objetivo específico do grupo](#-objetivo-específico-do-grupo)
- [Integrantes do grupo](#-integrantes-do-grupo)

## 📌 Descrição da atividade
Considerando os métodos de busca sem informação vistos e o problema prático estabelecido para o grupo, o objetivo foi implementar um programa cuja interface gráfica contivesse:

1. **Opção para se selecionar qual método de busca será aplicado:**  
   - Amplitude
   - Profundidade  
   - Profundidade Limitada  
   - Aprofundamento Iterativo  
   - Bidirecional  
   - Custo Uniforme  
   - Greedy  
   - A*  
   - AIA*  

2. **Opções para escolher os estados inicial e objetivo**, dentre todos os estados possíveis do problema.  

3. **Área para exibição do caminho encontrado** e seu respectivo custo.  

4. **Visualização gráfica do problema**, exibindo todos os estados e o caminho encontrado.

**Observações do professor:**
- Os métodos de busca deverão ser implementados baseado no código disponibilizado.
- Não serão aceitos trabalhos entregues fora da data limite estabelecido.

## 🚀 Como executar o projeto
Para executar a interface gráfica, siga os passos abaixo.

**Pré-requisitos**
- Python 3 (ou versões mais recentes) instalado.

**Passo a passo**
1. **Navegue até a pasta do projeto**
Abra um terminal (CMD, PowerShell, Terminal do linux/macOS ou da IDE que estiver usando) e utlize o comando `cd` para entrar na pasta onde os arquivos do projeto foram salvos.
2. **Instale as dependências**
O projeto utiliza algumas bibliotecas Python que precisam ser instaladas. Execute o comando abaixo no terminal para instalá-las:
```bash
pip install PyQt5 networkx matplotlib
```
4. **Execute a aplicação**
Execute o arquivo `interface.py` para iniciar o programa. O arquivo `grafo.txt` deve estar na mesma pasta.
```bash
python interface.py
ou
py interface.py
```

## 📄 Estrutura do grafo
Este arquivo define a estrutura do grafo. Cada linha representa um nó e segue o formato abaixo:
```
NÓ  COORDENADA-X  COORDENADA-Y : VIZINHO+PESO ...
```
- As coordenadas X e Y servem para o calculo da heurística em buscas informadas (ex: A*, Greedy).
- `:` serve para separar a definição do nó da lista de vizinhos.

## 🎯 Objetivo específico do grupo
- Desenvolver um sistema que planeje trajetórias do TCP (Tool Center Point) para braços robóticos aplicados em:
  - Movimentação dentro de ambientes da empresa

## 👥 Integrantes do grupo
- Danilo Pereira
- Giovanni Guedes Baptista
