import helper


def init_board(rows, columns):
    board = []
    for row in range(rows):
        board.append([helper.WATER for col in range(columns)])
    return board


def cell_loc(name):
    if len(name) < 2 or len(name) > 3:
        return
    if name[0] < 'A' or name[0] > 'Z':
        return
    number = name[1:]
    if not helper.is_int(number) or int(number) < 1 or int(number) > 99:
        return
    return int(number) - 1, ord(name[0]) - ord('A')


def valid_ship(board, size, loc):
    row_ship, col_ship = loc
    if (row_ship < 0 or row_ship + size > len(board) - 1 or col_ship < 0 or
            col_ship > len(board[row_ship]) - 1):
        return False
    for row in range(row_ship, row_ship + size + 1):
        if board[row][col_ship] != helper.WATER:
            return False
    return True


def _check_sizes_validity(ship_sizes):
    ship_sizes = sorted(ship_sizes, reverse=True)
    for size in ship_sizes:
        if size not in helper.SHIP_SIZES or ship_sizes.count(size) > \
                helper.SHIP_SIZES.count(size):
            return False
    return True


def create_player_board(rows, columns, ship_sizes): #TODO: ask about ship_sizes
    board = init_board(rows, columns)
    if not board or not _check_sizes_validity(ship_sizes): #???
        return []
    helper.print_board(board)
    for size in sorted(ship_sizes, reverse=True):
        loc = helper.get_input("enter top coordinate for ship of size " +
                               str(size) + ": ")
        while not _check_location(loc, rows, columns):
            print("not a valid location")
            loc = helper.get_input("enter top coordinate for ship of size " +
                                   str(size) + ": ")
        row_ship, col_ship = int(loc[1:]) - 1, ord(loc[0]) - ord('A')
        for row in range(row_ship, row_ship + size + 1):
            board[row][col_ship] = helper.SHIP
        helper.print_board(board)
    return board


def fire_torpedo(board, loc):
    row, col = loc
    if (row < 0 or row > len(board) - 1 or col < 0 or col >
            len(board[row]) - 1):
        return board
    if board[row][col] == helper.WATER:
        board[row][col] = helper.HIT_WATER
    elif board[row][col] == helper.SHIP:
        board[row][col] = helper.HIT_SHIP
    return board


def _get_ship_locations(board, size):
    locations = []
    for row in range(helper.NUM_ROWS):
        for col in range(helper.NUM_COLUMNS):
            if valid_ship(board, size, (row, col)):
                locations.append((row, col))
    return locations


def _create_ai_board():
    board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    for size in helper.SHIP_SIZES:
        loc = helper.choose_ship_location(board, size,
                                          _get_ship_locations(board, size))
        row_ship, col_ship = loc
        for row in range(row_ship, row_ship + size + 1):
            board[row][col_ship] = helper.SHIP
    return board


def _check_finish_condition(board):
    for row in range(helper.NUM_ROWS):
        for col in range(helper.NUM_COLUMNS):
            if board[row][col] == helper.SHIP:
                return False
    return True


def _check_location(loc, rows, cols):
    if len(loc) < 2 or len(loc) > 3:
        return False
    letter = loc[0]
    str_number = loc[1:]
    if not letter.isalpha():
        return False
    letter = letter.upper()
    if ord(letter) > ord('A') + cols:
        return False
    if not helper.is_int(str_number) or int(str_number) < 1 or \
            int(str_number) > rows:
        return False
    return True


def _get_torpedo_locations(board):
    locations = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] not in [helper.HIT_SHIP, helper.HIT_WATER]:
                locations.append((row, col))
    return locations


def _hide_ships(board):
    new_board = []
    for row in range(len(board)):
        new_row = []
        for col in range(len(board[row])):
            if board[row][col] == helper.SHIP:
                new_row.append(helper.WATER)
            else:
                new_row.append(board[row][col])
        new_board.append(new_row)
    return new_board


def _main_helper():
    board_human = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS,
                                      helper.SHIP_SIZES)
    board_ai = _create_ai_board()
    while not _check_finish_condition(board_human) and not \
            _check_finish_condition(board_ai):
        helper.print_board(board_human, _hide_ships(board_ai))
        torpedo_loc = helper.get_input("choose target: ")
        while not _check_location(torpedo_loc, helper.NUM_ROWS,
                                  helper.NUM_COLUMNS):
            print("invalid target")
            torpedo_loc = helper.get_input("choose target: ")
        row, col = int(torpedo_loc[1:]) - 1, ord(torpedo_loc[0]) - ord('A')
        board_ai = fire_torpedo(board_ai, (row, col))
        row, col = helper.choose_torpedo_target(
            board_human, _get_torpedo_locations(board_human))
        board_human = fire_torpedo(board_human, (row, col))
    helper.print_board(board_human, board_ai)
    answer = helper.get_input("do you want to play again? Y/N")
    while answer not in ["Y", "N"]:
        answer = helper.get_input("do you want to play again? Y/N")
    if answer == "N":
        return False
    return True


def main():
    play_again = True
    while play_again:
        play_again = _main_helper()


if __name__ == "__main__":
    main()
