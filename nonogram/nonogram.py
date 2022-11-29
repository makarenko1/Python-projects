#############################################################################
# FILE: nonogram.py
# EXERCISE: intro2cs1 ex8 2020
# DESCRIPTION: A simple program that solves nonograms.
#############################################################################
# WHY DID WE DECIDE TO NOT WRITE 1 OR 0 IN PLACES WHERE ARE -1?:
# First, the number -1, so that -1 can be said to be 1 or 0 must be very
# small. Moreover, for a small number of rows, this number should be so small
# that it will not affect the result in any way. Secondly, by defining -1 at
# will, we create the risk that our choice will be wrong. Thus, in case of an
# error, the function will have to recursively fix it, which will take time.
import copy

BLACK = 1
WHITE = 0
UNKNOWN = -1


def constraint_satisfactions(n, blocks):
    """
    This function returns all the ways of placing the blocks of number 1 in a
    row of length n.
    :param n: the length of a row.
    :param blocks: a list of constraints.
    :return: all the ways of placing.
    """
    if not blocks:
        return [[0]*n]
    if min_row_size(blocks) > n:
        return []
    return _constraint_satisfactions_helper(n, blocks, [], [])


def _constraint_satisfactions_helper(n, blocks, temp, result):
    """
    This function is a recursive helper function for the
    constraint_satisfactions() function.
    :param n: the length of a row.
    :param blocks: a list of constraints.
    :param temp: a list with a current pattern that will be checked.
    :param result: all the ways of placing.
    :return: result.
    """
    if len(blocks) == 0 and len(temp) <= n:
        for i in range(n-len(temp)):
            temp.append(WHITE)
        result.append(temp)
        return
    if len(blocks) == 0 or len(temp) > n:
        return
    if temp and temp[len(temp)-1] == BLACK:
        _constraint_satisfactions_helper(n, blocks, temp + [WHITE], result)
    else:
        _constraint_satisfactions_helper(n, blocks[1:], temp + [BLACK] *
                                         blocks[0], result)
        _constraint_satisfactions_helper(n, blocks, temp + [WHITE], result)
    return result


def row_variations(row, blocks):
    """
    This function returns all the possible ways of completing the pattern of
    row (choosing for -1 if it is 1 or 0) so that in a completed row the block
    constraints would be followed.
    :param row: a row with not distributed places (-1) and distributed ones.
    :param blocks: a list of constraints.
    :return: all the possible ways of completion.
    """
    blocks_new = copy.deepcopy(blocks)
    if not blocks_new:
        blocks_new = [0]
    if not row:
        return [[]]
    return _row_variations_helper(row, blocks_new, [], [], 0, 0, 0)


def max_block_cell(row_size, blocks, cur_block_index):
    """
    This function returns the maximal cell index that is possible to fit all
    the blocks starting from the current one in the cells of the row.
    :param row_size: the length of the row.
    :param blocks: a list of constraints.
    :param cur_block_index: a current block index.
    :return: the maximal cell index.
    """
    result = 0
    for i in range(cur_block_index + 1, len(blocks)):
        result += blocks[i]
    spaces = max(len(blocks) - cur_block_index - 2, 0)
    result = row_size - result - spaces - 1
    return result


def min_row_size(blocks):
    """
    This function returns a minimal row size to fit all the constraints with
    spaces between them in the row.
    :param blocks: a list of constraints.
    :return: a minimal row size.
    """
    result = 0
    for block in blocks:
        result += block
    result += len(blocks) - 1  # The number of spaces.
    return result


