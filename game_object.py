import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    # Конструктор класса
    def __init__(self, x, y, img='hero_mini.png'):
        super().__init__()
        # Загружаем изображение спрайта
        self.image = pygame.image.load(img).convert_alpha()
        pygame.transform.flip(self.image, True, False)
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Задаем скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        self.artifacts = pygame.sprite.Group()
        self.score = 0
        self.lives = 5


    def update(self):
        # учитываем эффект гравитации:
        self.calc_grav()
        # Пересчитываем положение спрайта игрока на экране

        # Смещение влево - вправо
        self.rect.x += self.change_x

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Если персонаж двигался вправо, остановим его слева от препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Наоборот, если движение было влево остановим его справа от препятствия
                self.rect.left = block.rect.right

        # Движение вверх-вниз
        self.rect.y += self.change_y

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Прид вижении вниз, персонаж упал на препятвие - он должен встать на него сверху
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # В прыжке персонаж врезался в препятствия - движение вверх должно прекратиться.
            self.change_y = 0

        # Проверяем столкновение с артефактом
        artifact_hit_list = pygame.sprite.spritecollide(self, self.artifacts, False)
        for artifact in artifact_hit_list:
            self.score += 1
            artifact.kill()

    # Расчет гравитации
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Моделируем ускорение свободного падения:
            self.change_y += .35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

        # Проверка: выход за границу экрана
        if self.rect.x < 0 :
            self.rect.x = 0
            self.change_x = 0
        if self.rect.x > WIN_WIDTH - self.rect.width:
            self.rect.x = WIN_WIDTH - self.rect.width
            self.change_x = 0

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    images = ['ground01.png', 'ground02.png']
# Препятствия, по которым моежт перемещаться персонаж, но не сквозь них
    def __init__(self, x, y, type, color=BLUE):
        super().__init__()
        # Загружаем изображение спрайта
        self.image = pygame.image.load(Platform.images[type]).convert_alpha()

        # Помещаем прямоугольник в заданное место на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()
        super().__init__()
        # Задаем размеры прямоугольника
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# Класс Enemy описывает противника персонажа
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img='thorns.png'):
        super().__init__()
        # Загружаем изображение в спрайт
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # спрайт противника ходит туда - обратно по горизонтали от точки start до точки stop:
        self.start = x
        self.stop = x
        # направление перемещения противника 1 - вправо, -1 - влево
        self.direction = 1
        # скосроть перемещения противника
        self.speed = 2
    
    # Обрабатываем сдвиг противника при сдвиге мира
    def shift(self, x):
        self.rect.x += x
        self.start += x
        self.stop += x

    def update(self):
        # спрайт дошел то stop и должен повернуть обратно, налево
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        # спрайт дошел до start и должен повернуть обратно, направо
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        # смещаем спрайт в указанном направлении
        self.rect.x += self.direction * self.speed



