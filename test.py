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
        Устанавливает состояние клетки после того, как в нее выстрелил игрок

    set_cords(row: int, col: int) -> None
        Устанавливает координаты клетки

    set_status(status: str):
        Устанавливает статус клетки игрового поля. Внутренняя функция,
        вызывается конструктором класса или сеттером
    """

    def __init__(self, row=0, col=0, status=' '):
        self.set_cords(row, col)
        self.set_status(status)

    def set_cords(self, row: int, col: int):
        self.__row = row
        self.__col = col
        # todo
        # Добавить исключения

    def set_status(self, status: str):
        self.__status = status

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.set_status(status)


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

    @staticmethod
    def create_ship(decks_num, field):

        # На входе было проверено, что decks_num может быть только целым числом от 1 до 3
        decks_num_str = ''
        if decks_num == 3:
            decks_num_str = 'трехпалубный'
        elif decks_num == 2:
            decks_num_str = 'двухпалубный'
        else:
            decks_num_str = 'однопалубный'

        print(f'Cоздаем {decks_num_str} корабль:')

        created_decks = 0    #Количество созданных палуб корабля
        while created_decks < decks_num:

            cords = input('Введите координаты палубы корабля (номер строки - пробел - номер колонки): ').split()

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
            field_size = 6
            if 0 > row or row > field_size or 0 > col or col > field_size:
                print(" Координаты вне игрового поля! ")
                continue

            cell = Cell(row, col, '*')
            created_decks += 1

        print('Корабль создан')

            # if field[x][y] != " ":
            #     print(" Клетка занята! ")
            #     continue
            #
            # return x, y

Ship.create_ship(3, 'qq')
