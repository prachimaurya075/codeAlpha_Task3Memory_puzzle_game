# Pynecone Memory Match  Game
# Modules


import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_TITLE = 'Memory Match Game'
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500  # Increased height to accommodate the timer
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(SCREEN_TITLE)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

# Define the box size and margin
box_size = 80
margin = 10

# Define fonts for text
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

# Create a list of colors for the game
colors = [RED, ORANGE, BLUE, YELLOW, GREEN, PINK] * 2  # Each color appears twice

# Shuffle colors to randomize the box layout
random.shuffle(colors)

# Create rectsData with positions and colors
rectsData = {}
for i, color in enumerate(colors):
    row = i // 4
    col = i % 4
    x = col * (box_size + margin) + margin
    y = row * (box_size + margin) + margin + 50  # Move the game area down to make space for the timer
    rectsData[i] = {'color': color, 'rect': pygame.Rect(x, y, box_size, box_size), 'revealed': False}

# Game variables
flipped = []
matched = []
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Get the starting time
time_limit = 55  # Time limit in seconds

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, data in rectsData.items():
                if data['rect'].collidepoint(pos) and i not in matched and i not in flipped:
                    flipped.append(i)

                    # Check if two cards are flipped
                    if len(flipped) == 2:
                        idx1, idx2 = flipped
                        if rectsData[idx1]['color'] == rectsData[idx2]['color']:
                            matched.extend([idx1, idx2])
                        # Set a short delay for better user experience
                        pygame.time.wait(200)  # Brief pause to show the second card
                        flipped = []

    # Calculate remaining time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert milliseconds to seconds
    remaining_time = max(time_limit - elapsed_time, 0)  # Calculate remaining time and ensure it doesn't go below 0

    # Fill the screen with a light blue color for a cartoonish look
    screen.fill((135, 206, 250))  # Light Sky Blue

    # Draw the timer
    timer_text = font.render(f'Time: {remaining_time}s', True, BLACK)
    screen.blit(timer_text, (10, 10))  # Draw timer in the top-left corner

    # Draw the colorful boxes using rectsData
    for i, data in rectsData.items():
        if i in matched or i in flipped:
            pygame.draw.rect(screen, data['color'], data['rect'])
        else:
            pygame.draw.rect(screen, BLACK, data['rect'])
            pygame.draw.rect(screen, WHITE, data['rect'], 5)  # Add white border

    # Draw the box labels
    for i, data in rectsData.items():
        if i in matched or i in flipped:
            label = font.render('?', True, BLACK)
            text_rect = label.get_rect(center=data['rect'].center)
            screen.blit(label, text_rect)

    # Check for win condition
    if len(matched) == len(rectsData):
        win_text = big_font.render('You Win!', True, BLACK)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(win_text, text_rect)
    elif remaining_time == 0:
        lose_text = big_font.render('You Lose!', True, BLACK)
        text_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(lose_text, text_rect)
    else:
        # Draw a black circle at the mouse position
        pygame.draw.circle(screen, BLACK, pygame.mouse.get_pos(), 10)

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Change the FPS to adjust game speed

    # Check for the game over condition
    if remaining_time <= 0 and len(matched) != len(rectsData):
        pygame.time.wait(1000)  # Brief pause before exiting
        running = False

# Quit Pygame
pygame.quit()
