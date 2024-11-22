import pygame
import sys

def show_win_screen(screen, n):
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    win_message = font.render("You Win !!", True, (0, 128, 0))
    win_rect = win_message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))

    # Boutons
    start_again_button = pygame.Rect(screen.get_width() // 4, screen.get_height() // 2, screen.get_width() // 2, 50)
    main_menu_button = pygame.Rect(screen.get_width() // 4, screen.get_height() // 2 + 70, screen.get_width() // 2, 50)

    while True:
        screen.fill((255, 255, 255))
        screen.blit(win_message, win_rect)

        # Dessiner les boutons
        pygame.draw.rect(screen, (0, 128, 0), start_again_button)
        start_again_text = button_font.render("Start Again", True, (255, 255, 255))
        start_again_text_rect = start_again_text.get_rect(center=start_again_button.center)
        screen.blit(start_again_text, start_again_text_rect)

        pygame.draw.rect(screen, (0, 128, 0), main_menu_button)
        main_menu_text = button_font.render("Main Menu", True, (255, 255, 255))
        main_menu_text_rect = main_menu_text.get_rect(center=main_menu_button.center)
        screen.blit(main_menu_text, main_menu_text_rect)

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_again_button.collidepoint(event.pos):
                    return "start_again"  # Rejouer avec la même dimension
                elif main_menu_button.collidepoint(event.pos):
                    return "main_menu" # Retourner à l'écran principal
