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
        possibleBoards.append(randomBoard(app))
    app.ans.setBoard(random.choice(possibleBoards))

def generateStartEndColors(minStep,level,startColor=None):
    minStep-=1 # remove startColor
    minStep*=50-level*8 # increased closeness of color hues with increased level
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
    colorBoard = copy.deepcopy(board)
    row,col = random.randint(0,rows-1),random.randint(0,cols-1)
    board = createBoolBoard(board,row,col,[],0)

    # Fill first and last rows with color
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

# Create a board of booleans (True: block space, False = no block)
# Randomized DFS, terminate at 12 blocks
def createBoolBoard(board,row,col,visited,nBlocks):

    # Base Case: board already has 14 block spaces
    if nBlocks == 14:
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
        return createBoolBoard(board,row,col,visited,nBlocks)

    # If current node has unvisited neighbor, move to neighbor
    else:
        row,col = neighbor
        return createBoolBoard(board,row,col,visited,nBlocks+1)

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
