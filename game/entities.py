import random
import pygame


class Paddle:
    """a játékosok vagy a gépi ellenfél által irányított ütő"""

    def __init__(self, x: int, y: int, width: int = 15, height: int = 100, speed: int = 7):
        self.start_x = x
        self.start_y = y
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.speed = speed

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def move(self, action: int, screen_height: int) -> None:
        """
        mozgatja az ütőt a megadott akció alapján:
        0 = helyben marad, 1 = felfelé, 2 = lefelé
        """
        if action == 1:
            self.y -= self.speed
        elif action == 2:
            self.y += self.speed

        # ne csússzon ki a képernyőről
        self.y = max(0.0, min(float(screen_height - self.height), self.y))

    def reset(self) -> None:
        self.x = float(self.start_x)
        self.y = float(self.start_y)

    def draw(self, screen: pygame.Surface, color: tuple = (255, 255, 255)) -> None:
        pygame.draw.rect(screen, color, self.rect, border_radius=4)


class Ball:
    """a játéktéren pattogó labda"""

    def __init__(self, x: int, y: int, radius: int = 8, base_speed: float = 6.0):
        self.start_x = x
        self.start_y = y
        self.radius = radius
        self.base_speed = base_speed
        self.max_speed = 12.0
        self.x = float(x)
        self.y = float(y)
        self.vx = base_speed
        self.vy = 0.0
        self.reset()

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def reset(self, direction: int | None = None) -> None:
        """visszahelyezi a labdát középre véletlenszerű függőleges iránnyal"""
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        dir_x = direction if direction in (-1, 1) else random.choice([-1, 1])
        self.vx = self.base_speed * dir_x
        self.vy = random.uniform(-4.5, 4.5)
        if abs(self.vy) < 1.5:
            self.vy = 2.0 if self.vy >= 0 else -2.0

    def draw(self, screen: pygame.Surface, color: tuple = (255, 255, 255)) -> None:
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)