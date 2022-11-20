from cmu_112_graphics import *
from classes import *
from generate_answer import *
import random,copy

##########################################
# Home Screen
##########################################

titlefont = "Ariel 40 bold"
subfont = "Ariel 25 bold"
smallfont = "Ariel 13 bold"
pinkfill = "#C292AA"
bluefill = "#8A9BBF"

def homeMode_redrawAll(app,canvas):
    drawBackground(app,canvas)
    canvas.create_text(app.width/2,app.height/3,text="B L E N D O K U",
                       font = titlefont, fill = pinkfill)
    canvas.create_text(app.width/2,app.height/3+app.margin,text="D I F F I C U L T Y",
                       font = subfont, fill = bluefill)
    drawLevelChoices(app,canvas)
    canvas.create_text(app.width/2,app.height*0.57,text="CHOOSE DIFFICULTY",
                       font = smallfont, fill = 'grey')
    drawPlayButton(app,canvas)

# Draw Level Buttons
def drawLevelChoices(app,canvas):
    r = app.margin*0.4
    startX = (app.width - 10*r)/2
    for i in range(1,app.totalLevels+1):
        cx = startX+(i-1)*2*r+r
        cy = app.height/2
        x0,y0,x1,y1 = getCircleBounds(app,i)
        if i == app.level:
            canvas.create_oval(x0,y0,x1,y1,
                               fill = pinkfill)
        else:
            canvas.create_oval(x0,y0,x1,y1,
                               fill = bluefill)
        canvas.create_text(cx,cy,text=f"{i}",font=subfont,fill='white')

# Find position of Level Buttons
def getCircleBounds(app,i):
    r = app.margin*0.4
    startX = (app.width - 10*r)/2
    cx = startX+(i-1)*2*r+r
    cy = app.height/2
    x0,y0,x1,y1 = cx-r*0.8,cy-r*0.8,cx+r*0.8,cy+r*0.8
    return x0,y0,x1,y1

# Draw Play Button
def drawPlayButton(app,canvas):
    recW,recH = app.width/3,app.width/10
    canvas.create_rectangle(app.width/2-recW/2,app.height*2/3-recH/2,
                            app.width/2+recW/2,app.height*2/3+recH/2,
                            fill=bluefill)
    canvas.create_text(app.width/2,app.height*2/3,text="P L A Y",
                       font=subfont,fill="white")

def homeMode_mousePressed(app,event):
    for i in range(1,app.totalLevels+1):
        x0,y0,x1,y1 = getCircleBounds(app,i)
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            app.level = i
    recW,recH = app.width/3,app.width/10
    playX0,playY0 = app.width/2-recW/2,app.height*2/3-recH/2
    playX1,playY1 = app.width/2+recW/2,app.height*2/3+recH/2
    if (playX0 <= event.x <= playX1 and playY0 <= event.y <= playY1
        and app.level != 0):
        initializeGame(app)
        app.mode = "gameMode"

def homeMode_keyPressed(app,event):
    if event.key.isdigit() and 1 <= int(event.key) <= 5:
        app.level = int(event.key)
    if event.key == "Enter":
        if app.level != 0:
            initializeGame(app)
            app.mode = "gameMode"

##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app,canvas):
    drawBackground(app,canvas)
    canvas.create_text(app.width/2,app.margin,
                       text=f"DIFFICULTY: {app.level}",
                       font=subfont,fill=bluefill)
    drawPalette(app,canvas)
    drawBoard(app,canvas)
    if app.selectedBlock != None:
        drawSelectedBlock(app,canvas)
    drawButtons(app,canvas)

# Draw Buttons
def drawButtons(app,canvas):
    canvas.create_image(app.margin,app.height-app.margin,
                        image=ImageTk.PhotoImage(app.backButton))
    canvas.create_image(app.width/2,app.height-app.margin,
                        image=ImageTk.PhotoImage(app.redo))
    canvas.create_image(app.width-app.margin,app.height-app.margin,
                        image=ImageTk.PhotoImage(app.help))

# Draw Palette
def drawPalette(app,canvas):
    for i in range(app.pRows):
        for j in range(app.pCols):
            drawBlock(app,canvas,
                      app.pStartX,app.pStartY,
                      i,j,app.palette[i][j])

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
    blockSize = app.blockSize*0.85
    x0,x1 = app.selectedX - blockSize/2, app.selectedX + blockSize/2
    y0,y1 = app.selectedY - blockSize/2, app.selectedY + blockSize/2
    r,g,b = lighterRGB(app.selectedBlock.rgb)
    print(f"selectedBlock: {app.selectedBlock.rgb}, outline: {(r,g,b)}")
    canvas.create_rectangle(x0,y0,x1,y1,
                            fill = app.selectedBlock.hex,
                            outline = ColorBlock.rgbToHex((r,g,b)),
                            width = 5)

