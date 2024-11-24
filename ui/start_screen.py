import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400

def show_start_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CHILL Puzzle Menu")
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)
    
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH // 2, 50)
    dimension_buttons = {
        "3x3": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 80, 40),
        "4x4": pygame.Rect(SCREEN_WIDTH // 4 + 120, SCREEN_HEIGHT // 2 + 20, 80, 40),
    }
    selected_dimension = "3x3"

    # Option "Let the AI play"
    ai_play_checkbox_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 80, 20, 20)
    ai_play_text_rect = pygame.Rect(SCREEN_WIDTH // 4 + 30, SCREEN_HEIGHT // 2 + 80, 200, 20)
    ai_play_selected = False

    while True:
        screen.fill((255, 255, 255))

        # Texte principal
        title = font.render("n-Puzzle", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title, title_rect)

        # Dessiner le bouton "PLAY"
        pygame.draw.rect(screen, (0, 128, 0), play_button_rect)
        play_text = font.render("PLAY", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, play_text_rect)

        # Dessiner les options de dimensions
        for dimension, rect in dimension_buttons.items():
            color = (0, 0, 128) if dimension == selected_dimension else (128, 128, 128)
            pygame.draw.rect(screen, color, rect)
            text = small_font.render(dimension, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Dessiner la case "Let the AI play" uniquement si "3x3" est sélectionné
        if selected_dimension == "3x3":
            pygame.draw.rect(screen, (0, 0, 0), ai_play_checkbox_rect, 2)
            if ai_play_selected:
                pygame.draw.line(screen, (0, 128, 0), ai_play_checkbox_rect.topleft, ai_play_checkbox_rect.bottomright, 2)
                pygame.draw.line(screen, (0, 128, 0), ai_play_checkbox_rect.topright, ai_play_checkbox_rect.bottomleft, 2)

            ai_play_text = small_font.render("Let the AI play", True, (0, 0, 0))
            screen.blit(ai_play_text, ai_play_text_rect)

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return int(selected_dimension[0]), ai_play_selected  # Retourne dimension et option AI
                for dimension, rect in dimension_buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_dimension = dimension
                        # Réinitialiser l'état de la case si "4x4" est sélectionné
                        if selected_dimension == "4x4":
                            ai_play_selected = False
                if selected_dimension == "3x3" and ai_play_checkbox_rect.collidepoint(event.pos):
                    ai_play_selected = not ai_play_selected
