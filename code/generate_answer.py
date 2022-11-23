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
    if app.level >= 3: pass
    if app.level >= 4: pass
    if app.level >= 5: pass
    app.ans.setBoard(random.choice(possibleBoards))

    # For testing:
    # app.ans.setBoard([[ColorBlock((255,102,0),app.blockSize),
    #                       ColorBlock((255,153,0),app.blockSize),
    #                       ColorBlock((255,204,0),app.blockSize)]])

def generateStartEndColors(minStep,level,startColor=None):
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
    startColor,endColor = generateStartEndColors(totalBlocks-1,level)
    colors = interpolateColors(startColor,endColor,totalBlocks)
    board = []
    for i in range(totalBlocks):
        board.append([ColorBlock(colors[i])])
    return board

def tBoard(level=2):
    # Create horizontal branch
    cols = random.randint(4,6)
    startColor,endColor = generateStartEndColors(cols-1,level)
    colors = interpolateColors(startColor,endColor,cols)
    board = [[ColorBlock(color) for color in colors]]

    # Create vertical branch from random horizontal position
    tCol = random.randint(0,cols-1)
    rows = random.randint(4,6)
    startColor = colors[tCol]
    startColor,endColor = generateStartEndColors(rows-1,level,startColor)
    colors = interpolateColors(startColor,endColor,rows)
    print(f"colors in tBoard: {colors}")
    for row in range(rows-1):
        board.append([False for i in range(cols)])
    print(f"tBoard: {board}")
    for row in range(len(board)):
        print(f"looping tBoard: {(row,tCol)}")
        board[row][tCol] = ColorBlock(colors[row])
    return board

# print(interpolateColors((255,102,0),(255,204,0),3))
# print(generateStartEndColors(2))
# print(linearBoard(3))
