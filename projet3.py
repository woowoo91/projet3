#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Here is the game "Aidez McGyver à s'échapper"
"""

import sys
import random
import pygame
from pygame.locals import*

### CONSTANTS ###

#screen settings
XTILES = 15 #number of columns
YTILES = 16 #number of rows, the last one (bottom) being used for the player inventory
TILESIZE = 32 #size of tiles in pixels
SCREENWIDTH = XTILES * TILESIZE #windows width in pixels
SCREENHEIGHT = YTILES * TILESIZE #windows height in pixels

#colors shortcuts for font and background
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

#window title
TITLE = "Aidez McGyver à s'échapper"

#textures
WALL = 'images/brick_gray0.png'
FLOOR = 'images/floor_sand_stone0.png'
MCGYVER = 'images/macgyver.png'
KEEPER = 'images/gardien.png'
NEEDLE = 'images/needle0.png'
BLOWGUN = 'images/blowgun1.png'
ETHER = 'images/brilliant_blue.png'
SLOT = 'images/slot.png'

#messages for starting and ending screens
START = "Aidez McGyver à s'échapper"
INSTRUCT = "Ramassez les objets pour vous débarasser du gardien"
WIN = "McGyver s'est échappé"
LOSS = "McGyver s'est fait attraper"

### CLASSES & FUNCTIONS###

class Level():
    """Level creation"""

    def __init__(self):
        self.map_frame = 0

    def load(self):
        """Load a grid from file 'map.txt'"""

        with open("map.txt", "r") as map: #read file
            map_frame = [] #list for rows 
            for line in map:
                map_line = [] #list for characters
                for char in line:
                    if char != '\n': #check for line break in text file
                        map_line.append(char) #add character to list
                map_frame.append(map_line) #add line to list
            self.frame = map_frame


    def draw(self, screen):
        """Draws the loaded level on screen"""

        n_line = 0
        for line in self.frame:
            n_tile = 0
            for sprite in line:
                x = n_tile * TILESIZE
                y = n_line * TILESIZE
                if sprite == 'X': #check for wall character
                    screen.blit(pygame.image.load(WALL).convert(), (x,y)) #draw wall tile on screen
                elif sprite == '_': #check for floor character
                    screen.blit(pygame.image.load(FLOOR).convert(), (x,y)) #draw floor tile on screen
                elif sprite == 'I': #check for slot character
                    screen.blit(pygame.image.load(SLOT).convert(), (x,y)) #draw slot tile on screen
                n_tile += 1
            n_line += 1


class Sprite():
    """general class to manage sprites in the game"""

    def __init__(self, image, name, tile_y, tile_x, level):

        self.image = pygame.image.load(image).convert_alpha() 
        self.name = name #name of sprite
        self.tile_x = tile_x #x tile position on grid
        self.tile_y = tile_y #y tile position on grid
        self.x = tile_x * TILESIZE #x position on screen
        self.y = tile_y * TILESIZE #y position on screen
        self.level = level
        sprite_instances.append(self) #add instance to the sprite_instances list for further drawing


    def move(self, key):
        """Changes position of sprite on grid and screen from keyboard input 'key'"""
        
        #Checks if input is left and changes sprite positions
        if key == 'left':
            #Checks level limit
            if self.tile_x > 0:
                #Checks for wall
                if self.level.frame[self.tile_y][self.tile_x - 1] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y][self.tile_x - 1] != 'I':
                        #Sets new position on grid  
                        self.tile_x -= 1
                        #Sets new position on screen
                        self.x = self.tile_x * TILESIZE

        #Checks if input is right and changes sprite positions
        elif key == 'right':
            #Checks level limits
            if self.tile_x < (XTILES - 1):
                #Checks for wall
                if self.level.frame[self.tile_y][self.tile_x + 1] != 'X':
                    #Checks for inventory tiles
                    if self.level.frame[self.tile_y][self.tile_x + 1] != 'I':
                        #set new position on grid
                        self.tile_x += 1
                        #Sets new position on screen
                        self.x = self.tile_x * TILESIZE
        
        #Checks if input is up and changes sprite positions
        elif key == 'up':
            #Checks level limits
            if self.tile_y > 0:
                #Checks for wall
                if self.level.frame[self.tile_y-1][self.tile_x] != 'X':
                    #Checks for inventory tiles
                    if self.level.frame[self.tile_y-1][self.tile_x] != 'I':
                        #Sets new position on grid 
                        self.tile_y -= 1
                        #Sets new position on screen
                        self.y = self.tile_y * TILESIZE

        #Checks if input is down and changes sprite positions
        elif key == 'down':
            #check level limits
            if self.tile_y < (YTILES - 1):
                #check for wall
                if self.level.frame[self.tile_y+1][self.tile_x] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y+1][self.tile_x] != 'I':
                        #Sets new position on grid
                        self.tile_y += 1
                        #Sets new position on screen
                        self.y = self.tile_y * TILESIZE
    

    def spawn(self, tile_y, tile_x):
        """Spawns a sprite and put an 'O' symbol in level to prevent spawning other sprites
            on the same tile, could be used later to spawn additional sprites from events"""
        self.tile_y = tile_y #y position on grid
        self.tile_x = tile_x #x position on grid
        self.level.frame[self.tile_y][self.tile_x] == 'O' #token for presence of spawned sprite
        self.y = self.tile_y * TILESIZE #y position on screen
        self.x = self.tile_x * TILESIZE #x position on screen

    def rdm_spawn(self):
        """Randomely spawns sprite avoiding walls 'X' and other spawned sprites 'O'"""

        spawned = False #sprite hasn't spawned
        while not spawned:

            self.tile_y = random.randrange(1,14) #randomely sets y postion on grid
            self.tile_x = random.randrange(1,14) #randomely sets x postion on grid

            #check for wall
            if self.level.frame[self.tile_y][self.tile_x] != 'X':
                #check for another spawned sprite
                if self.level.frame[self.tile_y][self.tile_x] != 'O': 

                    #place 'spawned' token on grid
                    self.level.frame[self.tile_y][self.tile_x] == 'O'

                    self.y = self.tile_y * TILESIZE #set y position on screen
                    self.x = self.tile_x * TILESIZE #set x position on screen

                    spawned = True #ends loop

    def pickup(self, slot_x):
        """Transfers item to chosen inventory slot"""
        player_inventory[self.name] += 1 #add item to inventory
        self.tile_y = 15 #last row reserved for inventory
        self.tile_x = slot_x #chosen inventory slot
        self.y = self.tile_y * TILESIZE #set new y position on screen
        self.x = self.tile_x * TILESIZE #set new x position on screen


    def draw(self):
        """Draws sprite on screen"""
        screen.blit(self.image, (self.x, self.y))


def message(event, color):
    """starting and ending screens messages"""

    #fill whole screen with solid black color
    screen.fill(BLACK)

    #print ending message on the middle of screen
    text = font.render(event, True, color)
    screen.blit(text,(SCREENWIDTH // 2 - text.get_width() // 2, SCREENHEIGHT // 2 - text.get_height() // 2))

    #update display
    pygame.display.flip()

    #pause program for 1.5 sec (user can't QUIT)
    pygame.time.wait(1500)

 
### MAIN ###

#initialize all imported pygame modules
pygame.init()

#initialize window with chosen resolution
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

#set title on top of window
pygame.display.set_caption(TITLE)

#initialize font
font = pygame.font.SysFont("bookman", 24)

#starting screens
message(START, BLUE) #title
message(INSTRUCT, BLUE) #basic instructions

#load level from file then draws it on screen without sprites
new_level = Level()
new_level.load()
new_level.draw(screen)

#creates player inventory
player_inventory = {"needle":0,"blowgun":0,"ether":0}

#creation of items and characters
sprite_instances = [] #list of all sprite instances
items = [] #list all items

player = Sprite(MCGYVER, "player", 0, 0, new_level)

keeper = Sprite(KEEPER, "keeper", 0, 0, new_level)

needle = Sprite(NEEDLE, "needle", 0, 0, new_level)
items.append(needle)

blowgun = Sprite(BLOWGUN, "blowgun", 0, 0, new_level)
items.append(blowgun)

ether = Sprite(ETHER, "ether", 0, 0, new_level)
items.append(ether)

#spawning characters
player.spawn(13,1) #spawn player to bottom left corner
keeper.spawn(1,13) #spawn keeper on top right corner

#randomely spawns items
for i in items:
    i.rdm_spawn()

#main loop
running = True

while running:

    #Limits updates to 10 per second
    pygame.time.Clock().tick(10)

    #Draws level on screen
    new_level.draw(screen)

    #Draws all sprites
    for sprite in sprite_instances:
        sprite.draw()

    #Updates display
    pygame.display.flip()

    #Listens keyboard inputs
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False #quit game if player clicks on close windows icon or press escape key
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move('left') #move player sprite left if left arrow key is pressed
            elif event.key == K_UP:
                player.move('up') #move player sprite up if up arrow key is pressed
            elif event.key == K_DOWN:
                player.move('down') #move player sprite down if down arrow key is pressed
            elif event.key == K_RIGHT:
                player.move('right') #move player sprite right if right arrow key is pressed
       
    #Checks if player and item locations match, transfer item to chosen inventory slot
    #Checks for needle item
    if (player.tile_x, player.tile_y) == (needle.tile_x, needle.tile_y):
        needle.pickup(6)
    
    #Checks for blowgun item
    elif (player.tile_x, player.tile_y) == (blowgun.tile_x, blowgun.tile_y):
        blowgun.pickup(7)
       
    #Checks for ether item
    elif (player.tile_x, player.tile_y) == (ether.tile_x, ether.tile_y):
        ether.pickup(8)
        
    #Checks for victory condition and draws ending screen
    #Checks if player and keeper locations match
    if (player.tile_x, player.tile_y) == (keeper.tile_x, keeper.tile_y):
        #Checks if the player inventory has the required items to anaesthetise the keeper
        if player_inventory == {"needle":1,"blowgun":1,"ether":1}:

            message(WIN, GREEN)# draws victory screen
            running = False
            pygame.quit()
            sys.exit("Merci d'avoir essayé mon jeu")

        else:

            message(LOSS, RED)# draws failure screen
            running = False
            pygame.quit()
            sys.exit("Vous ferez mieux la prochaine fois.")