import time

from board import board
from squares import squares
from boardInformation import BoardPieces, BoardSquares, PieceBorder
from movement import generatePossibleMovementsAtSelectedSquare, makeMove
from evaluatingFunctions import setVictoryConditions, minimax, checkWinCondtion

class game():

    def __init__(self, boardSize, secondPlayer, difficulty):

        self.boardSize = boardSize
        self.secondPlayer = secondPlayer
        self.halmaGameBoard = []

        for row in range(0, boardSize):  # Creating 2D list that represents the game board
            tempList = []
            for col in range(0, boardSize):
                tempList.append(None)
            self.halmaGameBoard.append(tempList)

        for row in range(0, boardSize):  # Filling 2D list with information about the color of the square,
                                         # the presence of a pawn and home area placement
            for col in range(0, boardSize):
                if row + col < 4:
                    self.halmaGameBoard[row][col] = squares(row, col, BoardSquares.whiteHomeArea, BoardPieces.whitePiece,
                                                       PieceBorder.noBorder)
                elif row + col > 2 * (boardSize - 3):
                    self.halmaGameBoard[row][col] = squares(row, col, BoardSquares.blackHomeArea, BoardPieces.blackPiece,
                                                       PieceBorder.noBorder)
                else:
                    self.halmaGameBoard[row][col] = squares(row, col, BoardSquares.neutralSquare, BoardPieces.noPiece,
                                                       PieceBorder.noBorder)

        setVictoryConditions(self.halmaGameBoard)

        self.currentPlayer = BoardPieces.whitePiece
        self.selectedPiece = None

        self.maxMinMaxLevel = difficulty
        self.alphaBetaPruningEnabled = True

        self.possibleMovementList = []
        self.boardView = board(self.boardSize, self.halmaGameBoard)
        self.boardView.clickedSquare(self.clickedSquare)
        self.isComputerThinking = False
        if self.secondPlayer == self.currentPlayer:
            self.computerMove()
        self.boardView.mainloop()


    def refreshScreen(self):
        self.boardView.drawSquares(self.halmaGameBoard)

    def squareBorder(self, squares):
        borderType = PieceBorder.possibleMovementBorder
        if squares is None:
            squares = []
            for row in self.halmaGameBoard:
                for col in row:
                    squares.append(col)

            borderType = PieceBorder.noBorder

        for square in squares:
            square.border = borderType

    def drawPossibleMovementBordersOnSquares(self, selectedSquare):
        self.squareBorder(None)
        selectedSquare.border = PieceBorder.selectedPieceBorder
        self.squareBorder(self.possibleMovementList)
        self.refreshScreen()

    def switchPlayer(self):
        if self.currentPlayer == BoardPieces.whitePiece:
            self.currentPlayer = BoardPieces.blackPiece
        else:
            self.currentPlayer = BoardPieces.whitePiece


    def clickedSquare(self, row, col):
        if self.isComputerThinking:
            return

        selectedSquare = self.halmaGameBoard[row][col]
        if selectedSquare.piece == self.currentPlayer:
            self.possibleMovementList = generatePossibleMovementsAtSelectedSquare(None, selectedSquare, self.boardSize,
                                                                                  self.halmaGameBoard, True)
            self.selectedPiece = selectedSquare
            self.drawPossibleMovementBordersOnSquares(selectedSquare)
        elif self.selectedPiece and selectedSquare in self.possibleMovementList:
            self.squareBorder(None)
            self.selectedPiece = makeMove(self.selectedPiece, selectedSquare)
            self.switchPlayer()
            winCondition = checkWinCondtion()
            self.refreshScreen()
            if winCondition == BoardPieces.whitePiece:
                self.boardView.winMessage(BoardPieces.whitePiece)
                self.currentPlayer = None
                self.boardView.destroy()
            elif winCondition == BoardPieces.blackPiece:
                self.boardView.winMessage(BoardPieces.blackPiece)
                self.currentPlayer = None
                self.boardView.destroy()
            elif self.secondPlayer is not None:
                self.computerMove()

    def computerMove(self):
        self.isComputerThinking = True
        self.boardView.update()

        setInitialAlpha = float(("-inf"))
        setInitialBeta = float(("inf"))
        bestScore, bestMovement = minimax(self.boardSize, self.halmaGameBoard, self.secondPlayer, self.maxMinMaxLevel,
                                          setInitialAlpha, setInitialBeta, "max")

        self.squareBorder(None)
        originMove = self.halmaGameBoard[bestMovement[0][0]][bestMovement[0][1]]
        targetMove = self.halmaGameBoard[bestMovement[1][0]][bestMovement[1][1]]
        self.selectedPiece = makeMove(originMove, targetMove)
        self.refreshScreen()
        winCondition = checkWinCondtion()
        if winCondition == BoardPieces.whitePiece:
            self.boardView.winMessage(BoardPieces.whitePiece)
            self.currentPlayer = None
            self.boardView.destroy()
        elif winCondition == BoardPieces.blackPiece:
            self.boardView.winMessage(BoardPieces.blackPiece)
            self.currentPlayer = None
            self.boardView.destroy()

        else:
            self.switchPlayer()

        self.isComputerThinking = False