def __possible_ships_areas(decks_num, size):
    ships_areas = []

    for x in range(1, size + 1):
        for offset in range(1, size - decks_num + 2):
            area = []
            for y in range(offset, offset + decks_num):
                cell = [f'{x}, {y}']
                area.append(cell)

            ships_areas.append(area)

    return ships_areas


print(__possible_ships_areas(2, 6))