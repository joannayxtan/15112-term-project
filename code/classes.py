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

class PrimsRandomBoard:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.maze = [[False for i in range(self.cols)] for j in range(self.rows)]
        self._dir_two = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]
        self._range = list(range(4))

    def prim(self):
        """Creates a maze using Prim's algorithm."""
        frontier = []  # List of unvisited cells [(x, y),...]

        # Start with random cell
        x = random.randint(0, self.rows - 1)
        y = random.randint(0, self.cols - 1)
        self.maze[x][y] = True  # Mark as visited

        # Add cells to frontier for random cell
        for direction in self._dir_two:
            tx, ty = direction(x, y)
            if not self._out_of_bounds(tx, ty):
                frontier.append((tx, ty))
                self.maze[tx, ty, 0] = 1  # Mark as part of frontier

        # Add and connect cells until frontier is empty
        while frontier:
            x, y = frontier.pop(random.randint(0, len(frontier) - 1))

            # Connect cells
            for idx in self._random:
                tx, ty = self._dir_two[idx](x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 255:  # Check if visited
                    self.maze[x, y] = self.maze[self._dir_one[idx](x, y)] = [255, 255, 255]  # Connect cells
                    break

            # Add cells to frontier
            for direction in self._dir_two:
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.maze[tx, ty, 0] == 0:  # Check if unvisited
                    frontier.append((tx, ty))
                    self.maze[tx, ty, 0] = 1  # Mark as part of frontier

    def _out_of_bounds(self, x, y):
        """Checks if indices are out of bounds."""
        return x < 0 or y < 0 or x >= self.rows or y >= self.cols
