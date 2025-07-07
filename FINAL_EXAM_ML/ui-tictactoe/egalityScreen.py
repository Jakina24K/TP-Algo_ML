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

WIDTH, HEIGHT = 450, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Draw Screen")

class Particle2:
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
        self.alpha -= 2  # disparition progressive

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color + (int(self.alpha),), (self.radius, self.radius), self.radius)
            surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

def draw_equality_screen():
    screen.fill(DARK_BLUE)

    font_big = pygame.font.SysFont("arial", 50)
    font_button = pygame.font.SysFont("arial", 36, bold=True)

    # Message de match nul
    text_color = WHITE
    draw_message = "It's a Draw!"
    text_surf = font_big.render(draw_message, True, text_color)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 3 - 30))

    # Dimensions des boutons
    button_width, button_height = 180, 50
    button_x = WIDTH // 2 - button_width // 2
    restart_y = HEIGHT // 2 + 60
    exit_y = restart_y + button_height + 20

    # Rects
    restart_rect = pygame.Rect(button_x, restart_y, button_width, button_height)
    exit_rect = pygame.Rect(button_x, exit_y, button_width, button_height)

    mouse_pos = pygame.mouse.get_pos()

    # Bouton RESTART
    restart_color = (255, 240, 100) if restart_rect.collidepoint(mouse_pos) else (255, 215, 0)
    pygame.draw.rect(screen, restart_color, restart_rect, border_radius=12)
    text_restart = font_button.render("RESTART", True, DARK_BLUE)
    screen.blit(text_restart, (button_x + (button_width - text_restart.get_width()) // 2,
                                restart_y + (button_height - text_restart.get_height()) // 2))

    # Bouton EXIT
    exit_color = (255, 100, 100) if exit_rect.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, exit_color, exit_rect, border_radius=12)
    text_exit = font_button.render("EXIT", True, WHITE)
    screen.blit(text_exit, (button_x + (button_width - text_exit.get_width()) // 2,
                            exit_y + (button_height - text_exit.get_height()) // 2))

    pygame.display.flip()
    return restart_rect, exit_rect


def main():
    import gameScreen  # <- à adapter selon le nom de ton fichier jeu principal

    particles = [Particle2() for _ in range(40)]
    clock = pygame.time.Clock()
    running = True

    try:
        while running:
            screen.fill(DARK_BLUE)
            restart_rect, exit_rect = draw_equality_screen()

            for p in particles[:]:
                p.update()
                p.draw(screen)
                if p.alpha <= 0:
                    particles.remove(p)

            while len(particles) < 40:
                particles.append(Particle2())

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        gameScreen.main()
                        return  # <- quitte avant de continuer
                    elif exit_rect.collidepoint(event.pos):
                        running = False

            clock.tick(60)
    finally:
        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    main()
