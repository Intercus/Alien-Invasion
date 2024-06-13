import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""

    def __init__(self, settings, screen, ship):
        """Создает объект снаряда в текущей позиции корабля."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Создание прямоугольника снаряда в позиции (0, 0), затем установка правильной позиции.
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Сохранение позиции снаряда в вещественном формате.
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снаряда в вещественном формате.
        self.y -= self.speed_factor
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        """Рисует снаряд на экране."""
        pygame.draw.rect(self.screen, self.color, self.rect)
