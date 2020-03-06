import pandas as pd
import pygame
# M*w>=340
M,N=40,30
w,h=20,20
x_Window_size=(M+1)*w
y_Window_size=(N+1)*h
pygame.init()
def show(x,y,colour,boundary_size):
    pygame.draw.rect(screen,colour, (x*w,y*h,w,h),boundary_size)
    pygame.display.update()
    
def text_objects(text,font,fc):
    textSurface = font.render(text,True,fc)
    return textSurface, textSurface.get_rect()

def mousepress(msg,x,y,w,h,ac,ic,fc,fs):
    mouse=pygame.mouse.get_pos()
    if x+w>=mouse[0]>=x and y+h>=mouse[1]>=y:
        pygame.draw.rect(screen,ac,((x,y,w,h)),0)
    else:
        pygame.draw.rect(screen,ic,((x,y,w,h)),0)
    pygame.font.init()
    smallText=pygame.font.Font('freesansbold.ttf',fs)
    textSurf, textRect=text_objects(msg,smallText,fc)
    textRect.center=(x+(w/2),y+(h/2))
    screen.blit(textSurf, textRect)
    pygame.display.update()

def f2(ip):
    opl=(ip[0],ip[1]-1)
    opr=(ip[0],ip[1]+1)
    opt=(ip[0]-1,ip[1])
    opb=(ip[0]+1,ip[1])
    ip=[opl,opr,opt,opb]
    op=[]
    for st in ip:
        if 0<=st[0]<=M and 0<=st[1]<=N:
            op.append(st)
    return op
def f3(end,op,A):
    op.append(end)
    steps=A.Steps[A[A.Cordinates==end].index.tolist()[0]]
    if steps==1:
        return op
    else:
        for i in f2(end):
            isteps=A.Steps[A[A.Cordinates==i].index.tolist()[0]]
            if isteps==steps-1:
                return f3(i,op,A)
                break           
def f1(start,ip,block):
    step_count={'Cordinates':[ip],'Steps':1}
    A=pd.DataFrame(step_count)
    try:
        for j in range((M+1)*(N+1)):
            ip=A.Cordinates[j]
            for i in f2(ip):
                steps=A.Steps[A[A.Cordinates==ip].index.tolist()[0]]
                if  not(i in block) and sum(A.Cordinates==i)==0 and steps != 0:
                    A=A.append({'Cordinates' :i ,'Steps' :steps+1 } , ignore_index=True)
                elif i in block and sum(A.Cordinates==i)==0:
                    A=A.append({'Cordinates' :i ,'Steps' : 0 } , ignore_index=True)
    except KeyError:
        pass
    if sum(A.Cordinates==start)==0:
        return []
    else:
        return f3(start,[],A)
    
    
    
    
    
mloop=True
while mloop:
    screen = pygame.display.set_mode((x_Window_size,y_Window_size+55))
    pygame.display.set_caption('Path finding')
    screen.fill((0,0,100))
    pygame.draw.rect(screen,(255,255,255), (0,(N+1)*h,x_Window_size,60),0)
    pygame.display.update()
    for i in range(M+1):
        for j in range(N+1):
            show(i,j,(255,0,0),1)
    block=[]
    point=[]
    loop=True
    while loop:
        ev=pygame.event.get()
        mousepress('Go!',x_Window_size-100,5+(N+1)*h,80,20,(255,0,0),(200,0,0),(255,255,255),15)
        mousepress('Refresh',x_Window_size-100,30+(N+1)*h,80,20,(0,255,0),(0,200,0),(255,255,255),15)
        mousepress('Start/End points : Right click ',0,5+(N+1)*h,250,20,(255,255,255),(255,255,255),(255,0,0),17)
        mousepress('Obstacles : Left click',0,30+(N+1)*h,250,20,(255,255,255),(255,255,255),(255,0,0),17)
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                loop=False
                mloop=False
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x,y=int(pos[0]//w),int(pos[1]//h)
                if x<M+1 and y<N+1:
                    block.append((x,y))
                    show(x,y,(255,255,0),0)
                elif x_Window_size-20 >= pos[0] >= x_Window_size-100 and (N+1)*h+25 >= pos[1] >=(N+1)*h+5 and len(point) >=2:
                    mousepress('processing...',x_Window_size-100,5+(N+1)*h,80,20,(255,0,0),(200,0,0),(255,255,255),12)
                    if len(f1(point[0],point[1],block)) != 0:
                        lst=f1(point[0],point[1],block)
                        lst.pop(0)
                        lst.pop(-1)
                        for i in lst:
                            show(i[0],i[1],(0,155,0),0)
                            show(i[0],i[1],(255,255,255),3)
                        mousepress('Go!',x_Window_size-100,5+(N+1)*h,80,20,(255,0,0),(200,0,0),(255,255,255),15)
                    else:
                        font = pygame.font.SysFont("comicsansms", int(y_Window_size/10))
                        text = font.render("No path found", True, (255,255,255))
                        screen.blit(text,((x_Window_size/2) - text.get_width() // 2, (y_Window_size/2) - text.get_height() // 2))
                        pygame.display.update()
                elif x_Window_size-20 >= pos[0] >= x_Window_size-100 and (N+1)*h+50 >= pos[1] >=(N+1)*h+30:
                    pygame.quit()
                    loop=False
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x,y=int(pos[0]//w),int(pos[1]//h)
                if len(point)<2:
                    show(x,y,(255,255,255),0)
                    point.append((x,y))