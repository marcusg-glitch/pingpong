import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_VELOCITY = 5

# Define ball properties
BALL_RADIUS = 7
INITIAL_BALL_VELOCITY_X, INITIAL_BALL_VELOCITY_Y = 4, 4
BALL_VELOCITY_X, BALL_VELOCITY_Y = INITIAL_BALL_VELOCITY_X, INITIAL_BALL_VELOCITY_Y

# Define paddle and ball positions
left_paddle = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Possible player names
player_names = ["Hissen AB", "Motum", "Kone"]

# Initialize player names and scores
def initialize_game():
    left_player_name = random.choice(player_names)
    right_player_name = random.choice(player_names)
    while right_player_name == left_player_name:
        right_player_name = random.choice(player_names)
    left_player_score = 0
    right_player_score = 0
    return left_player_name, right_player_name, left_player_score, right_player_score

left_player_name, right_player_name, left_player_score, right_player_score = initialize_game()

# Game loop control
run = True
clock = pygame.time.Clock()

# Timer for increasing ball speed
start_time = time.time()

def draw_score():
    font = pygame.font.SysFont(None, 36)
    left_score_text = font.render(f"{left_player_name}: {left_player_score}", True, WHITE)
    right_score_text = font.render(f"{right_player_name}: {right_player_score}", True, WHITE)
    win.blit(left_score_text, (50, 20))
    win.blit(right_score_text, (WIDTH - 50 - right_score_text.get_width(), 20))

def countdown():
    font = pygame.font.SysFont(None, 72)
    for i in range(3, 0, -1):
        win.fill(BLACK)
        count_text = font.render(str(i), True, WHITE)
        win.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - count_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)
    win.fill(BLACK)
    start_text = font.render("Start!", True, WHITE)
    win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

def reset_ball():
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2
    BALL_VELOCITY_X, BALL_VELOCITY_Y = INITIAL_BALL_VELOCITY_X, INITIAL_BALL_VELOCITY_Y
    BALL_VELOCITY_X *= random.choice([1, -1])
    BALL_VELOCITY_Y *= random.choice([1, -1])
    return BALL_VELOCITY_X, BALL_VELOCITY_Y

# Perform countdown before game starts
countdown()

# Game loop
paused = False
while run:
    clock.tick(60)  # Run at 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if not paused:
                    start_time = time.time()  # Reset the timer when resuming

    if not paused:
        keys = pygame.key.get_pressed()
        # Left paddle movement
        if keys[pygame.K_w] and left_paddle.y - PADDLE_VELOCITY > 0:
            left_paddle.y -= PADDLE_VELOCITY
        if keys[pygame.K_s] and left_paddle.y + PADDLE_VELOCITY + PADDLE_HEIGHT < HEIGHT:
            left_paddle.y += PADDLE_VELOCITY
        # Right paddle movement
        if keys[pygame.K_UP] and right_paddle.y - PADDLE_VELOCITY > 0:
            right_paddle.y -= PADDLE_VELOCITY
        if keys[pygame.K_DOWN] and right_paddle.y + PADDLE_VELOCITY + PADDLE_HEIGHT < HEIGHT:
            right_paddle.y += PADDLE_VELOCITY

        # Ball movement
        ball.x += BALL_VELOCITY_X
        ball.y += BALL_VELOCITY_Y

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_VELOCITY_Y = -BALL_VELOCITY_Y

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            BALL_VELOCITY_X = -BALL_VELOCITY_X

        # Ball reset and score update if it goes out of bounds
        if ball.left <= 0:
            right_player_score += 1
            BALL_VELOCITY_X, BALL_VELOCITY_Y = reset_ball()
            start_time = time.time()  # Reset the timer

        if ball.right >= WIDTH:
            left_player_score += 1
            BALL_VELOCITY_X, BALL_VELOCITY_Y = reset_ball()
            start_time = time.time()  # Reset the timer

        # Check for game winner
        if left_player_score >= 5 or right_player_score >= 5:
            winner = left_player_name if left_player_score >= 5 else right_player_name
            font = pygame.font.SysFont(None, 72)
            win.fill(BLACK)
            winner_text = font.render(f"{winner} Wins!", True, WHITE)
            win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
            pygame.display.flip()
            time.sleep(3)  # Display the winner for 3 seconds
            left_player_name, right_player_name, left_player_score, right_player_score = initialize_game()
            countdown()
            BALL_VELOCITY_X, BALL_VELOCITY_Y = reset_ball()
            start_time = time.time()  # Reset the timer for a new game

        # Increase ball speed every 5 seconds by 0.5%
        if time.time() - start_time >= 5:
            BALL_VELOCITY_X *= 1.25
            BALL_VELOCITY_Y *= 1.25
            start_time = time.time()

        # Determine ball color based on the score
        if left_player_score == 4 and right_player_score == 4:
            ball_color = BLUE
        elif left_player_score == 4 or right_player_score == 4:
            ball_color = RED
        else:
            ball_color = WHITE

        # Drawing the paddles, ball, net, and score
        win.fill(BLACK)
        pygame.draw.rect(win, WHITE, left_paddle)
        pygame.draw.rect(win, WHITE, right_paddle)
        pygame.draw.ellipse(win, ball_color, ball)
        pygame.draw.aaline(win, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        draw_score()

        pygame.display.flip()

pygame.quit()