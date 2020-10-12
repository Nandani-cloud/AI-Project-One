#  
# Nandani Patidar & Julian Torres
#
# AI Assignment One - Fall 2020
#
# Implementation of Repeated Backward A* algorithm
#
from maze import *
from random import randrange, shuffle
import heapq as hp
import itertools
import copy as cp
import time


# Initiate H, G and F grids 
def initiateGrid(maze):
    global gGrid
    for row in maze:
        hRow = []
        for block in row:   
            hRow.append(None)
        hGrid.append(hRow)
        
    gGrid = cp.deepcopy(hGrid)
 
# Initialize cost of every node from its adjacent node as 1  
def initiateCostGrid(maze):
    global costGrid              
    for row in maze:
        hRow = []
        for block in row:   
            hRow.append(1)
        costGrid.append(hRow)
          
def upd_H_Val(state):
    hValue = (state[0]- sGoal[0]) + (state[1]- sGoal[1])
    hGrid[state[0]][state[1]] = hValue
    return hValue  

def upd_G_Val(state, gValue):      
    gGrid[state[0]][state[1]] = gValue
    return gValue

def computePath():
    while (len(openList)>=1 and gGrid[sGoal[0]][sGoal[1]] > openList[0][0]):
                                                            ##        print("Open List before pop: ", openList)
        s = hp.heappop(openList)
        sCoordinates = (s[2][0], s[2][1])
                                                           ##print("sCoordinates: ", sCoordinates)   
                                                           ##print("Open List: ", openList)
        closedList.append(s)

        # Exploring adjacent blocks of state s 
        adj_block_X = [sCoordinates[0]-1, sCoordinates[0], sCoordinates[0]+1,  sCoordinates[0]]
        adj_block_Y = [sCoordinates[1],  sCoordinates[1]-1, sCoordinates[1], sCoordinates[1]+1]
        
        for i in range(4):
            x = adj_block_X[i]
            y = adj_block_Y[i]
                                                                ##            print("x, y ", x, y)
            if not (x in range(0, mazeDimension) and y in range(0, mazeDimension)):
               continue
                                                          ##            print("Counter: ", counter)
                                                          ##print("search: ", search[x][y])
            if search[x][y] < counter:
                gGrid[x][y] = float('inf')
                search[x][y] = counter   
                                                            ##            print ("G grid: ", gGrid[x][y])
                                                            ##            print("G grid s: ", gGrid[sCoordinates[0]][sCoordinates[1]])
            if gGrid[x][y] > gGrid[sCoordinates[0]][sCoordinates[1]] + costGrid[x][y]:
                gGrid[x][y] = gGrid[sCoordinates[0]][sCoordinates[1]] + costGrid[x][y]
                tree[(x, y)] = sCoordinates
                gVal = gGrid[x][y]
                hVal = upd_H_Val((x, y))
                fVal = gVal + hVal    
                for i in range(len(openList)):              # Logic taken from: https://stackoverflow.com/questions/13800947/deleting-from-python-heapq-in-ologn/13801331
                    if openList[i][2] == (x, y):
                        openList[i], openList[-1] = openList[-1], openList[i]
                        openList.pop()
                        hp.heapify(openList)
                                                            ##                        print("After heapify open List: ", openList)
                        break
            
                hp.heappush(openList, (fVal, gVal, (x, y)))
                                                            ##                print("Open List: ", openList)
                                                                                                                        


def repeatedbackwardAStar(maze):

    # Records start time of program execution
    startTime = time.time()
    
    global hGrid, gGrid, costGrid 
    hGrid =[]
    gGrid = []
    costGrid = []
    
    a.displaySingleMaze(maze)

    # Call function to initialize grids
    initiateGrid(maze)
    initiateCostGrid(maze)

    global counter, search
    counter = 0
    search = [ ]
    fullPath = [ ]

    # Put search for every state in the grid as 0
    for row in maze:
        hRow = [ ]
        for block in row:
            hRow.append(0)
        search.append(hRow)

    # Defining start and goal         
    global sGoal, sStart, openList, closedList, mazeDimension, tree
    sGoal = (0, 0)
    mazeDimension = len(maze)
    sStart = (mazeDimension-1, mazeDimension-1)
    flagQuit = False
    while(not(sStart == sGoal)):

        # A tree which stores parent value of a node 
        tree = {} 
        counter = counter + 1
        # Updating g, h, f and search values of start state 
        gStart = 0
        
        upd_G_Val(sStart, 0)
        hStart = upd_H_Val(sStart)
        fStart = gStart + hStart                                                               
        search[sStart[0]][sStart[1]] = counter

        # Upadting g and search for goal state 
        gGoal = float('inf')
        upd_G_Val(sGoal, gGoal)
        search[sGoal[0]][sGoal[1]] = counter
        
        openList = []
        closedList = []
        # Push start state into open list which is heap 
        hp.heappush(openList, (fStart, gStart , sStart))

        # Calling computePath 
        computePath()
        
        if (len(openList) == 0):
            print("No path exists to target.")
            a.displaySingleMazeWithPath(fullPath, costGrid)
            flagQuit = True
            break
       
        # Getting path from the tree
        pre =()
        lastValue = sGoal
        path = [lastValue]
        while not(pre == sStart):
            pre =(tree[lastValue])
            path.insert(0, pre)
            lastValue = pre
       
        # Displays path on the maze
    ##    a.displaySingleMazeWithPath(path, costGrid)

        
        # Agent start moving from start point towards goal by iterating the blocks stored in the path
        for i in path:
                                                                ##        print("i: ", i)
                                                                ##        print("Maze %s  %s", maze[i[0]][i[1]])
            # checks if a block is equal to 1 that means it is unblocked                                                    
            if maze[i[0]][i[1]] == 1:
                sStart = i
                
                fullPath.append(sStart) 
                
                
                # Explore adjacent blocks when robot moves on the estimated shortest path 
                adj_block_X = [sStart[0]+1, sStart[0], sStart[0]-1, sStart[0]]
                adj_block_Y = [sStart[1], sStart[1]+1, sStart[1], sStart[1]-1]
            
                for i in range(4):
                    x = adj_block_X[i]
                    y = adj_block_Y[i]
                    if not (x in range(0, mazeDimension) and y in range(0, mazeDimension)):
                       continue
                    
                    # checks for adjacent blocks while moving and update thier cost to infinity if blocked
                    if maze[x][y] == 0:
                        costGrid[x][y] = float('inf')
                    
                                                                    ##            print("Updated start state: ", sStart)
            else:
    ##            a.displaySingleMazeWithPath(path, costGrid)
                costGrid[i[0]][i[1]] = float('inf')
                break
    ##    a.displaySingleMazeWithPath(fullPath, costGrid)

    if flagQuit is not True:
        print("I reached the target")
        print("Path from start state to goal state: ")
        a.displaySingleMazeWithPath(fullPath, costGrid)
        print("Time to execute the program by repeated backward A* is %s seconds" % (time.time() - startTime))
                    
    

   

 

                




