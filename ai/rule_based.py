import random
from game.entities import Ball, Paddle


class RuleBasedAI:
    """egyszerű szabályalapú gépi ellenfél állítható nehézséggel"""

    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        # a holttér és a hibázási esély adja a nehézségi szintet
        if difficulty == "easy":
            self.deadzone = 35
            self.error_rate = 0.20
        elif difficulty == "hard":
            self.deadzone = 8
            self.error_rate = 0.02
        else:  # közepes fokozat
            self.deadzone = 18
            self.error_rate = 0.08

    def choose_action(self, paddle: Paddle, ball: Ball) -> int:
        """eldönti, merre mozogjon az ütő (0: áll, 1: fel, 2: le)"""
        if random.random() < self.error_rate:
            return 0

        diff = ball.y - paddle.center_y
        if diff < -self.deadzone:
            return 1
        if diff > self.deadzone:
            return 2
        return 0