import pygame, sys, random, time
from pygame.locals import *

WINDOWHEIGHT = 600
WINDOWWIDTH = 800

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

BOARDWIDTH = 10
BOARDHEIGHT = 20
CELLSIZE = 25

XMARGIN = (WINDOWWIDTH - CELLSIZE * BOARDWIDTH) / 2
YMARGIN = (WINDOWHEIGHT - BOARDHEIGHT * CELLSIZE) / 2
BORDERWIDTH = 6

BLANK = "."

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)

BORDERCOLOR = BLUE
BGCOLOR = BLACK


COLORS = (GREEN, RED, BLUE, YELLOW)

S_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]


FPS = 30

PIECES = {
    "L": L_TEMPLATE,
    "O": O_TEMPLATE,
    "S": S_TEMPLATE,
    "I": I_TEMPLATE,
    "J": J_TEMPLATE,
    "Z": Z_TEMPLATE,
    "T": T_TEMPLATE
}

def main():
    global DISPLAYSURF, CLOCK
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Tetris")
    CLOCK = pygame.time.Clock()
    showTextScreen("Tetris")
    while True:
        if random.random() > 0.5:
            pygame.mixer.music.load("tetrisb.mid")
        else:
            pygame.mixer.music.load("tetrisc.mid")
        pygame.mixer.music.play(-1, 0, 0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen("Game Over")

def runGame():
    board = getStartingBoard()
    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    level = 1
    score = 0
    fallFreq = 0.3
    lastFallTime = time.time()

    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()
            if not isValidPosition(board, fallingPiece):
                return


        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP and event.key == K_SPACE:
                pygame.mixer.music.stop()
                showTextScreen("Paused")
                pygame.mixer.music.play(-1, 0, 0)
            elif event.type == KEYUP and event.key == K_LEFT and isValidPosition(board, fallingPiece, -1, 0):
                fallingPiece["x"] -= 1
            elif event.type == KEYUP and event.key == K_RIGHT and isValidPosition(board, fallingPiece, 1, 0):
                fallingPiece["x"] += 1
            elif event.type == KEYUP and event.key == K_DOWN and isValidPosition(board, fallingPiece, 0, 1):
                fallingPiece["y"] += 1
            elif event.type == KEYUP and event.key == K_UP:
                fallingPiece["rotation"] = (fallingPiece["rotation"] + 1) % len(PIECES[fallingPiece["shape"]])
                if not isValidPosition(board, fallingPiece):
                    fallingPiece["rotation"] = (fallingPiece["rotation"] - 1) % len(PIECES[fallingPiece["shape"]])


        if time.time() - lastFallTime >= fallFreq:
            if isValidPosition(board, fallingPiece, 0, 1):
                fallingPiece["y"] += 1
                lastFallTime = time.time()
            else:
                addPieceToBoard(fallingPiece, board)
                fallingPiece = None
                score += removeCompleteLines(board)
                level = int(score / 10) + 1
                fallFreq = 0.3 - level * 0.02

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        drawGameStatus(score, level, nextPiece)

        pygame.display.update()
        CLOCK.tick(FPS)


def getStartingBoard():
    board =  []
    for x in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def terminate():
    pygame.quit()
    sys.exit()

def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {
        "shape": shape, 
        "rotation": random.randint(0, len(PIECES[shape]) - 1),
        "x": int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        "y": -2,
        "color": random.randint(0, len(COLORS) - 1)
    }
    return newPiece

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def isValidPosition(board, piece, dx = 0, dy = 0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if y + dy + piece["y"] < 0:
                continue
            if PIECES[piece["shape"]][piece["rotation"]][y][x] != BLANK and not isOnBoard(x + dx + piece["x"], y + dy + piece["y"]):
                return False
            elif PIECES[piece["shape"]][piece["rotation"]][y][x] != BLANK and board[x + piece["x"] + dx][y + piece["y"] + dy] != BLANK:
                return False
            
    return True

def addPieceToBoard(piece, board):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece["shape"]][piece["rotation"]][y][x] != BLANK:
                board[x + piece["x"]][y + piece["y"]] = piece["color"]

def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - BORDERWIDTH, YMARGIN - BORDERWIDTH, BOARDWIDTH * CELLSIZE + 2 * BORDERWIDTH, BOARDHEIGHT * CELLSIZE + 2 * BORDERWIDTH), BORDERWIDTH)

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawCell(x, y, board[x][y])

def drawCell(x, y, color, left = 0, top = 0):
    if color == BLANK: 
        return
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (x * CELLSIZE + XMARGIN + left, y * CELLSIZE + YMARGIN + top, CELLSIZE, CELLSIZE))
    pygame.draw.rect(DISPLAYSURF, BLACK, (x * CELLSIZE + XMARGIN + left, y * CELLSIZE + YMARGIN + top, CELLSIZE, CELLSIZE), 1)

def drawPiece(piece, left = 0, top = 0):
    shape = PIECES[piece["shape"]][piece["rotation"]]
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shape[y][x] != BLANK:
                 drawCell(piece["x"] + x, piece["y"] + y, piece["color"], left, top)

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def removeCompleteLines(board):
    y = BOARDHEIGHT - 1
    removedLinesNum = 0
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDown in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDown] = board[x][pullDown - 1]

            for x in range(BOARDWIDTH):
                board[x][0] = BLANK

            removedLinesNum += 1
        else:
            y -= 1
    return removedLinesNum

def drawGameStatus(score, level, nextPiece):
    scoreSurf, scoreRect = makeText("score: " + str(score), 20)   
    levelSurf, levelRect = makeText("level: " + str(level), 20)
    nextSurf, nextRect = makeText("next: ", 20)

    scoreRect.topleft = (WINDOWWIDTH - 200, 100)
    levelRect.topleft = (WINDOWWIDTH - 200, 150)
    nextRect.topleft = (WINDOWWIDTH - 200, 200)
    
    DISPLAYSURF.blit(scoreSurf, scoreRect) 
    DISPLAYSURF.blit(levelSurf, levelRect)
    DISPLAYSURF.blit(nextSurf, nextRect)
    drawPiece(nextPiece, 250, 250)

def makeText(text, fontSize, color=WHITE):
    font = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect()    
    return textSurf, textRect

def showTextScreen(message):
    messageSurf, messageRect = makeText(message, 120, GRAY)
    messageRect.center = (WINDOWWIDTH / 2 + 3, WINDOWHEIGHT / 2 - 50 + 3)
    DISPLAYSURF.blit(messageSurf, messageRect)

    messageSurf, messageRect = makeText(message, 120)
    messageRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 50)
    DISPLAYSURF.blit(messageSurf, messageRect)


    keyPressSurf, keyPressRect = makeText("Press a key to play.", 20)
    keyPressRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50)
    DISPLAYSURF.blit(keyPressSurf, keyPressRect)

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                return
            elif event.type == QUIT:
                terminate()
        pygame.display.update()
        CLOCK.tick(FPS)

main()