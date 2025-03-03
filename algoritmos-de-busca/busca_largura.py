from collections import deque

class Grafo:
    def __init__(self):
        self.adjacencia = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = []

    def adicionar_aresta(self, vertice1, vertice2):
        if vertice1 in self.adjacencia and vertice2 in self.adjacencia:
            self.adjacencia[vertice1].append(vertice2)
            self.adjacencia[vertice2].append(vertice1)

    def busca_largura(self, inicio):

        visitados = set()
        fila = deque()
        fila.append(inicio)
        visitados.add(inicio)

        while fila:
            no_atual = fila.popleft()
            print(no_atual, end=" ")

            for vizinho in self.adjacencia[no_atual]:
                if vizinho not in visitados:
                    fila.append(vizinho)
                    visitados.add(vizinho)

if __name__ == "__main__":
    grafo = Grafo()
    
    # Adicionando nós
    cidades = ["A", "B", "C", "D", "E"]
    for cidade in cidades:
        grafo.adicionar_vertice(cidade)

    # Adicionando arestas
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("A", "C")
    grafo.adicionar_aresta("B", "D")
    grafo.adicionar_aresta("C", "E")

    print("\nOrdem de visitação usando Busca em Largura a partir do nó(cidade) A:")
    grafo.busca_largura("A")