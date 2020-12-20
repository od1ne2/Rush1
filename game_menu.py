import pygame
from constants import *

# Класс позволяет создать прямоугольную кнопку с надписью на ней
class Button():
    def __init__(
            self, x, y, w, h, name,
            font_color=WHITE,
            normal_color=BLUE,
            highlight_color = GREEN,
            active_color=BLACK,
            size=24,
            font='Arial',
            padding=5
    ):
        # Текущее состояние кнопки. Все состояния: 'normal', 'highlight', 'active'
        self.state = 'normal'
        # Задаем цвета кнопки в нормальном, веделенном и активном состоянии:
        self.normal_color = normal_color
        self.highlight_color = highlight_color
        self.active_color = active_color
        # Задаем название  - текст на кнопке
        self.name = name
        self.font = pygame.font.SysFont(font, size, True)
        # Создаем надпись на кнопке
        self.text = self.font.render(name, True, font_color)
        # Задаем размеры прямоугольника
        self.image = pygame.Surface([w,h])
        self.image.fill(normal_color)
        # Задаем положение верхней панели на экране
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Задаем поля - отступы от границы кнопки для текста
        self.padding = padding

    # Рисуем прямоугольник кнопки и надпись на ней
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, (self.rect.x + self.padding, self.rect.y + self.padding))

    # В методе update меняем цвет кнопки в зависимости от состояния
    def update(self):
        if self.state == 'normal':
            self.image.fill(self.normal_color)
        elif self.state == 'highlight':
            self.image.fill(self.highlight_color)
        elif self.state == 'active':
            self.image.fill(self.active_color)

    # Обработка событий кнопки:  меняем состояние в зависимости от события
    def handle_mouse_action(self, event=None):
        # Получаем текущее положение курсора
        pos_x, pos_y = pygame.mouse.get_pos()
        # Проверяем, находится курсор над кнопкой или нет:
        check_pos = self.rect.left <= pos_x <= self.rect.right and self.rect.top <= pos_y <= self.rect.bottom
        # Курсор движется над кнопкой:
        if event == pygame.MOUSEMOTION:
            if check_pos:  self.state = 'highlight'
            else: self.state = 'normal'

        # На кнопку кликнули:
        elif event == pygame.MOUSEBUTTONDOWN:
            if check_pos: self.state = 'active'
            else: self.state = 'normal'
            
        # На кнопку кликнули и отпустили:
        elif event == pygame.MOUSEBUTTONUP:
            if check_pos:  self.state = 'highlight'
            else: self.state = 'normal'
            
class MainMenu():
    def __init__(self, w, h):
        # Создаем список пунктов меню:
        self.labels = [
            'START',
            'CONTINUE',
            'SETTINGS',
            'QUIT'
        ]
        # Задаем координаты верхнего левого угла меню:
        self.x = (WIN_WIDTH - w) // 2
        self.y = (WIN_HEIGHT - h) // 2
        # Создаем список кнопок:
        self.buttons = []
        # Рассчитываем высоту для каждой кнопки меню, исходя и общей высоты:
        button_height = int(h / (len(self.labels) + 1))
        # Локальная переменная, хранит y координату для текущей кнопки:
        current_y = self.y
        for label in self.labels:
            # Создаем новую кнопку:
            new_button = Button(self.x, current_y, w, button_height, label)
            # Переходим по вертикали к следующей кнопке с отступом в 2 пикселя,
            # чтобы кнопки визуально не "слиплись" между собой:
            current_y += button_height + 2
            # Добавляем новую кнопку в список всех кнопок меню:
            self.buttons.append(new_button)

    # Вызвать метод update() для всех кнопок в меню:
    def update(self):
        for button in self.buttons:
            button.update()

    # Вызвать метод обработки события для всех кнопок в меню:
    def handle_mouse_event(self, event):
        for button in self.buttons:
            button.handle_mouse_action(event)
            # запоминаем и возвращаем кнопку, на которую сейчас нажали:
            if button.state == 'active':
                return button

    # Вызвать метод draw для всех кнопок в меню
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

