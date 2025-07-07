
import pygame
import sys
import random
pygame.init()

# Couleurs
BLUE = (10, 10, 63)
YELLOW = (255, 215, 0)
RED = (255, 60, 56)
WHITE = (255, 255, 255)
DARK_BLUE = (5, 5, 40)

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Win Screen")

class Particle:

    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT
        self.radius = random.randint(2, 5)
        self.color = random.choice([YELLOW, RED, WHITE])
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-4, -1)
        self.gravity = 0.05
        self.alpha = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.alpha -= 2  # disparaît lentement

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color + (int(self.alpha),), (self.radius, self.radius), self.radius)
            surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

def draw_win_screen(winner):
    screen.fill(DARK_BLUE)

    # Police plus simple, plus petite, sans gras
    font_big = pygame.font.SysFont("arial", 50)  # taille 50, pas bold
    font_button = pygame.font.SysFont("arial", 36, bold=True)  # bouton un peu plus grand

    # Message gagnant avec couleurs conditionnelles
    text_color = YELLOW if winner == "O" else RED
    win_message = f"Player {winner} Wins!"
    text_surf = font_big.render(win_message, True, text_color)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 3 - 30))

    # Bouton RESTART
    button_width, button_height = 180, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 60
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Bouton jaune avec ombre et arrondi
    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 240, 100) if button_rect.collidepoint(mouse_pos) else (255, 215, 0)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)

    # Texte RESTART centré et coloré en bleu foncé
    text_restart = font_button.render("RESTART", True, DARK_BLUE)
    screen.blit(text_restart, (button_x + (button_width - text_restart.get_width()) // 2,
                               button_y + (button_height - text_restart.get_height()) // 2))

    pygame.display.flip()

    return button_rect

def main(winner):
    particles = [Particle() for _ in range(40)]  # 40 particules initiales
    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK_BLUE)
        button_rect = draw_win_screen(winner)

        # Mettre à jour et afficher les particules
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.alpha <= 0:
                particles.remove(p)

        # En créer de nouvelles pour un effet continu
        while len(particles) < 40:
            particles.append(Particle())

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    import startScreen
                    startScreen.main()
                    return

        clock.tick(60)


if __name__ == "__main__":
    main("X")
