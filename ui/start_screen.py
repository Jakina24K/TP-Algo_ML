import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400

def show_start_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("n-Puzzle Menu")
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)
    
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH // 2, 50)
    dimension_buttons = {
        "3x3": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 20, 80, 40),
        "4x4": pygame.Rect(SCREEN_WIDTH // 4 + 120, SCREEN_HEIGHT // 2 + 20, 80, 40),
    }
    selected_dimension = "3x3"

    while True:
        screen.fill((255, 255, 255))

        title = font.render("n-Puzzle", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title, title_rect)

        pygame.draw.rect(screen, (0, 128, 0), play_button_rect)
        play_text = font.render("PLAY", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, play_text_rect)

        for dimension, rect in dimension_buttons.items():
            color = (0, 0, 128) if dimension == selected_dimension else (128, 128, 128)
            pygame.draw.rect(screen, color, rect)
            text = small_font.render(dimension, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return int(selected_dimension[0])
                for dimension, rect in dimension_buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_dimension = dimension
