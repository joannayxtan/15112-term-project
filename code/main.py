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
    canvas.create_text(app.width/2,app.height*0.57,text="CHOOSE DIFFICULTY",
                       font = smallfont, fill = 'grey')
    homeMode_drawButtons(app,canvas)

# Draw Level Buttons
def homeMode_drawButtons(app,canvas):
    for button in app.buttons:
        if button.type=="level":
            x0,y0,x1,y1 = button.getBounds()
            if int(button.text) == app.level:
                button.color=pinkfill
            else: button.color=bluefill
            canvas.create_oval(x0,y0,x1,y1,
                               fill = button.color)
            canvas.create_text(button.x,button.y,text=button.text,font=subfont,fill='white')
        elif button.type=="play":
            x0,y0,x1,y1 = button.getBounds()
            canvas.create_rectangle(x0,y0,x1,y1,fill=button.color)
            canvas.create_text(button.x,button.y,text="P L A Y",
                               font=subfont,fill="white")

def homeMode_mousePressed(app,event):
    for button in app.buttons:
        if button.type=="level" and button.mousePressed(event.x,event.y):
            app.level = int(button.text)
        if (button.type=="play" and button.mousePressed(event.x,event.y)
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
    for button in app.buttons:
        if button.type in ["home","redo","help"]:
            canvas.create_image(button.x,button.y,
                                image=ImageTk.PhotoImage(button.img))

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
    # print(f"selectedBlock: {app.selectedBlock.rgb}, outline: {(r,g,b)}")
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
    # print(f"{rgb} -> {(rgbList[0],rgbList[1],rgbList[2])}")
    return (rgbList[0],rgbList[1],rgbList[2])

def gameMode_mousePressed(app,event):
    cx,cy = event.x,event.y

    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and isinstance(app.palette[row][col],ColorBlock)):
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
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and isinstance(app.gameBoard.board[row][col],ColorBlock)):
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

    checkButtons(app,cx,cy)
    # print(f"currently selecting: {app.selectedBlock}")
    # print(f"mousePressed at {(event.x,event.y)}")

def checkButtons(app,cx,cy):
    for button in app.buttons:
        if button.type=="home" and button.mousePressed(cx,cy):
            app.level = 0
            app.mode = "homeMode"
        if button.type=="redo" and button.mousePressed(cx,cy):
            initializeGame(app)
        if button.type=="help" and button.mousePressed(cx,cy):
            pass

def gameMode_mouseDragged(app,event):
    app.selectedX = event.x-app.cxCenterDiff
    app.selectedY = event.y-app.cyCenterDiff
    # print(f"dragging {app.selectedBlock}")
    # print(f"mouseDragged at {(event.x,event.y)}")

