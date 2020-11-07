pred={}
size = 25
grid = [ [ ' ' for j in range(size)] for i in range(size)]
getXY = lambda x_y : tuple(map(int,x_y.split('_')))
prevPath=[]
getKey  = lambda x,y : '%d_%d' % (x,y)
latestWall = None
wall=set()
def explore(i,j):
    toBe=[]
    if i!=0 and grid[i-1][j] == ' ':#up
        toBe.append((i-1,j))
    if j!=0 and grid[i][j-1] == ' ':#left
        toBe.append((i,j-1))
    if i!= size-1 and grid[i+1][j] == ' ': #down
        toBe.append((i+1,j))
    if j!= size-1 and grid[i][j+1] == ' ': #right
        toBe.append((i,j+1))
    return toBe


def pairPresent(pair,lst):
    for i in lst:
        if i[0]==pair[0] and i[1] == pair[1]:
            return True
    return False
def path_finder():
    size= len(grid)
    global pred
    visited=[[False for col in range(size)] for row in range(size)]
    visited[s_x][s_y]=True
    parent = getKey(s_x,s_y)
    pred[parent]=None
    toBeVisited=explore(s_x,s_y)
    for i,j in toBeVisited:
        pred[getKey(i,j)] =parent
    while toBeVisited:
        temp=set()
        for i,j in toBeVisited:
            if i==t_x and j==t_y :
                return True
            visited[i][j]=True
            parent = getKey(i,j)
            for x,y in explore(i,j):
                if (not visited[x][y] )and  not pairPresent((x,y), toBeVisited):#cycle detection
                    pred[getKey(x,y)] =parent
                    temp.add((x,y))
        toBeVisited=temp
    return visited[t_x][t_y]

from tkinter import *
import tkMessageBox

def resetGrid(all=True):
    global clickCount,grid,prevPath,wall
    for i,j in prevPath:
        if (i,j) not in wall:
            changeLabelColor(i,j,'yellow',True)
    if all:
        for i,j in wall:
            grid[i][j]=' '
            changeLabelColor(i,j,'yellow',True)
        if s_x>-1:
            changeLabelColor(s_x,s_y,'yellow',True)
        if t_x >-1:
            changeLabelColor(t_x,t_y,'yellow',True)
        clickCount=0
        prevPath=[]
        wall=set()

def calculate():
    global prevPath
    if clickCount <2:
        tkMessageBox.showinfo('Warning','Specify Source and Destination ')
        return 
    if path_finder():
        resetGrid(False)
        nextHop = pred[getKey(t_x,t_y)]
        startNode = getKey(s_x,s_y)
        path=[]
        while nextHop != startNode:
            path.append(getXY(nextHop))
            nextHop = pred[nextHop]
        prevPath = path
        for x,y in path[::-1]:
            changeLabelColor(x,y,'blue')
        Label(root,text='Shortest Path Distance : %d' % (len(path)),fg="red").grid(row=size+4,column=size)
    else:
        tkMessageBox.showinfo('Result','No Path Found !')


root = Tk()

root.geometry('500x500')
root.title('Shortest Path Visualizer')
clickCount = 0
s_x,s_y ,t_x,t_y = -1,-1,-1,-1
def onclick(r,c):
    global s_x,s_y,t_x,t_y,clickCount,grid,wall,latestWall
    clickCount+=1
    if clickCount ==1:
        s_x,s_y = r,c
        color = 'green'
    elif clickCount ==2:
        t_x,t_y = r,c
        color='red'
    else:
        reset = grid[r][c] == '*'
        grid[r][c]= ' ' if reset  else '*'
        color='yellow' if reset else 'black'
        wall.remove((r,c)) if reset else wall.add((r,c))
        if not reset:
            latestWall = r,c
    changeLabelColor(r,c,color,clickCount>2)

def changeLabelColor(r,c,color,addEvent=False):
    label = Label(root,fg='black',bg=color,width=2,height=1,borderwidth=1,relief='solid')
    label.grid(row=r,column=c)
    if addEvent:
        label.bind("<Button-1>",lambda e,r=r,c=c:onclick(r,c))

def drawWall(direction):
    global wall,grid,latestWall
    if len(wall) == 0:
        tkMessageBox.showinfo('Info','Atleast one wall should be present')
        return
    elif not latestWall or clickCount <2:
        return
    x,y = latestWall
    if direction == 'left':
        for c in range(y-1,-1,-1):
            if (s_x,s_y) != (x,c) and (t_x,t_y) != (x,c):
                changeLabelColor(x,c,'black',True)
                wall.add((x,c))
                latestWall = x,c
                if grid[x][c] == '*':
                    break
                grid[x][c]='*'

    elif direction == 'right':
        for c in range(y+1,size):
            if (s_x,s_y) != (x,c) and (t_x,t_y) != (x,c):
                changeLabelColor(x,c,'black',True)
                wall.add((x,c))
                latestWall = x,c
                if grid[x][c] == '*':
                    break
                grid[x][c]='*'

    elif direction == 'down':
        for r in range(x+1,size):
            if (s_x,s_y) != (r,y) and (t_x,t_y) != (r,y):
                changeLabelColor(r,y,'black',True)
                wall.add((r,y))
                latestWall = r,y
                if  grid[r][y] =='*' :
                    break
                grid[r][y]='*'

    else:
        for r in range(x-1,-1,-1):
            if (s_x,s_y) != (r,y) and (t_x,t_y) != (r,y):
                changeLabelColor(r,y,'black',True)
                wall.add((r,y))
                latestWall = r,y
                if  grid[r][y] =='*' :
                    break
                grid[r][y]='*'

colorGrid = [ [ Label(root,fg='black',bg='yellow',width=2,height=1,borderwidth=1,relief='solid') for j in range(size) ] for i in range(size) ]


for i in range(0,size):
    for j in range(0,size):
        colorGrid[i][j].grid(row=i,column=j)
        colorGrid[i][j].bind("<Button-1>",lambda e,r=i,c=j:onclick(r,c))

Button(root,text='Create Shortest Path',fg='blue',bg='orange',command=calculate).grid(row=size,column=size)
Button(root,text='Clear All',fg='blue',bg='orange',command=resetGrid).grid(row=size+1,column=size)
Button(root,text='Clear Path',fg='blue',bg='orange',command=lambda : resetGrid(False)).grid(row=size+2,column=size)

Button(root,text='Up',fg='blue',bg='orange',command=lambda : drawWall('up')).grid(row=size,column=size+1)
Button(root,text='Down',fg='blue',bg='orange',command= lambda : drawWall('down')).grid(row=size+1,column=size+1)
Button(root,text='Left',fg='blue',bg='orange',command=lambda : drawWall('left')).grid(row=size+2,column=size+1)
Button(root,text='Right',fg='blue',bg='orange',command=lambda : drawWall('right')).grid(row=size+3,column=size+1)

root.mainloop()

