import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    """Инициализирует pygame, настройки и объект экрана."""
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play.
    play_button = Button(settings, screen, "Play")

    # Создание экземпляра для хранения игровой статистики и табло.
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    # Установка фона.
    #bg_color = (99, 99, 99)

    # Создание корабля, группы снарядов и группы пришельцев.
    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()

    # Создание флота пришельцев.
    gf.create_fleet(settings, screen, ship, aliens)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
