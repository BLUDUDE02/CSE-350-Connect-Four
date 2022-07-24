import numpy as np
import pygame
import math
import os

Player1 = 0
Player2 = 1
myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 75)
RED = (155, 26, 10)
YELLOW = (171, 92, 28)
BLUE = (60, 159, 156)


class GamePlay:
    def _init_(self, board):
        self.board = board
    
    #Placement Function
    def PlacePiece(self, row, col, piece):
        board = self.board
        board[row,col] = piece
        
    #Play Validator
    def CheckValid(self,col):
        board = self.board
        return board[(board.RowCount-1), col] == 0
    
    #Top Available Spot Locator Function
    def GetTopRow(self,col):
        board = self.board
        for r in range(board.RowCount):
            if board[r, col] == 0:
                return r
    
    #Output Board in Log
    def LogMove(self):
        board = self.board
        print(np.flip(board,0))
    
    #Handle input from mouse position
    def MakeMove(self, posx, piece):
        global ValidMove
        board = self.board
        col = int(math.floor(posx/board.SquareSize))
        if self.CheckValid(board, col):
            ValidMove = True
            row = self.GetTopRow(board, col)
            self.PlacePiece(board, row, col, piece)
        else:
            ValidMove = False
            
    #Find Winning Move       
    def CheckWin(self, piece):
        tiescore = 0
        board = self.board
        RowCount = board.RowCount
        ColumnCount = board.ColumnCount
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
            
    def StartGame(self, mode):
        board = self.board
        GameOver = False
        screen = board.screen
        SquareSize = board.SquareSize
        width, height = pygame.display.get_surface().get_size()
        turn = 0
        
        
        while not GameOver:
            # application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    os._exit(00)
                #elif event.type == pygame.KEYDOWN:
                #   if event.key == pygame.K_ESCAPE:
                #       main_menu.enable()
                #       return
                    
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
                        self.MakeMove(board, posx, 1)
                        if self.CheckWin(board, 1):
                            print("PLAYER ONE WINS")
                            label = myfont.render("PLAYER ONE WINS", 1, RED)
                            text_rect = label.get_rect(center=(700/2, 100/2))
                            screen.blit(label, text_rect)
                            GameOver = True
                    elif turn == Player2 and not mode:              
                        posx = event.pos[0]
                        self.MakeMove(board, posx, 2)
                        if self.CheckWin(board, 2):
                            print("PLAYER TWO WINS")
                            label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                            text_rect = label.get_rect(center=(700/2, 100/2))
                            screen.blit(label, text_rect)
                            GameOver = True
                            
                    if ValidMove:
                        turn += 1
                        turn = turn % 2
    
                    self.LogMove()
                    board.DrawBoard()
                    
                # if turn == Player2 and mode:
                #     col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    
                #     if CheckValid(board, col):
                #         row = GetTopRow(board, col)
                #         PlacePiece(board, row, col, 2)
    
                #         if CheckWin(board, 2):
                #             label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                #             text_rect = label.get_rect(center=(width/2, SquareSize/2))
                #             screen.blit(label, text_rect)
                #             GameOver = True
                    
                #     turn += 1
                #     turn = turn % 2 
                    
                #     LogMove(board)
                #     DrawBoard(board)
                    
                if tie:
                    print("TIE")
                    label = myfont.render("TIE", 1, BLUE)
                    text_rect = label.get_rect(center=(700/2, 100/2))
                    screen.blit(label, text_rect)
                    GameOver = True
                    
                if GameOver:
                    #send to endgame menu
                    main_menu.disable()
                    options_menu.enable()
                    break