import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс для представления одного пришельца в флоте."""

    def __init__(self, settings, screen):
        """Инициализация пришельца и задание его начальной позиции."""
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load("images/alien.png")
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется у верхнего левого угла экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельца вправо или влево."""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Рисует пришельца в его текущем положении."""
        self.screen.blit(self.image, self.rect)
