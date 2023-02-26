#pylint:disable=W062
import math
import pygame
from functions import averagecolorer,randomcolor,recolor,globalizer,brightner,generate_random_hsv
pygame.init()
#initalization...

screen_x = 1080
screen_y = 2200
#adjusted for my smartphone display
#keep screen_x value in check to prevent grid from going out of bounds

sizeofboard_x = 8
#number of columns, default 8

sizeofboard_y =16
#number of rows, default 16

players=2
#number of players, default 2

cx=screen_x/sizeofboard_x
#cx = screen_y/sizeofboard_y
#maybe enable seacond option for pc , i didnt test it

randomcoloring=0
#set to 1 for older method, may produce similar colors
#set to 0 to produce colors with evenly distributed hue, garunteed to produce distinct colors (recomended)
distinctcoloring= 25
#tries to make colors more distinct ; too big of a value will make no diffrence at all
#only when randomcoloring is set to 1

#initialized
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Chain Reaction")
clock = pygame.time.Clock()

glob=globalizer(sizeofboard_x,cx)
delta_x,delta_y,text_size=glob[0],glob[1],glob[2]

if randomcoloring ==1:
    color = [randomcolor() for i in range(players)]
    color_brighter =[]
    for c in color:
        color_brighter.append(brightner(c))
else:
    color,color_brighter = generate_random_hsv(players)
#color 0 = default
losers=[0 for i in range(players)]

class ball:
    def __init__(self,xy,number,color):
        self.x = xy[0]
        self.y = xy[1]
        self.number = number
        self.colornumber = color
        self.surroundings = []
        if self.x != 0:
            self.surroundings.append((self.x-1,self.y))
        if self.x != sizeofboard_x-1:
            self.surroundings.append((self.x+1,self.y))
        if self.y != 0:
            self.surroundings.append((self.x,self.y-1))
        if self.y != sizeofboard_y-1:
            self.surroundings.append((self.x,self.y+1))
        self.limit = len(self.surroundings)-1
    def draw(self):
        if self.colornumber!=0 and self.limit-self.number!=0:
            pygame.draw.rect(screen, color[self.colornumber-1], ( (self.x)*(cx), (self.y)*(cx), (cx), (cx) ) )
            font = pygame.font.SysFont('franklingothicheavy', text_size)
            text = font.render(str(self.number), 1, (255,255,255))
            screen.blit(text, ((self.x)*(cx)+delta_x, (self.y)*(cx)+delta_y))
        elif  self.colornumber!=0:
            pygame.draw.rect(screen, color_brighter[self.colornumber-1], ( (self.x)*(cx), (self.y)*(cx), (cx), (cx) ) )
            font = pygame.font.SysFont('franklingothicheavy', text_size)
            text = font.render(str(self.number), 1, (255,255,255))
            screen.blit(text, ((self.x)*(cx)+delta_x, (self.y)*(cx)+delta_y))

update = 0

def beam(x,y,playernumber):
    global update
    if board[x][y].number < board[x][y].limit:
        board[x][y].colornumber = playernumber
        board[x][y].number += 1
    else:
        board[x][y].number = 0
        board[x][y].colornumber = 0
        for i in board[x][y].surroundings:
            beam(i[0],i[1],playernumber)
        update += 1
        if update==250:
            redraw()
            declarewinner()
            update=0

def drawboard():
    for i in range(sizeofboard_x):
        pygame.draw.line(screen, (50, 60, 70), ((i+1)*(cx), 0), ((i+1)*(cx), cx*sizeofboard_y), 1)
    for i in range(sizeofboard_y):
        pygame.draw.line(screen, (50, 60, 70), (0, (i+1)*(cx)), (screen_x, (i+1)*(cx)), 1)

def redraw():
    screen.fill((0, 0, 10))
    drawboard()
    for i in range(sizeofboard_x):
        for j in range(sizeofboard_y):
            board[i][j].draw()
    decoration()
    pygame.display.update()

def declarewinner():
    winner=[0 for i in range(players)]
    for i in range(sizeofboard_x):
          for j in range(sizeofboard_y):
                if board[i][j].colornumber != 0:
                    winner[board[i][j].colornumber-1] = 1
                    global losers
                    losers =[1-i for i in winner]
    if winner.count(1)==1:
        for i in range(players):
            if winner[i]!= 0:
                
                pygame.draw.circle(screen,color[i],(screen_x*(1/2),screen_y*(5.1/10)),screen_y/10)
                pygame.draw.ellipse(screen,color_brighter[i],(screen_x*(2.5/10),screen_y*(4.36/10),screen_x*(5/10),screen_y*(1.5/10)))
                font = pygame.font.SysFont('franklingothicheavy', 90)
                text = font.render('Player ' + str(i) +' wins!!!! ', 1, (0,0,0))
                screen.blit(text, (screen_x*(2.8/10),screen_y/2))
                pygame.display.update()
                delayy()

if randomcoloring ==1:
    for i in range(players*2):
        recolor(color,distinctcoloring)


averagecolor = tuple(averagecolorer(color,players))

def decoration():
    font = pygame.font.SysFont('franklingothicheavy', 40)
    text = font.render('Player '+str(playernumber), 1, averagecolor)
#    text = font.render('Player '+str(playernumber), 1, randomcolor())
    screen.blit(text, (screen_x*(44/100),1))
#    pygame.display.update()

def delayy():
    i = 0
    while i < 350:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    pygame.quit()

    
board = [ ]
for i in range(sizeofboard_x):
    ki =[]
    for j in range(sizeofboard_y):
        ki.append(ball((i,j),0,0))
    board.append(ki[:])

playernumber = 0
redraw()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            while losers[playernumber]==1:
                playernumber += 1
                playernumber=playernumber%players
            x,y = pygame.mouse.get_pos()
            x = int(x//(cx))
            y = int(y//(cx))
            if x < sizeofboard_x and y < sizeofboard_y:
                if board[x][y].colornumber == ((playernumber%players)+1) or board[x][y].colornumber == 0 :
                    beam(x,y,(playernumber%players)+1)
                    playernumber += 1
                    playernumber = playernumber%players
    redraw()
    if update!= 0:
        declarewinner()
    update = 0
pygame.quit()
