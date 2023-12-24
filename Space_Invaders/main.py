import pygame as pg
import random
from math import sqrt

# initialize
pg.init()

# create screen 
screen=pg.display.set_mode((800,600))

# screen title
pg.display.set_caption("Space Invaders")
title_icon=pg.image.load("./images/title_icon.png")
pg.display.set_icon(title_icon)

# background
bg1=pg.image.load("./images/background1.jpg")
bg2=pg.image.load("./images/background2.jpg")
bg3=pg.image.load("./images/background3.jpg")

# score
score_val=0
font=pg.font.Font('./fonts/karmaticarcade.ttf',32)
textx=10
texty=10

def show_score(x,y):
    global screen
    global score_val
    score=font.render("Score: "+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))

# bullet class
bullet_img=pg.image.load("./images/bullet.png")

class bullet:
    def __init__(self,x=None,y=None,state="ready"):
        self.sprite=bullet_img.copy()

        self.x=x
        self.y=y

        self.delX=0
        self.delY=1

        self.state=state
    
    def fire(self):
        self.state="fired"
        screen.blit(self.sprite,(self.x,self.y))

# player/spaceship class template
player_img=pg.image.load("./images/player.png")

class spaceship:
    def __init__(self):
        self.sprite=player_img.copy()   # the sprite for the spaceship

        self.x=370                      # represents the current x coordinate of the player
        self.y=480                      # #represents the current y coordinate of the player

        # velocity parameters of ship
        self.delX0=0.4
        self.delX=0

        # bullet
        self.killer=bullet(self.x+16,self.y+10) # the extra 16 and 10 are to align the bullet

    def render(self):
        global screen
        '''
        Render the player aka spaceship
        '''
        screen.blit(self.sprite,(self.x,self.y))

player=spaceship()  # instantiate one spaceship object

# enemy class
enemy_img1=pg.image.load("./images/enemy1.png")
enemy_img2=pg.image.load("./images/enemy2.png")
enemy_img3=pg.image.load("./images/enemy3.png")

class alien:
    def __init__(self,n=1):
        
        self.n=n

        self.sprite=None
        self.x=random.randint(0,736)
        self.y=random.randint(50,150)
        self.delX=0.2*random.choice([-1,1])
        self.delY=40

    def render(self):
        global screen
        '''
        Render the enemy aka alien
        '''
        if(self.n==1):
            self.sprite=enemy_img1.copy()
        elif(self.n==2):
            self.sprite=enemy_img2.copy()
        else:
            self.sprite=enemy_img3.copy()
        screen.blit(self.sprite,(self.x,self.y))
    
nenemies=6
enemy_array=[]
for i in range(nenemies):
    enemy_array.append(alien(random.randint(1,3)))

def collided(obj1,obj2):
    d=sqrt((obj1.x-obj2.x)**2 + (obj1.y-obj2.y)**2)
    return d<=32

# game loop
running=True
while running:

    # background image
    screen.blit(bg3,(0,0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running=False

        if event.type==pg.KEYDOWN:
            if event.key==pg.K_LEFT:
                player.delX= -player.delX0

            if event.key==pg.K_RIGHT:
                player.delX=player.delX0

            if event.key==pg.K_SPACE:
                # this gives the firing sequence of bullet
                if player.killer.state=="ready":   # only fire when ready 
                    player.killer.x=player.x+16    # initialize x-value 
                    player.killer.fire()           #

        if event.type==pg.KEYUP:
            if event.key==pg.K_LEFT or event.key==pg.K_RIGHT:
                player.delX=0
        
    
    # update player position
    player.x+=player.delX
    #prevent player ship from going outside boundaries
    if(player.x<=0):
        player.x=0
    elif(player.x>=736):
        player.x=736     # 64 less than 800 since that is the width of the ship

    # update enemy position
    for enemy in enemy_array:
        enemy.x+=enemy.delX
        # prevent enemyersary from moving out of bounds
        if(enemy.x<=0 or enemy.x>=736):
            enemy.delX*=-1
            enemy.y+=enemy.delY
    
     
    # check for out of bounds, then update bullet state 
    if(player.killer.y<=0):
        player.killer.state="ready"
        player.killer.y=player.y+10     # this will stay constant and bullet x value updated whenever fired, giving illusion of being fired from the ship

    # when fired, update bullet's y-value only    
    if player.killer.state == "fired":
        player.killer.fire()
        player.killer.y-=player.killer.delY
    
    for enemy in enemy_array:
        if(collided(player.killer,enemy)):
            score_val+=1
            player.killer.state="ready"
            player.killer.y=player.y+10
            # respawn killed enemy
            enemy.x=random.randint(0,736)
            enemy.y=random.randint(50,150)
            enemy.n=random.randint(1,3)
            break


    # render player with its globally declared X and Y cordinates
    player.render()
    for enemy in enemy_array:
        enemy.render()
    show_score(textx,texty)
    pg.display.update()