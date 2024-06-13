import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Класс для отображения игровой информации о счете."""

    def __init__(self, settings, screen, stats):
        """Инициализация атрибутов подсчета очков."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Настройки шрифта для отображения счета.
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка начальных изображений счета.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Размещение счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Размещение рекордного счета по центру верхней части экрана.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)

        # Размещение уровня под текущим счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Показывает количество оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Отображает счет на экране."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Отображение оставшихся кораблей.
        self.ships.draw(self.screen)
