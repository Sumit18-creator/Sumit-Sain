import pygame
import random
import sys
import json
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCORE_PANEL_HEIGHT = 60  # Height of the score panel
PLAYING_AREA_HEIGHT = WINDOW_HEIGHT - SCORE_PANEL_HEIGHT
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = PLAYING_AREA_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (40, 40, 40)  # Color for score panel

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

def load_high_score():
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open('high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.game_over = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        
        # Check for border collision
        if (new[0] < 0 or new[0] >= GRID_WIDTH or 
            new[1] < 0 or new[1] >= GRID_HEIGHT):
            self.game_over = True
            return False
            
        # Check for self collision
        if new in self.positions[3:]:
            self.game_over = True
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.game_over = False

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                           (p[0] * GRID_SIZE, 
                            p[1] * GRID_SIZE + SCORE_PANEL_HEIGHT,
                            GRID_SIZE - 2, GRID_SIZE - 2))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE,
                         self.position[1] * GRID_SIZE + SCORE_PANEL_HEIGHT,
                         GRID_SIZE - 2, GRID_SIZE - 2))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_score_panel(surface, score, high_score):
    # Draw score panel background
    pygame.draw.rect(surface, GRAY, (0, 0, WINDOW_WIDTH, SCORE_PANEL_HEIGHT))
    
    # Draw score panel border
    pygame.draw.line(surface, WHITE, (0, SCORE_PANEL_HEIGHT), 
                    (WINDOW_WIDTH, SCORE_PANEL_HEIGHT), 2)
    
    # Render scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, BLUE)
    
    # Center the scores in the panel
    surface.blit(score_text, (WINDOW_WIDTH//4 - score_text.get_width()//2, 
                             SCORE_PANEL_HEIGHT//2 - score_text.get_height()//2))
    surface.blit(high_score_text, (3*WINDOW_WIDTH//4 - high_score_text.get_width()//2, 
                                  SCORE_PANEL_HEIGHT//2 - high_score_text.get_height()//2))

def show_game_over(screen, score, high_score):
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    
    game_over_text = font.render('GAME OVER', True, RED)
    score_text = small_font.render(f'Score: {score}', True, WHITE)
    high_score_text = small_font.render(f'High Score: {high_score}', True, WHITE)
    restart_text = small_font.render('Press SPACE to restart', True, WHITE)
    
    screen.blit(game_over_text, 
                (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                 WINDOW_HEIGHT//2 - 100))
    screen.blit(score_text, 
                (WINDOW_WIDTH//2 - score_text.get_width()//2, 
                 WINDOW_HEIGHT//2))
    screen.blit(high_score_text, 
                (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 
                 WINDOW_HEIGHT//2 + 40))
    screen.blit(restart_text, 
                (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                 WINDOW_HEIGHT//2 + 80))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    high_score = load_high_score()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if snake.game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not snake.game_over:
            # Update snake
            if not snake.update():
                if snake.score > high_score:
                    high_score = snake.score
                    save_high_score(high_score)

            # Check if snake ate the food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

            # Draw everything
            screen.fill(BLACK)
            draw_score_panel(screen, snake.score, high_score)
            snake.render(screen)
            food.render(screen)

            pygame.display.update()
            clock.tick(10)  # Control game speed
        else:
            show_game_over(screen, snake.score, high_score)
            pygame.display.update()

if __name__ == '__main__':
    main() 