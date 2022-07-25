from game import game
import boardInformation
import tkinter as tk
import tkinter.font as font
from tkinter.ttk import Combobox, Style
import tkinter.scrolledtext as tkst
global difficulty, playerCol, boardSize

class Menu():

    def __init__(self):
        self.menu = tk.Tk()
        self.menu.title("Halma")
        self.menu.resizable(False, False)
        self.menu.geometry('400x400')

        style = Style()
        style.configure('my.TButton', font=('Helvetica', 12))

        title = tk.Label(self.menu, text="Halma")
        title.config(font=("Helvetica", 40))
        title.place(x=125, y=20)

        self.createButtons()
        self.boardSize()
        self.choosePlayer()
        self.selectDifficulty()
        self.menu.mainloop()

    def boardSize(self):
        boardSizeLabel = tk.Label(self.menu, text="Size of the board")
        boardSizeLabel.config(font=("Courier", 12))
        boardSizeLabel.place(x=20, y=270)

        self.boardSizeData = ("8", "10", "16")
        self.boardSize = Combobox(values=self.boardSizeData)
        self.boardSize.current(0)
        self.boardSize.place(x=20, y=300)

    def choosePlayer(self):
        self.playerColorData = ("White", "Black")
        self.playerColor = Combobox(values=self.playerColorData)
        self.playerColor.current(0)
        self.playerColor.place(x=220, y=300)

        playerColorLabel = tk.Label(self.menu, text="Player color")
        playerColorLabel.config(font=("Courier", 12))
        playerColorLabel.place(x=220, y=270)

    def selectDifficulty(self):
        self.difficultyData = ("Easy", "Normal", "Hard")
        self.difficulty = Combobox(values=self.difficultyData)
        self.difficulty.current(0)
        self.difficulty.place(x=120, y=360)

        difficultyLabel = tk.Label(self.menu, text="Difficulty level", state='disabled')
        difficultyLabel.config(font=("Courier", 12))
        difficultyLabel.place(x=120, y=330)

    def createButtons(self):
        playAgainstComputerButton = tk.ttk.Button(self.menu, text='Play against computer', style='my.TButton', width=18,
                                                  command=self.playAgainstComputerFunc)
        playAgainstComputerButton.place(x=125, y=120)

        playAgainstPlayerButton = tk.ttk.Button(self.menu, text='Play against player', style='my.TButton', width=18,
                                                command=self.playAgainstPlayerFunc)
        playAgainstPlayerButton.place(x=125, y=170)

        gameRulesButton = tk.ttk.Button(self.menu, text='Game rules', style='my.TButton', width=18,
                                        command=self.gameRulesFunc)
        gameRulesButton.place(x=125, y=220)

    def playAgainstComputerFunc(self):
        global difficulty, playerCol, boardSize
        difficulty = self.difficulty.get()
        if difficulty == "Easy":
            difficulty = 1
        elif difficulty == "Normal":
            difficulty = 2
        else:
            difficulty = 3
        playerCol = self.playerColor.get()
        if playerCol == "White":
            playerCol = boardInformation.BoardPieces.blackPiece
        else:
            playerCol = boardInformation.BoardPieces.whitePiece

        boardSize = self.boardSize.get()
        if int(boardSize) not in [8, 10, 16]:
            boardSize = 8
        else:
            boardSize = int(boardSize)
        self.menu.destroy()

    def playAgainstPlayerFunc(self):
        global difficulty, playerCol, boardSize
        difficulty = 1
        playerCol = None
        boardSize = self.boardSize.get()
        if int(boardSize) != 8 or int(boardSize) != 10 or int(boardSize) != 16:
            boardSize = 8
        else:
            boardSize = int(boardSize)
        self.menu.destroy()

    def gameRulesFunc(self):
        win = tk.Toplevel()
        win.wm_title("Game rules")

        frame1 = tk.Frame(
            master=win,
            bg='#808000'
        )
        frame1.pack(fill='both', expand='yes')
        editArea = tkst.ScrolledText(
            master=frame1,
            wrap=tk.WORD,
            width=60,
            height=20
        )
        editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        editArea.insert(tk.INSERT,
"""\
1.	Object of the game 
	The game is won as the first one to move all the pieces from his own camp to the camp in the opposite corner.

2	Movement of Pieces
	Each turn, a player has to move one of his pieces. The player must always move them to an empty space. A pawn can also jump over adjacent pawns belonging to the player or the opponent, as long as it lands on an empty space. The jump can be done in any direction: horizontally, vertically or diagonally. A stone can make more than one jump in one turn. This allows the player to jump over the entire field. Contrary to checkers, the pieces do not disappear from the field, because in Halma the pieces never disappear from the board. In Halma, jumping is not compulsory, so if a player wants to stop after the first jump and there are more possible jumps, he can stop, but must make a jump each round. 

3.	Game setup
	The board consists of a grid of 8 × 8 squares. There is also a variation of the game 10x10 squares and 16x16 squares. In a two-player game of 8x8, the number of pieces each player has is 10. They are placed in a 1-2-3-4 pattern counting from the corner of the board
""")

menu = Menu()

try:
    game = game(boardSize, playerCol, difficulty)
except NameError:
    game = game(8, boardInformation.BoardPieces.blackPiece, 1)
