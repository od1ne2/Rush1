
import pygame
import game_object
from constants import *
from game_menu import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        pygame.display.set_caption('Rush')
        self.background_img = pygame.image.load("background_wide.png").convert()
        self.all_sprite_list = pygame.sprite.Group()


        # Скорость движения врагов по умолчанию
        self.speed = 2

        # Создаем платформы
        self.platform_list = pygame.sprite.Group()
        self.create_walls()

        # Создаем артефакты
        self.artifact_list = pygame.sprite.Group()
        self.create_artifacts()

        # Создаем противников
        self.enemy_list = pygame.sprite.Group()
        self.create_enemies()

        # Создаем спрайт игрока
        self.player = game_object.Player(0, 0)
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list
        self.all_sprite_list.add(self.player)

        # Создаем главное меню
        self.top_panel = TopPanel(20, 10)
        self.main_menu = MainMenu(300, 200)
        # Создаем меню настроек
        self.settings_menu = SettingsMenu(300, 200)
        # Программируем смещение грового мира:
        self.shift = 0
        self.player_global_x = self.player.rect.x
        self.game_width = self.background_img.get_rect().width

        self.clock = pygame.time.Clock()
        # Будем вести отсчет игрового времени:
        self.time = 0
        # время столкновения с противником:
        # нужно для того, чтобы игрок не получал урон от противника чаще чем раз в секунду
        self.hit_time = 0

        # Игровые сцены state: 'START', MENU', 'SETTINGS', 'GAME', 'PAUSE' ' 'FINISH', 'GAME_OVER'
        self.state = 'START'

    # Создаем стены и платформы
    def create_walls(self):
        platform_coords = [
            [200, 450],
            [200, 500],
            [200, 550],
            [300, 500],
            [300, 550],
            [400, 450],
            [450, 450],
            [550, 350],
            [600, 350],
            [700, 300],
            [750, 300],
            [850, 250],
            [900, 250],
            [850, 550],
            [900, 550],
            [950, 450],
            [1100, 500],
            [1100, 550],
            [1150, 400],
            [1150, 450],
            [1150, 500],
            [1150, 550],
            [1300, 400],
            [1400, 400],
            [1500, 400]
        ]
        for coord in platform_coords:
            platform = game_object.Platform(coord[0], coord[1], 0)
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)

    # Создаем артефакты (монеты) в игре
    def create_artifacts(self):
        artifact_coords = [
            [200, 250],
            [200, 300],
            [200, 350],
            [200, 400],
            [450, 400],
            [600, 200],
            [600, 300],
            [600, 550],
            [750, 550],
            [750, 250],
            [750, 150],
            [900, 50],
            [900, 100],
            [900, 150],
            [900, 200],
            [1150, 300],
            [1150, 350],
            [1300, 200],
            [1300, 250],
            [1400, 200],
            [1400, 250],
            [1500, 200],
            [1500, 250],
        ]
        artifact_coords = [
            [200, 250],
            [200, 300],
            [200, 350],
            [200, 400],
            [450, 400],
            [600, 200],
            [600, 300],
            [600, 550],
            [750, 550],
            [750, 250],
            [750, 150],
            [900, 50],
            [900, 100],
            [900, 150],
            [900, 200],
            [1150, 300],
            [1150, 350],
            [1300, 200],
            [1300, 250],
            [1400, 200],
            [1400, 250],
            [1500, 200],
            [1500, 250],
        ]
        for coord in artifact_coords:
            artifact = game_object.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)

    # Создаем противников в игре
    def create_enemies(self):

        enemies_coords = [
            [0, 300, 400],
            [450, 550, 750],

        ]
        for coord in enemies_coords:
            enemy = game_object.Enemy(coord[0], coord[1], self.speed)
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

    # Выполняем сдвиг игрового мира при перемещении игрока
    def shift_world(self, shift_x):
        self.shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for artifact in self.artifact_list:
            artifact.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.shift(shift_x)

    # Обработка события для разных сотояний в игре
    def handle_states(self, event):
        # Обработка событий стартового экрана
        if self.state in ['START', 'FINISH', 'GAME OVER']:
            # Нажали на любую клавишу
            if event.type == pygame.KEYDOWN:
                self.state = 'MENU'

        # Обрабатываем события главного меню:
        elif self.state in ['MENU', 'PAUSE']:
            # Получаем кнопку, на которую нажали в главном меню:
            active_button = self.main_menu.handle_mouse_event(event.type)

            if active_button:
                # После того, как на кнопку нажали, возвращаем ее состояние в "normal":
                active_button.state =  'normal'

                # Нажали на кнопку START, начинаем игру заново:
                if active_button.name == 'START':
                    self.__init__()
                    self.state = 'GAME'

                # На паузе и нажали CONTINUE, переведем игру с состояние GAME:
                elif active_button.name == 'CONTINUE':
                    self.state = 'GAME'

                # Вызвали меню настроек:
                elif active_button.name == 'SETTINGS':
                    self.state = 'SETTINGS'

                # Нажали на QUIT - завершим работу приложения:
                elif active_button.name == 'QUIT':
                    pygame.quit()

        # Обрабатываем события меню настроек:
        elif self.state == 'SETTINGS':
            # Получаем кнопку, на которую нажали в меню настроек:
            active_button = self.settings_menu.handle_mouse_event(event.type)
            if active_button:
                # Проверяем кнопки подтверждения или выбора скорости
                if active_button.name in ['OK', 'CANCEL']:
                    # После того, как на кнопку нажали, возвращаем ее состояние в "normal":
                    active_button.state =  'normal'
                    if active_button.name == 'OK':
                        # Изменяем скорость врагов в соответствии с тем что выбрали
                        for enemy in self.enemy_list:
                            enemy.speed = self.speed
                        self.state = 'MENU'
                    else:
                        self.state = 'MENU'
                else:
                    # Нажали на кнопку FAST, меняем скорость движения врагов:
                    if active_button.name == 'HARD':
                        self.speed = 10
                    # Нажали на кнопку MEDIUM, меняем скорость движения врагов:
                    elif active_button.name == 'MEDIUM':
                        self.speed = 5
                    # Нажали на кнопку SLOW, меняем скорость движения врагов:
                    elif active_button.name == 'EASY':
                        self.speed = 2
        elif self.state == 'FINISH':
            pass


        # Обработка событий, когда идет игра
        elif self.state == 'GAME':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'MENU'


    # Прорисовка сцены
    def draw(self):
        # Выполняем заливку фона:
        self.screen.fill(BLACK)
        if self.state == 'START':
            # Рисуем заставку
            self.screen.blit(pygame.image.load("start_screen.png").convert(), [0, 0])
        elif self.state == 'MENU':
            # Заливаем фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            # Рисуем главное меню:
            self.main_menu.draw(self.screen)
        elif self.state == 'SETTINGS':
            # Заливаем фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            # Рисуем меню настроек:
            self.settings_menu.draw(self.screen)
        elif self.state == 'GAME':
            # Выполняем заливку фона:
            self.screen.blit(self.background_img, [self.shift, 0])
            # Рисуем все спрайты в игре:
            self.top_panel.draw(self.screen)
            self.all_sprite_list.draw(self.screen)

        elif self.state == 'FINISH':
            # Заливаем фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            # Создаем и отображаем надпись
            self.label = FONT.render('CONGRATILATIONS' , True, )
            self.screen.blit(self.label, [WIN_WIDTH / 2, WIN_HEIGHT / 2])
        elif self.state == 'GAME OVER':
            # Заливаем фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            # Создаем и отображаем надпись
            self.label = FONT.render('GAME OVER' , True, YELLOW)
            self.screen.blit(self.label, [WIN_WIDTH / 2, WIN_HEIGHT / 2])

    # Обновление текущего состояния игры
    def update(self):
        print(self.player.rect.x)
        print(self.player.rect.y)
        # Если идет игра, обновляем все объекты в игре:
        if self.state == 'GAME':
            self.time += 1
            self.all_sprite_list.update()
            self.top_panel.update(coin=self.player.score, lives=self.player.lives)

            # Проверяем стокновение игрока с противником:
            if pygame.sprite.spritecollideany(self.player, self.enemy_list, False):
                # Очки жизней при столкновении с противником буду отниматься не чаще 1 раза в секунду:
                if self.time - self.hit_time > FPS:
                    self.player.lives -= 1
                    # зафиксируем время последнего столкновения
                    self.hit_time = self.time
                # "отбросим" игрока от противника
                self.player.change_x = -5

            # Проверяем, не достиг ли персонаж выхода:
            if self.player.rect.x > WIN_WIDTH - 80 and self.player.rect.y > WIN_HEIGHT - 80:
                self.state = 'FINISH'

            # Проверяем остаток жизней у игрока:
            if self.player.lives <= 0:
                self.state = 'GAME OVER'

        # Если игра в состоянии SETTINGS, обновляем меню настроек:
        elif self.state == 'SETTINGS':

            self.settings_menu.update()
        # Если игра на паузе или на старте, обновляем  меню:
        else:
            self.main_menu.update()


    def run(self):
        done = False
        print(self.player.rect.x)
        print(self.player.rect.y)
        # Запустили главный игровой цикл:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # Обрабатываем события для разных состояний:
                self.handle_states(event)
                if self.player.rect.x > WIN_WIDTH - 70 and self.player.rect.y > WIN_HEIGHT - 70:
                    self.state = "FINISH"
                    done = True



            # Если игрок приближается к правому краю экрана, смещаем мир влево на (-x)
            if self.player.rect.right >= 500 and abs(self.shift) < self.game_width - WIN_WIDTH:
                diff = self.player.rect.right - 500
                self.player.rect.right = 500
                self.shift_world(-diff)

            # Если игрок приближается к левому краю экрана, смещаем мир вправо на (+x)
            if self.player.rect.left <= 120 and abs(self.shift) > 0:
                diff = 120 - self.player.rect.left
                self.player.rect.left = 120
                self.shift_world(diff)

            self.update()
            # Отрисовываем окно игры для текущего состояния:
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

game = Game()
game.run()
