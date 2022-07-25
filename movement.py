from boardInformation import BoardPieces, PieceBorder


def checkOutsideOfBoardSquares(x, y, boardSize):
    if x < 0 or y < 0 or x >= boardSize or y >= boardSize:
        return True
    else:
        return False


def checkImpossibleSquares(newX, newY, oldX, oldY, boardSize):
    if (newX == oldX and newY == oldY) or checkOutsideOfBoardSquares(newX, newY, boardSize):
        return True
    else:
        return False


def checkJumpSquares(newX, newY, xMovement, yMovement, boardSize, movementList, gameBoard):
    newX = newX + xMovement
    newY = newY + yMovement

    if checkOutsideOfBoardSquares(newX, newY, boardSize):   # check if move is inside the game board
        return movementList

    considerateSquare = gameBoard[newX][newY]
    if considerateSquare in movementList:   # check if move is already in list of possible movements
        return movementList

    if considerateSquare.piece == BoardPieces.noPiece:
        movementList.append(considerateSquare)
        generatePossibleMovementsAtSelectedSquare(movementList, considerateSquare, boardSize, gameBoard, False)

    return movementList


def generatePossibleMovementsAtSelectedSquare(movementList, square, boardSize, gameBoard, firstJump):
    if movementList is None:
        movementList = []

    xCoordniate = square.coordinates[0]
    yCoordinate = square.coordinates[1]
    for yMovement in range(-1, 2):
        for xMovement in range(-1, 2):
            newXCoordinate = xCoordniate + xMovement
            newYCoordinate = yCoordinate + yMovement
            if checkImpossibleSquares(newXCoordinate, newYCoordinate, xCoordniate, yCoordinate, boardSize):
                continue

            considerateSquare = gameBoard[newXCoordinate][newYCoordinate]
            if considerateSquare.piece == BoardPieces.noPiece:
                if firstJump:
                    movementList.append(considerateSquare)
                continue

            movementList = checkJumpSquares(newXCoordinate, newYCoordinate, xMovement, yMovement, boardSize,
                                            movementList, gameBoard)

    return movementList


def makeMove(origin, destination):
    destination.piece = origin.piece
    destination.border = PieceBorder.movedBorder
    origin.piece = BoardPieces.noPiece
    origin.border = PieceBorder.movedBorder
    return None


def checkIfPieceBelongsToEcaluatedSide(evaluwatedSide, piece):
    return evaluwatedSide != piece

def generatePossibleMovementForAllEvaluatedSidePieces(evaluwatedSide, boardSize, halmaGameBoard):
    listOfAllPossibleMovementsList = []
    for col in range(0, boardSize):
        for row in range(0, boardSize):

            startingPossition = halmaGameBoard[row][col]
            if checkIfPieceBelongsToEcaluatedSide(evaluwatedSide, startingPossition.piece):
                continue
            listOfPossibleMovementPositions = generatePossibleMovementsAtSelectedSquare(None, startingPossition,
                                                                                        boardSize,
                                                                                        halmaGameBoard, True)

            possibleMovementList = [startingPossition, listOfPossibleMovementPositions]
            listOfAllPossibleMovementsList.append(possibleMovementList)
    return listOfAllPossibleMovementsList