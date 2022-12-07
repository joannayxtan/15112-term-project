from cmu_112_graphics import *
import random
from classes import *

# RGB Interpolation
# Takes start/end RGB and number of steps to interpolate
def interpolateColors(startColor,endColor,totalBlocks):
    startR,startG,startB = startColor
    endR,endG,endB = endColor
    diffR,diffG,diffB = endR-startR,endG-startG,endB-startB
    colors = []
    for i in range(0, totalBlocks):
        r = round(startR+i*diffR/(totalBlocks-1))
        g = round(startG+i*diffG/(totalBlocks-1))
        b = round(startB+i*diffB/(totalBlocks-1))
        colors.append((r,g,b))
    return colors

# Generate all possible answer boards for that level and choose one
def generateAnswerBoard(app):
    possibleBoards = []
    app.ans = GameBoard()
    if app.level == 1:
        possibleBoards.append(linearBoard(app))
    if app.level >= 2:
        possibleBoards.append(linearBoard(app))
        possibleBoards.append(tBoard(app))
    if app.level >= 3:
        possibleBoards = [randomBoard(app)]
    if app.level == 4:
        possibleBoards.append(primsRandomBoard(app))
    if app.level == 5:
        possibleBoards = [randomBoard(app),primsRandomBoard(app)]
    app.ans.setBoard(random.choice(possibleBoards))

def generateStartEndColors(minStep,level,startColor=None):
    minStep-=1 # remove startColor
    minStep*=50-level*8 # increased closeness of color hues with increased level
    originalStartColor = startColor
    if startColor == None:
        startColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    endColor = [0,0,0]

    # Randomly choose an end r,g,b
    for i in range(len(startColor)):
        if startColor[i] <= minStep:
            endColor[i] = random.randint(minStep,255)
        elif startColor[i] >= 255-minStep:
            endColor[i] = random.randint(0,255-minStep)
        else:
            num1 = random.randint(0,startColor[i]-minStep)
            num2 = random.randint(startColor[i]+minStep,255)
            endColor[i] = random.choice((num1,num2))
    if endColor == [255,255,255] or startColor == [255,255,255]:
        return generateStartEndColors(minStep,level,originalStartColor)
    return startColor,tuple(endColor)

##########################################
# All Possible Boards
##########################################

"""
For all boards:
True: blockspace, False: not block space
"""

# Create linear board with random colors and random num of blocks
def linearBoard(app):
    totalBlocks = random.randint(5,7)
    startColor,endColor = generateStartEndColors(totalBlocks,app.level)
    colors = interpolateColors(startColor,endColor,totalBlocks)
    board = []
    for i in range(totalBlocks):
        board.append([ColorBlock(colors[i])])
    return board

# Create T-shaped board with random colors and random num of blocks
def tBoard(app):

    # Create horizontal branch
    cols = random.randint(4,6)
    startColor,endColor = generateStartEndColors(cols,app.level)
    colors = interpolateColors(startColor,endColor,cols)
    board = [[ColorBlock(color) for color in colors]]

    # Create vertical branch from random horizontal position
    tCol = random.randint(0,cols-1)
    rows = random.randint(4,6)
    startColor = colors[tCol]
    startColor,endColor = generateStartEndColors(rows,app.level,startColor)
    colors = interpolateColors(startColor,endColor,rows)
    for row in range(rows-1):
        board.append([False for i in range(cols)])
    for row in range(len(board)):
        board[row][tCol] = ColorBlock(colors[row])
    return board

# Create board with random shape, colors, and num of blocks
# maximum dimensions = 6x7
def randomBoard(app):
    rows,cols = 5+(app.level-3),6 # Level 3: 5 rows, level 4: 6 rows, level 5: 7 rows
    board = [[False for i in range(cols)] for j in range(rows)]
    row,col = random.randint(0,rows-1),random.randint(0,cols-1)
    board = createBoolBoard(app,board,row,col,[],0)
    return fillBoard(app,board)

# Create a board of booleans (True: block space, False = no block)
# Randomized DFS
# Source: https://www.algosome.com/articles/maze-generation-depth-first.html
def createBoolBoard(app,board,row,col,visited,nBlocks):

    # Base Case: board already has enough block spaces
    if nBlocks == app.numBlocks:
        return board

    # Add a block space
    if (row,col) not in visited:
        board[row][col] = True
        visited.append((row,col))

    # Look for neighbors
    neighbor = getNeighbors(board,row,col)

    # If all neighbors have been visited, return to last visited node
    if neighbor == None:
        visited.pop()
        row,col = visited[-1]
        return createBoolBoard(app,board,row,col,visited,nBlocks)

    # If current node has unvisited neighbor, move to neighbor
    else:
        row,col = neighbor
        return createBoolBoard(app,board,row,col,visited,nBlocks+1)

def getNeighbors(board,row,col):
    rows,cols = rows,cols = len(board),len(board[0])
    neighbors = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
    i = 0

    # Find unvisited and valid neighbors
    while i < len(neighbors):
        row,col = neighbors[i]
        if 0 <= row < rows and 0 <= col < cols and board[row][col] == False:
            i += 1
        else:
            neighbors.pop(i)
    if neighbors == []:
        return None

    # Randomly select neighbor
    return random.choice(neighbors)

