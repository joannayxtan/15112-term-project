from cmu_112_graphics import *
import random
from classes import *
# Interpolation
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
        possibleBoards.append(linearBoard(random.randint(5,7)))
        app.ans.setBoard(possibleBoards[0])
    elif app.level == 2: pass
    elif app.level == 3: pass
    elif app.level == 4: pass
    elif app.level == 5: pass

    # app.ans.setBoard([[ColorBlock((255,102,0),app.blockSize),
    #                       ColorBlock((255,153,0),app.blockSize),
    #                       ColorBlock((255,204,0),app.blockSize)]])

def linearBoard(totalBlocks):
    startColor,endColor = generateStartEndColors(totalBlocks-1)
    colors = interpolateColors(startColor,endColor,totalBlocks)
    board = []
    for i in range(totalBlocks):
        board.append([ColorBlock(colors[i])])
    return board

def generateStartEndColors(minStep):
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

# print(interpolateColors((255,102,0),(255,204,0),3))
# print(generateStartEndColors(2))
# print(linearBoard(3))
