import pygame
import pygame_menu
import os

Player1 = 0
Player2 = 1
width = 700
height = 700

RED = (155, 26, 10)
YELLOW = (171, 92, 28)
BLUE = (60, 159, 156)

class Menu():   
    def __init__(self, board, game):
        self.board = board
        self.game = game
        
    def StartGame(self, mode):
        board = self.board
        game = self.game
        GameOver = False
        screen = pygame.display.get_surface()
        SquareSize = 100
        width, height = pygame.display.get_surface().get_size()
        turn = 0
        myfont = pygame.font.Font("HackbotFreeTrial-8MgA2.otf", 75)
        
        top = pygame.image.load('Top.png')
        top.convert()

        rect4 = top.get_rect()
        rect4.center = (width/2, SquareSize/2)
        screen.blit(top, rect4)
        
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
                    
                    if turn % 2 == Player1:
                        posx = event.pos[0]
                        game.MakeMove(posx, 1)
                        if game.CheckWin(1):
                            print("PLAYER ONE WINS")
                            label = myfont.render("PLAYER ONE WINS", 1, RED)
                            text_rect = label.get_rect(center=(700/2, 100/2))
                            screen.blit(label, text_rect)
                            GameOver = True
                    elif turn % 2 == Player2 and not mode:              
                        posx = event.pos[0]
                        game.MakeMove(posx, 2)
                        if game.CheckWin(2):
                            print("PLAYER TWO WINS")
                            label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                            text_rect = label.get_rect(center=(700/2, 100/2))
                            screen.blit(label, text_rect)
                            GameOver = True
                            
                    turn += 1
    
                    game.LogMove()
                    board.DrawBoard()
                    
                # if turn == Player2 and mode:
                #     col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    
                #     if game.CheckValid(board, col):
                #         row = game.GetTopRow(board, col)
                #         game.PlacePiece(board, row, col, 2)
    
                #         if game.CheckWin(board, 2):
                #             label = myfont.render("PLAYER TWO WINS", 1, YELLOW)
                #             text_rect = label.get_rect(center=(width/2, SquareSize/2))
                #             screen.blit(label, text_rect)
                #             GameOver = True
                    
                #     turn += 1
                #     turn = turn % 2 
                    
                #     game.LogMove(board)
                #     game.DrawBoard(board)
                    
                # if tie:
                #     print("TIE")
                #     label = myfont.render("TIE", 1, BLUE)
                #     text_rect = label.get_rect(center=(700/2, 100/2))
                #     screen.blit(label, text_rect)
                #     GameOver = True
                    
                if GameOver:
                    #send to endgame menu
                    break

