import pygame
import sys
from kqparser import KQGame
 
def createtile(xpos,ypos,zoom,sprite):
    i = 0
    j = 7
    for y in range(sprite.ysize):
        for x in range(sprite.rowbytes*8):
            if x < sprite.xsize:
                if sprite.image[i] & 2**j:
                    pygame.draw.rect(screen, BLACK, [xpos*zoom+x*zoom, ypos*zoom+y*zoom, zoom, zoom])
            if j == 0:
                j = 7
                i += 1
            else:
                j = j - 1


game = KQGame(str(sys.argv[1]))

# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

# Define zoom level
ZOOM = 1
 
# Set the height and width of the screen
size = [100*16*ZOOM, 100*16*ZOOM]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Glen's Quest Map Drawing Test")

done = False
clock = pygame.time.Clock()
i = 0


# Main Loop
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            
    # All drawing code happens after the for loop but
    # inside the main while done==False loop.
     
    # Clear the screen and set the screen background
    screen.fill(WHITE)
 
    # Draw sprites
    x = 0
    y = 0
    i=0
    while i < 10000:
        createtile(x*16,y*16,ZOOM,game.tiles[game.mainmap[x][y]].sprite)
        if x < 99:
            x += 1
        else:
            y += 1
            x = 0
        i += 1


    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    pygame.time.delay(500)
 
# Be IDLE friendly
pygame.quit()
