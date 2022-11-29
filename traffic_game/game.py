from board import Board
from car import Car
from helper import *
import sys

ENTER_CHOICE_MESSAGE = "Please enter <car_name,movekey>: "
INPUT_LENGTH = 3
POSSIBLE_NAMES = {'Y', 'B', 'O', 'G', 'W', 'R'}
POSSIBLE_LENGTH = {2, 3, 4}
POSSIBLE_ORIENTATION = {0, 1}
POSSIBLE_MOVEKEYS = {'u', 'd', 'l', 'r'}
ERROR_MESSAGE = "Something went wrong!"
GAME_STOP_SIGN = '!'


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code here (and then delete the next line - 'pass')
        pass

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while self.__board.cell_content(self.__board.target_location()) is \
                None:
            print(self.__board)
            user_input = input(ENTER_CHOICE_MESSAGE)
            if user_input == '!':
                break
            while len(user_input) != INPUT_LENGTH or user_input[0] not in \
                    POSSIBLE_NAMES or user_input[1] != ',' or user_input[2] \
                    not in POSSIBLE_MOVEKEYS:
                print(ERROR_MESSAGE)
                user_input = input(ENTER_CHOICE_MESSAGE)
            if not self.__board.move_car(user_input[0], user_input[2]):
                print(ERROR_MESSAGE)


if __name__ == "__main__":
    board = Board()
    for car_name, parameters in load_json(sys.argv[1]).items():
        if car_name not in POSSIBLE_NAMES or parameters[0] not in \
                POSSIBLE_LENGTH or parameters[2] not in POSSIBLE_ORIENTATION:
            print(ERROR_MESSAGE)
            break
        car = Car(car_name, parameters[0], tuple(parameters[1]), parameters[2])
        if not board.add_car(car):
            print(ERROR_MESSAGE)
            break
    game = Game(board)
    game.play()
