from cmu_112_graphics import *

def appStarted(app):
    pass

def redrawAll(app,canvas):
    drawBackground(app,canvas)
    drawPalette(app,canvas)
    drawBoard(app,canvas)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

def drawPalette(app,canvas):
    pass

def drawBoard(app,canvas):
    pass

runApp(height=600,width=400)
