import random
import sys

import pygame


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
FPS = 12

BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
GREEN = (46, 204, 113)
RED = (231, 76, 60)


def random_food_position(snake):
    cols = WINDOW_WIDTH // GRID_SIZE
    rows = WINDOW_HEIGHT // GRID_SIZE
    while True:
        position = (random.randrange(cols), random.randrange(rows))
        if position not in snake:
            return position


def draw_cell(surface, color, position):
    x, y = position
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def draw_text(surface, text, size, color, center):
    font = pygame.font.SysFont("consolas", size, bold=True)
    rendered = font.render(text, True, color)
    text_rect = rendered.get_rect(center=center)
    surface.blit(rendered, text_rect)


def game_over_screen(surface, score):
    surface.fill(BLACK)
    draw_text(surface, "GAME OVER", 48, RED, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
    draw_text(surface, f"Score: {score}", 32, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
    draw_text(
        surface,
        "Press R to restart or Q to quit",
        24,
        WHITE,
        (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60),
    )
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_r:
                    return True


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    cols = WINDOW_WIDTH // GRID_SIZE
    rows = WINDOW_HEIGHT // GRID_SIZE

    while True:
        snake = [(cols // 2, rows // 2), (cols // 2 - 1, rows // 2), (cols // 2 - 2, rows // 2)]
        direction = (1, 0)
        pending_direction = direction
        food = random_food_position(snake)
        score = 0

        alive = True
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        pending_direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        pending_direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        pending_direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        pending_direction = (1, 0)

            direction = pending_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            if (
                new_head[0] < 0
                or new_head[0] >= cols
                or new_head[1] < 0
                or new_head[1] >= rows
                or new_head in snake
            ):
                alive = False
                break

            snake.insert(0, new_head)
            if new_head == food:
                score += 1
                food = random_food_position(snake)
            else:
                snake.pop()

            screen.fill(BLACK)
            for segment in snake:
                draw_cell(screen, GREEN, segment)
            draw_cell(screen, RED, food)
            draw_text(screen, f"Score: {score}", 24, WHITE, (70, 20))

            pygame.display.flip()
            clock.tick(FPS)

        should_restart = game_over_screen(screen, score)
        if not should_restart:
            break

    pygame.quit()


if __name__ == "__main__":
    try:
        run_game()
    except pygame.error:
        print("Pygame is required. Install it with: pip install pygame")
