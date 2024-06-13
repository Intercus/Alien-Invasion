import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Реагирует на нажатие клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Начинает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс настроек игры.
        settings.initialize_dynamic_settings()

        # Скрытие указателя мыши.
        pygame.mouse.set_visible(False)

        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True

        # Сброс изображений табло.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Очистка списков пришельцев и снарядов.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(settings, screen, ship, bullets):
    """Выпускает снаряд, если максимум еще не достигнут."""
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    # Отображение изображения фона.
    screen.blit(settings.bg_image, (0, 0))
    
    # Перерисовка всех снарядов позади корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Отображение информации о счете.
    sb.show_score()

    # Отображение кнопки Play, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции снарядов и уничтожает старые снаряды."""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    """Реагирует на столкновения снарядов с пришельцами."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(settings, screen, ship, aliens)

def check_fleet_edges(settings, aliens):
    """Реагирует на достижение флотом края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    """Опускает весь флот и меняет его направление."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def ship_hit(settings, screen, stats, sb, ship, aliens, bullets):
    """Реагирует на столкновение корабля с пришельцем."""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    aliens.empty()
    bullets.empty()

    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()

    sleep(0.5)

def check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, достиг ли флот нижней части экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(settings, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, достиг ли флот края, и обновляет позиции всех пришельцев."""
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets)

def get_number_aliens_x(settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x

def get_number_rows(settings, ship_height, alien_height):
    """Вычисляет количество рядов, помещающихся на экране."""
    available_space_y = settings.screen_height - (3 * alien_height) - ship_height
    number_rows = available_space_y // (2 * alien_height)
    return number_rows

def create_alien(settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)
