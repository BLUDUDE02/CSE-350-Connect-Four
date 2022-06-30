import numpy as np
import pygame
import pygame_menu
import sys
import math

#Variable Declarations
RowCount = 6
ColumnCount = 7

Player1 = 0
Player2 = 1

P1Token = 1
P2Token = 2

RED = (155, 26, 10)
YELLOW = (171, 92, 28)

GameMode = 0
Difficulty = 0
ValidMove = True;

#Game Board Class
def CreateBoard():
    board = np.zeros((RowCount, ColumnCount))
    return board

def DrawBoard(board):
    casing = pygame.image.load('Casing.png')
    casing.convert()
    rect = casing.get_rect()
    blankspace = pygame.image.load('Blank-Space.png')
    blankspace.convert()
    rect0 = blankspace.get_rect()
    redtok = pygame.image.load('Red-Token.png')
    redtok.convert()
    rect1 = redtok.get_rect()
    yeltok = pygame.image.load('Yellow-Token.png')
    yeltok.convert()
    rect2 = yeltok.get_rect()
    
    print("Building Board!")
    
    for c in range(ColumnCount):
        for r in range(RowCount):
            rect.center = (int(c*SquareSize+SquareSize/2), int(r*SquareSize+SquareSize+SquareSize/2))
            rect0.center = (int(c*SquareSize+SquareSize/2), int(r*SquareSize+SquareSize+SquareSize/2))
            screen.blit(casing, rect)
            screen.blit(blankspace, rect0)
    for c in range(ColumnCount):
        for r in range(RowCount):        
            if board[r][c] == P1Token:
                rect1.center = (int(c*SquareSize+SquareSize/2), height-int(r*SquareSize+SquareSize/2))
                screen.blit(redtok, rect1)
            elif board[r][c] == P2Token: 
                rect2.center = (int(c*SquareSize+SquareSize/2), height-int(r*SquareSize+SquareSize/2))
                screen.blit(yeltok, rect2)
    pygame.display.update()
#

#Game Play Class
#Placement Function
def PlacePiece(board, row, col, piece):
    board[row,col] = piece
    
#Play Validator
def CheckValid(board, col):
    return board[(RowCount-1), col] == 0

#Top Available Spot Locator Function
def GetTopRow(board, col):
    for r in range(RowCount):
        if board[r, col] == 0:
            return r

#Output Board in Log
def LogMove(board):
    print(np.flip(board,0))

#Handle input from mouse position
def MakeMove(board, posx, piece):
    global ValidMove
    col = int(math.floor(posx/SquareSize))
    if CheckValid(board, col):
        ValidMove = True
        row = GetTopRow(board, col)
        PlacePiece(board, row, col, piece)
    else:
        ValidMove = False
        
#Find Winning Move       
def CheckWin(board, piece):
    # Check horizontal locations for win
    for c in range(ColumnCount-3):
        for r in range(RowCount):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(ColumnCount):
        for r in range(RowCount-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(ColumnCount-3):
        for r in range(RowCount-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(ColumnCount-3):
        for r in range(3, RowCount):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
#

#Main Menu Class
def StartGame():
    global board
    global SquareSize
    global width
    global height
    global turn
    global screen
    
    GameOver = False
    
    board = CreateBoard()
    LogMove(board)
    pygame.init()

    #Post PyGame Initialization Variable Declarations
    SquareSize = 100

    width = 700
    height = 700
    size = (width, height)

    screen = pygame.display.set_mode(size)
    
    myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 75)
    
    top = pygame.image.load('Top.png')
    top.convert()

    rect4 = top.get_rect()
    rect4.center = (width/2, SquareSize/2)
    screen.blit(top, rect4)

    DrawBoard(board)

    turn = 0
    
    while not GameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                top = pygame.image.load('Top.png')
                top.convert()
                
                rect4 = top.get_rect()
                rect4.center = (width/2, SquareSize/2)
                screen.blit(top, rect4)
                posx = event.pos[0]
                posxr = round(posx/10)*10
                if turn == Player1:
                    redtok = pygame.image.load('Red-Token.png')
                    redtok.convert()

                    rect1 = redtok.get_rect()
                    rect1.center = (posxr, int(SquareSize/2))
                    screen.blit(redtok, rect1)
                elif turn == Player2:
                    yeltok = pygame.image.load('Yellow-Token.png')
                    yeltok.convert()
                    
                    rect2 = yeltok.get_rect()
                    rect2.center = (posxr, int(SquareSize/2))
                    screen.blit(yeltok, rect2)
                    
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                top = pygame.image.load('Top.png')
                top.convert()
                
                rect4 = top.get_rect()
                rect4.center = (width/2, SquareSize/2)
                screen.blit(top, rect4)
                
                if turn == Player1:
                    posx = event.pos[0]
                    MakeMove(board, posx, 1)
                    if CheckWin(board, 1):
                        print("PLAYER ONE WINS")
                        label = myfont.render("PLAYER ONE WINS", 1, RED)
                        text_rect = label.get_rect(center=(700/2, 100/2))
                        screen.blit(label, text_rect)
                        GameOver = True
                elif turn == Player2:              
                    posx = event.pos[0]
                    MakeMove(board, posx, 2)
                    if CheckWin(board, 2):
                        print("PLAYER TWO WINS")
                        label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                        text_rect = label.get_rect(center=(700/2, 100/2))
                        screen.blit(label, text_rect)
                        GameOver = True
                        
                if ValidMove:
                    turn += 1
                    turn = turn % 2

                LogMove(board)
                DrawBoard(board)
                
            if GameOver:
                pygame.time.wait(3000)
#

#Main Class
StartGame()
    
    