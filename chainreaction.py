#pylint:disable=W0621
import pygame
import pygame.gfxdraw
import random
from functions import averagecolorer,randomcolor,recolor,globalizer,brightner,generate_random_hsv,ceil,floor
pygame.init()
#initalization...

screen_x = 1080
screen_y = 2200
#adjusted for my smartphone display
#keep screen_x value in check to prevent grid from going out of bounds

sizeofboard_x = 5
#number of columns, default 8

sizeofboard_y =10
#number of rows, default 16

players=2
#number of players, default 2

paused =1
#1,0 to show or to not show pause menu

randomcoloring=0
#set to 1 for older method, may produce similar colors
#set to 0 to produce colors with evenly distributed hue, garunteed to produce distinct colors (recomended)
distinctcoloring= 25
#tries to make colors more distinct ; too big of a value will make no diffrence at all
#only when randomcoloring is set to 1

width_incomplete =0
#how transtaparent is a cell(only those not about to blast)
#value from 0 to 255
#initialized


def readfile():
    global sizeofboard_x,sizeofboard_y,players,width_incomplete
    file = open('settings','r')
    line = file.read().split(' ')
    sizeofboard_x,sizeofboard_y,players,width_incomplete=int(line[0]),int(line[1]),int(line[2]),int(line[3])
    file.close()

def writefile():
    file = open('settings','w')
    file.write(str(sizeofboard_x)+' '+str(sizeofboard_y)+' '+str(players)+' '+str(width_incomplete))
    file.close()

readfile()

update = 0
playernumber = 0
init =0
color=[]
color_brighter = []
losers=[0 for i in range(players)]
padding =[0,0]
cx=min(screen_x/sizeofboard_x,screen_y/sizeofboard_y)


screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Chain Reaction")
clock = pygame.time.Clock()


#glob=globalizer(sizeofboard_x,cx)
#delta_x,delta_y,text_size=glob[0],glob[1],glob[2]
def initializer():
    global color_brighter
    global color
    if randomcoloring ==0:
        color = [randomcolor() for i in range(players)]
        color_brighter =[]
        for c in color:
            color_brighter.append(brightner(c))
    else:
        color,color_brighter = generate_random_hsv(players)
    if randomcoloring ==1:
        for i in range(players*2):
            recolor(color,distinctcoloring)

def repadding():
    global padding
    if screen_x/sizeofboard_x<screen_y/sizeofboard_y:
        padding = [0,(screen_y-cx*sizeofboard_y)/2]
    elif screen_x/sizeofboard_x>screen_y/sizeofboard_y:
        padding =[(screen_x-cx*sizeofboard_x)/2,0]
initializer()
repadding()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
width_complete=0

class ball:
    def __init__(self,xy,number,color):
        self.x = xy[0]
        self.y = xy[1]
        self.xy = xy
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
            pygame.draw.rect(screen, color[self.colornumber-1], ( floor((self.x)*(cx)+padding[0])+width_incomplete, floor((self.y)*(cx)+padding[1])+width_incomplete, ceil(cx)-width_incomplete, ceil(cx)-width_incomplete ),width_incomplete+1*int(bool(width_incomplete)))
            font = pygame.font.SysFont('aria2', text_size)
            text = font.render(str(self.number), 1, (255,255,255))
            screen.blit(text, ((self.x)*(cx)+delta_x, (self.y)*(cx)+delta_y))
        elif  self.colornumber!=0:
            pygame.draw.rect(screen, color_brighter[self.colornumber-1], ( floor((self.x)*(cx)+padding[0])+width_complete, floor((self.y)*(cx)+padding[1])+width_complete, ceil(cx)-width_complete, ceil(cx)-width_complete ),width_complete+1*int(bool(width_complete)))
            font = pygame.font.SysFont('aria2', text_size)
            text = font.render(str(self.number), 1, (255,255,255))
            screen.blit(text, ((self.x)*(cx)+delta_x, (self.y)*(cx)+delta_y))


