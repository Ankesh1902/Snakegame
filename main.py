import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game window dimensions
WIDTH = 800
HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Game variables
snake_block = 20
snake_speed = 15

# Font setup
font = pygame.font.SysFont("Arial", 50)


def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_block, snake_block])


def display_message(msg, color):
    text = font.render(msg, True, color)`
    screen.blit(text, [WIDTH / 6, HEIGHT / 3])


def generate_food():
    return (random.randrange(0, WIDTH - snake_block) // snake_block * snake_block,
            random.randrange(0, HEIGHT - snake_block) // snake_block * snake_block)


def game_loop():
    running = True
    game_active = True

    # Snake initial position
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake = []
    snake_length = 1
    score = 0

    # Food initial position
    food_x, food_y = generate_food()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -snake_block
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = snake_block
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -snake_block
                        dx = 0
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = snake_block
                        dx = 0
                else:
                    if event.key == pygame.K_r:
                        game_active = True
                        x, y = WIDTH // 2, HEIGHT // 2
                        dx = dy = 0
                        snake = []
                        snake_length = 1
                        score = 0
                        food_x, food_y = generate_food()
                    elif event.key == pygame.K_q:
                        running = False

        if game_active:
            # Update snake position
            x += dx
            y += dy

            # Boundary check
            if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
                game_active = False

            # Check self-collision
            head = (x, y)
            if head in snake[:-1]:
                game_active = False

            # Update snake body
            snake.append(head)
            if len(snake) > snake_length:
                del snake[0]

            # Food collision
            if x == food_x and y == food_y:
                food_x, food_y = generate_food()
                snake_length += 1
                score += 1

            # Drawing
            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (food_x, food_y, snake_block, snake_block))
            draw_snake(snake)

            # Score display
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            screen.fill(BLACK)
            display_message("Game Over! Press R-Restart Q-Quit", RED)
            score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()


# Start the game
if __name__ == "__main__":
    game_loop()