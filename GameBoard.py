import numpy as np
import pygame

P1Token = 1
P2Token = 2
height = 700

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
    
    def DrawBoard(self):
        SquareSize = self.SquareSize
        RowCount = self.RowCount
        ColumnCount = self.ColumnCount
        screen = self.screen
        board = self.CreateBoard()
        
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

