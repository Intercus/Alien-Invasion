class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_settings):
        """Инициализация статистики."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Игра начинается в неактивном состоянии.
        self.game_active = False

        # Рекордный счет не должен сбрасываться.
        self.high_score = 0

    def reset_stats(self):
        """Инициализация статистики, изменяющейся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
