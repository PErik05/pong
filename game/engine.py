from game.entities import Ball, Paddle


class PongEngine:
    """a pong játék logikai motorja"""

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.left_paddle = Paddle(30, height // 2 - 50)
        self.right_paddle = Paddle(width - 45, height // 2 - 50)
        self.ball = Ball(width // 2, height // 2)
        self.left_score = 0
        self.right_score = 0

    def reset_match(self) -> None:
        """teljes meccs újraindítása"""
        self.left_score = 0
        self.right_score = 0
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()

    def step(self, left_action: int, right_action: int) -> None:
        """egyetlen időlépést hajt végre a játékban"""
        self.left_paddle.move(left_action, self.height)
        self.right_paddle.move(right_action, self.height)
        self.ball.move()

        # felső és alsó falról való visszapattanás
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = float(self.ball.radius)
            self.ball.vy *= -1
        elif self.ball.y + self.ball.radius >= self.height:
            self.ball.y = float(self.height - self.ball.radius)
            self.ball.vy *= -1

        # ütközés a bal oldali ütővel
        if self.ball.vx < 0 and self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.x = float(self.left_paddle.rect.right + self.ball.radius)
            self.ball.vx = min(self.ball.max_speed, abs(self.ball.vx) * 1.05)
            offset = (self.ball.y - self.left_paddle.center_y) / (self.left_paddle.height / 2)
            self.ball.vy = offset * 6.5

        # ütközés a jobb oldali ütővel
        elif self.ball.vx > 0 and self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.x = float(self.right_paddle.rect.left - self.ball.radius)
            self.ball.vx = -min(self.ball.max_speed, abs(self.ball.vx) * 1.05)
            offset = (self.ball.y - self.right_paddle.center_y) / (self.right_paddle.height / 2)
            self.ball.vy = offset * 6.5

        # pontszerzés ellenőrzése
        if self.ball.x < 0:
            self.right_score += 1
            self.ball.reset(direction=-1)
        elif self.ball.x > self.width:
            self.left_score += 1
            self.ball.reset(direction=1)