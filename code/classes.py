import random
import math
class ColorBlock:
    def __init__(self,color=(0,0,0),size=35):
        self.rgb = color
        self.hex = self.rgbToHex(self.rgb)
        self.size = size

    @staticmethod
    # Source: https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
    def rgbToHex(rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'

    def __repr__(self):
        return f"Block with color: {self.hex}"

class GameBoard:
    def __init__(self):
        # hard coding the board
        self.board = []

    # Pass in a set board
    def setBoard(self,board):
        self.board = board

# TODO: use **kwargs

class Button:
    def __init__(self,x,y,type,w=None,h=None,text=None,color=None,img=None):
        self.x = x
        self.y = y
        self.type = type
        if self.type in ["home","redo","help"]:
            self.img = img
            self.w,self.h = img.size
        else:
            self.w = w
            self.h = h
            self.color = color
            self.text = text

    def mousePressed(self,x,y):
        if (self.x-self.w/2 <= x <= self.x+self.w/2 and
            self.y-self.h/2 <= y <= self.y+self.h/2):
            return True
        return False

    def getBounds(self):
        return (self.x-self.w/2,self.y-self.h/2,
                self.x+self.w/2,self.y+self.h/2)
