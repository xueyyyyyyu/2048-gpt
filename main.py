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


# 打印游戏板
def print_board(board):
    for row in board:
        print(" ".join(str(tile) if tile != 0 else '.' for tile in row))
    print()


# 移动数字
def move_tiles(row):
    non_zero_tiles = [tile for tile in row if tile != 0]
    new_row = []
    i = 0
    while i < len(non_zero_tiles):
        if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
            new_row.append(non_zero_tiles[i] * 2)
            i += 2
        else:
            new_row.append(non_zero_tiles[i])
            i += 1
    new_row.extend([0] * (len(row) - len(new_row)))
    return new_row


# 在游戏板上执行移动操作
def perform_move(board, direction):
    size = len(board)
    moved = False

    if direction == 'up':
        for j in range(size):
            col = [board[i][j] for i in range(size)]
            new_col = move_tiles(col)
            if col != new_col:
                moved = True
            for i in range(size):
                board[i][j] = new_col[i]

    elif direction == 'down':
        for j in range(size):
            col = [board[i][j] for i in range(size)][::-1]
            new_col = move_tiles(col)[::-1]
            if col != new_col:
                moved = True
            for i in range(size):
                board[i][j] = new_col[i]

    elif direction == 'left':
        for i in range(size):
            row = board[i]
            new_row = move_tiles(row)
            if row != new_row:
                moved = True
            board[i] = new_row

    elif direction == 'right':
        for i in range(size):
            row = board[i][::-1]
            new_row = move_tiles(row)[::-1]
            if row != new_row:
                moved = True
            board[i] = new_row

    return moved


# 检查游戏是否胜利或失败
def check_game_status(board):
    for row in board:
        if 2048 in row:
            return 'win'

    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return 'not over'

    for i in range(size - 1):
        for j in range(size - 1):
            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]:
                return 'not over'

    return 'lose'


# 主游戏循环
def main():
    size = 4
    board = initialize_board(size)
    generate_new_tile(board)
    generate_new_tile(board)
    print_board(board)

    while True:
        direction = input("Enter direction (up/down/left/right) or 'q' to quit: ").lower()
        if direction == 'q':
            break

        if direction in ['up', 'down', 'left', 'right']:
            moved = perform_move(board, direction)
            if moved:
                generate_new_tile(board)
                print_board(board)
                status = check_game_status(board)
                if status == 'win':
                    print("Congratulations! You win!")
                    break
                elif status == 'lose':
                    print("Game over. You lose.")
                    break
        else:
            print("Invalid direction. Please enter 'up', 'down', 'left', 'right', or 'q' to quit.")


if __name__ == "__main__":
    main()
