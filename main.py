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
        - - граница корабля (клетка, которая примыкает к кораблю сбоку или по диагонали)

    status_public : str
        Указывает состояние клетки, которое видит противник (только результаты ходов - попадания и промахи)

    Методы
    -----------
    status() -> str
        Устанавливает состояние клетки при создании корабля. Виден только "своему" игроку

    status_public() -> str
        Устанавливает публичное состояние клетки после того, как в нее выстрелил игрок. Виден "противнику"

    hit(row, col) -> Bool
        Принимает координаты (номер строки и номер колонки) и возвращает True, если они совпадают с координатами
        клетки, иначе False
    """

    def __init__(self, row=0, col=0, status=' ', status_public=' '):
        self.__set_cords(row, col)
        self.__set_status(status)
        self.__set_status_public(status_public)

    def __set_cords(self, row: int, col: int):
        """
        Устанавливает координаты клетки. Вызывается конструктором класса
        :param row: Номер строки
        :param col: Номер колонки
        :return: None
        """
        self.__row = row
        self.__col = col

    def __set_status(self, status: str):
        """
        Устанавливает статус клетки. Вызывается конструктором класса или сеттером
        :param status: str
        :return: None
        """
        self.__status = status

    def __set_status_public(self, status_public: str):
        """
        Устанавливает публичный статус клетки, т.е. тот, который видит противник. Вызывается конструктором класса
         или сеттером
        :param status: str
        :return: None
        """
        self.__status_public = status_public

    def hit(self, row, col):
        """
        Проверяет попадание в клетку при ходе игрока (установке палубы корабля или выстреле)
        :param row: Номер строки
        :param col: Номер колонки
        :return: True если переданные координаты совпадают с координатами клетки. Иначе False
        """
        if (self.__row == row) and (self.__col == col):
            return True
        else:
            return False

    @property
    def status(self):
        """
        :return: str Статус клетки
        """
        return self.__status

    @status.setter
    def status(self, status):
        """
        Устанавливает статус клетки
        :param status: str Статус, который нужно установить
        :return: None
        """
        self.__set_status(status)

    @property
    def status_public(self):
        """
        :return: str Публичный статус клетки
        """
        return self.__status_public

    @status_public.setter
    def status_public(self, status_public):
        """
        Устанавливает публичный статус клетки
        :param status_public: str Статус, который нужно установить
        :return: None
        """
        self.__status_public = status_public

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
        Список объектов Cell, т.е. список ячеек, которые занимает корабль (список палуб)

    Методы
    -----------
    add_deck(deck) : -> None
        Добавляет ячейку (объект Cell) в список палуб корабля (decks)

    decks() : -> list
        Возвращает список палуб корабля (объектов Cell)
    """

    def __init__(self, decks=None):
        self.__set_decks(decks)

    def add_deck(self, deck):
        """
        Добавляет ячейку (объект Cell) в список палуб корабля (decks)
        :param deck: Объект Cell
        :return: None
        """
        self.__decks.append(deck)

    def __set_decks(self, decks):
        """
        Выполняет первоначальное заполнение корабля палубами в конструкторе класса
        :param decks: list Список объектов Cell
        :return: None
        """
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
    ships : list
        Содержит список кораблей (объектов Ship), расположенных на игровом поле

    ships_area_list list
        Содержит список списков (вложенный список = строка) всех объектов Cell игрового поля

    Методы
    -----------
    add_ship(ship) : -> None
        Добавляет объект Ship к списку кораблей игрового поля

    create_ship_borders(ship) : None
        Присваивает всем ячейкам, находящимся рядом с кораблем, status '-', который исключает эти ячейки
        из списка доступных ячеек при выполнении операции установки кораблей на поле,
        используется при установке кораблей как человеком, так и компьютером

    delete_ship_borders() : -> None
        Удаляет у всех ячеек, которые являются границами кораблей, status '-', поскольку после расстановки кораблей
        на поле эти метки уже не нужны. Удалять необязательно, сделано для более приятного вида игрового поля человека

    check_ships_hit(row, col) : -> bool
        По полученным на вход координатам (номеру строки и номеру колонки) определяет в списке кораблей, было ли
        попадание в какую-то палубу

    possible_ships_areas(decks_num, public) : -> list
        Анализирует уже занятые ячейки игрового поля и определяет доступные группы ячеек,
        в которые может поместиться корабль с требуемым количеством палуб. Используется как для заполнения
        игрового поля при расстановке кораблей (ручном или автоматическом), так и в процессе игры, предоставляя
        пользователю, особенно компьютеру, исчерпывающий список возможных ходов с учетом уже сделанных им выстрелов,
        куда можно походить

    all_ships_sunk() : -> bool
        Проверяет, что все корабли на игровом поле подбиты

    alive_decks_num(self):
        Проверяет, сколько неподбитых палуб осталось на игровом поле
    """

    def __init__(self, size: int, ships_list=None):
        self.__set_ships_list(ships_list)
        self.__fill_cells(size)

    def __set_ships_list(self, ships_list):
        """
        Заполняет список кораблей объектами Ship в конструкторе класса
        :param ships_list: list Список объектов Ship
        :return: None
        """
        if ships_list is None:
            self.__ships_list = []
        else: self.__ships_list = ships_list

    def __fill_cells(self, size):
        """
        Автоматически заполняет все пространство игрового поля объектами Cell
        при создании объекта Field так, чтобы любое обращение к любой ячейке поля по координатам
        возвращало объект Cell
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
        """
        Добавляет объект Ship к списку кораблей игрового поля
        :param ship: объект Ship
        :return: None
        """
        self.__ships_list.append(ship)

    @property
    def ships(self):
        """
        :return: list Возвращает список кораблей (объектов Ship), расположенных на игровом поле
        """
        return self.__ships_list

    @property
    def ships_area_list(self):
        """
        :return: list Возвращает список всех ячеек (Список списков, содержащих объекты Cell) игрового поля
        """
        return self.__ships_area_list

    def create_ship_borders(self, ship):
        """
        Присваивает всем ячейкам, находящимся рядом с кораблем, status '-', который исключает эти ячейки
        из списка доступных ячеек при выполнении операции установки кораблей на поле,
        используется при установке кораблей как человеком, так и компьютером
        :param ship: объект Ship
        :return: None
        """

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

    def delete_ship_borders(self):
        """
        Удаляет у всех ячеек, которые являются границами кораблей, status '-', поскольку после расстановки кораблей
        на поле эти метки уже не нужны. Удалять необязательно, сделано для более приятного вида игрового поля человека
        :return: None
        """
        for line in self.__ships_area_list:
            for cell in line:
                if cell.status == '-':
                    cell.status = ' '

    def check_ships_hit(self, row, col):
        """
        По полученным на вход координатам (номеру строки и номеру колонки) определяет в списке кораблей, было ли
        попадание в какую-то палубу
        :param row: int Номер строки
        :param col: int Номер колонки
        :return: True если попадание было, иначе False
        """
        for curr_ship in self.ships:
            for curr_deck in curr_ship.decks:
                if curr_deck.hit(row, col):
                    return True

        return False

    def possible_ships_areas(self, decks_num, public=False):
        """
        Определяет доступные группы ячеек, в которые может поместиться корабль с требуемым количеством палуб
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
                    # При этом учитываем, внутренний или публичный статус нужно проверять
                    if public:
                        if cell.status_public == ' ':
                            area.append(cell)
                    else:
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
                        # При этом учитываем, внутренний или публичный статус нужно проверять
                        if public:
                            if cell.status_public == ' ':
                                area.append(cell)
                        else:
                            if cell.status == ' ':
                                area.append(cell)

                    # Добавляем список ячеек в общий массив свободных зон только если все ячейки в смещении свободны,
                    # т.е. в них влазит корабль требуемого размера
                    if len(area) == decks_num:
                        ships_areas.append(area)

        return ships_areas

    def all_ships_sunk(self):
        """
        Проверяет, что все корабли на игровом поле подбиты
        :return: True если все ячейки (палубы), входящие во все корабли, имеют публичный статус '*', иначе False
        """
        thats_all = True
        for ship in self.__ships_list:
            for deck in ship.decks:
                if deck.status_public == ' ':
                    thats_all = False
                    break

        return thats_all

    def alive_decks_num(self):
        """
        Проверяет, сколько неподбитых палуб осталось на игровом поле
        :return: int Количество неподбитых палуб
        """
        alive_decks = 0
        for ship in self.__ships_list:
            for deck in ship.decks:
                if deck.status_public == ' ':
                    alive_decks += 1

        return alive_decks

class HumansField(Field):
    """
    Представляет собой игровое поле человека
    Свойства
    -----------
    Все свойства такие же, как и у родительского класса Field

    Статические методы
    -----------
    victory_speech() -> str
        Возвращает текст речи в случае победы человека по окончании игры

    Методы
    -----------
    Методы предполагают интерактивное взаимодействие с пользователем

    fill_ships() -> None
        Заполняет игровое поле кораблями

    input_sell() -> None
        Реализует операцию интерактивного ввода пользователем информации в ячейку игрового поля
        (при расстановке кораблей и при стрельбе человеком)

    fill_ships() -> None
        Интерактивно заполняет игровое поле кораблями (объектами Ship). При этом создает:
            - один трехпалубный корабль
            - два двухпалубных корабля
            - три однопалубных корабля

    shot() -> None
        Реализует процедуру интерактивного хода (выстрела) человека по кораблям компьютера
    """

    @staticmethod
    def victory_speech():
        """
        Заготовка речи на случай победы человека
        :return: -> Текст речи
        """
        return 'Ура! Ты победил!! Все корабли противника потоплены. Роботы не захватят этот мир!'

    def input_cell(self, current_deck=None):
        """
        Реализует операцию интерактивного ввода пользователем информации в ячейку игрового поля
        (при расстановке кораблей и при стрельбе человеком)
        :param current_deck: int При интерактивном создании палубы корабля указывает текущую палубу, которая создается,
        при стрельбе не заполняется
        :return: -> None
        """
        if current_deck is None:
            question = 'Ваш ход! укажите координаты выстрела (номер строки - пробел - номер колонки): '
        else:
            question = f'Введите координаты {current_deck} палубы корабля (номер строки - пробел - номер колонки): '

        valid_cords = False
        while not valid_cords:

            cords = input(question).split()

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

            valid_cords = True

        return row, col

    def __create_ship(self, decks_num):
        """
        Интерактивно создает корабль (объект Ship) с заданным количеством палуб и помещает его в список
        кораблей игрового поля.

        Фактически, находит ячейки, которые выбрал пользователь на игровом поле, и присваивает им статус '*',
        при этом также помещает ячейку в список палуб корабля объекта Ship. Это позволяет, оперируя ячейками
        игрового поля, отслеживать статус всего корабля, поскольку каждая отдельная ячейка входит в объект Field и
        объект Ship одновременно

        :param decks_num: int количество палуб создаваемого корабля
        :return: None
        """
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

            row, col = self.input_cell(current_deck)

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
        """
        Интерактивно заполняет игровое поле кораблями (объектами Ship). При этом создает:
        - один трехпалубный корабль
        - два двухпалубных корабля
        - три однопалубных корабля

        :return: None
        """
        print('Заполним игровое кораблями')

        #Интерактивное создание трехпалубного корабля
        self.__create_ship(3)

        #Интерактивное создание двух двухпалубных кораблей
        for i in range(2):
            self.__create_ship(2)

        #Интерактивное создание трех однопалубных кораблей
        for i in range(3):
            self.__create_ship(1)

        self.delete_ship_borders()
        print('Отлично! корабли заняли свои места на поле!')

    def shot(self, skynet_field):
        """
        Реализует процедуру интерактивного хода (выстрела) человека по кораблям компьютера
        :param skynet_field: Объект SkynetField
        :return: None
        """
        # Заполним список доступных ходов
        shot_var = skynet_field.possible_ships_areas(1, True)

        correct_shot = None
        while correct_shot is None:

            row, col = self.input_cell()

            for area in shot_var:
                for cell in area:
                    if cell.hit(row, col):
                        if cell.status == '*':
                            print('Есть попадание! Так держать!')
                            cell.status_public = 'X'
                            correct_shot = True
                        else:
                            print('Промах!')
                            cell.status_public = 'T'
                            correct_shot = False

                        break

            # Пользователь ткнул куда-то повторно
            if correct_shot is None:
                print('В это поле уже стреляли. Сделай выстрел в другое поле')

            continue

        # Покажем результат выстрела
        game.show_fields()

class SkynetField(Field):
    """
    Представляет собой игровое поле компьютера

    Свойства
    -----------
    Все свойства такие же, как и у родительского класса Field

    Статические методы
    -----------
    victory_speech() -> str
        Возвращает текст речи в случае победы компьютера по окончании игры

    Методы
    -----------
    Методы предполагают автоматическое выполнение действий за играющий компьютер

    fill_ships() -> None
        Программно заполняет игровое поле кораблями (объектами Ship). При этом создает:
            - один трехпалубный корабль
            - два двухпалубных корабля
            - три однопалубных корабля

    shot() -> None
        Реализует процедуру программного хода (выстрела) компьютера по кораблям человека
    """
    @staticmethod
    def victory_speech():
        """
        Возвращает текст речи в случае победы компьютера по окончании игры
        :return: текст речи
        """
        return 'Компьютер в этот раз победил. Собирайся с силами и приходи брать реванш!'

    def __create_ship(self, decks_num):
        """
            Программно создает корабль (объект Ship) с заданным количеством палуб и помещает его в список
            кораблей игрового поля.

            Случайно выбирает ячейки из доступных зон (списков ячеек, в которые помещается корабль выбранного размера),
            и создает из этих ячеек корабль (объект Ship), т.е. присваивает выбранным ячейкам статус '*',
            при этом также помещает ячейку в список палуб корабля объекта Ship. Это позволяет, оперируя ячейками
            игрового поля, отслеживать статус всего корабля, поскольку каждая отдельная ячейка входит в объект Field и
            объект Ship одновременно

            :param decks_num: int количество палуб создаваемого корабля
            :return: None
            """
        # Теоретически возможно, что при неудачном случайном расположении кораблей на каком-то ходе
        # создание следующего корабля флотилии станет невозможным из-за ограничений,
        # связанных с соблюдением границ других, уже созданных кораблей

        try:

            # Создаем объект корабля, пока без палуб
            ship = Ship()
            # Сразу добавим его в поле
            self.add_ship(ship)

            # Список всех доступных зон размещения корабля указанного размера
            ships_areas = self.possible_ships_areas(decks_num)

            # Выбираем случайно зону, подходящую для размещения корабля
            # Она и станет кораблем нужного нам размера
            ship_area = random.choice(ships_areas)
            for deck in ship_area:
                deck.status = '*'
                ship.add_deck(deck)

            # Заполним границы вокруг корабля, чтобы следующий корабль учел их и исключил эти клетки
            # из списка доступных зон для размещения кораблей
            self.create_ship_borders(ship)

        except IndexError as e:

            # Не получилось найти зону (группу непрерывных ячеек) для создания корабля требуемого размера
            # вероятно из-за неудачного случайного расположения ранее созданных кораблей
            # принимаем решение, что в этом случае комп играет теми кораблями, которые смог создать

            print('')
            print(
                f'Компьютер запутался и не смог создать корабль с количеством палуб {decks_num}. будет играть без него')
            print('')

    def fill_ships(self):
        """
        Программно заполняет игровое поле кораблями (объектами Ship)
        :return: None
        """
        #Автоматическое создание трехпалубного корабля
        self.__create_ship(3)

        #Автоматическое создание двух двухпалубных кораблей
        for i in range(2):
            self.__create_ship(2)

        # Автоматическое создание трех однопалубных кораблей
        for i in range(3):
            self.__create_ship(1)

        print('')
        print('Компьютер расставил свои корабли и к игре готов!')
        print('')

        game.show_fields()

    def shot(self, humans_field):
        """
        Реализует процедуру программного хода (выстрела) компьютера по кораблям человека
        :param humans_field: объект HumansField, игровое поле человека
        :return: None
        """
        print('Выстрел компьютера:')

        # Заполним список доступных ходов
        shot_var = humans_field.possible_ships_areas(1, True)

        area = random.choice(shot_var)
        for cell in area:
            if cell.status == '*':
                print('Есть попадание в твой корабль!')
                cell.status_public = 'X'
                cell.status = 'X'
            else:
                print('Компьютер промазал!')
                cell.status_public = 'T'
                cell.status = 'T'

        # Покажем результат выстрела
        game.show_fields()

class Game:
    """
    Класс представляет собой экземпляр конкретной игры, реализует игровую логику

    Константы
    -----------
    FIELD_SIZE - размер игрового поля

    Методы
    -----------
    show_fields() -> None
        Выводит в консоль игровые поля человека и компьютера (свое поле показывает с расположенными всеми кораблями и
        результатами выстрелов, поле компьютера - только с результатами выстрелов).
        Также для каждого поля выводит количество оставшихся живых палуб всех кораблей,
        информация обновляется после каждого хода

    start() -> None
        Запускает игру и управляет игровым процессом:
        Игроки ходят по очереди. Даже после попадания по вражескому кораблю ход переходит к другому игроку.
        Компьютер туп: после попадания по палубе корабля человека следующий ход он делает случайно

    Статические методы
    -----------
    greet() -> None
        Выводит начальное приветствие и правила игры
    """

    def __init__(self):
        self.__humans_field = []
        self.__skynet_field = []

    # Вводим константу для определения количества полей игрового поля
    @staticmethod
    def FIELD_SIZE():
        return 6

    @staticmethod
    def greet():

        greet_text = '''
        Добро пожаловать в игру Морской бой!
        -----------
        Тебе предстоит сыграть с компьютером
            
        Правила игры:
        -----------
        Сначала нужно будет расставить корабли на игровом поле
        В битве участвует один трехпалубный корабль, два двухпалубных и три однопалубных корабля
        Корабли должны располагаться на расстоянии как минимум одной клетки друг от друга 
        
        Стреляем по очереди с компьютером
        Чтобы сделать выстрел, нужно ввести координаты клетки, в которую ты стреляешь, в формате: номер строки - пробел - номер колонки
        Даже после попадания по вражескому кораблю ход переходит к другому игроку
        
        Побеждает тот, кто первым уничтожит все корабли противника
        
        Удачи в бою!
        '''

        print(greet_text)

    def show_fields(self):
        """
        Выводит в консоль игровые поля человека и компьютера (свое поле показывает с расположенными всеми кораблями и
        результатами выстрелов, поле компьютера - только с результатами выстрелов)
        :return: None
        """
        # Создадим шаблон игрового поля
        indent = ['          ']
        field_base = [[" "] * Game.FIELD_SIZE() + indent + [" "] * Game.FIELD_SIZE()for i in range(Game.FIELD_SIZE())]

        for x, ships_row in enumerate(self.__humans_field.ships_area_list):
            for y, cell in enumerate(ships_row):
                field_base[x][y] = cell.status
        humans_alive_decks_num = self.__humans_field.alive_decks_num()

        # Если поле еще не заполнялось - выводить нечего
        skynet_alive_decks_num = 0
        if self.__skynet_field:
            for x, ships_row in enumerate(self.__skynet_field.ships_area_list):
                for y, cell in enumerate(ships_row):
                    field_base[x][y+7] = cell.status_public
            skynet_alive_decks_num = self.__skynet_field.alive_decks_num()

            # for x, ships_row in enumerate(self.__skynet_field.ships_area_list):
            #     for y, cell in enumerate(ships_row):
            #         field_base[x][y] = cell.status

        print(f'     Мои корабли (живых палуб - {humans_alive_decks_num})         Корабли компьютера (живых палуб - {skynet_alive_decks_num})')
        print('    | 1 | 2 | 3 | 4 | 5 | 6 |            | 1 | 2 | 3 | 4 | 5 | 6 |')
        print('  ---------------------------         ---------------------------- ')
        for i, row in enumerate(field_base):
            row_str = f'  {i + 1} | {" | ".join(row)} | '
            print(row_str)
            print(' ----------------------------         ---------------------------- ')
        print('')

    def start(self):
        """
        Запускает игру и управляет игровым процессом
        :return: None
        """
        # Выведем приветствие
        Game.greet()

        #Создадим игровое поле человека
        self.__humans_field = HumansField(Game.FIELD_SIZE())
        self.__humans_field.fill_ships()

        # Создадим игровое поле компа
        self.__skynet_field = SkynetField(Game.FIELD_SIZE())
        self.__skynet_field.fill_ships()

        game_over = False
        current_field = self.__humans_field
        current_enemys_field = self.__skynet_field
        while not game_over:

            current_field.shot(current_enemys_field)

            if current_enemys_field.all_ships_sunk():
                game_over = True
                print(current_field.victory_speech())
                break

            current_field, current_enemys_field = current_enemys_field, current_field


if __name__ == '__main__':

    game = Game()
    game.start()