#pylint:disable=W0621
import math
import random
import pygame
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

distinctcoloring= 25
#tries to make colors more distinct ; too big of a value will make no diffrence at all



#initialized
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Chain Reaction")
clock = pygame.time.Clock()

const1=(1-1/math.log(sizeofboard_x+2.5))*math.atan(sizeofboard_x)*3.2/math.pi
const2 = (1/sizeofboard_x)+(((1/sizeofboard_x) + math.atan(sizeofboard_x)*2/math.pi))*(math.pi/2)/math.atan(sizeofboard_x)
#scaling factors for text size, x offset,y offset
#dont ask how i came up with these :)

if sizeofboard_x<18:
    const3=const2
elif sizeofboard_x<65:
	const3=(1/const2)-1/sizeofboard_x
else:
	const3= 1/const2 -math.log10(math.log2(sizeofboard_x))	
if sizeofboard_x<13:
	const4 = (const3**1.72)*(const1)
else:
	const4=1
delta_x = round(cx*const4*30/108)
delta_y = round(cx*const3*20/108)
text_size = round(1100*const1/sizeofboard_x)

def randomcolor():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    color = (a,b,c)
    g = (a + b + c)/3
    if g<75 and g>235:
        color = randomcolor()
    return color
color = [randomcolor() for i in range(players)]
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
        if self.colornumber!=0:
            pygame.draw.rect(screen, color[self.colornumber-1], ( (self.x)*(cx), (self.y)*(cx), (cx), (cx) ) )
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
    decoration()
    drawboard()
    for i in range(sizeofboard_x):
        for j in range(sizeofboard_y):
            board[i][j].draw()
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
                font = pygame.font.SysFont('franklingothicheavy', 40)
                text = font.render('Player ' + str(i) +' wins!!!! ', 1, randomcolor())
                screen.blit(text, (screen_x*(4/10),screen_y/2))
                pygame.display.update()
                delayy()

def recolor():
    for i in range(len(color)):
        for j in range(i+1,len(color)):
            delta_c = math.sqrt((color[i][0]-color[j][0])**2 + (color[i][1]-color[j][1])**2 + (color[i][2]-color[j][2])**2)
        if delta_c < distinctcoloring:
            color[j] =randomcolor()
for i in range(players*2):
    recolor()

averagecolor =[0,0,0]
for i in color:
    averagecolor[0]  += i[0]
    averagecolor[1]  += i[1]
    averagecolor[2]  += i[2]
for i in range(len(averagecolor)):
    averagecolor[i] =int(155*(255 - averagecolor[i]/players)/255 +100)
averagecolor = tuple(averagecolor)
print(averagecolor)
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
    clock.tick(30)
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
