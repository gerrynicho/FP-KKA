#!/usr/bin/env python3
import pygame
import random
import heapq


# Screen settings
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 21, 21
CELL_SIZE = WIDTH // COLS

# Colors
WHITE   = (255, 255,    255)
BLACK   = (0,   0,      0)
BLUE    = (0,   0,      255)
GREEN   = (0,   255,    0)
RED     = (255, 0,      0)
PURPLE  = (128, 0,      128)

# Directions for maze generation (Up, Right, Down, Left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game with Player Movement")
clock = pygame.time.Clock()

# Maze grid initialization
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
# Player's starting position
player_x, player_y = 0, 0
player_path = []

def generate_maze():
    global maze, player_x, player_y
    stack = [(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))]
    
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0  # Set the current cell as a path
        neighbors = []

        # Check all neighbors in DIRECTIONS
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx, dy))

        if neighbors:
            # Randomly choose a neighbor to create branching
            random.shuffle(neighbors)
            nx, ny, dx, dy = neighbors[0]

            # Clear walls between the cells to create a corridor
            maze[y + dy][x + dx] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))

            # Add additional branches randomly to create more complexity
            if len(neighbors) > 1 and random.random() < 0.3:
                nx, ny, dx, dy = neighbors[1]
                maze[y + dy][x + dx] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
        else:
            stack.pop()

    # Place player at a random starting point on a path cell
    while maze[player_y][player_x] != 0:
        player_x, player_y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for pos in player_path:
        pygame.draw.rect(screen, RED, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))



def draw_player():
    global player_x, player_y

    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_player_movement(keys):
    global player_x, player_y
    new_x, new_y = player_x, player_y
    if keys[pygame.K_UP]:      # Move up
        new_y -= 1
    if keys[pygame.K_DOWN]:    # Move down
        new_y += 1
    if keys[pygame.K_LEFT]:    # Move left
        new_x -= 1
    if keys[pygame.K_RIGHT]:   # Move right
        new_x += 1

    # Check if new position is within bounds and is a path
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y
        if (player_x, player_y) not in player_path:
            player_path.append((player_x, player_y))  # Store movement if new

# A* algorithm to find shortest path in player_path
def find_shortest_path():
    global shortest_path
    if len(player_path) < 2:
        return  # Not enough points to find a path

    start, end = player_path[0], player_path[-1]
    queue = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == end:
            break

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in player_path and (neighbor not in cost_so_far or cost_so_far[current] + 1 < cost_so_far[neighbor]):
                cost_so_far[neighbor] = cost_so_far[current] + 1
                priority = cost_so_far[neighbor]
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct path from end to start
    shortest_path = []
    current = end
    while current != start:
        shortest_path.append(current)
        current = came_from.get(current)
        if current is None:
            return  # If no path was found
    shortest_path.append(start)
    shortest_path.reverse()  # Start to end order

def draw_shortest_path():
    for pos in shortest_path:
        pygame.draw.rect(screen, PURPLE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    generate_maze()
    running = True
    show_shortest_path = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to calculate shortest path
                    find_shortest_path()
                    show_shortest_path = True  # Toggle flag to display path

        keys = pygame.key.get_pressed()
        handle_player_movement(keys)

        screen.fill(BLACK)
        draw_maze()
        draw_player()
        if show_shortest_path:
            draw_shortest_path()  # Display shortest path if flag is True
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()