def gameMode_mouseReleased(app,event):
    cx,cy = event.x,event.y

    # Do nothing if no block selected
    if app.selectedBlock == None:
        return

    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1):
                if (app.gameBoard.board[row][col] == True):
                    app.gameBoard.board[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return
                if (app.gameBoard.board[row][col] != False and app.wasOnBoard == True):
                    app.gameBoard.board[app.originalRow][app.originalCol] = app.gameBoard.board[row][col]
                    app.gameBoard.board[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return
                if (app.gameBoard.board[row][col] != False and app.wasOnBoard == False):
                    result = nextEmptySpacePalette(app)
                    if result != None:
                        i,j = result
                        app.palette[i][j] = app.gameBoard.board[row][col]
                        app.gameBoard.board[row][col] = app.selectedBlock
                        app.selectedBlock = None
                        return
    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1):
                if app.palette[row][col] == False:
                    app.palette[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return
                if app.wasOnBoard == False:
                    app.palette[app.originalRow][app.originalCol] = app.palette[row][col]
                    app.palette[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return

    # Return block to original position
    if app.wasOnBoard == True:
        app.gameBoard.board[app.originalRow][app.originalCol] = app.selectedBlock
    else:
        app.palette[app.originalRow][app.originalCol] = app.selectedBlock
    app.selectedBlock = None

    # print(f"mouseReleased at {(event.x,event.y)}")
    # print(f"palette: {app.palette}")

def nextEmptySpacePalette(app):
    for i in range(app.pRows):
        for j in range(app.pCols):
            if app.palette[i][j] == False:
                return i,j
    return None

##########################################
# Main App
##########################################

# app initialization
def appStarted(app):
    app.mode = "homeMode"
    app.totalLevels = 5
    app.level = 0
    app.buttons = []

    # Drawing Dimensions
    app.blockSize = app.width/9
    app.margin = (app.width - 6*app.blockSize)/2

    # Level Buttons
    w,h = app.margin*0.7,app.margin*0.7
    startX = (app.width - 5*w)/2
    for level in range(1,app.totalLevels+1):
        cx = startX+(level-1)*(w+w/4)
        cy = app.height/2
        app.buttons.append(Button(cx,cy,"level",w,h,str(level),bluefill))

    # Play Button
    x,y = app.width/2,app.height*2/3
    w,h = app.width/3,app.width/10
    app.buttons.append(Button(x,y,"play",w,h,"play",bluefill))

    # Game Buttons
    # Source: https://www.flaticon.com/free-icons/back
    x,y = app.margin,app.height-app.margin
    img = app.loadImage('images/back.png')
    img = app.scaleImage(img,0.05)
    app.buttons.append(Button(x,y,"home",img=img))
    # Source: "https://www.flaticon.com/free-icons/redo"
    x,y = app.width/2,app.height-app.margin
    img = app.loadImage('images/redo.png')
    img = app.scaleImage(img,0.05)
    app.buttons.append(Button(x,y,"redo",img=img))
    # Source: https://www.flaticon.com/free-icons/question
    x,y = app.width-app.margin,app.height-app.margin
    img = app.loadImage('images/help.png')
    img = app.scaleImage(img,0.05)
    app.buttons.append(Button(x,y,"help",img=img))

    # Moving Block
    app.selectedBlock = None
    app.selectedX,app.selectedY = (0,0)
    app.cxCenterDiff,app.cyCenterDiff = (0,0)
    app.wasOnBoard = False
    app.originalRow,app.originalCol = (0,0)

def initializeGame(app):
    generateAnswerBoard(app)
    # Create Palette according to Answer Board
    # app.palette: list of ColorBlock instances
    createPalette(app)
    print(f"Answer Board: {app.ans.board}")
    print(f"Palette: {app.palette}")
    # Palette and Board Dimensions
    app.pRows = len(app.palette)
    app.pCols = len(app.palette[0])
    app.bRows = len(app.ans.board)
    app.bCols = len(app.ans.board[0])
    print(f"board dim: {(app.bRows,app.bCols)}")

    # Where to start drawing Palette and Board
    app.pStartX = app.margin
    app.pStartY = app.height/2-app.margin*3
    app.bStartX = (app.width - app.bCols*app.blockSize)/2
    app.bStartY = app.height*0.6-app.bRows*app.blockSize/2
    # app.height/2-app.margin*1.3

    # Create Game Board to be drawn
    createGameBoard(app)
    # print(app.gameBoard.board)
    # print(app.ans.board)
    # print(app.bRows,app.bCols)

# Create Palette function
# Assumption: palette will not have more than 12 blocks
def createPalette(app):
    # print(f"in createPalette")
    colors = createPaletteHelper(app.ans.board)
    onlyColors = []
    for color in colors:
        if color != False:
            onlyColors.append(color)
    colors = onlyColors
    random.shuffle(colors)
    app.palette = [[False for i in range(6)] for j in range(2)]
    i = 0
    # print(colors)
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
    """
    Creates empty game board to be filled in.
    True: this is a block space, False: this is not a block space.
    """
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
