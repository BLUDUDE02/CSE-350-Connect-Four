import numpy as np
import pygame
import pygame_menu
import sys
import math
import os.path as path

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
BACKGROUND = path.join(path.dirname(path.abspath(__file__)), '{0}').format('Background.png')

background_image = pygame_menu.BaseImage(
    image_path=BACKGROUND
)


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
 
    SquareSize = 100 
    
    myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 75)
    
    top = pygame.image.load('Top.png')
    top.convert()

    rect4 = top.get_rect()
    rect4.center = (width/2, SquareSize/2)
    screen.blit(top, rect4)

    DrawBoard(board)

    turn = 0
    
    while not GameOver:
        
        # application events
        events = pygame.event.get()
        for event in events:
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
                #send to endgame menu
                #pygame.time.wait(3000)
                main_menu.disable()
                options_menu.enable()
                
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        quit()
                break        

                    

#Main Class
def background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    

    background = pygame.image.load('Background.png')
    background.convert()
    
    background_image = pygame.image.load('Background.png')
    surface.blit(background_image)
    
    pygame.display.update()
    """
    global screen
    background_image.draw(screen)

def main(test: bool = False) -> None:
    
    global main_menu
    global options_menu
    global screen
    global width
    global height
    
    pygame.init()
    
    #Post PyGame Initialization Variable Declarations    
    width = 700
    height = 700
    size = (width, height)
    screen = pygame.display.set_mode(size)
    
    

    
    # -------------------------------------------------------------------------
    # Menus
    # -------------------------------------------------------------------------
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_8BIT
    theme.widget_font = pygame_menu.font.FONT_8BIT
    theme.background_color = (0, 0, 0, 180)
    
    main_menu = pygame_menu.Menu('Connect 4', width*0.8, height*0.8, theme=theme)
    main_menu.add.button('Two Player', StartGame)
    main_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    options_menu = pygame_menu.Menu('Game Over', 400, 300, theme=theme)
    options_menu.add.button('Back to Start', pygame_menu.events.BACK)
    options_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    
    while True:
        
        # events handling for menus -- turn this in to function
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu.enable()
        
                    # Quit this function, then skip to loop of main-menu
                    return
        
        # Pass events to main_menu
        if main_menu.is_enabled():
            main_menu.update(events)
            
        if options_menu.is_enabled():
            options_menu.update(events)
            options_menu.draw(screen)
    
        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(screen, background)
            
        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break
        
if __name__ == '__main__':
        main()

      
    
    