import pygame
from ui.start_screen import show_start_screen
from ui.game_screen import game_loop

def main():
    pygame.init()
    n = show_start_screen()  # Affiche l'écran d'accueil et retourne la dimension sélectionnée
    while True:
        game_loop(n)  # Lance le jeu pour la dimension sélectionnée

if __name__ == "__main__":
    main()
