import pygame
import random


# 初始化游戏板
def initialize_board(size):
    board = [[0] * size for _ in range(size)]
    return board


# 在随机空位置生成一个新数字（2或4）
def generate_new_tile(board):
    size = len(board)
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4


# 初始化Pygame
pygame.init()

# 游戏参数
GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 20
WIDTH = GRID_SIZE * (TILE_SIZE + PADDING) + PADDING
HEIGHT = WIDTH
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    # Add more colors for higher values
}

# 创建游戏界面
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')

# 加载字体
font = pygame.font.Font(None, 48)

# 初始化游戏板和生成初始数字
board = initialize_board(GRID_SIZE)
generate_new_tile(board)
generate_new_tile(board)


def draw_tile(tile_value, row, col):
    tile_color = TILE_COLORS.get(tile_value, (255, 255, 255))
    pygame.draw.rect(screen, tile_color, (
    col * (TILE_SIZE + PADDING) + PADDING, row * (TILE_SIZE + PADDING) + PADDING, TILE_SIZE, TILE_SIZE))

    if tile_value:
        text_surface = font.render(str(tile_value), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(
        col * (TILE_SIZE + PADDING) + TILE_SIZE / 2 + PADDING, row * (TILE_SIZE + PADDING) + TILE_SIZE / 2 + PADDING))
        screen.blit(text_surface, text_rect)


def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(board[row][col], row, col)
    pygame.display.flip()


def move(direction):
    global board

    moved = False

    if direction == "up":
        for col in range(GRID_SIZE):
            column = [board[row][col] for row in range(GRID_SIZE)]
            merged = merge_tiles(column)
            for row in range(GRID_SIZE):
                board[row][col] = merged[row]

    elif direction == "down":
        for col in range(GRID_SIZE):
            column = [board[row][col] for row in range(GRID_SIZE)]
            column.reverse()
            merged = merge_tiles(column)
            merged.reverse()
            for row in range(GRID_SIZE):
                board[row][col] = merged[row]

    elif direction == "left":
        for row in range(GRID_SIZE):
            merged = merge_tiles(board[row])
            board[row] = merged

    elif direction == "right":
        for row in range(GRID_SIZE):
            row_tiles = board[row]
            row_tiles.reverse()
            merged = merge_tiles(row_tiles)
            merged.reverse()
            board[row] = merged

    if any(2048 in row for row in board):
        # Handle game win here
        pass

    if moved:
        generate_new_tile(board)
        draw_board()

    return moved


def merge_tiles(tiles):
    merged = [0] * GRID_SIZE
    merged_idx = 0

    for tile in tiles:
        if tile != 0:
            if merged[merged_idx] == 0:
                merged[merged_idx] = tile
            elif merged[merged_idx] == tile:
                merged[merged_idx] *= 2
                merged_idx += 1
            else:
                merged_idx += 1
                merged[merged_idx] = tile

    return merged


# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move("up")
            elif event.key == pygame.K_DOWN:
                move("down")
            elif event.key == pygame.K_LEFT:
                move("left")
            elif event.key == pygame.K_RIGHT:
                move("right")

    draw_board()

pygame.quit()