# Create a board of booleans (True: block space, False = no block)
# Randomized Prim's Algorithm
# Source: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
def primsRandomBoard(app):
    if app.numBlocks <= 14:
        rows,cols = 7,6
    else:
        rows,cols = 9,9
    board = [[False for i in range(cols)] for j in range(rows)]
    row,col = random.randint(1,rows-2),random.randint(1,cols-2)
    board[row][col] = True

    neighbors = set([(row-1,col),(row,col-1),(row+1,col),(row,col+1)])
    '''
    for neighbor in neighbors:
        i,j = neighbor
        board[i][j] = False
    '''

    nBlocks = app.numBlocks
    while(len(neighbors) != 0 and nBlocks != 0):

        # Pick a random block
        # Source: https://www.geeksforgeeks.org/retrieve-elements-from-python-set/
        nextBlock = next(iter(neighbors))
        row,col = nextBlock

        # Check if block is on left edge
        if col != 0:
            if board[row][col-1] == False and board[row][col+1] == True:
                numNeighbors = countNeighbors(board,nextBlock)
                if numNeighbors < 2:
                    board[row][col] = True
                    nBlocks -=1

                    if row != 0 and board[row-1][col] != True:
                        neighbors.add((row-1,col))

                    if row != rows-1 and board[row+1][col] != True:
                        neighbors.add((row+1,col))

                    if board[row][col-1] != True:
                        neighbors.add((row,col-1))
                temp = list(neighbors)
                temp.remove((row,col))
                neighbors = set(temp)
                continue

        if row != 0:
            if board[row-1][col] == False and board[row+1][col] == True:
                numNeighbors = countNeighbors(board,nextBlock)
                if numNeighbors < 2:
                    board[row][col] = True
                    nBlocks -=1

                    if board[row-1][col] != True:
                        neighbors.add((row-1,col))

                    if col != 0 and board[row][col-1] != True:
                        neighbors.add((row,col-1))

                    if col != rows-1 and board[row][col+1] != True:
                        neighbors.add((row,col+1))

                temp = list(neighbors)
                temp.remove((row,col))
                neighbors = set(temp)
                continue

        if row != rows-1:
            if board[row+1][col] == False and board[row-1][col] == True:
                numNeighbors = countNeighbors(board,nextBlock)
                if numNeighbors < 2:
                    board[row][col] = True
                    nBlocks -=1

                    if board[row+1][col] != True:
                        neighbors.add((row+1,col))

                    if col != 0 and board[row][col-1] != True:
                        neighbors.add((row,col-1))

                    if col != rows-1 and board[row][col+1] != True:
                        neighbors.add((row,col+1))

                temp = list(neighbors)
                temp.remove((row,col))
                neighbors = set(temp)
                continue

        if col != cols-1:
            if board[row][col+1] == False and board[row][col-1] == True:
                numNeighbors = countNeighbors(board,nextBlock)
                if numNeighbors < 2:
                    board[row][col] = True
                    nBlocks -=1

                    if board[row][col+1] != True:
                        neighbors.add((row,col+1))

                    if row != rows-1 and board[row+1][col] != True:
                        neighbors.add((row+1,col))

                    if row != 0 and board[row-1][col] != True:
                        neighbors.add((row-1,col))

                temp = list(neighbors)
                temp.remove((row,col))
                neighbors = set(temp)
                continue

        temp = list(neighbors)
        temp.remove((row,col))
        neighbors = set(temp)

    # for i in range(0,rows):
    #     for j in range(0,cols):
    #         if board[i][j] == None:
    #             board[i][j] = False
    return fillBoard(app,board)

def countNeighbors(board,block):
    num = 0
    row,col = block
    if (board[row-1][col] == True):
        num += 1
    if (board[row+1][col] == True):
        num += 1
    if (board[row][col-1] == True):
        num += 1
    if (board[row][col+1] == True):
        num += 1
    return num

def fillBoard(app,board):
    rows,cols = len(board),len(board[0])
     # Fill first and last rows with color
    colorBoard = copy.deepcopy(board)
    totalBlocks = cols
    start,end = generateStartEndColors(totalBlocks,app.level)
    colors = interpolateColors(start,end,totalBlocks)
    colorBoard[0] = [ColorBlock(colors[i]) for i in range(len(colorBoard[0]))]
    start,end = generateStartEndColors(totalBlocks,app.level)
    colors = interpolateColors(start,end,totalBlocks)
    colorBoard[-1] = [ColorBlock(colors[i]) for i in range(len(colorBoard[-1]))]

    # Fill columns with color
    colorBoard = [list(n) for n in zip(*colorBoard)] # Transpose matrix
    for row in range(len(colorBoard)):
        totalBlocks = len(colorBoard[row])
        start,end = colorBoard[row][0].rgb,colorBoard[row][-1].rgb
        colors = interpolateColors(start,end,totalBlocks)
        colorBoard[row] = [ColorBlock(colors[i]) for i in range(len(colorBoard[row]))]
    colorBoard = [list(n) for n in zip(*colorBoard)] # Transpose back

    # Remove blocks that are not in block spaces
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == False:
                colorBoard[i][j] = False

    # Remove empty rows and cols so board can be centered
    rows,cols = len(colorBoard),len(colorBoard[0])
    temp = []
    for row in colorBoard:
        if any(row):
            temp.append(row)

    # Transpose temp to remove cols
    temp = [list(n) for n in zip(*temp)]
    finalBoard = []
    for row in temp:
        if any(row):
            finalBoard.append(row)

    # Transpose colorBoard back to original dim
    finalBoard = [list(n) for n in zip(*finalBoard)]
    return finalBoard
