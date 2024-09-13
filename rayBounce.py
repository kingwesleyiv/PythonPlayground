import pygame
import sys
import time
import random
import math as m
import numpy as n
from numpy import array
from mathLib import lerp, rotate_point

# Initialize Pygame, Set window size
pygame.init()
window_size = (800, 800)  # width, height
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
fps = 30

# Define Circle parameters as a dictionary to allow passing data easier.
circle = {
    "pos": array([window_size[0] / 2, window_size[1] / 2]),
    "radius": 300,
    "color": (255,255,255)
}

# This fraction is used to make stars. (1 / X) will produce a star with X points.
# Setting the fraction above 1/2 (or equivalent fraction) will no longer produce a star but a polygon.
# Setting the fraction to a "prime fraction" or a fraction that cannot be reduced will result in a unique star shape.
# The larger the fraction (closer to 1) the wider the middle of the star becomes.
ray_dist = 1 - (51 / 101)
# A set of color gradients used for the rays. The list is itterated through each frame.
gradient = [
    [255,0,0],
    [255,255,0],
    [0,255,0],
    [0,255,255],
    [0,0,255],
    [255,0,255],
]
color = gradient[0] # Initial ray color

start_pos : array = (circle["pos"][0], circle["pos"][1] + circle["radius"]) # Bottom center of the circle.
last_end_pos : array = start_pos # Initialize the last ending position with the current start.

loop = 1 # The current iterration of the ray loop.

# Set window title
pygame.display.set_caption(random.choice([
    "Chicken Nuggest",
    "Happy Birthday!", 
    "Johnathan Price is a cuck", 
    "How do magnets work?", 
    "WORB WORB WORB",
    "I don't like this eyeliner it make me look all chinky",
    "Wtf wrong wit U",
    " Uh",
    "                     yuh.",
    "You know what absolutely fucking infuriates me? The endless, endless bullshit about Linux! I’ve tried it. Oh, I’ve tried it —",
    "ooooooooo daddy likey.",
]))

def chooseColor():
    
    return 0

# Circle draw function
def draw_circle(): # Center of the 600x600 window
    pygame.draw.circle(screen, circle["color"], circle["pos"], circle["radius"], 1)
    pygame.draw.circle(screen, circle["color"], circle["pos"], 1, 1) # Draw a dot in the middle

# Raycast Function
def raycast():
    # Itterate over gradient list, and lerp between entries. Frame Independent.
    color = lerp(gradient[int((loop / fps) % len(gradient))], gradient[int(((loop / fps) +1) % len(gradient))], (loop % fps) / fps)
    # Find the end position based on rotational math and circle relative position.
    end_pos = circle["pos"] + rotate_point(start_pos - circle["pos"], ray_dist * (loop))
    # Draw the line.
    pygame.draw.line(screen, tuple(color), last_end_pos, end_pos, 1)
    return end_pos

# Input the Localized coordinates of the point being rotated and the degrees of rotaton. Will rotate around 0,0 counter-clockwise.


# Fill the screen with black
screen.fill((0, 0, 0))

# Draw measurement Circles
#draw_circle()

# Loop
while True:
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Limit the FPS.
    clock.tick(fps)

    # For each next step the raycast function merely needs to repeat with new starting coordinates.
    # Due to precision errors with pixel location and Pi calculation, the more steps made the more innacurate the positions become.
    # We can achieve this by merely calculating the end_pos by the 'step' number (simple for loop >> i), multiplied by the ray_dist.
    last_end_pos = raycast() # This simultaniously draws the line and sets the start_pos as the previous end_pos.

    loop += 1
    if loop > 2^29 : loop = 0

    # Update the display
    pygame.display.flip()
