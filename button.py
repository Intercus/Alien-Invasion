import pygame.font

class Button:
    def __init__(self, settings, screen, msg):
        """Инициализация атрибутов кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Установка размеров и свойств кнопки.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Создание объекта rect кнопки и выравнивание его по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки нужно подготовить только один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует текст в графическое изображение и выравнивает текст по центру кнопки."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отображение кнопки и сообщения на экране."""
        # Сначала рисуем кнопку, затем рисуем текст.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
