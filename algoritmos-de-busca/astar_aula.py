import heapq

class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # Coordenada (x, y)
        self.parent = parent  # Nó pai para reconstrução do caminho
        self.g = g  # Custo do caminho até este nó
        self.h = h  # Heurística estimada até o objetivo
        self.f = g + h  # Função f = g + h

    def __lt__(self, other):
        return self.f < other.f  # Comparação para a fila de prioridade. Vai olhar sempre para 'f' do objeto

def heuristic(a, b):
    """ Distância de Manhattan entre dois pontos """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    closed_set = set()

    start_node = Node(start, None, 0, heuristic(start, goal))

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position) # Adiciona nó atual na lista do caminho
                current_node = current_node.parent # Na próxima iteração o nó atual é o pai
            return path[::-1]  # Retorna o caminho na ordem correta. Foi adicionado do último nó até o primeiro

        closed_set.add(current_node.position)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # Posição de cada vizinho adjacente
            neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)

            # Verifica se vizinho está "out of bounds"
            # Verifica se vizinho está na lista fechada
            if 0 <= neighbor_pos[0] < rows and 0 <= neighbor_pos[1] < cols and grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and neighbor_pos not in closed_set:
                g = current_node.g + 1 # Custo acumulado
                h = heuristic(neighbor_pos, goal) # Heurística
                neighbor_node = Node(neighbor_pos, current_node, g, h) # Cria o nó do vizinho

                heapq.heappush(open_list, neighbor_node)

    return None  # Retorna None se não houver caminho

# Testando a função
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path = a_star(grid, start, goal)
print("Caminho encontrado:", path)
