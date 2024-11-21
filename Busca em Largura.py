import pygame
from collections import deque
import time

# Dimensões do labirinto e configuração
GRID_SIZE = 12
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
GRAY = (180, 180, 180)

# Labirinto (1 é caminho, 0 é parede)
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

start = (4, 11)  # Início
end = (10, 0)  # Fim

# Direções possíveis (cima, esquerda, direita, baixo)
directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def bfs_with_animation(screen, maze, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}  # Para rastrear o caminho
    explored = []  # Para visualização em tempo real
    steps = 0  # Contador de passos

    while queue:
        current = queue.popleft()
        explored.append(current)
        steps += 1  # Incrementa o contador de passos

        # Verifica se chegamos ao destino
        if current == end:
            # Reconstruir o caminho
            path = []
            while current:
                path.append(current)
                current = parent.get(current)
            return path[::-1], explored, steps  # Retorna o caminho, as células exploradas e o número de passos

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if (
                0 <= neighbor[0] < GRID_SIZE
                and 0 <= neighbor[1] < GRID_SIZE
                and neighbor not in visited
                and maze[neighbor[0]][neighbor[1]] == 1
            ):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

        # Atualiza a tela para mostrar a exploração
        draw_maze(screen, maze, start, end, explored, [])
        pygame.display.flip()
        time.sleep(0.2)  # Controla a velocidade da exploração

    return [], explored, steps

def draw_maze(screen, maze, start, end, explored, path):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Adiciona linhas de grade
            pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Células exploradas
    for pos in explored:
        pygame.draw.rect(screen, BLUE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Destacar os pontos de início e fim
    pygame.draw.rect(screen, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Busca em Largura")
clock = pygame.time.Clock()

path, explored, steps = bfs_with_animation(screen, maze, start, end)

print(f"Total de passos: {steps}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_maze(screen, maze, start, end, explored, path)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()