from cmu_112_graphics import *
from classes import *
from generate_answer import *
import random,copy

##########################################
# Home Screen
##########################################

# Global Variables
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

def homeMode_drawButtons(app,canvas):
    for button in app.buttons:
        # Draw Level Buttons
        if button.type=="level":
            x0,y0,x1,y1 = button.getBounds()
            if int(button.text) == app.level:
                button.color=pinkfill
            else: button.color=bluefill
            canvas.create_oval(x0,y0,x1,y1,
                               fill = button.color)
            canvas.create_text(button.x,button.y,text=button.text,font=subfont,fill='white')
        # Draw Play Button
        elif button.type=="play":
            x0,y0,x1,y1 = button.getBounds()
            canvas.create_rectangle(x0,y0,x1,y1,fill=button.color)
            canvas.create_text(button.x,button.y,text="P L A Y",
                               font=subfont,fill="white")

def homeMode_mousePressed(app,event):
    for button in app.buttons:
        # Press Level Buttons
        if button.type=="level" and button.mousePressed(event.x,event.y):
            app.level = int(button.text)

        # Press Play Button
        if (button.type=="play" and button.mousePressed(event.x,event.y)
            and app.level != 0):
            initializeGame(app)
            app.mode = "gameMode"

# Alternative to using mouse
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
    drawTimer(app,canvas)

def drawTimer(app,canvas):
    canvas.create_text(app.width/2,app.height-app.margin*1.5,
                       text=f"{app.minutes:02d}:{app.seconds:02d}",
                       font=smallfont,fill="white")

# Draw Buttons
def drawButtons(app,canvas):
    for button in app.buttons:
        if (button.type in ["home","redo","help"]):
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
        # if is hint block and in gameMode: draw check mark
        if (row,col) in app.hintIndex and isBoard==True and app.mode in ["gameMode","helpMode"]:
            x,y = x1-app.blockSize*0.3,y1-app.blockSize*0.3
            canvas.create_image(x,y,
                                image=ImageTk.PhotoImage(app.check))

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

# Selected block has a border of lighter RGB
def drawSelectedBlock(app,canvas):
    blockSize = app.blockSize*0.85
    x0,x1 = app.selectedX - blockSize/2, app.selectedX + blockSize/2
    y0,y1 = app.selectedY - blockSize/2, app.selectedY + blockSize/2
    r,g,b = lighterRGB(app.selectedBlock.rgb)
    canvas.create_rectangle(x0,y0,x1,y1,
                            fill = app.selectedBlock.hex,
                            outline = ColorBlock.rgbToHex((r,g,b)),
                            width = 5)

# Lighter RGB for border of selected blocks
def lighterRGB(rgb):
    rgbList = list(rgb)
    for i in range(len(rgbList)):
        if rgbList[i] + 50 <= 255:
            rgbList[i] += 50
        else:
            rgbList[i] = 255
    return (rgbList[0],rgbList[1],rgbList[2])

def gameMode_mousePressed(app,event):
    cx,cy = event.x,event.y

    # Check if block is in Palette
    for row in range(app.pRows):
        for col in range(app.pCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.pStartX,app.pStartY,row,col)

            # Selected block in palette and has color
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and
                isinstance(app.palette[row][col],ColorBlock)):
                app.selectedBlock = app.palette[row][col]
                app.wasOnBoard = False

                # Store original positions in case of return
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

            # Selected block in board, has color, not hint block
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and
                isinstance(app.gameBoard.board[row][col],ColorBlock) and
                (row,col) not in app.hintIndex):
                app.selectedBlock = app.gameBoard.board[row][col]
                app.wasOnBoard = True

                # Store original positions in case of return
                blockX,blockY = (x0+x1)/2,(y0+y1)/2
                app.selectedX,app.selectedY = blockX,blockY
                app.originalRow,app.originalCol = row,col

                # Block is not centered at drag event, only follows drag
                app.cxCenterDiff = cx-blockX
                app.cyCenterDiff = cy-blockY
                app.gameBoard.board[row][col] = True
                return

    checkButtons(app,cx,cy)

def checkButtons(app,cx,cy):
    for button in app.buttons:
        if button.type=="home" and button.mousePressed(cx,cy): # Home Button
            app.level = 0
            app.mode = "homeMode"
        if button.type=="redo" and button.mousePressed(cx,cy): # Redo Button
            app.mode = "gameMode"
            initializeGame(app)
        if button.type=="help" and button.mousePressed(cx,cy): # Help Button
            if app.mode == "helpMode":
                app.mode = "gameMode"
            else:
                app.mode = "helpMode"
    print(app.mode)

def gameMode_mouseDragged(app,event):
    app.selectedX = event.x-app.cxCenterDiff
    app.selectedY = event.y-app.cyCenterDiff

