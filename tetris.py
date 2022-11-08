#################################################
# hw8.py: 2d Lists + Tetris!
#
# Your name: Audrey Simon
# Your andrew id: afsimon
#
# Your partner's name: NA
# Your partner's andrew id: NA
#################################################

import cs112_s21_week8_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

# First, we must check whether L is a list and if the length is smaller than 2.
# Next, we check if the first index of L is also a list. If so, we make the 
# variable listLength equal the first index length. For special cases 
# such as when L is a 2d list with empty lists, we make listLength 0. 
# Next, we loop through each value in L. If any value isn't a list or isn't 
# equal to the length of the first index, the function returns False. 
# If all values are lists and have the same length, the function returns True.
def isRectangular(L):
    if not isinstance(L,list) or len(L)<2:
        return False
    if len(L)<=0:
        listLength = 0
    else:
        if isinstance(L[0],list):
            listLength = len(L[0])
    for i in L:
        if not isinstance(i,list) or listLength!=len(i):
            return False
    return True

# make2dList function copied from cmu112
def make2dList(rows, cols, placement):
    return [ ([placement] * cols) for row in range(rows) ]

# First check if n is odd and above 0. Then, we create a variable lst that
# makes a 2d list of dimensions n x n. Before looping through each value 
# up to n^2, we first place 1 at the middle of the first row. In the loop, 
# we subtract 1 from row and add 1 to col to get the top right index from
# the previous number. If the row is looped over twice (-n-1), row is changed
# to -1. If col moves out of the index (n), col is changed to 0. If the place
# that the value is supposed to be placed at is occupied, the rows are added
# 2 and the col subtracts 1 so the value is placed in the row below. 
def makeMagicSquare(n):
    if n%2==0 or n<=0:
        return None
    lst = (make2dList(n,n,0))
    lst[0][n//2]=1
    row = 0
    col = n//2
    for i in range(1,n**2):
        row-=1
        col+=1
        if row==-n-1:
            row=-1
        if col==n:
            col=0
        if lst[row][col]!=0:
            row+=2
            col-=1
        lst[row][col]=i+1
    return lst
###########################################################################
# gameDimensions stores the rows, cols, cellSize, and margins of the game. 
# If a player wants to change any dimensions, they should do so in this 
# function.
def gameDimensions():
    rows = 30
    cols = 10
    cellSize = 30
    margin = 25
    return rows,cols,cellSize,margin

# playTetris takes the values given in gameDimensions to create the width 
# and height for the game. This is where the canvas size is stored.
def playTetris():
    rows,cols,cellSize,margin = gameDimensions()
    width = 2*margin+cellSize*cols
    height = 2*margin+cellSize*rows
    runApp(width=width, height=height)

# The global variables are kept under appStarted. app.gameOver stays False
# until the game is over. The app.rows, app.cols, app.cellSize, app.margin,
# app.width, and app.height are all created using gameDimensions. 
# app.emptyColor stores the color of the empty squares, and app.board stores
# the 2d list of each square. app.score stores the score the player has every
# game. 
def appStarted(app):
    app.gameOver=False
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.width = 2*app.margin+app.cellSize*app.cols
    app.height = 2*app.margin+app.cellSize*app.rows
    app.emptyColor = "grey"
    app.board = make2dList(app.rows,app.cols,app.emptyColor)
    app.score = 0
    app.timerDelay = 700
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [iPiece,jPiece,lPiece,oPiece,sPiece,tPiece,zPiece]
    app.tetrisPieceColors = ['red','yellow','magenta','pink','cyan','green',
    'orange']
    newFallingPiece(app)
    print(app.board)
# newFallingPiece randomly selects a number in the index of app.tetrisPieces
# to select a piece and color for tetris. app.fallingPiece and 
# app.fallingPieceColor store the type of piece and color of the current
# falling piece. The fallingPieceRow starts at the top of the screen (0),
# and the fallingPieceCol is placed so the piece is in the center. 
def newFallingPiece(app):
    import random
    randomIndex = random.randint(0,len(app.tetrisPieces)-1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols//2-len(app.fallingPiece[0])//2

# The current falling piece is drawn using this function by creating a nested
# for loop and iterating through each value in app.fallingPiece. If the value
# is true, the color of the cell changes to app.fallingPieceColor. 
def drawFallingPiece(app,canvas):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col] == True:
                drawCell(app,canvas,app.fallingPieceRow+row,
                app.fallingPieceCol+col,
                app.fallingPieceColor)

# This function checks if the location of the falling piece is legal in the 
# game. If any of the rows or cols of the falling piece are out of bounds,
# meaning less than 0 or greater than the cell row/col length, the function 
# returns false. The function also returns false if the falling piece row
# or col is placed at an occupied cell, meaning the cell isn't the empty color.
def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            cellRow = app.fallingPieceRow+row
            cellCol = app.fallingPieceCol+col 
            if app.fallingPiece[row][col] == True:
                if 0>app.fallingPieceRow or 0>app.fallingPieceCol:
                    return False
                elif cellRow>app.rows-1 or cellCol>app.cols-1:
                    return False
                elif app.board[cellRow][cellCol]!=app.emptyColor:
                    return False
    return True

# This function rotates the piece and centers it on the screen. The old 
# variables are created to compare app.fallingRow before it rotated. The
# variable rotated is created, which makes a 2d list of the dimensions of 
# the falling piece but with the rows and cols switched. By creating a
# nested for loop, the values of rotated take in the rows and cols of 
# the falling piece. The falling piece then becomes the variable rotated. 
# If the rotated piece is not legal, the falling piece reverts back to its
# original self. 
def rotateFallingPiece(app):
    oldRow = app.fallingPieceRow
    oldNumRows = len(app.fallingPiece)
    oldCol = app.fallingPieceCol
    oldNumCols = len(app.fallingPiece[0])
    tempPiece = app.fallingPiece
    rotated = make2dList(oldNumCols,oldNumRows,None)
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            rotated[oldNumCols-col-1][row]=app.fallingPiece[row][col]
    app.fallingPiece = rotated
    newNumRows = len(app.fallingPiece)
    newNumCols = len(app.fallingPiece[0])
    app.fallingPieceRow = oldRow + oldNumRows//2 - newNumRows//2
    app.fallingPieceCol = oldCol + oldNumCols//2 - newNumCols//2
    if not fallingPieceIsLegal(app):
        app.fallingPiece = tempPiece

# This function moves the falling piece in a direction based on what the
# parameters are. If drow is +1, the falling piece moves down. If drow is -1,
# the falling piece moves up. If dcol is +1, the piece moves right, and if
# dcol lis -1, the piece moves left. If the move is illegal, the row and col
# will revert to its original position and the falling piece doesn't move.
def moveFallingPiece(app,drow,dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True

# R key makes the app restart. The rest of the keys only work if the game 
# is not over. When the player presses right, the piece will go right.
# When the player presses left, the piece will go left. If the player presses
# up, the piece rotates. If the player presses space, the falling piece will
# be moved all the way to the bottom.
def keyPressed(app,event):
    if event.key=="r":
        appStarted(app)
    if app.gameOver==True:
        return
    if event.key=='Right':
        moveFallingPiece(app,0,1)
    if event.key=='Left':
        moveFallingPiece(app,0,-1)
    if event.key=="Up":
        rotateFallingPiece(app)
    if event.key=="Space":
        while moveFallingPiece(app,1,0)==True:
            moveFallingPiece(app,1,0)

# timerFired is constantly checking gameOver to see when the game is finished.
# Once the falling piece can't move down anymore, a new piece is generated 
# at the top and placeFallingPiece is called for the old piece. 
def timerFired(app):
    if app.gameOver==True:
        return
    if moveFallingPiece(app,1,0)==False:
        placeFallingPiece(app)
        newFallingPiece(app)
    if moveFallingPiece(app,0,0)==False:
        app.gameOver=True
    removeFullRows(app)

# This function adds the falling piece that can't move anymore to app.board.
# This happens by making a nested for loop for the falling piece. If the
# row and col of the falling piece is true, the app.board color in that pos
# changes to the falling piece color. 
def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]==True:
                boardRow = app.fallingPieceRow+row
                boardCol = app.fallingPieceCol+col
                app.board[boardRow][boardCol]=app.fallingPieceColor

# This will remove all the full rows in the board. When there are no empty 
# colors in a row, the board removes the row and adds a new row of empty colors
# to the top of the board.
def removeFullRows(app):
    for row in app.board:
        if app.emptyColor not in row:
            app.board = [[app.emptyColor]*app.cols]+app.board
            app.board.remove(row)
            app.score += 1

# drawCell creates each cell for the tetris board. The color of the cell depends
# on the color put in the parameter. 
def drawCell(app,canvas,row,col,color):
    canvas.create_rectangle(app.margin+app.cellSize*col,
    app.cellSize*row+app.margin,app.cellSize*(col+1)+app.margin,
    app.cellSize*(row+1)+app.margin,fill=color,width=3)

# drawBoard creates the grid shown on tetris. It creates a nested for loop then
# calls drawCell to create each cell. 
def drawBoard(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app,canvas,row,col,app.board[row][col])

# This function shows the score of the player at the top of the tetris game.
# A f string is created to do this. 
def drawScore(app,canvas):
    canvas.create_text(app.width//2,app.margin//2,text=f'Score: {app.score}',
    font="Arial 16 bold",fill="Navy")

# When the game is over, this function creates a sign at the top of the tetris
# game to tell the player that the game is over. 
def drawGameOver(app,canvas):
    if app.gameOver==True:
        canvas.create_rectangle(app.margin,app.margin+app.cellSize,
        app.width-app.margin,app.margin+3*app.cellSize,fill='black')
        canvas.create_text(app.width//2,app.margin+2*app.cellSize,
        text="Game Over!!",font="Arial 18 bold",fill="Yellow")

# RedrawAll calls all the canvas functions to be rewritten when the app starts
# and restarts.
def redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='orange')
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    drawGameOver(app,canvas)
    drawScore(app,canvas)