def _row_variations_helper(row, blocks, temp, result, cell, cur_block_index,
                           units_in_cur_block):
    """
    This function is a recursive helper function for the row_variations()
    function.
    :param row: a row with not distributed places (-1) and distributed ones.
    :param blocks: a list of constraints.
    :param temp: a temporary pattern that will be checked for constraints
    :param result: a list with the all possible ways.
    :param cell: a current index in the row
    :param cur_block_index: a current index in the list of constraints.
    :param units_in_cur_block: a counter for 1 that have already been placed.
    :return: a list of all possible ways (result).
    """
    if len(temp) == len(row):
        result.append(temp)
        return
    if row[cell] == UNKNOWN:
        local_temp_0 = temp[:]
        local_row_0 = copy.deepcopy(row)
        local_row_0[cell] = WHITE
        _row_variations_helper(local_row_0, blocks, local_temp_0, result,
                               cell, cur_block_index, units_in_cur_block)
        local_temp_1 = temp[:]
        local_row_1 = copy.deepcopy(row)
        local_row_1[cell] = BLACK
        _row_variations_helper(local_row_1, blocks, local_temp_1, result,
                               cell, cur_block_index, units_in_cur_block)
    elif row[cell] == WHITE:
        # If index cell in row is bigger than the maximal possible in the
        # current block OR if the number of 1 that have already been placed
        # in the current block is smaller than is in the current block and
        # the current block's index is not 0 (it is not the first block)
        # OR if for the first block (index 0) the cell index is bigger then
        # max_block_cell() and we still have no 1, it's a dead end. Return.
        if (cell > max_block_cell(len(row), blocks, cur_block_index)) or \
                (units_in_cur_block < blocks[cur_block_index] and
                 units_in_cur_block != 0) or \
                (cur_block_index == 0 and cell >
                 max_block_cell(len(row), blocks, cur_block_index) - blocks[0]
                 and units_in_cur_block == 0):
            return
        _row_variations_helper(row, blocks, temp + [WHITE], result, cell + 1,
                               cur_block_index, units_in_cur_block)
    elif row[cell] == BLACK:
        # IF IT IS A NEW BLOCK:
        # If it is a new block that is not the first (index not 0), making the
        # block index bigger by 1.
        if units_in_cur_block != 0 and temp[cell - 1] == WHITE:
            cur_block_index += 1
            # If the new index is bigger than the maximal possible, return.
            if cur_block_index > len(blocks) - 1:
                return
            _row_variations_helper(row, blocks, temp + [1], result, cell + 1,
                                   cur_block_index, 1)
        else:
            # IF IT IS A CONTINUATION OF THE CURRENT BLOCK OR IT IS THE FIRST
            # BLOCK (INDEX 0):
            units_in_cur_block += 1
            # If the number of 1 that have been already placed for this block
            # is bigger than the number of 1 in this block, return.
            if (blocks and units_in_cur_block > blocks[cur_block_index]) or \
                    not blocks and units_in_cur_block > 0:
                return
            _row_variations_helper(row, blocks, temp + [BLACK], result,
                                   cell + 1, cur_block_index,
                                   units_in_cur_block)
    return result


def intersection_row(rows):
    """
    This function receives an array of rows and returns the intersection of
    those rows, that is, one row containing only uniquely filled cells in each
    column (all either 0 or 1). If not all the cells that are in one column
    are 0 or not all are 1, the function writes -1 at this place.
    :param rows: an array of rows of equal length.
    :return: a row with unambiguously filled cells.
    """
    return _intersection_row_helper(rows, 0, [])


def _intersection_row_helper(rows, cell, result):
    """
    This function is a recursive helper function for the intersection_row()
    function.
    :param rows: an array of rows of equal length.
    :param cell: a current column index.
    :param result: a row with unambiguously filled cells.
    :return: result.
    """
    if (rows and len(result) == len(rows[0])) or not rows:
        return result
    temp = rows[0][cell]  # Making a temp the first element in each column.
    for row in range(1, len(rows)):
        if temp != rows[row][cell]:  # Comparing each element in the column
            # with index cell with temp.
            temp = UNKNOWN  # If not equal, then there is no intersection.
            break
    return _intersection_row_helper(rows, cell + 1, result + [temp])


def solve_easy_nonogram(constraints):
    """This function receives a list of constraints that contains blocks for
    rows and blocks for columns and returns a full solution if a nonogram has
    just one. If more then one, the function returns -1 in the places where
    there are multiple possibilities."""
    if not constraints:
        return None
    board = initialize_board(constraints)
    return _solve_easy_nonogram_helper(board, constraints, 1)


def initialize_board(constraints):
    """This function initializes a board based on the quantity of the
    constraints. Each row in the board is an intersection of all
    possibilities for this row based on its length and its constraint. Then
    the function returns the board."""
    board = []
    new_constraints = zero_constraint(constraints)
    for row_constraint in new_constraints[0]:
        board.append(
            intersection_row(constraint_satisfactions(len(new_constraints[1]),
                             row_constraint)))
    return board


