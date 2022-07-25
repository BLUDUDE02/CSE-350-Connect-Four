import pygame
import pygame_menu
import os.path as path
import os
from GameBoard import GameBoard
from GamePlay import GamePlay
from Menu import Menu


BACKGROUND = path.join(path.dirname(path.abspath(__file__)), '{0}').format('Background.png')

background_image = pygame_menu.BaseImage(
    image_path=BACKGROUND)

           
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
    width = 700
    height = 700
    pygame.init()
     
    #Post PyGame Initialization Variable Declarations    

    size = (width, height)
    screen = pygame.display.set_mode(size)
    gameBoard = GameBoard(6,7,100, screen)
    board = gameBoard.CreateBoard()
    game = GamePlay(gameBoard, board)
    menu = Menu(gameBoard, game)
    
    # -------------------------------------------------------------------------
    # Menus
    # -------------------------------------------------------------------------
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_8BIT
    theme.widget_font = pygame_menu.font.FONT_8BIT
    theme.background_color = (0, 0, 0, 180)
    
    main_menu = pygame_menu.Menu('Connect 4', width, height, theme=theme)
    main_menu.add.button('Two Player', menu.StartGame, False)
    main_menu.add.button('Player VS AI', menu.StartGame, True)
    main_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    options_menu = pygame_menu.Menu('Game Over', 400, 300, theme=theme)
    options_menu.add.button('Two Player', menu.StartGame, False)
    options_menu.add.button('Player VS AI', menu.StartGame, True)
    options_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    
    while True:
        
        # events handling for menus -- turn this in to function
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