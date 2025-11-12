import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Themes
THEMES = [
    {"bg": (30, 30, 30), "snake": (0, 255, 0), "food": (255, 0, 0)},
    {"bg": (0, 0, 50), "snake": (0, 200, 255), "food": (255, 200, 0)},
    {"bg": (50, 20, 50), "snake": (255, 100, 255), "food": (255, 50, 50)}
]
current_theme = random.choice(THEMES)

# Snake settings
snake_size = 10
snake_speed = 10
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = (0, -snake_size)
trail = []

# Food settings
food = (random.randint(0, WIDTH // 10 - 1) * 10, random.randint(0, HEIGHT // 10 - 1) * 10)
food_pulse = 0

# Score Handling
score = 0


# Load high score from file High Score functions
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


# Save high score to file
def save_high_score(high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))


high_score = load_high_score()

#Font Setup
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 50)

#Drawing the snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(SCREEN, current_theme["snake"], (*segment, snake_size, snake_size), border_radius=5)

#Drawing the pulsating food
def draw_food(food):
    global food_pulse
    food_pulse = (food_pulse + 1) % 30
    pulse_size = int(math.sin(food_pulse / 5) * 3 + 5)
    pygame.draw.circle(SCREEN, current_theme["food"], (food[0] + 5, food[1] + 5), pulse_size)

#Message
def show_message(score, high_score):
    SCREEN.fill(current_theme["bg"])
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    restart_text = font.render("Press ENTER to Play Again", True, (255, 255, 0))
    SCREEN.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
    SCREEN.blit(score_text, (WIDTH // 3, HEIGHT // 3 + 30))
    SCREEN.blit(high_score_text, (WIDTH // 3, HEIGHT // 3 + 60))
    SCREEN.blit(restart_text, (WIDTH // 4, HEIGHT // 3 + 90))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    game_loop()

#Main Game Loop
def game_loop():
    global snake, snake_dir, food, score, high_score, current_theme, trail
    snake = [(WIDTH // 2, HEIGHT // 2)]
    trail = []
    snake_dir = (0, -snake_size)
    score = 0
    current_theme = random.choice(THEMES)
    running = True
    clock = pygame.time.Clock()

#Handling Events

    while running:
        SCREEN.fill(current_theme["bg"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, snake_size):
                    snake_dir = (0, -snake_size)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -snake_size):
                    snake_dir = (0, snake_size)
                elif event.key == pygame.K_LEFT and snake_dir != (snake_size, 0):
                    snake_dir = (-snake_size, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-snake_size, 0):
                    snake_dir = (snake_size, 0)

# Game Logic
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in snake:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            show_message(score, high_score)
            return

        snake.insert(0, new_head)

#Upadating the snake and food
        if new_head == food:
            score += 1
            food = (random.randint(0, WIDTH // 10 - 1) * 10, random.randint(0, HEIGHT // 10 - 1) * 10)
        else:
            snake.pop()

#Drawing the Game
        draw_snake(snake)
        draw_food(food)
        score_text = font.render(f"Score: {score}  High Score: {high_score}", True, (255, 255, 255))
        SCREEN.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(snake_speed)

#Start Screen
def start_screen():
    SCREEN.fill(current_theme["bg"])
    title_text = title_font.render("SNAKE GAME", True, (255, 255, 0))
    instruction_text = font.render("Press Any Key to Start", True, (255, 255, 255))
    SCREEN.blit(title_text, (WIDTH // 4, HEIGHT // 3))
    SCREEN.blit(instruction_text, (WIDTH // 4, HEIGHT // 3 + 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                game_loop()
                return

#Game Execution
start_screen()
pygame.quit()