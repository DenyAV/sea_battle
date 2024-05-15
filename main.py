import random


class Cell:
    """
    Класс описывает клетку игрового поля

    Свойства
    -----------
    row : int
        Номер строки, на которой находится клетка

    col : int
        Номер колонки, на которой находится клетка

    status : str
        Указывает состояние клетки:
        ' ' - пустая
        * - живой корабль
        Х - подбитый корабль
        Т - промах

    Методы
    -----------
    status() -> str
        Устанавливает состояние клетки после того, как в нее выстрелил игрок, а также при создании корабля


    """

    def __init__(self, row=0, col=0, status=' '):
        self.__set_cords(row, col)
        self.__set_status(status)

    def __eq__(self, other):
        return (self.__row == other.__row) and (self.__col == other.__col)

    # Внутренняя функция. Устанавливает координаты клетки. Вызывается конструктором класса
    def __set_cords(self, row: int, col: int):
        self.__row = row
        self.__col = col
        # todo
        # Добавить исключения

    # Внутренняя функция. Устанавливает статус клетки. Вызывается конструктором класса или сеттером
    def __set_status(self, status: str):
        self.__status = status

    def hit(self, row, col):
        if (self.__row == row) and (self.__col == col):
            return True
        else:
            return False

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__set_status(status)

    @property
    def row(self):
        return self.__row


    @property
    def col(self):
        return self.__col

class Ship:
    """
    Класс используется для представления корабля

    Свойства
    -----------
    decks : []
        Список объектов Deck, т.е. список палуб корабля

    Методы
    -----------

    Статические методы
    -----------
    create_ship(decks_num, players_field)
        Мастер интерактивного создания нового корабля с заданным количеством палуб на игровом поле

        Параметры:

        decks_num : int
            Количество палуб корабля (сколько клеток корабль занимает на поле - целое число от 1 до 3)
        players_field : object Field
            Игровое поле, на котором будет размещаться корабль.
            Создавать корабль отдельно от игрового поля бессмысленно, поскольку
            на поле могут быть другие корабли и при создании корабля нужно проверять,
            не пересекается ли он с другими кораблями на поле

    """

    def __init__(self, decks=None):
        self.__set_decks(decks)


    def add_deck(self, deck):
        self.__decks.append(deck)


    def __set_decks(self, decks):
        if decks is None:
            self.__decks = []
        else:
            self.__decks = decks

    @property
    def decks(self):
        return self.__decks


class Field:
    """
    Класс используется для представления игрового поля

    Свойства
    -----------
    ships : []
        Содержит список кораблей, расположенных на игровом поле

    Методы
    -----------
    show()
        Выводит в консоль заполненное игровое поле, в котором:
        ' ' - пустое поле
        * - клетка, заполненная кораблем
        Х - подбитый корабль
        Т - промах

    Статические методы
    -----------
    create_field()
        Мастер создания игрового поля и заполнения его кораблями

        Последовательно предлагает пользователю создать корабли:
        1 трехпалубный корабль;
        2 двухпалубных корабля;
        3 трехпалубных корабля

        Затем создает объект класса Field и заполняет его созданными кораблями
    """

    def __init__(self, size: int, ships_list=None):
        self.__set_ships_list(ships_list)
        self.__fill_cells(size)

    def __set_ships_list(self, ships_list):
        if ships_list is None:
            self.__ships_list = []
        else: self.__ships_list = ships_list

    def __fill_cells(self, size):
        """
        Функция автоматически заполняет все пространство игрового поля объектами Cell
        при создании объекта Field
        :param size: Константа - размер игрового поля
        :return: None
        """
        self.__size = size
        self.__ships_area_list = []

        for x in range(1, size+1):
            row_list = []
            for y in range(1, size+1):
                cell = Cell(x, y)
                row_list.append(cell)
            self.__ships_area_list.append(row_list)

    def add_ship(self, ship):
        self.__ships_list.append(ship)

    @property
    def ships(self):
        return self.__ships_list

    @property
    def ships_area_list(self):
        return self.__ships_area_list

    def create_ship_borders(self, ship):

        # Пройдемся вокруг всех палуб корабля и отметим соседние ячейки как границу,
        # в которой ставить другие корабли нельзя

        for deck in ship.decks:
            border_row = deck.row - 1
            border_col = deck.col - 1
            for x in range(border_row, border_row+3):
                for y in range(border_col, border_col+3):

                    if x == 0:
                        xx = 1
                    elif x > 5:
                        xx = 5
                    else:
                        xx = x - 1

                    if y == 0:
                        yy = 1
                    elif y > 5:
                        yy = 5
                    else:
                        yy = y - 1

                    cell = self.ships_area_list[xx][yy]
                    if cell.status == ' ':
                        cell.status = '-'

    def check_ships_hit(self, row, col):

        for curr_ship in self.ships:
            for curr_deck in curr_ship.decks:
                if curr_deck.hit(row, col):
                    return True

        return False

    def possible_ships_areas(self, decks_num):
        """
        Функция определяет доступные группы ячеек, в которые может поместиться корабль с требуемым количеством палуб
        :param decks_num: количество палуб (ячеек). Определяет размер корабля, который нужно поместить в поле
        :return: Список списков. Каждый вложенный список представляет собой набор рядом расположенных объектов cell,
        подходящих для размещения корабля требуемого размера, т.е. свободных ячеек, не занятых другими кораблями
        и не граничащих с другими кораблями
        """

        size = Game.FIELD_SIZE()
        ships_areas = []

        for x in range(1, size + 1):
            # Вводим смещение - т.е. потенциальную группу ячеек, которую проверяем на предмет того, свободны ли они
            # Если все объекты в смещении свободны - добавляем смещение в виде списка в список доступных групп
            for offset in range(1, size - decks_num + 2):
                area = []
                for y in range(offset, offset + decks_num):
                    cell = self.ships_area_list[x-1][y-1]
                    # Добавляем ячейку в список только если статус у нее пустой, т.е. ячейка свободна
                    if cell.status == ' ':
                        area.append(cell)

                # Добавляем список ячеек в общий массив свободных зон только если все ячейки в смещении свободны,
                # т.е. в них влазит корабль требуемого размера
                if len(area) == decks_num:
                    ships_areas.append(area)

        # Если количество палуб > 1, то проходимся также и по колонкам, поскольку корабли могут быть и вертикальными
        if decks_num > 1:
            for y in range(1, size + 1):
                for offset in range(1, size - decks_num + 2):
                    area = []
                    for x in range(offset, offset + decks_num):
                        cell = self.ships_area_list[x-1][y-1]
                        # Добавляем ячейку в список только если статус у нее пустой, т.е. ячейка свободна
                        if cell.status == ' ':
                            area.append(cell)

                    # Добавляем список ячеек в общий массив свободных зон только если все ячейки в смещении свободны,
                    # т.е. в них влазит корабль требуемого размера
                    if len(area) == decks_num:
                        ships_areas.append(area)

        return ships_areas


