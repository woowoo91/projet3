#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Here is the game "Aidez McGyver à s'échapper"
"""

import pygame
from pygame.locals import*
import random

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
INVENTORY ='images/unseen.png'
SLOT = 'images/slot.png'



### CLASSES ###

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
        """draw the loaded level on screen"""

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
                elif sprite == 'U': #check for inventory character
                    screen.blit(pygame.image.load(INVENTORY).convert(), (x,y)) #draw inventory tile on screen
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


    def move(self, direction):
        """move sprite"""
        #check keyboard input
        if direction == 'right':
            #check level limit
            if self.tile_x < (XTILES - 1):
                #check for wall
                if self.level.frame[self.tile_y][self.tile_x + 1] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y][self.tile_x + 1] != 'I':
                        #set new position on grid
                        self.tile_x += 1
                        #set new position on screen
                        self.x = self.tile_x * TILESIZE
        
        #check keyboard input
        elif direction == 'left':
            #check level limit
            if self.tile_x > 0:
                #check for wall
                if self.level.frame[self.tile_y][self.tile_x - 1] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y][self.tile_x - 1] != 'I':
                        #set new position on grid   
                        self.tile_x -= 1
                        #set new position on screen
                        self.x = self.tile_x * TILESIZE
        
        #check keyboard input
        elif direction == 'up':
            #check level limit
            if self.tile_y > 0:
                #check for wall
                if self.level.frame[self.tile_y-1][self.tile_x] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y-1][self.tile_x] != 'I':
                        #set new position on grid 
                        self.tile_y -= 1
                        #set new position on screen
                        self.y = self.tile_y * TILESIZE

        #check keyboard input
        elif direction == 'down':
            #check level limit
            if self.tile_y < (YTILES - 1):
                #check for wall
                if self.level.frame[self.tile_y+1][self.tile_x] != 'X':
                    #check for inventory tiles
                    if self.level.frame[self.tile_y+1][self.tile_x] != 'I':
                        #set new position on grid 
                        self.tile_y += 1
                        #set new position on screen
                        self.y = self.tile_y * TILESIZE
    

    def spawn(self, tile_y, tile_x):
        """spawn a sprite and put an 'O' symbol in level to prevent spawning other sprites
        on the same tile, could be used later to spawn additional sprites from events"""
        self.tile_y = tile_y #y position on grid
        self.tile_x = tile_x #x position on grid
        self.level.frame[self.tile_y][self.tile_x] == 'O' #token for presence of spawned sprite
        self.y = self.tile_y * TILESIZE #y position on screen
        self.x = self.tile_x * TILESIZE #x position on screen

    def rdm_spawn(self):
        """randomely spawn sprite avoiding walls 'X' and other spawned sprites 'O'"""

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
        """Transfer item to chosen inventory slot"""
        player_inventory[self.name] += 1 #add item to inventory
        self.tile_y = 15 #last row reserved for inventory
        self.tile_x = slot_x #chosen inventory slot
        self.y = self.tile_y * TILESIZE #set new y position on screen
        self.x = self.tile_x * TILESIZE #set new x position on screen


    def draw(self):
        """draw sprite on screen"""
        screen.blit(self.image, (self.x, self.y))



### MAIN ###

#initialize all imported pygame modules
pygame.init()

#initialize window with chosen resolution
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

#set title on top of window
pygame.display.set_caption(TITLE)

#initialize font
font = pygame.font.SysFont("bookman", 24)

#messages for starting and ending screens
START = font.render("Aidez McGyver à s'échapper", True, BLUE)
INSTRUCT = font.render("Ramassez les objets pour vous débarasser du gardien", True, BLUE)
WIN = font.render("McGyver s'est échappé", True, GREEN)
LOSS = font.render("McGyver s'est fait attraper", True, RED)

#starting screen
#fill whole screen with solid black color
screen.fill(BLACK)

#prints game title in middle of screen
screen.blit(START,(SCREENWIDTH // 2 - START.get_width() // 2, SCREENHEIGHT // 2 - START.get_height() // 2))
#prints instructions on middle bottom of screen
screen.blit(INSTRUCT,(SCREENWIDTH // 2 - INSTRUCT.get_width() // 2, SCREENHEIGHT - INSTRUCT.get_height()))

#update display
pygame.display.flip()

#pause program for 3 seconds (user can't QUIT)
pygame.time.wait(3000)

#main loop condition
running = True

#load level from file then draws it on screen without sprites
new_level = Level()
new_level.load()
new_level.draw(screen)

#create player inventory
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
while running:

    #limit updates to 10 per second
    pygame.time.Clock().tick(10)

    #draws level on screen
    new_level.draw(screen)

    #draw all sprites
    for sprite in sprite_instances:
       sprite.draw()

    #update display
    pygame.display.flip()

    #listen keyboard inputs
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
       
    #check if player and item locations match, transfer item to chosen inventory slot
    #check for needle item
    if (player.tile_x, player.tile_y) == (needle.tile_x, needle.tile_y):
        needle.pickup(6)
    
    #check for blowgun item
    elif (player.tile_x, player.tile_y) == (blowgun.tile_x, blowgun.tile_y):
        blowgun.pickup(7)
       
    #check for ether item
    elif (player.tile_x, player.tile_y) == (ether.tile_x, ether.tile_y):
        ether.pickup(8)
        
    #checks for victory condition and draws ending screen
    #check if player and keeper locations match
    if (player.tile_x, player.tile_y) == (keeper.tile_x, keeper.tile_y):
        #check if the player inventory has the required items to anaesthetise the keeper
        if player_inventory == {"needle":1,"blowgun":1,"ether":1}:

            #fill whole screen with solid black color
            screen.fill(BLACK)

            #print ending message on the middle of screen
            screen.blit(WIN,(SCREENWIDTH // 2 - WIN.get_width() // 2, SCREENHEIGHT // 2 - WIN.get_height() // 2))

            #update display
            pygame.display.flip()

            #pause program for 3 sec (user can't QUIT)
            pygame.time.wait(3000)

            #ends the game
            running = False

        else:

            #fill whole screen with solid black color
            screen.fill(BLACK)

            #print ending message on the middle of screen
            screen.blit(LOSS,(SCREENWIDTH // 2 - LOSS.get_width() // 2, SCREENHEIGHT // 2 - LOSS.get_height() // 2))

            #update display
            pygame.display.flip()

            #pause program for 3 sec (user can't QUIT)
            pygame.time.wait(3000)

            #ends the game
            running = False

