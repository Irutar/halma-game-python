import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from boardInformation import BoardPieces, PieceBorder, BoardSquares
import os


class board(tk.Tk):

    def __init__(self, boardSize, halmaGameBoard):
        tk.Tk.__init__(self)
        self.boardSize = boardSize
        self.halmaGameBoard = halmaGameBoard
        self.squares = {}

        self.title("Halma")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=BoardSquares.width, height=BoardSquares.height, cursor="circle")
        self.canvas.grid()
        self.canvas.bind("<Configure>", self.drawSquares)

        self.oneSquareSize = int(BoardSquares.width / self.boardSize - (PieceBorder.borderSize * 2))
        whiteImg = Image.open("images/white.png")
        whiteImg = whiteImg.resize((self.oneSquareSize, self.oneSquareSize), Image.ANTIALIAS)
        self.whitePawn = ImageTk.PhotoImage(whiteImg)

        blackImg = Image.open("images/black.png")
        blackImg = blackImg.resize((self.oneSquareSize, self.oneSquareSize), Image.ANTIALIAS)
        self.blackPawn = ImageTk.PhotoImage(blackImg)

    def winMessage(self, player):
        if player == BoardPieces.whitePiece:
            messagebox.showinfo('White WIN', ' White player has won !!!')
        else:
            messagebox.showinfo('Black WIN', ' Black player has won !!!')

    def clickedSquare(self, clickedSquare):
        self.clickedSquare = clickedSquare

    def drawSinglePiece(self, row, col, x, y):
        if self.halmaGameBoard[row][col].piece == BoardPieces.whitePiece:
            piece = self.canvas.create_image(x + PieceBorder.borderSize / 2, y + PieceBorder.borderSize / 2,
                                             image=self.whitePawn, anchor=tk.NW)
            return piece

        elif self.halmaGameBoard[row][col].piece == BoardPieces.blackPiece:
            piece = self.canvas.create_image(x + PieceBorder.borderSize / 2, y + PieceBorder.borderSize / 2,
                                             image=self.blackPawn, anchor=tk.NW)
            return piece
        else:
            return False


    def drawPieces(self):
        squareSize = int(self.canvas.winfo_width() / self.boardSize)
        for col in range(self.boardSize):
            for row in range(self.boardSize):
                xCoordinate = col * squareSize + PieceBorder.borderSize / 2
                yCoordinate = row * squareSize + PieceBorder.borderSize / 2
                piece = self.drawSinglePiece(row, col, xCoordinate, yCoordinate)
                if piece:
                    self.canvas.tag_bind(piece, "<Button>", lambda event,
                                                                   row=row, col=col: self.clickedSquare(row, col))
        self.update()

    def drawSingleSquare(self, row, col):
        squareSize = int(self.canvas.winfo_width() / self.boardSize)
        squareColor, borderColor = self.halmaGameBoard[row][col].getSquareColors()
        x1 = col * squareSize + PieceBorder.borderSize / 2
        y1 = row * squareSize + PieceBorder.borderSize / 2
        x2 = (col + 1) * squareSize - PieceBorder.borderSize / 2
        y2 = (row + 1) * squareSize - PieceBorder.borderSize / 2
        square = self.canvas.create_rectangle(x1, y1, x2, y2, fill=squareColor, outline=borderColor,
                                              width=PieceBorder.borderSize)
        return square

    def drawSquares(self, event=None):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                square = self.drawSingleSquare(row, col)
                self.squares[row, col] = square
                self.canvas.tag_bind(square, "<Button>", lambda event, row=row, col=col: self.clickedSquare(row, col))
        self.drawPieces()





