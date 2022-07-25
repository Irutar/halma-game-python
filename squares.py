from boardInformation import PieceBorder, MovementClolor


class squares():
    def __init__(self, row, col, tile, piece, border):
        self.tile = tile
        self.piece = piece
        self.border = border
        self.coordinates = (row, col)

    def getSquareColors(self):

        neutralAreaSquares = ["#ffffff", "#757678"]
        playersAreaSquares = ["#FEFFDA", "#2F3535"]

        boardSquares = [neutralAreaSquares, playersAreaSquares, playersAreaSquares]

        if self.tile == "WhitePlayerTile":
            squareColor = boardSquares[2][(self.coordinates[0] + self.coordinates[1]) % 2]
        elif self.tile == "BlackPlayerTile":
            squareColor = boardSquares[1][(self.coordinates[0] + self.coordinates[1]) % 2]
        else:
            squareColor = boardSquares[0][(self.coordinates[0] + self.coordinates[1]) % 2]

        if self.border == PieceBorder.selectedPieceBorder:
            borderColor = MovementClolor.selectedPieceBorder
        elif self.border == PieceBorder.possibleMovementBorder:
            borderColor = MovementClolor.possibleMovementBorder
        elif self.border == PieceBorder.movedBorder:
            borderColor = MovementClolor.movedBorder
        else:
            borderColor = squareColor

        return squareColor, borderColor

