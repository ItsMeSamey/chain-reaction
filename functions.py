import random
import math
import colorsys

def globalizer(sizeofboard_x,cx):
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
    return (delta_x,delta_y,text_size)


def averagecolorer(color,players):
    average =[0,0,0]
    for i in color:
        average[0]  += i[0]
        average[1]  += i[1]
        average[2]  += i[2]
    for i in range(len(average)):
        average[i] =int(155*(255 - average[i]/players)/255 +100)
    return average


def randomcolor():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    color = (a,b,c)
    g = (a + b + c)/3
    if g<25 and g>235:
        color = randomcolor()
    return color

def recolor(color,distinctcoloring):
    for i in range(len(color)):
        for j in range(i+1,len(color)):
            delta_c = ((color[i][0]-color[j][0])**2 + (color[i][1]-color[j][1])**2 + (color[i][2]-color[j][2])**2)**(1/2)
        if delta_c < distinctcoloring:
            color[j] =randomcolor()

def brightner(color):
    #final = (round(125*color[0]/255 +130),round(125*color[1]/255 +130),round(125*color[2]/255 +130))
    hsv=colorsys.rgb_to_hsv(color[0]/255,color[1]/255,color[2]/255)
    col = (hsv[0]*0.92+0.02,hsv[1]*0.95 +0.05,hsv[2]*0.95+0.05)
    coll = colorsys.hsv_to_rgb(col[0],col[1],col[2])
    colll=(coll[0]*255,coll[1]*255,coll[2]*255)
    return colll
def generate_random_hsv(num):
    color = []
    color_brighter=[]
    color_hsv=[]
    r=random.randint(0,1000)
    for i in range(num):
        color_hsv.append(((r+ i*1000/num)/1000, random.randint(200,1000)/1000,random.randint(250,1000)/1000))
    for col in color_hsv:
        colll = colorsys.hsv_to_rgb(col[0],col[1],col[2])
        coll=[]
        for i in colll:
            coll.append(255*i)
        color.append(tuple(coll))
    for col in color_hsv:
        colll = colorsys.hsv_to_rgb((((col[0]+0.03)*1000)%1000)/1000,(col[1]),(col[2])-0.05)
        coll=[]
        for i in colll:
            coll.append(255*i)
        color_brighter.append(tuple(coll))
    return (color,color_brighter)