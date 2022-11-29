#############################################################################
# FILE: wordsearch.py
# WRITER: Mariia Makarenko, makarenko, 342849676
# EXERCISE: intro2cs1 ex5 2020
# DESCRIPTION: A simple program that searches for the words in the matrix of
# letters
# STUDENTS I DISCUSSED THE EXERCISE WITH: Konstantin Perstin, rerstin127
# WEB PAGES I USED: docs.python.org/3/library/os.path.html
# stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-
# lowercasing-the-result
# NOTES: ...
#############################################################################
import sys
import copy
import os.path


def read_wordlist(filename):
    """
    Loads a list of words from a file
    :param filename: The file of words
    :return: A list containing all the words from the file
    """
    words = []
    file_words = open(filename)
    for line in file_words:
        words.append(line.strip())
    file_words.close()
    return words


def read_matrix(filename):
    """
    Loads a list of lists of letters (matrix) from a file
    :param filename: The file with matrix
    :return: A list containing lists (each list is a string)
    """
    matrix = []
    file_matrix = open(filename)
    for line in file_matrix:
        word = []
        for letter in line:
            if letter != "," and letter != "\n":
                word.append(letter)
        matrix.append(word)
    file_matrix.close()
    return matrix


def form_word_from_row(candidate, letter, row, matrix_new,
                       word_list, words):
    """
    This function checks for each letter if it in combination with all other
    letters in the column are in words_list
    :param candidate: A string that contains letters
    :param letter: A letter starting from which all letters are added to the
    candidate
    :param row: A row that is currently being checked
    :param matrix_new: A changed matrix regarding the directions
    :param word_list: A list of all words from a file
    :param words: A dictionary with the words found in the direction and
    counters that are their quantity
    :return: words
    """
    new_candidate = candidate
    for next_letter in range(letter + 1, len(matrix_new[row])):
        new_candidate += matrix_new[row][next_letter]
        if len(new_candidate) > 20:
            break
        words = search(new_candidate, word_list, words)
    return words


def search(new_candidate, word_list, words):
    """
    This function checks if the candidate is in word_list and if it is,
    updates the counter. If it isn't, adds it with counter 1
    :param new_candidate: A word that is currently being checked
    :param word_list: A list of all words from a file
    :param words: A dictionary with all results of the checks
    :return: words
    """
    if new_candidate in word_list:
        if new_candidate in words:
            counter = words[new_candidate]
            for word in words.keys():
                if word == new_candidate:
                    words[new_candidate] = counter + 1
        else:
            words[new_candidate] = 1
    return words


def check_direction(word_list, matrix_new):
    """
    This function chooses a row and a candidate from it for further check
    process
    :param word_list: A list of all words from a file
    :param matrix_new: A changed matrix regarding the directions
    :return: A dictionary with the words found in the direction and counters
    that are their quantity
    """
    words = {}
    for row in range(0, len(matrix_new)):  # Rows
        for letter in range(0, len(matrix_new[row])):  # Columns
            candidate = matrix_new[row][letter]
            words = form_word_from_row(candidate, letter,
                                       row, matrix_new,
                                       word_list, words)
            words = one_letter_candidate(candidate, word_list, words)
    return words


def one_letter_candidate(candidate, word_list, words):
    """This function checks if one-letter words are in words_list"""
    if len(candidate) == 1:  # Check for one letter candidates
        if candidate in word_list and candidate not in words:
            words[candidate] = 1
        elif candidate in word_list and candidate in words:
            words = search(candidate, word_list, words)
    return words


def update_column(matrix):
    """
    This function returns a matrix where all rows of the given matrix
    are columns of the new matrix
    :param matrix: A given matrix
    :return: A changed matrix regarding the directions
    """
    matrix_new = []
    if not matrix:
        return []
    for column in range(0, len(matrix[0])):
        word = []
        for line in range(0, len(matrix)):
            word.append(matrix[line][column])
        matrix_new.append(word)
    return matrix_new


def update_diagonal(matrix):
    """
    This function returns a matrix where all diagonals of the given matrix are
    rows of the new matrix
    :param matrix: A given matrix
    :return: A changed matrix regarding the directions
    """
    matrix_new = []
    if not matrix:
        return []
    for row in range(0, len(matrix)+len(matrix[0])-1):
        matrix_new.append([])
    for col in range(0, len(matrix[0])):
        for row in range(0, len(matrix)):
            matrix_new[col+row].append(matrix[row][col])
    return matrix_new


