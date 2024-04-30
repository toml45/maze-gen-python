import sys, pygame
import random
import time

# ---------init stuff-----------
pygame.init()

size = width, height = 801, 801
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS =30

screen = pygame.display.set_mode(size)
pygame.display.set_caption('aaaaa')
screen.fill(BLACK)
clock = pygame.time.Clock()
#-------------------------------


                             #store the cell coords
w = 40                                              #cell width/height
cell_count = int(width/w)   
cell_grid = [[] for _ in range((cell_count*cell_count))]                        #no of cells
cell_visited = [False] * cell_count*cell_count      #visited thing for algorithm idk
cell_frontier = []                                  #kkeps track of the forntier cells
cell_visited_frontier = [False] *cell_count*cell_count

            

def drawGrid():
    for i in range(0, cell_count):
        for j in range(0, cell_count):
            pygame.draw.line(screen, WHITE, (i*w, j*w), (i*w+w, j*w))
            pygame.draw.line(screen, WHITE, (i*w+w, j*w), (i*w+w, j*w+w))
            pygame.draw.line(screen, WHITE, (i*w+w, j*w+w), (i*w, j*w+w))
            pygame.draw.line(screen, WHITE, (i*w, j*w+w), (i*w, j*w))
            

def del_right(x, y):
    pygame.draw.rect(screen, BLACK, pygame.Rect(x*w+1, y*w+1, 2*(w)-1, w-1))
    pygame.display.update()

def del_left(x, y):
    pygame.draw.rect(screen, BLACK, pygame.Rect(x*w-w+1, y*w+1, 2*(w)-1, w-1))
    pygame.display.update()

def del_up(x, y):
    pygame.draw.rect(screen, BLACK, pygame.Rect(x*w+1, y*w-w+1, w-1, 2*(w)-1))
    pygame.display.update()

def del_down(x, y):
    pygame.draw.rect(screen, BLACK, pygame.Rect(x*w+1, y*w+1, w-1, 2*(w)-1))
    pygame.display.update()

def changeColor(color, x, y):
    pygame.draw.rect(screen, color, pygame.Rect(x*w+1, y*w+1, w-1, w-1))
    pygame.display.update()

#draw base grid
drawGrid()
pygame.display.update()

#maze algorithm functions
def add_frontier(x, y):
    if x >= 0 and x < cell_count and y >= 0 and y < cell_count:
        if cell_visited[y*cell_count+x] == False and cell_visited_frontier[y*cell_count+x] == False:
            cell_visited_frontier[y*cell_count+x] = True
            cell_frontier.append((x,y))
            changeColor(BLUE, x, y)

def mark_cell(x, y):
    #hangeColor(GREEN, x, y)
    cell_visited[y*cell_count+x] = True
    
    add_frontier(x+1, y) 
    add_frontier(x, y+1)
    add_frontier(x-1, y)
    add_frontier(x, y-1)

def neighbors(x, y):
    n = []

    if x >= 0 and x < cell_count and y >= 0 and y < cell_count:
        if x > 0 and cell_visited[y*cell_count+x-1] == True:
            n.append((x-1, y))
        if x < cell_count-1 and cell_visited[y*cell_count+x+1] == True:
            n.append((x+1, y))
        if y < cell_count-1 and cell_visited[(y+1)*cell_count+x] == True:
            n.append((x, y+1))
        if y > 0 and cell_visited[(y-1)*cell_count+x] == True:
            n.append((x, y-1))
    
    return n
    
rand_x = random.randint(0, cell_count-1)
rand_y = random.randint(0, cell_count-1) # start
mark_cell(rand_x, rand_y)
pygame.display.update()
pygame.time.delay(50)

while len(cell_frontier) != 0:
    
    if len(cell_frontier) == 1:
        rand_frontier = 0
    else:
        rand_frontier = random.randint(0, len(cell_frontier)-1)
    
    n = neighbors(cell_frontier[rand_frontier][0],cell_frontier[rand_frontier][1])

    if len(n) == 1:
        rand_neighbor = 0
    else:
        rand_neighbor = random.randint(0, len(n)-1)


    nx = n[rand_neighbor][0]
    ny = n[rand_neighbor][1]
    fy = cell_frontier[rand_frontier][1]
    fx = cell_frontier[rand_frontier][0]

    cell_grid[ny*cell_count+nx].append((fx, fy))
    cell_grid[fy*cell_count+fx].append((nx, ny))
    
    cell_frontier.pop(rand_frontier)
    
    if nx > fx:
        del_left(nx, ny)
        
    if nx < fx:
        del_right(nx, ny)
        
    if ny > fy:
        del_up(nx, ny)
        
    if ny < fy:
        del_down(nx, ny)
    
    mark_cell(fx, fy)
    pygame.display.update()
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()



q = []
q_visited = [False] * cell_count * cell_count
q.append((rand_x, rand_y))
q_visited[rand_y*cell_count+rand_x] = True
prev = [() for _ in range(cell_count*cell_count)]

changeColor(RED, fx, fy)
changeColor(GREEN, rand_x, rand_y)
pygame.display.update()

while len(q) != 0:
    a = q.pop(0)
    if a == (fx, fy):
        break
    for i in cell_grid[a[1]*cell_count+a[0]]:
        if q_visited[i[1]*cell_count+i[0]] == False:
            q.append(i)
            q_visited[i[1]*cell_count+i[0]] = True
            changeColor((43, 43, 43), i[0], i[1])
            prev[i[1]*cell_count+i[0]] = (a[0], a[1])
            pygame.display.update()
            pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        
changeColor(RED, fx, fy)
changeColor(GREEN, rand_x, rand_y)
pygame.display.update()

cur = prev[fy*cell_count+fx]
while cur != (rand_x, rand_y):
    changeColor((0, 128, 128), cur[0], cur[1])
    pygame.display.update()
    cur = prev[cur[1]*cell_count+cur[0]]
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        