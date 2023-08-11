import pygame
import sys

# 初始化Pygame
pygame.init()

# 游戏参数
WIDTH = 400
HEIGHT = 400

# 创建游戏界面
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test Draw Game Over')

# 加载字体
font = pygame.font.Font(None, 48)


def draw_game_over():
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()


# 测试绘制游戏结束页面
def test_draw_game_over():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_game_over()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    test_draw_game_over()
