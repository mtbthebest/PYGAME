#!/usr/bin/env python
# coding=utf-8
# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame,sys,random
from pygame.locals import *
FPS = 30
WINDOWSWIDTH = 640
WINDOWSHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0
XMARGIN = int((WINDOWSWIDTH - (BOARDWIDTH *(BOXSIZE + GAPSIZE)))/2)
YMARGIN = int((WINDOWSHEIGHT - (BOARDHEIGHT *(BOXSIZE + GAPSIZE)))/2)

GRAY= (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE= (255, 255, 255)
RED= (255,0,0)
GREEN= ( 0, 255,0)
BLUE= ( 0,0, 255)
YELLOW= (255, 255,0)
ORANGE= (255, 128,0)
PURPLE= (255,0, 255)
CYAN= ( 0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        shape , color = getShapeAndColor(board,box[0],box[1])
        drawIcon(shape,color,box[0],box[1])

        if coverage >0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage,BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE *0.25)
    half = int(BOXSIZE * 0.5)

    left , top = leftTopCoordsOfBox(boxx, boxy)

    if shape ==DONUT:
        pygame.draw.circle(DISPLAYSURF, color,(left + half, top + half), half -5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))

    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half),
                                                 (left + half, top + BOXSIZE - 1), (left, top +half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter,  BOXSIZE, half))

def leftTopCoordsOfBox(boxx,boxy):
    '''
    Get the top left corners
    :param boxx
    :param boxy
    :return:X_LEFTTOP,Y_LEFTTOP
    '''
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top =boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawBoard(board,revealed):
    '''
    Draws all of the boxes in their covered or revealed state.
    :param board
    :param revealed
    :return: None
    '''
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape,color,boxx,boxy)

def generateRevealedBoxesData(val):
    """
    List of boolean of boxes revealed during the game
    :return revealBoxes=[[BOOL]*HEIGHT] with len(revealBoxes) = BOARDWIDTH
    """
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] *BOARDHEIGHT)
    return revealedBoxes

def splitIntoGroupsOf(groupSize,theList):
    '''
    Split the board into groupSize
    :param groupSize
    :param theList
    :return: List of group of icons
    '''
    result = []
    for i in range(0,len(theList), groupSize):
        result.append((theList[i:i+groupSize]))
    return result

def startGameAnimation(board):
    '''
    Randomly reveal 8 boxes  at a time.
    :param board
    :return: None
    '''
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8,boxes)
    drawBoard(board,coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        coverBoxesAnimation(board,boxGroup)

def getRandomizeBoard():
    """
    Extract board with specific shape and color
    :return board=[(SHAPE,COLOR)] with len(board) = number of icons * 2 in the board
    """
    icons= []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape,color))
    random.shuffle(icons)
    numIconUsed = int(BOARDWIDTH * BOARDHEIGHT /2)
    icons = icons[:numIconUsed] *2
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board




def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWSWIDTH,WINDOWSHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Memory game")
    mainBoard = getRandomizeBoard()
    revealedBoxes= generateRevealedBoxesData(False)

    firstSelection =None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)




if __name__ == '__main__':
    main()