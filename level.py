import constants
class Level:
    def __init__(self, filename="Levels.txt"):
        # список уровней
        self.maps = []
        current_map = []
        # Чтение из файла
        content = open(filename, "r")

        # читаем построчно содержимое файла
        for line in content:
            # начало уровня
            if line[0] == "{":
                # то создаем новый список для текущего уровня
                current_map = []
            # конец уровня
            if line[0] == "}":
                # карту текущего уровня добавляем в список всех уровней
                self.maps.append(current_map)
            if line[0] not in (";", "{", "}"):
                # в итоге получаем список из строк, содержащих только представление уровня
                current_map.append(line.strip())

        # закрываем файл
        content.close()

        # задаем размеры мира в соответствии с размерами уроня в txt
        # размеры тайлов из которых строится уровень 40 x 40
        self.map_width = len(self.maps[0][0]) * 40
        self.map_height = len(self.maps[0]) * 40



    def load_level(self, num):
        """ функция определяет координаты объектов в игре по расположению
            символов в списке.
            Принимает в качестве аргумента порядковый номер уровня.
        """
        # задаем размеры мира в соответствии с размерами уроня в txt
        # размеры тайлов из которых строится уровень 40 x 40
        self.map_width = len(self.maps[num][0]) * 40
        self.map_height = len(self.maps[num]) * 40

        self.platform_coords = []
        self.artifact_coords = []
        self.enemies_coords = []
        # начальное положение игрока
        startX = 0
        startY = 0
        # текущая строка
        line_num = 0
        # читаем построчно в текущем уровне (списке)
        for line in self.maps[num]:
            # номер символа в строке
            sym_num = 0
            # проверяем посимвольно в строке
            for symbol in line:
                if symbol == "#":
                    # получаем координаты блока платформ
                    self.platform_coords.append([sym_num * 40, line_num * 40 ])
                if symbol == "*":
                    # получаем координаты расположения артефакта
                    self.artifact_coords.append([sym_num * 40, line_num * 40 ])
                if symbol == "@":
                    self.enemies_coords.append([sym_num * 40, line_num * 40 ])
                if symbol == "+":
                    # получаем координаты начального положения игрока
                    startX = sym_num * 40
                    startY = line_num * 40
                sym_num += 1
            line_num += 1
        return startX, startY