class HumansField(Field):
    """
    Представляет собой игровое поле человека
    Свойства
    -----------
    Все свойства такие же, как и у родительского класса

    Методы
    -----------
    Методы предполагают интерактивное взаимодействие с пользователем

    fill_ships()
        Заполняет игровое поле кораблями
    """


    def __create_ship(self, decks_num):

        # Создаем объект корабля, пока без палуб
        ship = Ship()
        # Сразу добавим его в поле
        self.add_ship(ship)

        # decks_num(количество палуб) может быть только целым числом от 1 до 3
        decks_num_str = ''
        if decks_num == 3:
            decks_num_str = 'трехпалубный'
        elif decks_num == 2:
            decks_num_str = 'двухпалубный'
        else:
            decks_num_str = 'однопалубный'

        print(f'Cоздаем {decks_num_str} корабль:')

        created_decks = 0  # Количество созданных палуб корабля
        ships_areas = self.possible_ships_areas(decks_num) #Список всех доступных зон размещения корабля указанного размера
        while created_decks < decks_num:

            # Создаваемая в данный момент палуба корабля
            if created_decks == 0:
                current_deck = 'первой'
            elif created_decks == 1:
                current_deck = 'второй'
            elif created_decks == 2:
                current_deck = 'третьей'

            cords = input(f'Введите координаты {current_deck} палубы корабля (номер строки - пробел - номер колонки): ').split()

            # Проверим, что введено именно два знака координат
            if len(cords) != 2:
                print(' Введите 2 координаты! ')
                continue

            row, col = cords

            # Проверим, что эти два знака являются числами
            if not (row.isdigit()) or not (col.isdigit()):
                print(' Введите числа! ')
                continue

            row, col = int(row), int(col)

            # Проверим, что координаты попали в игровое поле
            if 0 > row or row > Game.FIELD_SIZE() or 0 > col or col > Game.FIELD_SIZE():
                print(' Координаты вне игрового поля! ')
                continue

            # Проверим, не попал ли пользователь в какой-то другой корабль
            if self.check_ships_hit(row, col):
                print('В этой клетке уже стоит палуба корабля или она граничит с какой-то палубой.  Выберите другую')
                continue


            # Пройдемся по списку доступных зон размещения кораблей и проверим, входит ли выбранная пользователем ячейка
            # хотя бы в одну зону
            used_ships_areas = []
            for area in ships_areas:
                for cell in area:
                    if cell.hit(row, col):
                        used_ships_areas.append(area)

            # Если не нашлось ни одной зоны, куда входит ячейка - построить корабль заданного размера в этой точке
            # невозможно. Предлагаем выбрать правильную точку, которая лежит в заданных зонах
            if len(used_ships_areas):
                ship_sell = self.ships_area_list[row-1][col-1]
                ship_sell.status = '*'
                ship.add_deck(ship_sell)
            else:
                print('В этой клетке нельзя ставить палубу корабля. выберите клетку, соседнюю с уже имеющимися палубами')
                continue

            # Заменим первоначальный список списков тем, которые подходят для данной ячейки.
            # Далее искать будем только в них
            ships_areas = used_ships_areas.copy()

            created_decks += 1

            # Покажем пользователю поле, чтобы он видел, куда ткнул
            game.show_fields()


        self.create_ship_borders(ship)
        game.show_fields()
        print(f'{decks_num_str} корабль создан')

    def fill_ships(self):

        print('Заполним игровое кораблями')

        #Интерактивное создание трехпалубного корабля
        self.__create_ship(3)

        #Интерактивное создание двух двухпалубных кораблей
        for i in range(2):
            self.__create_ship(2)

        #Интерактивное создание трех однопалубных кораблей
        for i in range(3):
            self.__create_ship(1)

        print('Отлично! корабли заняли свои места на поле!')

