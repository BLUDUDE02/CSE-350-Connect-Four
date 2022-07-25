import numpy as np
import pygame
import pygame_menu
import random
import sys
import math
import os.path as path
import os

#Variable Declarations
RowCount = 6
ColumnCount = 7

Player1 = 0
Player2 = 1

EMPTY = 0
P1Token = 1
P2Token = 2

RED = (155, 26, 10)
YELLOW = (171, 92, 28)
BLUE = (60, 159, 156)

GameMode = 0
Difficulty = 0
ValidMove = True;

tie = False;

WINDOW_LENGTH = 4


saveString = ""
prntUpdate = "Building Board!"
prntWin1 = "PLAYER ONE WINS"
prntWin2 = "PLAYER TWO WINS"
prntTie = "TIE"

#Game Board Class
class GameBoard():
    def __init__(self, RowCount, ColumnCount, SquareSize, screen):
        self.RowCount = RowCount
        self.ColumnCount = ColumnCount
        self.SquareSize = SquareSize
        self.screen = screen
        
    def CreateBoard(self):
        RowCount = self.RowCount
        ColumnCount = self.ColumnCount
        board = np.zeros((RowCount, ColumnCount))
        return board
    
    def DrawBoard(self, board):
        SquareSize = self.SquareSize
        RowCount = self.RowCount
        ColumnCount = self.ColumnCount
        screen = self.screen
        
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
        
        print(prntUpdate)
        global saveString
        saveString += prntUpdate + "\n"
        
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
    global saveString
    print(np.flip(board,0))
    boardtext = np.array2string(np.flip(board,0), 25)
    saveString += boardtext
    

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
    tiescore = 0
    global tie
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
    # Check Tie
    for c in range(ColumnCount):
        for r in range(RowCount):
            if board[r][c] != 0:
                tiescore += 1
    
    if tiescore == RowCount * ColumnCount:
        tie = True
#

