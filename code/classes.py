class ColorBlock():
    def __init__(self,color=(0,0,0),size=35):
        self.rgb = color
        self.hex = self.rgbToHex()
        self.size = size

    # Source: https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
    def rgbToHex(self):
        r, g, b = self.rgb
        return f'#{r:02x}{g:02x}{b:02x}'

    def __repr__(self):
        return f"Block with color: {self.hex}"

class GameBoard():
    def __init__(self):
        self.possibleBoards = [
            [[True,True,True],
             [True,True,True],
             [True,True,True]],

            [[True,True,True]]
        ]
        # hard coding the board
        self.board = self.possibleBoards[1]
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    # For testing purposes, allows passing in a set board
    def setBoard(self,board):
        rows = len(board)
        cols = len(board[0])
        if self.rows==rows and self.cols==cols:
            self.board = board
