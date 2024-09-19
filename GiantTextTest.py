import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Text Input")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the font
font = pygame.font.Font(None, 36)  # Use the default system font with size 36

# Main game loop
text = ""  # Initialize an empty string to store the typed text
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character from the text
                text = text[:-1]
            else:
                # Add the typed character to the text
                text += event.unicode
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Render the text surface
    text_surface = font.render(text, True, WHITE)
    
    # Blit the text surface onto the screen
    screen.blit(text_surface, (10, 10))
    
    # Update the display
    pygame.display.flip()
    
    # Limit frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()