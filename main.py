import sys
import pygame

from game.engine import PongEngine
from ai.rule_based import RuleBasedAI

WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (18, 22, 30)
WHITE = (240, 240, 240)
ACCENT = (80, 200, 120)
MUTED = (140, 150, 170)


def draw_centered_text(screen, text: str, font, color, y: int) -> None:
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_menu(screen, title_font, menu_font, small_font) -> None:
    screen.fill(BG_COLOR)
    draw_centered_text(screen, "PONG PROJEKT", title_font, ACCENT, 110)

    options = [
        "[1] Ember vs. Ember  (W/S és Fel/Le)",
        "[2] Ember vs. AI  -  Könnyű",
        "[3] Ember vs. AI  -  Közepes",
        "[4] Ember vs. AI  -  Nehéz",
        "[ESC] Kilépés",
    ]
    for idx, text in enumerate(options):
        draw_centered_text(screen, text, menu_font, WHITE, 230 + idx * 52)

    draw_centered_text(
        screen, "Játék közben ESC: vissza a menübe", small_font, MUTED, 550
    )
    pygame.display.flip()


def draw_game(screen, engine: PongEngine, score_font, small_font, mode_label: str) -> None:
    screen.fill(BG_COLOR)

    # középvonal kirajzolása
    for y in range(0, HEIGHT, 24):
        pygame.draw.rect(screen, (60, 70, 90), (WIDTH // 2 - 2, y, 4, 14))

    engine.left_paddle.draw(screen, WHITE)
    engine.right_paddle.draw(screen, ACCENT)
    engine.ball.draw(screen, WHITE)

    # pontszámok megjelenítése
    left_txt = score_font.render(str(engine.left_score), True, WHITE)
    right_txt = score_font.render(str(engine.right_score), True, ACCENT)
    screen.blit(left_txt, (WIDTH // 4 - left_txt.get_width() // 2, 25))
    screen.blit(right_txt, (3 * WIDTH // 4 - right_txt.get_width() // 2, 25))

    draw_centered_text(screen, mode_label, small_font, MUTED, HEIGHT - 22)
    pygame.display.flip()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong - Python Projektfeladat")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(None, 64)
    score_font = pygame.font.SysFont(None, 56)
    menu_font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 24)

    engine = PongEngine(WIDTH, HEIGHT)
    rule_ai = RuleBasedAI(difficulty="medium")

    state = "MENU"
    mode = ""
    mode_label = ""

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "MENU":
                    if event.key == pygame.K_1:
                        engine.reset_match()
                        mode = "PVP"
                        mode_label = "Ember vs. Ember"
                        state = "PLAYING"
                    elif event.key == pygame.K_2:
                        engine.reset_match()
                        rule_ai = RuleBasedAI(difficulty="easy")
                        mode = "AI"
                        mode_label = "Ember vs. AI (Könnyű)"
                        state = "PLAYING"
                    elif event.key == pygame.K_3:
                        engine.reset_match()
                        rule_ai = RuleBasedAI(difficulty="medium")
                        mode = "AI"
                        mode_label = "Ember vs. AI (Közepes)"
                        state = "PLAYING"
                    elif event.key == pygame.K_4:
                        engine.reset_match()
                        rule_ai = RuleBasedAI(difficulty="hard")
                        mode = "AI"
                        mode_label = "Ember vs. AI (Nehéz)"
                        state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif state == "PLAYING" and event.key == pygame.K_ESCAPE:
                    state = "MENU"

        if state == "MENU":
            draw_menu(screen, title_font, menu_font, small_font)
            continue

        # bal oldali játékos irányítása (w/s)
        keys = pygame.key.get_pressed()
        left_action = 0
        if keys[pygame.K_w]:
            left_action = 1
        elif keys[pygame.K_s]:
            left_action = 2

        # jobb oldali játékos vagy gépi ellenfél
        if mode == "PVP":
            right_action = 0
            if keys[pygame.K_UP]:
                right_action = 1
            elif keys[pygame.K_DOWN]:
                right_action = 2
        else:
            right_action = rule_ai.choose_action(engine.right_paddle, engine.ball)

        engine.step(left_action, right_action)
        draw_game(screen, engine, score_font, small_font, mode_label)


if __name__ == "__main__":
    main()