class SettingsMenu():
    def __init__(self, w, h):
        # Создаем список пунктов меню выбора скорости:
        self.labels = [
            'FAST',
            'MEDIUM',
            'SLOW'
        ]
        # Создаем список пунктов горизонтальных кнопок OK и CANCEL:
        self.labels_hor = [
            'OK',
            'CANCEL'
        ]
        # Задаем координаты верхнего левого угла меню:
        self.x = (WIN_WIDTH - w) // 2
        self.y = (WIN_HEIGHT - h) // 2
        # Создаем список кнопок:
        self.buttons = []
        # Рассчитываем высоту для каждой кнопки меню, исходя и общей высоты:
        button_height = int(h / (len(self.labels) + 1))
        # Локальная переменная, хранит y координату для текущей кнопки:
        current_y = self.y
        for label in self.labels:
            # Создаем новую кнопку:
            # Эти кнопки будут с залипанием
            new_button = Button(self.x, current_y, w, button_height, label)
            # Переходим по вертикали к следующей кнопке с отступом в 2 пикселя,
            # чтобы кнопки визуально не "слиплись" между собой:
            current_y += button_height + 2
            # Добавляем новую кнопку в список всех кнопок меню:
            self.buttons.append(new_button)
        # Создаем кнопки по горизонтали
        i = 0
        for label in self.labels_hor:
            # Создаем новую кнопку:
            new_button = Button(self.x + i * w / 2 + i, current_y, w / 2, button_height, label)
            # Добавляем новую кнопку в список всех кнопок меню:
            self.buttons.append(new_button)
            # Отступ, чтобы не слипались кнопки
            i += 1
        
        # Создаем надпись для информирования о выбранной скорости:
        self.info_label = 'SLOW'
        self.info = FONT.render('ENEMY SPEED: ' + self.info_label , True, YELLOW)
        self.info_rect = self.info.get_rect()
        self.info_rect.x = 10
        self.info_rect.y = 50
        
    # Вызвать метод update() для всех кнопок в меню:
    def update(self):
        for button in self.buttons:
            button.update()
        # Обновляем надпись, сообщающую о выбраном уровне сложности (скорости)
        self.info = FONT.render('ENEMY SPEED: ' + self.info_label , True, YELLOW)

    # Вызвать метод обработки события для всех кнопок в меню:
    def handle_mouse_event(self, event):
        for button in self.buttons:
            button.handle_mouse_action(event)
            # запоминаем и возвращаем кнопку, на которую сейчас нажали:
            if button.state == 'active':
                # Если кнопка не ОК и не CANCEL
                if button.name not in self.labels_hor:
                    # Приравниваем значение надписи, имени кнопки
                    self.info_label = button.name
                return button

    # Вызвать метод draw для всех кнопок в меню
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        # Отображаем налпись сверху
        screen.blit(self.info, self.info_rect)

# Класс TimeLabel создает таймер и отсчитывает время в игре
class TimerLabel:
    def __init__(
            self, x=0, y=0,
            font='Arial',
            font_size=24,
            bold=True,
            color=RED,
            format='%02d:%02d'
    ):
        # количество итераций игрового цикла
        self.tick_count = 0
        self.minutes = 0
        self.sec = 0
        self.font = pygame.font.SysFont(font, font_size, bold)
        self.format = format
        self.color = color
        self.text = FONT.render(format % (self.minutes, self.sec), True, color)
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.tick_count += 1
        if self.tick_count >= FPS:
            self.tick_count = 0
            self.sec += 1
            if self.sec >= 60:
                self.sec = 0
                self.minutes += 1
            self.text = FONT.render(self.format % (self.minutes, self.sec),True, self.color)

    def draw(self, screen):
        screen.blit(self.text, self.rect)

# Класс TopPanel отвечает за отрисовку верхней панели в игре
# На верхней панели должно отображаться:
# - количеств собранных в игре монет (картинка монеты + число)
# - количество жизней игрока (картинка сердечка + число)
# - таймер отсчета времени
class TopPanel():

    def __init__(self, x=5, y=5):
        self.x = x
        self.y = y
        self.width = WIN_WIDTH - 2 * x

        # Создаем надпись для количества жизней игрока:
        self.lives_label = FONT.render('3' , True, YELLOW)
        self.lives_rect = self.lives_label.get_rect()
        self.lives_rect.x = x + 35
        self.lives_rect.y = y

        # Создаем пиктограмму сердечка:
        self.lives_img = pygame.image.load('heart.png').convert_alpha()
        self.lives_img_rect = self.lives_img.get_rect()
        self.lives_img_rect.y = y
        self.lives_img_rect.x = x

        # Создаем надпись для количество собранных монет:
        self.coin_label = FONT.render('0' , True, YELLOW)
        self.coin_rect = self.coin_label.get_rect()
        self.coin_rect.x = x + 135
        self.coin_rect.y = y

        # Создаем пиктограмму монеты:
        self.coin_img = pygame.image.load('coin.png').convert_alpha()
        self.coin_img_rect = self.coin_img.get_rect()
        self.coin_img_rect.y = y
        self.coin_img_rect.x = x + 100

        # Создаем таймер на панели
        self.timer = TimerLabel(x + 200, y)

    def update(self, lives=3, coin=0):
        self.lives_label = FONT.render(str(lives) , True, YELLOW)
        self.coin_label = FONT.render(str(coin) , True, YELLOW)
        self.timer.update()

    def draw(self, screen):
        screen.blit(self.lives_label, self.lives_rect)
        screen.blit(self.lives_img, self.lives_img_rect)
        screen.blit(self.coin_label, self.coin_rect)
        screen.blit(self.coin_img, self.coin_img_rect)
        self.timer.draw(screen)
