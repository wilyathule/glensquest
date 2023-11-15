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
ZOOM = 6
 
# Set the height and width of the screen
size = [9*16*ZOOM, 9*16*ZOOM]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Glen's Quest Drawing Test")

done = False
clock = pygame.time.Clock()
i = 0
x = game.levelinfo['startx']
y = game.levelinfo['starty']

# Initialize sprites to character down animation
imagelist = [game.levelinfo['customgraphicsd1'],
             game.levelinfo['customgraphicsd2']
            ]



# Main Loop
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            
        if event.type == pygame.KEYDOWN: # If user pressed a key
            if event.key == pygame.K_LEFT:
                imagelist = [game.levelinfo['customgraphicsl1'],
                             game.levelinfo['customgraphicsl2']
                            ]
                i=0
                #if game.tiles[game.mainmap[x-1][y]].walk:
                x -= 1
            if event.key == pygame.K_RIGHT:
                imagelist = [game.levelinfo['customgraphicsr1'],
                             game.levelinfo['customgraphicsr2']
                            ]
                i=0
                x += 1
            if event.key == pygame.K_UP:
                imagelist = [game.levelinfo['customgraphicsu1'],
                             game.levelinfo['customgraphicsu2']
                            ]
                i=0
                y -= 1
            if event.key == pygame.K_DOWN:
                imagelist = [game.levelinfo['customgraphicsd1'],
                             game.levelinfo['customgraphicsd2']
                            ]
                i=0
                y += 1
 
    # All drawing code happens after the for loop but
    # inside the main while done==False loop.
     
    # Clear the screen and set the screen background
    screen.fill(WHITE)
    
    mx = -4
    my = -4
    nx = 0
    ny = 0
    j=0
    while j < 81:
        if mx == 0 and my == 0:
            pass
        else:
            createtile(nx*16,ny*16,ZOOM,game.tiles[game.mainmap[x+mx][y+my]].sprite)
        if mx < 4:
            mx += 1
            nx += 1
        else:
            my += 1
            ny += 1
            
            mx = -4
            nx = 0
        j += 1
 
    # Draw sprites
    createtile(64,64,ZOOM,imagelist[i])
    if i < len(imagelist) - 1:
        i += 1
    else:
        i = 0

    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    pygame.time.delay(500)
 
# Be IDLE friendly
pygame.quit()
