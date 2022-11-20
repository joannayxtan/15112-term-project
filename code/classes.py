
class ColorBlock():
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

class GameBoard():
    def __init__(self):
        # hard coding the board
        self.board = []

    # For testing purposes, allows passing in a set board
    def setBoard(self,board):
        self.board = board