#################################################
# Test Functions
#################################################

def testIsRectangular():
    print('Testing isRectangular()...', end='')
    assert(isRectangular([[1,2],[3,4]]) == True)
    assert(isRectangular([[1,2],[3,4,5]]) == False)
    assert(isRectangular([[1],[2]]) == True)
    assert(isRectangular([[],[]]) == True)
    assert(isRectangular([]) == False)
    assert(isRectangular(["this", "is", "silly"]) == False)
    assert(isRectangular([["this"], "is", "silly"]) == False)
    assert(isRectangular([["this"], ["is"], ["fine"]]) == True)
    assert(isRectangular([[1], [2,3], [4]]) == False)
    assert(isRectangular([[1,2], [3], [4]]) == False)
    assert(isRectangular([12, [3], [4]]) == False)
    assert(isRectangular(["abc", [1,2,3]]) == False)
    print('Passed!')

def testMakeMagicSquare():
    print('Testing makeMagicSquare()...', end='')
    L1 = [[1]]
    L3 = [[8 , 1 , 6],
          [3 , 5 , 7],
          [4 , 9 , 2]]
    L5 = [[17 , 24 ,  1 ,   8 , 15],
          [23 ,  5 ,  7 ,  14 , 16],
          [ 4 ,  6 , 13 ,  20 , 22],
          [10 , 12 , 19 ,  21 ,  3],
          [11 , 18 , 25 ,   2 ,  9]]
    L9 = [[47,58,69,80,1,12,23,34,45],
          [57,68,79,9,11,22,33,44,46],
          [67,78,8,10,21,32,43,54,56],
          [77,7,18,20,31,42,53,55,66],
          [6,17,19,30,41,52,63,65,76],
          [16,27,29,40,51,62,64,75,5],
          [26,28,39,50,61,72,74,4,15],
          [36,38,49,60,71,73,3,14,25],
          [37,48,59,70,81,2,13,24,35]]
    assert(makeMagicSquare(1) == L1)
    assert(makeMagicSquare(3) == L3)
    assert(makeMagicSquare(5) == L5)
    assert(makeMagicSquare(9) == L9)
    assert(makeMagicSquare(0) == None)
    assert(makeMagicSquare(2) == None)
    assert(makeMagicSquare(4) == None)
    assert(makeMagicSquare(-3) == None)
    print('Passed!')

def testAll():
    testIsRectangular()
    testMakeMagicSquare()

#################################################
# main
#################################################

def main():
    cs112_s21_week8_linter.lint()
    testAll()
    playTetris()

if __name__ == '__main__':
    main()
