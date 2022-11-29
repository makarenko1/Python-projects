#############################################################################
# FILE: model.py
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A helper file for the Boggle game (logical part).
#############################################################################
import ex12_utils as utils
import boggle_board_randomizer as randomizer
INITIAL_SCORE = 0


class BoggleModel:
    def __init__(self, filepath):
        """This is a constructor of the Model class that contains all the game
        logic.
        Stored values:
        1. A game board that is created by randomizer;
        2. A dictionary of all words;
        3. A recent guessed words;
        4. A current game score."""
        self.__board = randomizer.randomize_board()
        self.__words = utils.load_words_dict(filepath)
        self.__previous_guessed = None
        self.__score = INITIAL_SCORE

    @staticmethod
    def check_legal_move(path, coordinates):
        """
        This function checks whether a user is trying to make a legal move.
        :param path: a current path
        :param coordinates: the coordinates on the board where the user clicked
        :return: True if a move is valid, False otherwise
        """
        if not path or utils.check_coordinates(coordinates, path):
            return True
        return False

    def get_and_check_word(self, path):
        """
        This function collects the word by its path and if the word hadn't
        been guessed in the past, updates the previous guessed word and the
        game score.
        :param path: the word's path
        :return: True if the word had not been guessed, False otherwise
        """
        if path:
            word = utils.get_word_by_path(self.__board, path, self.__words)
            if word:
                self.__previous_guessed = word
                self.__words[word] = False
                self._update_score(len(word))
                return True
        return False

    def _update_score(self, n):
        """
        This function calculates game score. Game score is calculated by the
        word's length and not by the length of its path. The score for each
        word is its length squared.
        :param n: word's length
        :return: None
        """
        self.__score += n**2

    def get_score(self):
        """This function returns the current game score."""
        return self.__score

    def get_previous_guessed(self):
        """This function returns the most recent guessed word."""
        return self.__previous_guessed

    def get_board(self):
        """This function returns the game board created by randomize_board."""
        return self.__board
