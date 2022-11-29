#############################################################################
# FILE: boggle.py
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: The main file for the Boggle game.
#############################################################################
import sys
import os.path
from view import BoggleView
from model import BoggleModel
INITIAL_TIME = 180


class BoggleController:
    def __init__(self, file):
        """
        This function is a constructor for the BoggleController class.
        Stored values:
        1. A filepath to the words dictionary file;
        2. An object of class BoggleModel (logical part of the game);
        3. An object of class BoggleView (visual part of the game);
        4. Board labels with letters;
        5. The current path.
        :param file: a filepath to the words dictionary file
        """
        self.__filepath = file
        self.__model = BoggleModel(file)
        self.__gui = BoggleView(INITIAL_TIME, self._labels_action,
                                self._submit_word, self._time_over)
        self._create_labels_and_path()

    def _create_labels_and_path(self):
        """
        This function iterates over the game board that it gets from the
        logical part and creates board labels in the visual part and adds
        them as the values in the class variable __labels that is a
        dictionary with keys that are the labels' coordinates and values that
        are the labels (tkinter objects).
        :return: None
        """
        self.__path = []
        board = self.__model.get_board()
        self.__labels = {}
        for row in range(len(board)):
            for col in range(len(board[row])):
                label = self.__gui.make_letter_cell(row, col,
                                                    board[row][col])
                self.__labels[(row, col)] = label

    def _labels_action(self, event):
        """
        This function is an event handler for the label clicks. It checks if
        the user did a legal move in the game. If yes, the current path is
        updated with the label's coordinates, in the visual part the word is
        updated and the label that was clicked is animated.
        :param event: an event object
        :return: None
        """
        for coordinates, label in self.__labels.items():
            if label is event.widget:
                if self.__model.check_legal_move(self.__path, coordinates):
                    # Updating path
                    self.__path.append(coordinates)
                    # Updating word
                    self.__gui.set_word(event.widget["text"])
                    # Animate cell
                    self.__gui.animate_cell(event.widget)

    def _submit_word(self):
        """
        This function is called when the user submits a word. The model checks
        if everything is correct and in the visual part the new score is set
        and the guessed words are updated. Anyway, the board gets cleared in
        the visual part and the current path is cleared in the controller.
        :return: None
        """
        if self.__model.get_and_check_word(self.__path):
            score = self.__model.get_score()
            word = self.__model.get_previous_guessed()
            self.__gui.set_all_words_and_score(word, score)
        self.__path = []
        self.__gui.clear_board()

    def _time_over(self):
        """
        This function is called when the time is over. The visual part asks
        the user is they want to continue. If yes, a new BoggleModel object is
        created and the visual part starts a new round. In the controller new
        board labels are created. Otherwise, the program shuts itself down.
        :return: None
        """
        answer = self.__gui.ask_question()
        if answer == "yes":
            self.__model = BoggleModel(self.__filepath)
            self.__gui.new_round(INITIAL_TIME)
            self._create_labels_and_path()
        else:
            self.__gui.exit()
            sys.exit()

    def run(self):
        """
        This function starts the mainloop in the visual part.
        :return: None
        """
        self.__gui.run()


if __name__ == "__main__":
    # The user can give their own word dictionary file via the command line.
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "boggle_dict.txt"
    if os.path.isfile(filepath):
        game = BoggleController(filepath)
        game.run()
