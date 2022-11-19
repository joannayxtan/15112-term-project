from cmu_112_graphics import *
from classes import *

# app initialization
def appStarted(app):
    # Create Answer Board
    # Note: currently hardcoded, will implement randomization later
    app.ans = GameBoard()
    app.blockSize = app.width/9
    app.ans.setBoard([[ColorBlock((255,102,0),app.blockSize),
                          ColorBlock((255,153,0),app.blockSize),
                          ColorBlock((255,204,0),app.blockSize)]])

    # Create Palette according to Answer Board
    createPalette(app)

    # Dimensions
    app.pRows = len(app.palette)
    app.pCols = len(app.palette[0])
    app.bRows = len(app.ans.board)
    app.bCols = len(app.ans.board[0])
    app.margin = (app.width - 6*app.blockSize)/2

    # Create Game Board to be drawn
    createGameBoard(app)
    print(app.gameBoard.board)
    print(app.ans.board)
    print(app.bRows,app.bCols)

# Create Palette function
# Assumption: palette will not have more than 12 blocks
def createPalette(app):
    colors = createPaletteHelper(app.ans.board)
    app.palette = [[False for i in range(6)] for j in range(2)]
    i = 0
    for row in range(len(app.palette)):
        for col in range(len(app.palette[0])):
            if i < len(colors):
                app.palette[row][col] = colors[i]
            i+=1

# Create Palette helper function (recursive)
def createPaletteHelper(board):
    if len(board) == 0:
        return []
    if isinstance(board[0],list):
        return createPaletteHelper(board[0]) + createPaletteHelper(board[1:])
    return [board[0]] + createPaletteHelper(board[1:])

# Create Game Board function
def createGameBoard(app):
    app.gameBoard = GameBoard()
    board = []
    for row in range(app.bRows):
        newRow = []
        for col in range(app.bCols):
            if app.ans.board[row][col] == False:
                newRow.append(False)
            else:
                newRow.append(True)
        board.append(newRow)
    app.gameBoard.setBoard(board)

# Drawing functions
def redrawAll(app,canvas):
    drawBackground(app,canvas)
    drawPalette(app,canvas)
    drawBoard(app,canvas)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

def drawPalette(app,canvas):
    for i in range(app.pRows):
        for j in range(app.pCols):
            drawBlock(app,canvas,
                      app.margin,app.margin,
                      i,j,app.palette[i][j])

def drawBoard(app,canvas):
    startX = (app.width - app.bCols*app.blockSize)/2
    startY = app.height/2+app.margin
    for i in range(app.bRows):
        for j in range(app.bCols):
            drawBlock(app,canvas,
                      startX,startY,
                      i,j,app.gameBoard.board[i][j],
                      True)

def getBlockBounds(app,startX,startY,row,col):
    x0 = startX + col*app.blockSize
    x1 = startX + (col+1)*app.blockSize
    y0 = startY + row*app.blockSize
    y1 = startY + (row+1)*app.blockSize
    return (x0,y0,x1,y1)

# Draw Block function
def drawBlock(app,canvas,startX,startY,row,col,block,isBoard=False):
    x0,y0,x1,y1 = getBlockBounds(app,startX,startY,row,col)

    # if has color: draw the colorBlock
    if isinstance(block,ColorBlock):
        canvas.create_rectangle(x0,y0,x1,y1,
                                fill = block.hex,
                                width = 5)

    # if no color, part of palette: draw round pin
    elif isBoard == False:
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        size = app.blockSize*0.1
        canvas.create_oval(cx-size,cy-size,
                           cx+size,cy+size,
                           fill='grey')

    # if no color, part of board, is block space: draw placeholder
    elif block == True:
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        size = app.blockSize*0.4
        canvas.create_rectangle(cx-size,cy-size,
                                cx+size,cy+size,
                                fill ='',
                                outline = 'grey',
                                width = 3)

runApp(height=853,width=480)
