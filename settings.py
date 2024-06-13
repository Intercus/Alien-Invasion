import pygame

class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Настройки экрана.
        self.screen_width = 1200
        self.screen_height = 800

        # Загрузка изображения фона.
        self.bg_image = pygame.image.load('images/background.jpg')
        
        # Настройки корабля.
        self.ship_limit = 3

        # Настройки снарядов.
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 230, 230, 230
        self.bullets_allowed = 3

        # Настройки пришельцев.
        self.fleet_drop_speed = 10

        # Темп ускорения игры.
        self.speedup_scale = 1.1
        # Темп увеличения стоимости очков за пришельцев.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, которые меняются в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.3

        # Начисление очков.
        self.alien_points = 50

        # fleet_direction: 1 означает движение вправо, -1 - влево.
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость очков за пришельцев."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