#AI Class
def EvaluateWindow(window, piece):
    score = 0
    opp_piece = P1Token
    if piece == P1Token:
        opp_piece = P2Token

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def ScorePosition(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, ColumnCount//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(RowCount):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(ColumnCount-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += EvaluateWindow(window, piece)

    ## Score Vertical
    for c in range(ColumnCount):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(RowCount-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += EvaluateWindow(window, piece)

    ## Score posiive sloped diagonal
    for r in range(RowCount-3):
        for c in range(ColumnCount-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += EvaluateWindow(window, piece)

    for r in range(RowCount-3):
        for c in range(ColumnCount-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += EvaluateWindow(window, piece)

    return score

def IsTerminalNode(board):
    return CheckWin(board, P1Token) or CheckWin(board, P2Token) or len(GetValidLocations(board)) == 0

def MiniMax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = GetValidLocations(board)
    is_terminal = IsTerminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if CheckWin(board, P2Token):
                return (None, 100000000000000)
            elif CheckWin(board, P1Token):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, ScorePosition(board, P2Token))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = GetTopRow(board, col)
            b_copy = board.copy()
            PlacePiece(b_copy, row, col, P2Token)
            new_score = MiniMax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = GetTopRow(board, col)
            b_copy = board.copy()
            PlacePiece(b_copy, row, col, P1Token)
            new_score = MiniMax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def GetValidLocations(board):
    valid_locations = []
    for col in range(ColumnCount):
        if CheckValid(board, col):
            valid_locations.append(col)
    return valid_locations

def PickBestMove(board, piece):

    valid_locations = GetValidLocations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = GetTopRow(board, col)
        temp_board = board.copy()
        PlacePiece(temp_board, row, col, piece)
        score = ScorePosition(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def SetDifficulty(value, difficulty):
    global Difficulty
    Difficulty = difficulty
    pass

#Main Menu Class
BACKGROUND = path.join(path.dirname(path.abspath(__file__)), '{0}').format('Background.png')

background_image = pygame_menu.BaseImage(
    image_path=BACKGROUND)

#


def StartGame(mode):
    global board
    global SquareSize
    global width
    global height
    global turn
    global screen
    global saveString
    global tie
    
    tie = False
    
    GameOver = False
    SquareSize = 100 
    turn = 0
    myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 75)
    
    top = pygame.image.load('Top.png')
    top.convert()

    rect4 = top.get_rect()
    rect4.center = (width/2, SquareSize/2)
    screen.blit(top, rect4)
    
    gameBoard = GameBoard(RowCount, ColumnCount, SquareSize, screen)
    board = gameBoard.CreateBoard()
    LogMove(board)
    gameBoard.DrawBoard(board)


    
    while not GameOver:
        
        # application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                os._exit(00)
                
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
                        print(prntWin1)
                        saveString += prntWin1 + "\n"
                        label = myfont.render("PLAYER ONE WINS", 1, RED)
                        text_rect = label.get_rect(center=(700/2, 100/2))
                        screen.blit(label, text_rect)
                        GameOver = True
                elif turn == Player2 and not mode:              
                    posx = event.pos[0]
                    MakeMove(board, posx, 2)
                    if CheckWin(board, 2):
                        print(prntWin2)
                        saveString += prntWin2 + "\n"
                        label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                        text_rect = label.get_rect(center=(700/2, 100/2))
                        screen.blit(label, text_rect)
                        GameOver = True
                        
                if ValidMove:
                    turn += 1
                    turn = turn % 2

                LogMove(board)
                gameBoard.DrawBoard(board)
                
            if turn == Player2 and mode:
                if Difficulty == 2:
                    col, MiniMax_score = MiniMax(board, 5, -math.inf, math.inf, True)
                    print("MINIMAX AI")
                else:
                    col = random.randint(0, RowCount - 1)
                    print("RANDOM AI")
                    
                if CheckValid(board, col):
                    row = GetTopRow(board, col)
                    PlacePiece(board, row, col, 2)

                    if CheckWin(board, 2):
                        label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                        print(prntWin2)
                        saveString += prntWin2 + "\n"
                        text_rect = label.get_rect(center=(width/2, SquareSize/2))
                        screen.blit(label, text_rect)
                        GameOver = True
                
                turn += 1
                turn = turn % 2 
                
                LogMove(board)
                gameBoard.DrawBoard(board)
                
            if tie:
                print(prntTie)
                saveString += prntTie + "\n"
                label = myfont.render("TIE", 1, BLUE)
                text_rect = label.get_rect(center=(700/2, 100/2))
                screen.blit(label, text_rect)
                GameOver = True
                
            if GameOver:
                #send to endgame menu
                main_menu.disable()
                options_menu.enable()
                break

    try:
        with open('ConnectFourSave.txt', 'w') as f:
            f.write(saveString) 
    except FileNotFoundError:
        print("The 'docs' directory does not exist")
    
            
#Main Class
def background() -> None:
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
    myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 45)
    
    # Menus
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_8BIT
    theme.widget_font = myfont
    theme.background_color = (0, 0, 0, 180)
    
    main_menu = pygame_menu.Menu('Connect 4', width, height, theme=theme)
    main_menu.add.button('Two Player', StartGame, False)
    main_menu.add.selector('AI Mode ', [('Easy', 1), ('Hard', 2)], onchange=SetDifficulty)
    main_menu.add.button('Player VS AI', StartGame, True)
    main_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    options_menu = pygame_menu.Menu('Game Over', 400, 300, theme=theme)
    options_menu.add.button('Two Player', StartGame, False)
    options_menu.add.selector('AI Mode ', [('Easy', 1), ('Hard', 2)], onchange=SetDifficulty)
    options_menu.add.button('Player VS AI', StartGame, True)
    options_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    
    while True:
        
        # events handling for menus 
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                os._exit(00)
        
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

      
    
    