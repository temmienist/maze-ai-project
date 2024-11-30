import pygame
import numpy as np
from heapq import heappop, heappush
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

# Matriz de covariância para cálculo da distância de Mahalanobis
covariance = np.array([[1, 0], [0, 1]])
inv_cov = np.linalg.inv(covariance)

def mahalanobis_distance(point1, point2):
    # Calcula a distância de Mahalanobis entre dois pontos.
    diff = np.array(point1) - np.array(point2)
    return np.sqrt(np.dot(np.dot(diff.T, inv_cov), diff))


def heuristic_search(screen, maze, start, end):
    # Busca heurística usando distância de Mahalanobis.
    priority_queue = []
    heappush(priority_queue, (0, start))  # Fila de prioridade
    visited = set()
    parent = {}
    explored = []
    steps = 0

    while priority_queue:
        _, current = heappop(priority_queue)
        explored.append(current)
        steps += 1

        # Verifica se alcançou o objetivo
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent.get(current)
            return path[::-1], explored, steps

        if current in visited:
            continue
        visited.add(current)

        # Adiciona os vizinhos na fila de prioridade
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < GRID_SIZE
                and 0 <= neighbor[1] < GRID_SIZE
                and neighbor not in visited
                and maze[neighbor[0]][neighbor[1]] == 1
            ):
                cost = mahalanobis_distance(neighbor, end)
                heappush(priority_queue, (cost, neighbor))
                parent[neighbor] = current

        # Atualiza a tela para mostrar a exploração
        draw_maze(screen, maze, start, end, explored, [])
        pygame.display.flip()
        time.sleep(0.2)

    return [], explored, steps


def draw_maze(screen, maze, start, end, explored, path):
    # Desenha o labirinto na tela.
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    for pos in explored:
        pygame.draw.rect(screen, BLUE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Busca em Heurística com Mahalanobis")
clock = pygame.time.Clock()

# Busca heurística com animação
path, explored, steps = heuristic_search(screen, maze, start, end)

print(f"Total steps: {steps}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_maze(screen, maze, start, end, explored, path)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()