def do_reverse_matrix(matrix):
    """
    This function returns a matrix with elements in rows
    :param matrix: A given matrix
    :return: A reversed matrix
    """
    reversed_matrix = []
    for row in matrix:
        reversed_matrix.append(row[::-1])
    return reversed_matrix


def sort_alphabet(dict_words):
    """
    This function sorts the results in alphabetical order
    :param dict_words: A list of results converted to dictionary
    :return: dict_words sorted in alphabetical order
    """
    alphabet_words = {}
    dict_words_keys = sorted(list(dict_words.keys()), key=str.lower)
    for key in dict_words_keys:
        alphabet_words[key] = dict_words[key]
    return alphabet_words


def final_edit(words):
    """
    This function deletes duplications in the final result
    :param words: Results for all the checks
    :return: words (list of tuples)
    """
    dict_words = {}
    for pair in words:
        if pair[0] in dict_words.keys():
            dict_words[pair[0]] += pair[1]
        else:
            dict_words[pair[0]] = pair[1]
    dict_words = sort_alphabet(dict_words)
    return dict_to_tuple(dict_words)


def dict_to_list(words):
    """This function converts dictionary to list"""
    words_list = []
    for word, counter in words.items():
        parameter = [word, counter]
        words_list.append(parameter)
    return words_list


def dict_to_tuple(words):
    """This function creates a list of tuples from a dictionary"""
    tuple_list = []
    for word, counter in words.items():
        tuple_list.append(tuple([word, counter]))
    return tuple_list


def find_words(word_list, matrix, directions):
    """
    This function runs through the matrix for words in the given directions
    :param word_list: A list of all words from a file
    :param matrix: A matrix given by user
    :param directions: Search directions given by user
    :return: Results for checks in all directions that are given in a list
    """
    words = []
    matrix_new = copy.deepcopy(matrix[::-1])
    if "u" in directions:
        words += dict_to_list(check_direction(word_list,
                                              update_column(matrix_new)))
    if "d" in directions:
        words += dict_to_list(check_direction(word_list,
                                              update_column(matrix)))
    if "r" in directions:
        words += dict_to_list(check_direction(word_list, matrix))
    if "l" in directions:
        words += dict_to_list(check_direction(word_list,
                              do_reverse_matrix(matrix)))
    if "w" in directions:
        words += dict_to_list(check_direction(word_list,
                                              update_diagonal(matrix)))
    if "x" in directions:
        words += dict_to_list(check_direction(word_list,
                                              do_reverse_matrix(update_diagonal
                                                                (matrix_new))))
    if "y" in directions:
        words += dict_to_list(check_direction(word_list,
                                              update_diagonal(matrix_new)))
    if "z" in directions:
        words += dict_to_list(check_direction(word_list,
                                              do_reverse_matrix(update_diagonal
                                                                (matrix))))
    words = final_edit(words)
    return words


def write_output(results, filename):
    """
    This function writes all the search results to the file with the name given
    by user
    :param results: All the search results from the find_words
    :param filename: The name of the file given by user
    """
    result_file = open(filename, 'w')
    for pair in results:
        result_file.write(str(pair[0]) + ',' + str(pair[1]) + '\n')
    result_file.close()


def main():
    """This function receives input from the command line. Then it checks the
    input, does the check in the given directions and creates a file with
    all the results of the check"""
    if len(sys.argv) != 5:  # Error if not exactly four arguments are given
        print("Check the quantity of the given arguments!")
        return
    words_filename = sys.argv[1]
    matrix_filename = sys.argv[2]
    if not os.path.isfile(words_filename) or not \
            os.path.isfile(matrix_filename):  # Error if the files don't exist
        print(f"{words_filename} does not exist!")
        return
    results_filename = sys.argv[3]
    directions = set(sys.argv[4])  # Deleting repetitions
    for direction in directions:
        if direction not in "udrlwxyz":  # Error if there is unknown directions
            print("Invalid direction!")
            return
    word_list = read_wordlist(words_filename)
    matrix = read_matrix(matrix_filename)
    if word_list == [] or matrix == []:
        write_output([], results_filename)
        return
    results = find_words(word_list, matrix, directions)
    write_output(results, results_filename)


if __name__ == "__main__":
    main()