class Button():
	def __init__(self, x, y, width,height,color,border,radii):
		self.x=int(x)
		self.y=int(y)
		self.width = int(width)
		self.height = int(height)
		self.clicked = False
		self.color=color
		self.border = border
		self.radii = radii
		self.rect = pygame.Rect(round(x-width/2),round( y- height/2),round(width),round(height))

	def draw(self,tex,left,top,siz):
		action = False
		pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
				while pygame.mouse.get_pressed()[0] == 1:
				    pygame.time.delay(10)
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		pygame.draw.rect(screen,self.color,self.rect,self.border,self.radii)
		font = pygame.font.SysFont('aria2', siz)
		text = font.render(tex, 1, (255,255,255))
		screen.blit(text,(self.x-left,self.y-top))
		return action



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
    for i in range(sizeofboard_x+1):
        pygame.draw.line(screen, (90, 80, 90), (((i)*cx)+padding[0] , padding[1]), (((i)*cx)+padding[0], cx*sizeofboard_y+padding[1]), 1)
    for i in range(sizeofboard_y+1):
        pygame.draw.line(screen, (90, 80, 90), (padding[0], ((i)*cx)+padding[1]), (cx*sizeofboard_x+padding[0], ((i)*cx)+padding[1]), 1)

def redraw():
    screen.fill((0, 0, 10))
    drawboard()
    drawboard()
    global update
    for i in range(sizeofboard_x):
        for j in range(sizeofboard_y):
            board[i][j].draw()
    decoration()
    pygame.display.update()
    if update!= 0:
        declarewinner()
        update = 0

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
                
                pygame.draw.circle(screen,color[i],(screen_x*(1/2),screen_y*(5.1/10)),screen_y/11)
                pygame.draw.ellipse(screen,color_brighter[i],(screen_x*(2.5/10),screen_y*(4.36/10),screen_x*(5/10),screen_y*(1.5/10)))
                font = pygame.font.SysFont('aria2', 90)
                text = font.render('Player ' + str(i) +' wins!!!! ', 1, (0,0,0))
                screen.blit(text, (screen_x*(2.8/10),screen_y/2))
                pygame.display.update()
                pygame.time.delay(2000)
                global init
                global paused
                init =0
                paused =1
                pygame.display.update()


def decoration():
    font = pygame.font.SysFont('aria2', 40)
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


def randomcoords(x):
    return [[[[random.randint(0,screen_x),random.randint(0,screen_y)] for i in range(random.randint(3,22))] for j in range(x)], [randomcolor() for k in range(x)]]

beziers = randomcoords(12)
for i in range(len(beziers[1])):
    beziers[0][i].append(beziers[0][i][0])
    beziers[0][i].append(beziers[0][i][1])

def update_bezier():
    for i in range(len(beziers[1])):
        for j in range(len(beziers[0][i])):
            beziers[0][i][j][0] +=random.randint(-100,100)/100
            beziers[0][i][j][1] +=random.randint(-100,100)/100
def drawcurves():
    screen.fill((0,0,20))
    for i in range(len(beziers[1])):
        pygame.gfxdraw.bezier(screen,beziers[0][i],20,beziers[1][i])
        update_bezier()

play_b = Button(screen_x/2,screen_y*1/10,220,110,randomcolor(),0,60)
players_b  = Button(screen_x/2,screen_y*2/10,330,110,randomcolor(),0,60)
settings_b = Button(screen_x/2,screen_y*3/10,330,110,randomcolor(),0,60)
quit_b = Button(screen_x/2,screen_y*4/10,220,110,randomcolor(),0,60)
colors_b  = Button(screen_x/2,screen_y*2/10,300,110,randomcolor(),0,60)
backbutton= Button(screen_x/2,screen_y/40,100,100,randomcolor(),0,100)
layer1_bp = Button(screen_x*1/3,screen_y/10,100,100,randomcolor(),0,100)
layer1_bn = Button(screen_x*2/3,screen_y/10,100,100,layer1_bp.color,0,100)
gridsize_b  = Button(screen_x/2,screen_y*1/10,360,110,randomcolor(),0,60)
layer2_bp = Button(screen_x*1/3,screen_y/5,100,100,randomcolor(),0,100)
layer2_bn = Button(screen_x*2/3,screen_y/5,100,100,layer2_bp.color,0,100)