def zero_constraint(constraints):
    """This function changes the empty constraints values to zero."""
    new_constraints = copy.deepcopy(constraints)
    while [] in new_constraints[0]:
        new_constraints[0][new_constraints[0].index([])] = [0]
    while [] in new_constraints[1]:
        new_constraints[1][new_constraints[1].index([])] = [0]
    return new_constraints


def rows_to_columns(board):
    """This function transposes a nonogram. It returns a nonogram with its
    rows as columns."""
    board_new = []
    if not board:
        return []  # Checking if the board is empty
    for column in range(0, len(board[0])):
        temp = []
        for line in range(0, len(board)):
            temp.append(board[line][column])
        board_new.append(temp)
    return board_new


def _solve_easy_nonogram_helper(board, constraints, row_or_col):
    """
    This function is a recursive helper function for the
    solve_easy_nonogram function. It transposes a board to check if each row
    matches the columns constraints. If not, it changes each row and checks
    the transposed board again. The function does it until the board in the
    previous loop is equal to the board in the current one, so there are no
    more conclusions left to make.
    :param board: a nonogram that is an intersection of all possibilities.
    :param constraints: a list of blocks for rows and columns.
    :param row_or_col: an indicator if we work with a transposed board or not.
    :return: one solution or an intersection of multiple solutions.
    """
    if [] in board:
        return
    board_columns = rows_to_columns(board)
    resulted_board_columns = []
    for row in range(len(board_columns)):
        all_variations = row_variations(board_columns[row],
                                        constraints[row_or_col][row])
        united_row = intersection_row(all_variations)
        resulted_board_columns.append(united_row)
    if resulted_board_columns == board_columns:
        if row_or_col == 0:
            return resulted_board_columns
        else:
            return rows_to_columns(resulted_board_columns)
    if row_or_col == 1:
        row_or_col = 0
    else:
        row_or_col = 1
    return _solve_easy_nonogram_helper(resulted_board_columns, constraints,
                                       row_or_col)


def solve_nonogram(constraints):
    """This function returns all solutions of a nonogram. If there is one
    solution or no, the function simply returns it before calling the
    recursive helper."""
    if not constraints:
        return None
    new_constraints = zero_constraint(constraints)
    board = solve_easy_nonogram(constraints)
    if board is None:
        return []
    elif checking_one_solution(board):
        return [board]
    else:
        result = _solve_nonogram_helper(board, new_constraints, [], [], 0)
        if not result:
            return None
        else:
            return result


def checking_one_solution(board):
    """This function checks if a board is a solution of a nonogram (if there
    is no -1 in each row)."""
    for row in board:
        if UNKNOWN in row:
            return False
    return True


def constraints_column_check_is_ok(board, constraints, temp):
    """This function checks if a transposed temporary board with all the
    remaining rows added fits in the column constraints. If it is, the
    function returns True. If not, False."""
    temp = temp + board[len(temp):]
    temp = rows_to_columns(temp)
    for column in range(len(temp)):
        all_variations = row_variations(temp[column], constraints[1][column])
        if not all_variations:
            return False
    return True


def _solve_nonogram_helper(board, constraints, result, temp, row):
    """
    This function is a recursive helper function for the solve_nonogram
    function. It changes each row to one of the possibilities for its
    completion and checks if a board now has one solution.
    :param board: an intersection of all solutions.
    :param constraints: a list of blocks for rows and columns.
    :param result: all solutions.
    :param temp: a current board to be transposed and checked.
    :param row: a current row index.
    :return: result.
    """
    if not constraints_column_check_is_ok(board, constraints, temp):
        return
    if len(temp) == len(board):
        print(temp)
        result.append(temp)
        return
    local_temp = copy.deepcopy(temp)
    if UNKNOWN not in board[row]:
        local_temp.append(board[row])
        _solve_nonogram_helper(board, constraints, result, local_temp, row + 1)
    else:
        all_variations = row_variations(board[row], constraints[0][row])
        for variation in all_variations:
            local_temp.append(variation)
            _solve_nonogram_helper(board, constraints, result, local_temp,
                                   row + 1)
            local_temp = local_temp[:len(local_temp) - 1]
    return result
