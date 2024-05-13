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
        self.__size = size

    @property
    def ships(self):
        return self.__ships_list

    def __set_ships_list(self, ships_list):
        if ships_list is None:
            self.__ships_list = []
        else: self.__ships_list = ships_list


    def add_ship(self, ship):
        self.__ships_list.append(ship)

    def show(self):
        field_size = [[" "] * 6 for i in range(6)]

        # field_size[1][1] = '*'

        print()
        print("    | 1 | 2 | 3 | 4 | 5 | 6 |")
        print("  --------------------------- ")
        for i, row in enumerate(field_size):
            row_str = f"  {i + 1} | {' | '.join(row)} | "
            print(row_str)
            print("  --------------------------- ")
        print()

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

    def __check_cell(self, cell):

        # Пройдемся по всем палубам всех созданных кораблей
        for ship in self.ships:
            for deck in ship.decks:

                # Сначала проверим, не пытается ли пользователь поставить палубу в клетку,
                # которая уже занята другой палубой этого же или другого корабля
                if deck == cell:


        return 1


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
                print(" Координаты вне игрового поля! ")
                continue

            # Создаем ячейку
            cell = Cell(row, col, '*')



            ship.add_deck(cell)
            created_decks += 1

            # Покажем пользователю поле, чтобы он видел, куда ткнул
            game.show_fields()



        print(f'{decks_num_str} корабль создан')


    def fill_ships(self):
        print('Заполним игровое кораблями')

        # print(self.ships)

        #Интерактивное создание трехпалубного корабля
        self.__create_ship(3)


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

    # Вводим константу для определения количества полей игрового поля
    @staticmethod
    def FIELD_SIZE():
        return 6

    def __init__(self):
        pass


    def start(self):

        # Выведем приветствие
        Game.greet()

        #Создадим игровое поле человека
        self.__humans_field = HumansField(Game.FIELD_SIZE)
        self.__humans_field.fill_ships()

    def show_fields(self):
        field_base = [[" "] * Game.FIELD_SIZE() for i in range(Game.FIELD_SIZE())]

        for ship in self.__humans_field.ships:
            for deck in ship.decks:
                # поскольку вставлять палубы будем по номерам индексов, то надо отнять 1 от всех координат
                field_base[deck.row-1][deck.col-1] = deck.status


        print('')
        print('    | 1 | 2 | 3 | 4 | 5 | 6 |')
        print('  --------------------------- ')
        for i, row in enumerate(field_base):
            row_str = f'  {i + 1} | {" | ".join(row)} | '
            print(row_str)
            print(' --------------------------- ')
        print()

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

if __name__ == '__main__':

    game = Game()
    game.start()