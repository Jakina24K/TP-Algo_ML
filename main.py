import pygame
from ui.start_screen import show_start_screen
from ui.game_screen import game_loop

def main():
    pygame.init()
    n, ai_play = show_start_screen() 
    while True:
        game_loop(n, ai_play) 

if __name__ == "__main__":
    main()
