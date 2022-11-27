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

def generateAnswerBoard(app):
    possibleBoards = []
    app.ans = GameBoard()
    if app.level == 1:
        possibleBoards.append(linearBoard(1))
    if app.level >= 2:
        possibleBoards.append(linearBoard(2))
        possibleBoards.append(tBoard(2))
    if app.level >= 3:
        possibleBoards.append(randomBoard())
    if app.level >= 4: pass
    if app.level >= 5: pass
    app.ans.setBoard(random.choice(possibleBoards))

    # For testing:
    # app.ans.setBoard([[ColorBlock((255,102,0),app.blockSize),
    #                       ColorBlock((255,153,0),app.blockSize),
    #                       ColorBlock((255,204,0),app.blockSize)]])

def generateStartEndColors(minStep,level,startColor=None):
    minStep-=1
    minStep*=50-level*9
    if startColor == None:
        startColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    endColor = [0,0,0]
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

def linearBoard(level=1):
    totalBlocks = random.randint(5,7)
    startColor,endColor = generateStartEndColors(totalBlocks,level)
    colors = interpolateColors(startColor,endColor,totalBlocks)
    board = []
    for i in range(totalBlocks):
        board.append([ColorBlock(colors[i])])
    return board

def tBoard(level=2):
    # Create horizontal branch
    cols = random.randint(4,6)
    startColor,endColor = generateStartEndColors(cols,level)
    colors = interpolateColors(startColor,endColor,cols)
    board = [[ColorBlock(color) for color in colors]]

    # Create vertical branch from random horizontal position
    tCol = random.randint(0,cols-1)
    rows = random.randint(4,6)
    startColor = colors[tCol]
    startColor,endColor = generateStartEndColors(rows,level,startColor)
    colors = interpolateColors(startColor,endColor,rows)
    for row in range(rows-1):
        board.append([False for i in range(cols)])
    for row in range(len(board)):
        board[row][tCol] = ColorBlock(colors[row])
    return board


# print(interpolateColors((255,102,0),(255,204,0),3))
# print(generateStartEndColors(2))
# print(linearBoard(3))

#maxDim = 6x7
def randomBoard(level=3):
    rows,cols = 7,6
    board = [[False for i in range(cols)] for j in range(rows)]
    colorBoard = copy.deepcopy(board)
    row,col = random.randint(0,rows-1),random.randint(0,cols-1)
    board = createBoolBoard(board,row,col,1)

    # Fill first and last rows with color
    totalBlocks = 6
    start,end = generateStartEndColors(totalBlocks,level)
    colors = interpolateColors(start,end,totalBlocks)
    colorBoard[0] = [ColorBlock(colors[i]) for i in range(len(colorBoard[0]))]
    start,end = generateStartEndColors(totalBlocks,level)
    colors = interpolateColors(start,end,totalBlocks)
    colorBoard[-1] = [ColorBlock(colors[i]) for i in range(len(colorBoard[-1]))]

    # Fill columns with color
    colorBoard = [list(n) for n in zip(*colorBoard)]
    for row in range(len(colorBoard)):
        totalBlocks = len(colorBoard[row])
        start,end = colorBoard[row][0].rgb,colorBoard[row][-1].rgb
        colors = interpolateColors(start,end,totalBlocks)
        colorBoard[row] = [ColorBlock(colors[i]) for i in range(len(colorBoard[row]))]
    colorBoard = [list(n) for n in zip(*colorBoard)]
    print(colorBoard)

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == False:
                colorBoard[i][j] = False

    # Remove empty rows and cols to center board
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
# Randomized DFS, terminated at 12 blocks
def createBoolBoard(board,row,col,nBlocks):
    rows,cols = len(board),len(board[0])
    if nBlocks == 13:
        return board
    if board[row][col] == False:
        nBlocks += 1
        board[row][col] = True
    nrow,ncol = random.choice([(row+1,col),(row-1,col),(row,col+1),(row,col-1)])
    if (0 <= nrow < rows and 0 <= ncol < cols):
        return createBoolBoard(board,nrow,ncol,nBlocks)
    else:
        return createBoolBoard(board,row,col,nBlocks)