while True:
    clock.tick(60)
    update_bezier()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif paused >0:
            if True:
                drawcurves()
                play_clicked = play_b.draw('Play',62,30,90)
                colors_clicked = colors_b.draw('Colors',100,30,90)
                settngs_clicked = settings_b.draw('Settings',130,30,90)
                quit_clicked = quit_b.draw('Quit',67,30,90)
                if play_clicked:
                   paused =0
                elif colors_clicked:
                    paused = 2
                    drawcurves()
                    cbuttons = []
                    cboxes = int(players**(1/2))
                    player_diffrence = players-cboxes**2
                    cbox_width = (screen_x/(cboxes+2))
                    deltaa = screen_x*2/((cboxes+1)*(cboxes+2))
                    for i in range(players):
                        if int(players**(1/2)) != players**(1/2):
                            alpha = 1
                        else:
                            alpha =0
                        for j in range(players//cboxes):
                            for k in range(cboxes):
                                cbuttons.append(Button((deltaa+cbox_width)*k+deltaa+cbox_width/2,(deltaa+cbox_width)*j +deltaa+cbox_width/2,cbox_width,cbox_width,color[cboxes*j+k],0,1000))
                        if alpha==1:
                            player_diffrence = players%cboxes
                            for j in range(player_diffrence):
                                nu_deltaa = (screen_x - (player_diffrence* cbox_width))/(player_diffrence+1)
                                cbuttons.append(Button((nu_deltaa+cbox_width)*j+nu_deltaa+cbox_width/2,(deltaa+cbox_width)*(players//cboxes) +deltaa+cbox_width/2,cbox_width,cbox_width,color[cboxes**2+j],0,1000))
                        while paused !=1:
                            backbutton_clicked = backbutton.draw('«',25,42,120)
                            if backbutton_clicked:
                                paused=1
                                backbutton_clicked= False
                            for btn in range(players):
                                if btn <10:
                                    clkd = cbuttons[btn].draw(str(btn),20,23,70)
                                else:
                                    clkd = cbuttons[btn].draw(str(btn),33,23,70)
                                if clkd:
                                    color[btn] = randomcolor()
                                    cbuttons[btn].color = color[btn]
                                    color_brighter[btn] = brightner(color[btn])
                            font = pygame.font.SysFont('aria2', 90)
                            text = font.render('Click to change colors', 1, (255,255,255))
                            screen.blit(text,(screen_x/2-330,screen_y*9/10))
                            pygame.display.update()  
                elif settngs_clicked:
                    paused=3
                    drawcurves()
                    while paused >2:
                        backbutton_clicked = backbutton.draw('«',25,42,120)
                        players_clicked = players_b.draw('Players',120,30,90)
                        gridsize_clicked = gridsize_b.draw('Grid Size',142,30,90)
                        
                        if backbutton_clicked:
                            paused = 1
                            backbutton_clicked = False
                            writefile
                        elif gridsize_clicked:
                            paused = 5
                            play_b_3 = Button(screen_x/2,screen_y*3/10,220,110,randomcolor(),0,60)
                            anychanges =False
                            while paused == 5:
                                screen.fill((0,0,10))
                                cx=min(screen_x/sizeofboard_x,screen_y/sizeofboard_y)
                                repadding()
                                drawboard()
                                layer1p_clicked = layer1_bp.draw('‹',16,43,120)
                                layer1n_clicked = layer1_bn.draw('›',12,43,120)
                                layer2p_clicked = layer2_bp.draw('‹',16,43,120)
                                layer2n_clicked =layer2_bn.draw('›',12,43,120)
                                play3_clicked = False #play_b_3.draw('Play',62,30,90)
                                backbutton_clicked = backbutton.draw('«',25,42,120)
                                font = pygame.font.SysFont('aria2', 120)
                                text = font.render(str(sizeofboard_x), 1, (255,255,255))
                                screen.blit(text,(screen_x/2-20*(len(str(players))),screen_y/10- 35))
                                font = pygame.font.SysFont('aria2', 120)
                                text = font.render(str(sizeofboard_y), 1, (255,255,255))
                                screen.blit(text,(screen_x/2-20*(len(str(players))),screen_y*2/10- 35))
                                if play3_clicked:
                                    paused = 0
                                if layer1p_clicked:
                                    if sizeofboard_x>1:
                                        sizeofboard_x-=1
                                        anychanges=True
                                elif layer1n_clicked:
                                    sizeofboard_x+=1
                                    anychanges=True
                                if layer2p_clicked:
                                    if sizeofboard_y>1:
                                        sizeofboard_y-=1
                                        anychanges=True
                                elif layer2n_clicked:
                                    sizeofboard_y+=1
                                    anychanges=True
                                elif backbutton_clicked:
                                    backbutton_clicked=False
                                    paused = 3
                                pygame.display.update()
                            drawcurves()
                            if anychanges==True:
                                init = 0
                        elif players_clicked:
                            paused =4
                            drawcurves()
                            anychanges=False
                            while paused ==4:
                                drawcurves()
                                layer1p_clicked = layer1_bp.draw('‹',16,43,120)
                                layer1n_clicked = layer1_bn.draw('›',12,43,120)
                                backbutton_clicked = backbutton.draw('«',25,42,120)
                                font = pygame.font.SysFont('aria2', 120)
                                text = font.render(str(players), 1, (255,255,255))
                                screen.blit(text,(screen_x/2-20*(len(str(players))),screen_y/10- 35))
                                if layer1p_clicked:
                                    if players>2:
                                        players-=1
                                        anychanges=True
                                elif layer1n_clicked:
                                    players+=1
                                    anychanges=True
                                elif backbutton_clicked:
                                    backbutton_clicked=False
                                    paused = 3
                                pygame.display.update()
                            drawcurves()
                            if anychanges==True:
                                initializer()
                        sizeofy_bp = Button(screen_x*1/3,screen_y*3/10,100,100,randomcolor(),0,100)
                        sizeofy_bn = Button(screen_x*2/3,screen_y*3/10,100,100,randomcolor(),0,100)
                        
                        pygame.display.update()
                elif quit_clicked:
                    writefile()
                    pygame.quit()
                pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN and init ==1:
            while losers[playernumber]==1:
                playernumber += 1
                playernumber=playernumber%players
            x,y = pygame.mouse.get_pos()
            xy=bool(x-padding[0]>0 and y-padding[1]>0)
            x = int((x-padding[0])//(cx))
            y = int((y-padding[1])//(cx))
            if xy and x < sizeofboard_x and y < sizeofboard_y and paused==-1:
                if board[x][y].colornumber == ((playernumber%players)+1) or board[x][y].colornumber == 0 :
                    beam(x,y,(playernumber%players)+1)
                    playernumber += 1
                    playernumber = playernumber%players
                redraw()
            if paused==0:
                pygame.time.delay(100)
                paused =-1
        elif init ==0:
            writefile()
            losers=[0 for i in range(players)]
            glob=globalizer(cx,screen_x)
            delta_x,delta_y,text_size=glob[0]+padding[0],glob[1]+padding[1],glob[2]
            averagecolor = tuple(averagecolorer(color,players))
            init =1
            board = [ ]
            for i in range(sizeofboard_x):
                ki =[]
                for j in range(sizeofboard_y):
                    ki.append(ball((i,j),0,0))
                board.append(ki[:])
            redraw()
pygame.quit()

