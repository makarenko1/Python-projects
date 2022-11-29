#############################################################################
# FILE: ex12_utils.py
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A helper file for the Boggle game.
#############################################################################
def load_words_dict(file_path):
    """
    This function loads all the words from the file in the file_path path in a
    dictionary.
    :param file_path: a path to the file
    :return: a dictionary of words
    """
    word_dict = {}
    words_file = open(file_path)
    for word in words_file:
        word = word.replace("\n", "")
        if word not in word_dict and word:
            word_dict[word] = True
    words_file.close()
    return word_dict


def is_valid_path(board, path, words):
    """
    This function receives a path and checks if it is in the borders of board
    and if the path goes only in the legal directions and there are no cells
    that appear more than once and a word is in the words dictionary. If so,
    the function returns a word. Otherwise, None.
    :param board: a list of lists that represents a board
    :param path: a list of tuples with coord_index of the cells
    :param words: a dictionary of words
    :return: word/None
    """
    if not path:
        return
    word = ""
    previous = []
    for coord_index in range(len(path)):
        if not check_board_limits(path[coord_index], board):
            return
        elif coord_index == 0:
            word, previous = update_word_and_previous(
                board, path[coord_index], previous, word)
            continue
        elif check_coordinates(path[coord_index], previous):
            word, previous = update_word_and_previous(
                 board, path[coord_index], previous, word)
        else:
            return
    if word in words:
        return word


def update_word_and_previous(board, coordinates, previous, word):
    """
    This function updates a current word that is collected from the coordinates
    of the path and a list of previous coordinates.
    :param board: a list of lists that represents a board
    :param coordinates: a tuple of current coordinates in the path
    :param previous: a list of previous coordinates
    :param word: a current word from the letters in the previous coordinates
    :return: word and previous
    """
    x, y = coordinates
    word += board[x][y]
    previous.append(coordinates)
    return word, previous


def check_board_limits(coordinates, board):
    """This function checks if the coordinates are in the board limits."""
    x, y = coordinates
    if 0 <= x <= len(board) - 1 and 0 <= y <= len(board[0]) - 1:
        return True
    return False


def check_coordinates(coordinates, previous):
    """
    This function checks if the path goes only in the allowed directions
    and there are no cells that appear more than once. If yes, the function
    returns True. Otherwise, False.
    :param coordinates: a tuple of current coordinates in the path
    :param previous: a list of previous coordinates
    :return: True/False
    """
    x, y = coordinates
    x_prev, y_prev = previous[len(previous) - 1]
    if x_prev - 1 <= x <= x_prev + 1 and y_prev - 1 <= y <= \
            y_prev + 1 and coordinates not in previous:
        return True
    return False


def get_word_by_path(board, path, words):
    """
    This function finds a word by path and checks if it has already been used.
    This is a simplified check path process.
    :param board:  a list of lists that represents a board
    :param path: a list of tuples with coord_index of the cells
    :param words: a dictionary of words
    :return: a word if it is in dictionary and hasn't yet been used.
    Otherwise, False
    """
    word = ""
    for coordinates in path:
        x, y = coordinates
        word += board[x][y]
    if word in words and words[word]:
        return word
    return False


def find_length_n_words(n, board, words):
    """
    This function returns all the words of the length n in the board and a list
    of all coordinates of its letters.
    :param n: a word's length (in letters, not in path)
    :param board: a list of lists that represents a board
    :param words: a dictionary of words
    :return: a list of tuples of word of length n and a path of all its letters
    in the board
    """
    result = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            temp = _find_length_n_words_helper(n, board, row, col, words, "",
                                               [], [])
            for item in temp:
                if item not in result:
                    result.append(item)
    return result


def _find_length_n_words_helper(n, board, x, y, words, word, path, result):
    """This is a recursive helper function for the find_length_n_words
    function."""
    if word in words and len(word) == n and (word, path) not in result:
        result.append((word, path))
    if len(word) > n:
        return
    rows = [row for row in range(x - 1, x + 2) if 0 <= row <= len(board) - 1]
    cols = [col for col in range(y - 1, y + 2) if 0 <= col <= len(board[0]) -
            1]
    for row in rows:
        for col in cols:
            if (row, col) in path:
                continue
            _find_length_n_words_helper(n, board, row, col, words, word +
                                        board[row][col], path + [(row, col)],
                                        result)
    return result
