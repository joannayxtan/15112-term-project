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
    # app.palette: list of ColorBlock instances
    createPalette(app)

    # Palette and Board Dimensions
    app.pRows = len(app.palette)
    app.pCols = len(app.palette[0])
    app.bRows = len(app.ans.board)
    app.bCols = len(app.ans.board[0])

    # Where to start drawing Palette and Board
    app.margin = (app.width - 6*app.blockSize)/2
    app.pStartX = app.margin
    app.pStartY = app.margin
    app.bStartX = (app.width - app.bCols*app.blockSize)/2
    app.bStartY = app.height/2+app.margin

    # Create Game Board to be drawn
    createGameBoard(app)
    print(app.gameBoard.board)
    print(app.ans.board)
    print(app.bRows,app.bCols)

    # Moving Block
    app.selectedBlock = None
    app.selectedX,app.selectedY = (0,0)
    app.cxCenterDiff,app.cyCenterDiff = (0,0)
    app.wasOnBoard = False
    app.originalRow,app.originalCol = (0,0)

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
    if app.selectedBlock != None:
        drawSelectedBlock(app,canvas)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

def drawPalette(app,canvas):
    for i in range(app.pRows):
        for j in range(app.pCols):
            drawBlock(app,canvas,
                      app.pStartX,app.pStartY,
                      i,j,app.palette[i][j])

def drawBoard(app,canvas):
    for i in range(app.bRows):
        for j in range(app.bCols):
            drawBlock(app,canvas,
                      app.bStartX,app.bStartY,
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

def drawSelectedBlock(app,canvas):
    x0,x1 = app.selectedX - app.blockSize/2, app.selectedX + app.blockSize/2
    y0,y1 = app.selectedY - app.blockSize/2, app.selectedY + app.blockSize/2
    canvas.create_rectangle(x0,y0,x1,y1,
                            fill = app.selectedBlock.hex,
                            outline = '',
                            width = 5)

def mousePressed(app,event):
    cx,cy = event.x,event.y

    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.palette[row][col] != False):
                app.selectedBlock = app.palette[row][col]
                app.wasOnBoard = False
                blockX,blockY = (x0+x1)/2,(y0+y1)/2
                app.selectedX,app.selectedY = blockX,blockY
                app.originalRow,app.originalCol = row,col
                # Block is not centered at drag event, only follows drag
                app.cxCenterDiff = cx-blockX
                app.cyCenterDiff = cy-blockY
                app.palette[row][col] = False
                return

    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.gameBoard.board[row][col] != False):
                app.selectedBlock = app.gameBoard.board[row][col]
                app.wasOnBoard = True
                blockX,blockY = (x0+x1)/2,(y0+y1)/2
                app.selectedX,app.selectedY = blockX,blockY
                app.originalRow,app.originalCol = row,col
                # Block is not centered at drag event, only follows drag
                app.cxCenterDiff = cx-blockX
                app.cyCenterDiff = cy-blockY
                app.gameBoard.board[row][col] = True
                return

    print(f"currently selecting: {app.selectedBlock}")
    print(f"mousePressed at {(event.x,event.y)}")

def mouseDragged(app,event):
    app.selectedX = event.x-app.cxCenterDiff
    app.selectedY = event.y-app.cyCenterDiff
    print(f"mouseDragged at {(event.x,event.y)}")

def mouseReleased(app,event):
    cx,cy = event.x,event.y

    # Do nothing if no block selected
    if app.selectedBlock == None:
        return

    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.gameBoard.board[row][col] != False):
                app.gameBoard.board[row][col] = app.selectedBlock

    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.palette[row][col] != False):
                app.palette[row][col] = app.selectedBlock

    if app.wasOnBoard == True:
        app.gameBoard.board[app.originalRow][app.originalCol] = app.selectedBlock
    else:
        app.palette[app.originalRow][app.originalCol] = app.selectedBlock

    app.selectedBlock = None

    print(f"mouseReleased at {(event.x,event.y)}")
runApp(height=853,width=480)
