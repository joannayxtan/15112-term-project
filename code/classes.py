class ColorBlock():
    def __init__(self,color):
        self.rgb = color
        self.hex = self.rgbToHex(color)

    def rgbToHex(rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'

    def getRGB(self):
        return self.rgb

    def getHex(self):
        return self.hex

class GameBoard():
    def __init__(self):
        self.possibleBoards = [
            [["x","x","x"],
             ['x','x','x'],
             ['x','x','x']],

            [["x","x","x"]]
        ]
        # hard coding the board
        self.board = self.possibleBoards[1]
        self.rows = len(self.board)
        self.cols = len(self.board[0])

        #store color blocks
        self.blocks

    #
    def setBoard(self,board):
        rows = len(board)
        cols = len(board[0])
        if self.rows==rows and self.cols==cols:
            self.board = board

    def getBoard(self):
        return self.board
