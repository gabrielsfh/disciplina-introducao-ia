import pygame
import random
from collections import deque

# Configurações iniciais
pygame.init()
largura, altura = 500, 500
tamanho_celula = largura // 5
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Aspirador de Pó Automático")
fonte = pygame.font.SysFont("Arial", 30)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Inicialização do ambiente
ambiente = [[random.choice([0, 1]) for _ in range(5)] for _ in range(5)]  # 0 = limpo, 1 = sujo
posicao_robo = [random.randint(0, 4), random.randint(0, 4)]  # Posição inicial aleatória
score = 0

# Função para desenhar o ambiente
def desenhar_ambiente():
    tela.fill(BRANCO)
    for i in range(5):
        for j in range(5):
            cor = VERDE if ambiente[i][j] == 0 else VERMELHO
            pygame.draw.rect(tela, cor, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))
            pygame.draw.rect(tela, PRETO, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula), 1)
    # Desenhar o robô
    pygame.draw.circle(tela, AZUL, (posicao_robo[1] * tamanho_celula + tamanho_celula // 2, posicao_robo[0] * tamanho_celula + tamanho_celula // 2), tamanho_celula // 3)
    # Desenhar o score
    texto = fonte.render(f"Score: {score}", True, PRETO)
    tela.blit(texto, (10, 10))

# Heurística de distância de Manhattan
def distancia_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Função de busca A* usando deque
def buscar_sujeira():
    direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direções possíveis: direita, baixo, esquerda, cima
    inicio = (posicao_robo[0], posicao_robo[1])
    
    # Encontrar todos os quadrados sujos
    alvos = [(i, j) for i in range(5) for j in range(5) if ambiente[i][j] == 1]
    if not alvos:  # Caso não haja mais sujeira
        return None
    
    # Escolher o alvo mais próximo com base na heurística
    alvo = min(alvos, key=lambda x: distancia_manhattan(inicio, x))
    
    # Fila para A* usando deque (ordenada manualmente por f_score)
    fila = deque([(0, 0, inicio)])  # (f_score, g_score, posição)
    veio_de = {}
    custo = {inicio: 0}
    visitado = set()
    
    while fila:
        # Ordenar a fila por f_score (menor custo primeiro)
        fila = deque(sorted(fila, key=lambda x: x[0]))
        f, g, atual = fila.popleft()
        
        # Verificar se a célula contém sujeira
        if ambiente[atual[0]][atual[1]] == 1:
            # Reconstruir o caminho até o alvo
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.reverse()
            return caminho[0] if caminho else None  # Retorna o próximo passo
        
        if atual in visitado:
            continue
        visitado.add(atual)
        
        for direcao in direcoes:
            nova_linha = atual[0] + direcao[0]
            nova_coluna = atual[1] + direcao[1]
            nova_pos = (nova_linha, nova_coluna)
            
            if 0 <= nova_linha < 5 and 0 <= nova_coluna < 5:
                novo_g = g + 1
                if nova_pos not in custo or novo_g < custo[nova_pos]:
                    custo[nova_pos] = novo_g
                    h = distancia_manhattan(nova_pos, alvo)
                    f = novo_g + h
                    fila.append((f, novo_g, nova_pos))
                    veio_de[nova_pos] = atual
    
    return None  # Caso não haja mais sujeira no ambiente

# Função para mover o robô
def mover_robo():
    global posicao_robo, score
    
    # Se a posição inicial estiver suja, limpar antes de buscar sujeira
    if ambiente[posicao_robo[0]][posicao_robo[1]] == 1:
        ambiente[posicao_robo[0]][posicao_robo[1]] = 0
        score += 1
    
    proxima_posicao = buscar_sujeira()
    if proxima_posicao:
        nova_linha, nova_coluna = proxima_posicao
        posicao_robo = [nova_linha, nova_coluna]
        # Verificar se há sujeira na nova posição
        if ambiente[nova_linha][nova_coluna] == 1:
            ambiente[nova_linha][nova_coluna] = 0
            score += 1

# Loop principal do jogo
clock = pygame.time.Clock()
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    mover_robo()
    desenhar_ambiente()
    pygame.display.flip()
    clock.tick(2)  # Controla a velocidade do robô (2 movimentos por segundo)

pygame.quit()
a