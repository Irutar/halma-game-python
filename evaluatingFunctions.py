import math
import numpy as np

from movement import generatePossibleMovementForAllEvaluatedSidePieces
from boardInformation import BoardPieces, BoardSquares

whiteStartingArea = None
blackStartingArea = None


def victoryConditions(currentBoard, homeArea):
    victoryList = []
    for board in currentBoard:
        for square in board:
            if square.tile == homeArea:
                victoryList.append(square)
    return victoryList


def setVictoryConditions(halmaGameBoard):
    global whiteStartingArea
    global blackStartingArea
    whiteStartingArea = victoryConditions(halmaGameBoard, BoardSquares.whiteHomeArea)
    blackStartingArea = victoryConditions(halmaGameBoard, BoardSquares.blackHomeArea)


def checkWinCondtion():

    winFlag = True
    for black in whiteStartingArea:
        if black.piece != BoardPieces.blackPiece:
            winFlag = False
    if winFlag:
        return BoardPieces.blackPiece

    winFlag = True
    for white in blackStartingArea:
        if white.piece != BoardPieces.whitePiece:
            winFlag = False
    if winFlag:
        return BoardPieces.whitePiece
    else:
        return None


def checkScoringCondition(computerPlayer, minMaxLevel, boardSize, halmaGameBoard):

    if minMaxLevel == 0:
        return scoringFunction(computerPlayer, boardSize, halmaGameBoard), None

    elif checkWinCondtion():
        return scoringFunction(computerPlayer, boardSize, halmaGameBoard), None

    else:
        return False


def minimax(boardSize, halmaGameBoard, computerPlayer, minMaxLevel, alpha, beta, minOrMaxOperation):

    conditionCheck = checkScoringCondition(computerPlayer, minMaxLevel, boardSize, halmaGameBoard)
    if conditionCheck:
        return conditionCheck

    minMaxedMove = None
    if minOrMaxOperation == "max":
        listOfAllPossibleMovementsList = generatePossibleMovementForAllEvaluatedSidePieces(computerPlayer, boardSize,
                                                                                           halmaGameBoard)
        unitlityValue = float("-inf")

    else:
        if computerPlayer == BoardPieces.blackPiece:
            listOfAllPossibleMovementsList = generatePossibleMovementForAllEvaluatedSidePieces(
                BoardPieces.whitePiece, boardSize, halmaGameBoard)
        else:
            listOfAllPossibleMovementsList = generatePossibleMovementForAllEvaluatedSidePieces(
                BoardPieces.blackPiece, boardSize, halmaGameBoard)

        unitlityValue = float("inf")

    for possibleMovementList in listOfAllPossibleMovementsList:
        for destinationMovement in possibleMovementList[1]:
            if minOrMaxOperation == "max":
                nextOperation = "min"
            else:
                nextOperation = "max"

            startingPossition = possibleMovementList[0].piece
            possibleMovementList[0].piece = BoardPieces.noPiece
            destinationMovement.piece = startingPossition
            finalUtilityValue, _ = minimax(boardSize, halmaGameBoard, computerPlayer, minMaxLevel - 1, alpha, beta,
                                           nextOperation)
            destinationMovement.piece = BoardPieces.noPiece
            possibleMovementList[0].piece = startingPossition
            if minOrMaxOperation == "max" and finalUtilityValue > unitlityValue:
                unitlityValue = finalUtilityValue
                minMaxedMove = (possibleMovementList[0].coordinates, destinationMovement.coordinates)
                if alpha < finalUtilityValue:
                    alpha = finalUtilityValue

            if minOrMaxOperation == "min" and finalUtilityValue < unitlityValue:
                unitlityValue = finalUtilityValue
                minMaxedMove = (possibleMovementList[0].coordinates, destinationMovement.coordinates)
                if beta > finalUtilityValue:
                    beta = finalUtilityValue

            if beta <= alpha:
                return unitlityValue, minMaxedMove

    return unitlityValue, minMaxedMove


def distanceFromWinningArea(destinationCoordinates, startingCoordinates):
    a = destinationCoordinates[0] - startingCoordinates[0]
    b = destinationCoordinates[1] - startingCoordinates[1]
    return math.sqrt(a ** 2 + b ** 2)


def scoringFunction(player, boardSize, halmaGameBoard):
    score = 0
    for row in range(0, boardSize):
        for col in range(0, boardSize):
            square = halmaGameBoard[row][col]
            if square.piece == BoardPieces.blackPiece:
                distances = []
                for startingSquare in whiteStartingArea:
                    if startingSquare.piece != BoardPieces.blackPiece:
                        distances.append(distanceFromWinningArea(startingSquare.coordinates, square.coordinates))
                if len(distances):
                    score = score - max(distances)

            elif square.piece == BoardPieces.whitePiece:
                distances = []
                for startingSquare in blackStartingArea:
                    if startingSquare.piece != BoardPieces.whitePiece:
                        distances.append(distanceFromWinningArea(startingSquare.coordinates, square.coordinates))
                if len(distances):
                    score = score + max(distances)
    if player == BoardPieces.whitePiece:
        score = np.negative(score)
    return score