class SkynetField(Field):

    def __create_ship(self, decks_num):

        # Создаем объект корабля, пока без палуб
        ship = Ship()
        # Сразу добавим его в поле
        self.add_ship(ship)

        # created_decks = 0  # Количество созданных палуб корабля
        ships_areas = self.possible_ships_areas(decks_num) #Список всех доступных зон размещения корабля указанного размера
        # while created_decks < decks_num:

        # Выбираем случайно зону, подходящую для размещения корабля
        # Она и станет кораблем нужного нам размера
        ship_area = random.choice(ships_areas)
        for deck in ship_area:
            deck.status = '*'
            ship.add_deck(deck)

        self.create_ship_borders(ship)

        # print(f'{decks_num_str} корабль создан')

    def fill_ships(self):

        #Автоматическое создание трехпалубного корабля
        self.__create_ship(3)

        #Автоматическое создание двух двухпалубных кораблей
        for i in range(2):
            self.__create_ship(2)

        #Автоматическое создание трех однопалубных кораблей
        for i in range(3):
            self.__create_ship(1)

        print('')
        print('Компьютер к игре готов!')
        print('')

        game.show_fields()

class Game:
    """
    Класс представляет собой экземпляр конкретной игры, реализует игровую логику

    Константы
    -----------
    FIELD_SIZE - размер игрового поля

    Методы
    -----------
    start() -> None
        Запускает игру

    Статические методы
    -----------
    greet() -> None
        Выводит начальное приветствие и правила игры


    """

    def __init__(self):
        pass

    # Вводим константу для определения количества полей игрового поля
    @staticmethod
    def FIELD_SIZE():
        return 6

    @staticmethod
    def greet():

        greet_text = '''
           Добро пожаловать в игру Морской бой!
           -----------
           Тебе предстоит сыграть с компьютером.

           Правила игры:
           -----------
           Сначала нужно будет расставить корабли на игровом поле
           В битве участвует один трехпалубный корабль, два двухпалубных и три однопалубных корабля
           Корабли должны располагаться на расстоянии как минимум одной клетки друг от друга. 

           Стреляем по очереди с компьютером
           Чтобы сделать выстрел, нужно ввести координаты клетки, в которую ты стреляешь, в формате: номер строки - пробел - номер колонки

           Побеждает тот, кто первым уничтожит все корабли противника

           Удачи в бою!
           '''

        print(greet_text)

    def show_fields(self):

        # Создадим шаблон игрового поля
        indent = ['          ']
        field_base = [[" "] * Game.FIELD_SIZE() + indent + [" "] * Game.FIELD_SIZE()for i in range(Game.FIELD_SIZE())]

        for x, ships_row in enumerate(self.__skynet_field.ships_area_list):
            for y, cell in enumerate(ships_row):
                field_base[x][y] = cell.status

        for x, ships_row in enumerate(self.__skynet_field.ships_area_list):
            for y, cell in enumerate(ships_row):
                field_base[x][y+7] = cell.status

        print('     Мое поле                             Поле компьютера')
        print('    | 1 | 2 | 3 | 4 | 5 | 6 |            | 1 | 2 | 3 | 4 | 5 | 6 |')
        print('  ---------------------------         ---------------------------- ')
        for i, row in enumerate(field_base):
            row_str = f'  {i + 1} | {" | ".join(row)} | '
            print(row_str)
            print(' ----------------------------         ---------------------------- ')
        print('')

    def start(self):

        # Выведем приветствие
        Game.greet()

        #Создадим игровое поле человека
        # self.__humans_field = HumansField(Game.FIELD_SIZE())
        # self.__humans_field.fill_ships()

        # Создадим игровое поле компа
        self.__skynet_field = SkynetField(Game.FIELD_SIZE())
        self.__skynet_field.fill_ships()


if __name__ == '__main__':

    game = Game()
    game.start()