def gameMode_mouseReleased(app,event):
    cx,cy = event.x,event.y

    # Do nothing if no block selected
    if app.selectedBlock == None:
        return

    # NOTE: hint blocks cannot be moved nor swapped
    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)
            if (x0 <= cx <= x1 and y0 <= cy <= y1):

                # Dragged block is in a board block space with no other blocks
                if (app.gameBoard.board[row][col] == True):
                    app.gameBoard.board[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return

                # Dragged board block is swapping with board block (not hint)
                if (app.gameBoard.board[row][col] != False and
                    app.wasOnBoard == True and
                    (row,col) not in app.hintIndex):
                    app.gameBoard.board[app.originalRow][app.originalCol] = app.gameBoard.board[row][col]
                    app.gameBoard.board[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return

                # Dragged palette block is swapping with board block (not hint)
                if (app.gameBoard.board[row][col] != False and
                    app.wasOnBoard == False and
                    (row,col) not in app.hintIndex):
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

                # Dragged block is in a palette block space with no other blocks
                if app.palette[row][col] == False:
                    app.palette[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return

                # Dragged palette block is swapping with palette block
                if app.wasOnBoard == False:
                    app.palette[app.originalRow][app.originalCol] = app.palette[row][col]
                    app.palette[row][col] = app.selectedBlock
                    app.selectedBlock = None
                    return

    # Return block to original position if invalid move
    if app.wasOnBoard == True:
        app.gameBoard.board[app.originalRow][app.originalCol] = app.selectedBlock
    else:
        app.palette[app.originalRow][app.originalCol] = app.selectedBlock
    app.selectedBlock = None

# Find first empty space in palette
def nextEmptySpacePalette(app):
    for i in range(app.pRows):
        for j in range(app.pCols):
            if app.palette[i][j] == False:
                return i,j
    return None

##########################################
# Help Mode
##########################################
def helpMode_redrawAll(app,canvas):
    drawBackground(app,canvas)
    canvas.create_text(app.width/2,app.margin,
                       text=f"DIFFICULTY: {app.level}",
                       font=subfont,fill=bluefill)
    drawPalette(app,canvas)
    drawBoard(app,canvas)
    if app.selectedBlock != None:
        drawSelectedBlock(app,canvas)
    drawButtons(app,canvas)
    drawTimer(app,canvas)

def helpMode_mousePressed(app,event):
    cx,cy = event.x,event.y

    checkButtons(app,cx,cy)

    # Check if block is in Board
    for row in range(app.bRows):
        for col in range(app.bCols):
            x0,y0,x1,y1 = getBlockBounds(app,app.bStartX,app.bStartY,row,col)

            # Selected block in board, has color, not hint block
            if (x0 <= cx <= x1 and y0 <= cy <= y1 and
                isinstance(app.ans.board[row][col],ColorBlock) and
                (row,col) not in app.hintIndex):

                # Empty the hint block space
                result = nextEmptySpacePalette(app)
                if result != None and isinstance(app.gameBoard.board[row][col],ColorBlock):
                    i,j = result
                    app.palette[i][j] = app.gameBoard.board[row][col]
                    app.gameBoard.board[row][col] = True

                # Find hint
                app.hintIndex.add((row,col))
                block = app.ans.board[row][col]

                # If hint block in palette, remove from palette
                for i in range(app.pRows):
                    for j in range(app.pCols):
                        if app.palette[i][j] == block:
                            app.palette[i][j] = False

                # If hint in wrong board space, remove from that space
                for i in range(app.bRows):
                    for j in range(app.bCols):
                        if app.gameBoard.board[i][j] == block:
                            app.gameBoard.board[i][j] = True

                # Add hint
                app.gameBoard.board[row][col] = block
                app.mode = "gameMode"
                return

##########################################
# Game End Mode
##########################################

def endMode_redrawAll(app,canvas):
    drawBackground(app,canvas)
    drawBoard(app,canvas)
    canvas.create_text(app.width/2,app.margin,
                       text=f"DIFFICULTY: {app.level}",
                       font=subfont,fill=bluefill)
    canvas.create_text(app.width/2,app.height/3-app.margin,text="A W E S O M E !",
                       font = titlefont, fill = pinkfill)
    canvas.create_text(app.width/2,app.height/3-app.margin*0.3,
                       text=f"time: {app.minutes:02d}:{app.seconds:02d}",
                       font = subfont,fill="white")
    drawButtons(app,canvas)

def endMode_mousePressed(app,event):
    checkButtons(app,event.x,event.y)

##########################################
# Main App
##########################################

# app initialization
def appStarted(app):
    app.mode = "homeMode"
    app.totalLevels = 5
    app.level = 0
    app.time = 0
    app.minutes = 0
    app.seconds = 0

    # Drawing Dimensions
    app.blockSize = app.width/9
    app.margin = (app.width - 6*app.blockSize)/2

    app.buttons = []
    # Level Buttons
    w,h = app.margin*0.7,app.margin*0.7
    startX = (app.width - 5*w)/2
    for level in range(1,app.totalLevels+1):
        cx = startX+(level-1)*(w+w/4)
        cy = app.height/2
        app.buttons.append(Button(cx,cy,"level",w=w,h=h,text=str(level),color=bluefill))

    # Play Button
    x,y = app.width/2,app.height*2/3
    w,h = app.width/3,app.width/10
    app.buttons.append(Button(x,y,"play",w=w,h=h,text="play",color=bluefill))

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

    # Hint Blocks Check Mark
    # Source: https://www.flaticon.com/free-icon-font/check_3917749?page=1&position=1&term=check&page=1&position=1&related_id=3917749&origin=search
    img = app.loadImage('images/check.png')
    app.check = app.scaleImage(img,0.2)

    # Moving Block
    app.selectedBlock = None
    app.selectedX,app.selectedY = (0,0)
    app.cxCenterDiff,app.cyCenterDiff = (0,0)
    app.wasOnBoard = False
    app.originalRow,app.originalCol = (0,0)

def initializeGame(app):

    # Create Answer Board
    generateAnswerBoard(app)

    # Board Dimensions
    app.bRows = len(app.ans.board)
    app.bCols = len(app.ans.board[0])

    # Create Game Board to be drawn
    createGameBoard(app)

    # Create Palette according to Answer Board
    # app.palette: list of ColorBlock instances
    createPalette(app)

    # Palette Dimensions
    app.pRows = len(app.palette)
    app.pCols = len(app.palette[0])

    # Where to start drawing Palette and Board
    app.pStartX = app.margin
    app.pStartY = app.height/2-app.margin*3
    app.bStartX = (app.width - app.bCols*app.blockSize)/2
    app.bStartY = app.height*0.6-app.bRows*app.blockSize/2

    app.time = 0

# Create Palette function
# Assumption: palette will not have more than 12 blocks
# NOTE: board can have max 14 blocks (2 immovable hint blocks)
def createPalette(app):
    # Remove hint blocks from palette
    board = [app.ans.board[i][j] if (i,j) not in app.hintIndex else False
             for i in range(app.bRows) for j in range(app.bCols)]

    # Extract color blocks from answer board, shuffle, and fill a (2x6) list
    colors = createPaletteHelper(board)
    onlyColors = []
    for color in colors:
        if color != False:
            onlyColors.append(color)
    colors = onlyColors
    random.shuffle(colors)
    app.palette = [[False for i in range(6)] for j in range(2)]
    i = 0
    for row in range(len(app.palette)):
        for col in range(len(app.palette[0])):
            if i < len(colors):
                app.palette[row][col] = colors[i]
            i+=1
    app.originalPalette = copy.deepcopy(app.palette)

# Create Palette helper function (recursive)
# Flatten answer board
def createPaletteHelper(board):
    if len(board) == 0:
        return []
    if isinstance(board[0],list):
        return createPaletteHelper(board[0]) + createPaletteHelper(board[1:])
    return [board[0]] + createPaletteHelper(board[1:])

# Create Game Board function
def createGameBoard(app):
    """
    Creates initial game board with hint blocks only.
    True: this is a block space, False: this is not a block space.
    """
    app.gameBoard = GameBoard()
    board = []
    totalBlocks = app.ans.getBlockNum()
    app.hintIndex = set()

    # For boards with 7- blocks: give one of the end blocks, else: give two random hints
    if totalBlocks <=7:
        app.hintIndex.add(random.choice([(0,0),(app.bRows-1,app.bCols-1)]))
    while totalBlocks > 7 and len(app.hintIndex) < 2:
        i,j = random.randint(0,app.bRows-1),random.randint(0,app.bCols-1)
        if app.ans.board[i][j] != False and (i,j) not in app.hintIndex:
            app.hintIndex.add((i,j))

    # Create initial game board with hint blocks
    for row in range(app.bRows):
        newRow = []
        for col in range(app.bCols):
            if app.ans.board[row][col] == False:
                newRow.append(False)
            elif (row,col) in app.hintIndex:
                newRow.append(app.ans.board[row][col])
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

def gameMode_timerFired(app):
    # check if reached solution
    app.time += 1
    app.minutes = int(app.time/10)//60
    app.seconds = int(app.time/10)%60
    if app.gameBoard.board == app.ans.board:
        app.mode = "endMode"

def helpMode_timerFired(app):
    app.time += 1
    app.minutes = int(app.time/10)//60
    app.seconds = int(app.time/10)%60

runApp(height=725,width=408)