# Lighter RGB for outlines of selected blocks
def lighterRGB(rgb):
    rgbList = list(rgb)
    for i in range(len(rgbList)):
        if rgbList[i] + 50 <= 255:
            rgbList[i] += 50
        else:
            rgbList[i] = 255
    print(f"{rgb} -> {(rgbList[0],rgbList[1],rgbList[2])}")
    return (rgbList[0],rgbList[1],rgbList[2])

def gameMode_mousePressed(app,event):
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

def gameMode_mouseDragged(app,event):
    app.selectedX = event.x-app.cxCenterDiff
    app.selectedY = event.y-app.cyCenterDiff
    print(f"dragging {app.selectedBlock}")
    print(f"mouseDragged at {(event.x,event.y)}")

def gameMode_mouseReleased(app,event):
    cx,cy = event.x,event.y

    # Do nothing if no block selected
    if app.selectedBlock == None:
        return

    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.gameBoard.board[row][col] == True):
                app.gameBoard.board[row][col] = app.selectedBlock
                app.selectedBlock = None
                return

    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and app.palette[row][col] == False):
                app.palette[row][col] = app.selectedBlock
                app.selectedBlock = None
                return

    # Return block to original position
    if app.wasOnBoard == True:
        app.gameBoard.board[app.originalRow][app.originalCol] = app.selectedBlock
    else:
        app.palette[app.originalRow][app.originalCol] = app.selectedBlock
    app.selectedBlock = None

    print(f"mouseReleased at {(event.x,event.y)}")
    print(f"palette: {app.palette}")

##########################################
# Main App
##########################################

# app initialization
def appStarted(app):
    app.mode = "homeMode"
    app.totalLevels = 5
    app.level = 0
    app.blockSize = app.width/9
    app.margin = (app.width - 6*app.blockSize)/2

    # Moving Block
    app.selectedBlock = None
    app.selectedX,app.selectedY = (0,0)
    app.cxCenterDiff,app.cyCenterDiff = (0,0)
    app.wasOnBoard = False
    app.originalRow,app.originalCol = (0,0)

    # Load Button Images
    # Source: https://www.flaticon.com/free-icons/back
    app.backButton = app.loadImage('images/back.png')
    app.backButton = app.scaleImage(app.backButton,0.05)
    # Source: "https://www.flaticon.com/free-icons/redo"
    app.redo = app.loadImage('images/redo.png')
    app.redo = app.scaleImage(app.redo,0.05)
    # Source: https://www.flaticon.com/free-icons/question
    app.help = app.loadImage('images/help.png')
    app.help = app.scaleImage(app.help,0.05)

def initializeGame(app):
    generateAnswerBoard(app)
    print(app.ans.board)
    # Create Palette according to Answer Board
    # app.palette: list of ColorBlock instances
    createPalette(app)
    # Palette and Board Dimensions
    app.pRows = len(app.palette)
    app.pCols = len(app.palette[0])
    app.bRows = len(app.ans.board)
    app.bCols = len(app.ans.board[0])

    # Where to start drawing Palette and Board
    app.pStartX = app.margin
    app.pStartY = app.height/2-app.margin*3
    app.bStartX = (app.width - app.bCols*app.blockSize)/2
    app.bStartY = app.height/2-app.margin

    # Create Game Board to be drawn
    createGameBoard(app)
    print(app.gameBoard.board)
    print(app.ans.board)
    print(app.bRows,app.bCols)

# Create Palette function
# Assumption: palette will not have more than 12 blocks
def createPalette(app):
    print(f"in createPalette")
    colors = createPaletteHelper(app.ans.board)
    random.shuffle(colors)
    app.palette = [[False for i in range(6)] for j in range(2)]
    i = 0
    print(colors)
    for row in range(len(app.palette)):
        for col in range(len(app.palette[0])):
            if i < len(colors):
                app.palette[row][col] = colors[i]
            i+=1
    app.originalPalette = copy.deepcopy(app.palette)

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
    app.originalGameBoard = copy.deepcopy(app.gameBoard)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

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

runApp(height=725,width=408)
