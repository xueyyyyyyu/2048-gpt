import sys
import pygame
import random

# 初始化Pygame
pygame.init()

# 加载字体
font = pygame.font.Font(None, 48)

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
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (128, 0, 128),
    # Add more colors for higher values
}

SCORE_FONT_SIZE = 24
SCORE_COLOR = (0, 0, 255)
score = 0

# 创建游戏界面
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')


# 初始化游戏板
def initialize_board(size):
    board = [[0] * size for _ in range(size)]
    return board


def clear_board(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            board[row][col] = 0


# 在随机空位置生成一个新数字（2或4）
def init_new_tile(board):
    size = len(board)
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4
        return True  # 更新 moved 的状态
    return False  # 没有生成新方块，不需要更新 moved 的状态


# 初始化游戏板和生成初始数字
board = initialize_board(GRID_SIZE)
init_new_tile(board)
init_new_tile(board)


def draw_tile(tile_value, row, col, step=0):
    tile_color = TILE_COLORS.get(tile_value, (255, 255, 255))
    pygame.draw.rect(screen, tile_color, (
        col * (TILE_SIZE + PADDING) + PADDING,
        row * (TILE_SIZE + PADDING) + PADDING + step,  # 添加 step 参数
        TILE_SIZE, TILE_SIZE))

    if tile_value:
        text_surface = font.render(str(tile_value), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(
            col * (TILE_SIZE + PADDING) + TILE_SIZE / 2 + PADDING,
            row * (TILE_SIZE + PADDING) + TILE_SIZE / 2 + PADDING + step  # 添加 step 参数
        ))
        screen.blit(text_surface, text_rect)


def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(board[row][col], row, col)

    # 绘制分数
    score_text = font.render("Score: " + str(score), True, SCORE_COLOR)
    score_rect = score_text.get_rect(topleft=(WIDTH - PADDING - score_text.get_width(), PADDING))
    screen.blit(score_text, score_rect)

    pygame.display.flip()


def generate_new_tile(board, direction):
    size = len(board)
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]

    # Choose the position to generate the new tile based on the direction and available empty cells
    if empty_cells:
        if direction == "up":
            row = max(empty_cells, key=lambda cell: cell[0])[0]
            col = random.choice([cell[1] for cell in empty_cells if cell[0] == row])
        elif direction == "down":
            row = min(empty_cells, key=lambda cell: cell[0])[0]
            col = random.choice([cell[1] for cell in empty_cells if cell[0] == row])
        elif direction == "left":
            col = max(empty_cells, key=lambda cell: cell[1])[1]
            row = random.choice([cell[0] for cell in empty_cells if cell[1] == col])
        elif direction == "right":
            col = min(empty_cells, key=lambda cell: cell[1])[1]
            row = random.choice([cell[0] for cell in empty_cells if cell[1] == col])

        board[row][col] = 2 if random.random() < 0.9 else 4
        return True  # 更新 moved 的状态
    return False  # 没有生成新方块，不需要更新 moved 的状态


def merge_tiles(tiles):
    merged = [0] * GRID_SIZE
    merged_idx = 0
    global score  # 声明全局分数变量

    for tile in tiles:
        if tile != 0:
            if merged[merged_idx] == 0:
                merged[merged_idx] = tile
            elif merged[merged_idx] == tile:
                merged[merged_idx] *= 2
                score += merged[merged_idx]  # 更新分数
                merged_idx += 1
            else:
                merged_idx += 1
                merged[merged_idx] = tile

    return merged


def is_game_over():
    # 检查是否有相邻的相同数字可以合并
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            if board[row][col] == board[row][col + 1]:
                return False

    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1):
            if board[row][col] == board[row + 1][col]:
                return False

    # 检查是否还有空格可以生成新数字
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                return False

    return True  # 游戏无法继续进行


def draw_game_over():
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, text_rect)

    # 显示分数
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()


def draw_win_screen():
    win_text = font.render("Congratulations! You Win!", True, (255, 255, 255))
    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))
    screen.blit(win_text, text_rect)
    pygame.display.flip()


def move(direction):
    global board

    moved = False
    step = 0
    step_delta = TILE_SIZE + PADDING

    if direction == "up":
        step_delta = -step_delta
        merge_func = merge_tiles

    elif direction == "down":
        merge_func = merge_tiles
        step_delta = -step_delta

    elif direction == "left":
        merge_func = merge_tiles

    elif direction == "right":
        step_delta = -step_delta
        merge_func = lambda tiles: merge_tiles(tiles[::-1])[::-1]

    while step < TILE_SIZE + PADDING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                draw_tile(board[row][col], row, col, step)
        pygame.display.flip()
        pygame.time.delay(50)

        step += abs(step_delta)

    for i in range(GRID_SIZE):
        if direction == "up" or direction == "down":
            if direction == "up":
                tiles = [board[row][i] for row in range(GRID_SIZE)]
            else:
                tiles = [board[row][i] for row in range(GRID_SIZE)][::-1]
        else:
            tiles = board[i][:]
        merged = merge_func(tiles)
        if tiles != merged:
            moved = True
        if direction == "up":
            for row in range(GRID_SIZE):
                board[row][i] = merged[row]
        elif direction == "down":
            for row in range(GRID_SIZE):
                board[GRID_SIZE - row - 1][i] = merged[row]
        else:
            board[i] = merged[:]

    if moved:
        generate_new_tile(board, direction)
        draw_board()

        if is_game_over():
            print("Game Over! Cannot make any more moves.")
            # 在这里可以添加其他游戏结束的逻辑，例如显示游戏结束的界面等

    return moved


def has_won_condition():
    for row in board:
        for tile_value in row:
            if tile_value == 2048:
                return True
    return False


def draw_start_screen():
    start_text = font.render("2048 Game", True, (255, 255, 255))
    text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))
    screen.blit(start_text, text_rect)
    pygame.display.flip()


# 游戏循环
running = True
game_state = "start"  # 添加状态变量

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "start":
            draw_start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("start")
                    game_state = "playing"

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move("up")
                elif event.key == pygame.K_DOWN:
                    move("down")
                elif event.key == pygame.K_LEFT:
                    move("left")
                elif event.key == pygame.K_RIGHT:
                    move("right")

            draw_board()

            if is_game_over():
                game_state = "finished"
                draw_game_over()
            elif has_won_condition():
                game_state = "finished"
                draw_win_screen()

        elif game_state == "finished":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press 'enter' to restart
                    print("restart")
                    clear_board(board)
                    init_new_tile(board)
                    init_new_tile(board)
                    score = 0
                    game_state = "playing"
                    draw_board()
                elif event.key == pygame.K_SPACE:  # Press 'Space' to quit
                    print("quit")
                    running = False

        pygame.display.flip()
pygame.quit()
sys.exit()
