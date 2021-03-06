import pygame
import sys
import time
pygame.init()
pygame.font.init()
M,N,grid_size,font_size,font_style1,font_style2=70,35,20,15,'C:\\WINDOWS\\Fonts\\HPSimplified_Rg.ttf','C:\\WINDOWS\\Fonts\\YuGothB.ttc'
sys.setrecursionlimit(M*N+100)
grids=[(i,j) for i in range(M) for j in range(N)]
font1,font2=pygame.font.Font(font_style1,font_size),pygame.font.Font(font_style2,font_size)
h1,h2=font1.render('psaikumar48@gmail.com',True,(0,0,0)).get_height()*1.2,font2.render('psaikumar48@gmail.com',True,(0,0,0)).get_height()*1.2
h=h1 if h1>h2 else h2
def path_finding_function1(lst,values=[1],n=0):
    if n<len(lst):
        (x,y)=lst[n]
        for i in [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]:
            if i in grids and i not in lst and i not in blocks:
                lst.append(i)
                values.append(values[n]+1)
        n+=1
        return path_finding_function1(lst,values,n)
    else:
        return lst,values
def path_finding_function2(op):
    point=op[-1]
    value=values[points.index(point)] if point in points else 0
    if value>1:
        (x,y)=point
        for l in [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]:
            if l in points and values[points.index(l)]==value-1:
                op.append(l)
                break
        return path_finding_function2(op)
    else:
        return [] if value==0 else op
def main_path_finding(start,end):
    global points,values
    points,values=path_finding_function1(lst=[end],values=[1],n=0)
    return path_finding_function2(op=[start])

def mousepress(msg,x,y,font_colour,active_colour,inactive_colour,font_style):
    pygame.font.init()
    font=pygame.font.Font(font_style,font_size)
    text=font.render(msg,True,font_colour)
    w,h=text.get_width(),text.get_height()
    colour=active_colour if (5*x-2*w)/5 <=position[0]<= (5*x+2*w)/5 and (5*y-2*h)/5 <= position[1]<= (5*y+2*h)/5 else inactive_colour
    pygame.draw.rect(screen,colour,((x-w/2-w/10,y-h/2-h/10,w+w/5,h+h/5)),0)
    screen.blit(text,(x-w/2,y-h/2))
    return ((5*x-2*w)/5,(5*x+2*w)/5,(5*y-2*h)/5,(5*y+2*h)/5)
n=1
def font_display():
    global n
    pygame.draw.rect(screen,(0,0,100), (0,N*grid_size,M*grid_size,4*h))
    mousepress('Start/End points : Double click',int(0.25*M*grid_size),int(N*grid_size+0.8*h),(255,255,255),(0,0,100),(0,0,100),font_style2)
    mousepress('To give obstacles : Single click',int(0.25*M*grid_size),int(N*grid_size+2*h),(255,255,255),(0,0,100),(0,0,100),font_style2)
    mousepress('To clear blocks : Left click',int(0.25*M*grid_size),int(N*grid_size+3.2*h),(255,255,255),(0,0,100),(0,0,100),font_style2)
    GL=mousepress('     Go!!    ',int(0.75*M*grid_size),int(N*grid_size+2*h),(0,0,255),(200,200,200),(255,255,255),font_style1)
    RL=mousepress(' Refresh ',int(0.75*M*grid_size),int(N*grid_size+3.2*h),(0,0,255),(200,200,200),(255,255,255),font_style1)
    if n<30: mousepress(Note,int(0.75*M*grid_size),int(N*grid_size+0.8*h),(0,255,0),(0,0,100),(0,0,100),font_style2)
    n=1 if n==60 else n+1
    return GL,RL
            
mloop=True
while mloop:
    screen = pygame.display.set_mode((M*grid_size,int(N*grid_size+4*h)))
    pygame.display.set_caption('MAZE')
    [pygame.draw.rect(screen,(255,0,0), (_[0]*grid_size,_[1]*grid_size,grid_size,grid_size),1) for _ in grids]
    loop,points_lst,blocks,path,Note,start_time,start_point=True,[],[],[],'Distance',time.time(),(0,0)
    while loop:
        pygame.display.update()
        position = pygame.mouse.get_pos()
        cordinates=(int(position[0]//grid_size),int(position[1]//grid_size))
        GL,RL=font_display()
        ev=pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                loop,mloop=False,False
            elif RL[0] <=position[0]<= RL[1] and RL[2] <= position[1]<= RL[3]  and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                loop=False 
            elif pygame.mouse.get_pressed()[0] and cordinates[0]<M and cordinates[1]<N:
                end_point,end_time=cordinates,time.time()
                if 0.15 < (end_time-start_time) < 0.3 and start_point==end_point and len(points_lst)<2 and cordinates not in points_lst:
                    pygame.draw.rect(screen,(255,255,255), (cordinates[0]*grid_size,cordinates[1]*grid_size,grid_size,grid_size))
                    points_lst.append(cordinates)
                    if cordinates in blocks: blocks.remove(cordinates)          
                elif cordinates not in blocks:
                    pygame.draw.rect(screen,(0,255,0), (cordinates[0]*grid_size,cordinates[1]*grid_size,grid_size,grid_size))
                    blocks.append(cordinates)
                    if cordinates in points_lst: points_lst.remove(cordinates)
                start_point,start_time=end_point,end_time
            elif pygame.mouse.get_pressed()[2] and cordinates[0]<M and cordinates[1]<N and cordinates in blocks+points_lst+path:
                pygame.draw.rect(screen,(0,0,0), (cordinates[0]*grid_size,cordinates[1]*grid_size,grid_size,grid_size))
                pygame.draw.rect(screen,(255,0,0),(cordinates[0]*grid_size,cordinates[1]*grid_size,grid_size,grid_size),1)
                points_lst.remove(cordinates) if cordinates in points_lst else path.remove(cordinates) if cordinates in path else blocks.remove(cordinates)     
            elif GL[0] <=position[0]<= GL[1] and GL[2] <= position[1]<= GL[3]  and pygame.mouse.get_pressed()[0]:
                [pygame.draw.rect(screen,(0,0,0), (_[0]*grid_size,_[1]*grid_size,grid_size,grid_size)) for _ in path if _ not in blocks]
                [pygame.draw.rect(screen,(255,0,0),(_[0]*grid_size,_[1]*grid_size,grid_size,grid_size),1) for _ in path if _ not in blocks]
                if len(points_lst)==0:
                    Note='Start/End points are missing'
                elif len(points_lst)==1:
                    Note='End point is missing'
                elif len(points_lst)==2:
                    path=main_path_finding(points_lst[0],points_lst[1])
                    Note=f' {len(path)-2} blocks' if path else 'No path found'
                    if not path: break 
                    path=path[1:-1]
                    [pygame.draw.rect(screen,(0,0,255), (_[0]*grid_size,_[1]*grid_size,grid_size,grid_size)) for _ in path]
                    [pygame.draw.rect(screen,(255,255,255), (_[0]*grid_size,_[1]*grid_size,grid_size,grid_size),1) for _ in path]
