POSSIBLE_MOVES = {0: {'u': "Move up", 'd': "Move down"},
                  1: {'l': "Move left", 'r': "Move right"}}
# Can be changed if the car needs to move some number of steps at once in some
# direction:
DIRECTION_TO_DELTA = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
UP_MOVE = 'u'
DOWN_MOVE = 'd'
LEFT_MOVE = 'l'
RIGHT_MOVE = 'r'


class Car:
    """
    Add class description here
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        result = list()
        for i in range(self.__length):
            if not self.__orientation:  # if orientation is vertical.
                result.append((self.__location[0] + i, self.__location[1]))
            else:
                result.append((self.__location[0], self.__location[1] + i))
        return result

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        return POSSIBLE_MOVES[self.__orientation]

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
        move to be legal.
        """
        if movekey not in self.possible_moves():
            return list()
        result = list()
        row, col = self.__location
        if movekey == UP_MOVE:
            result.append((row - 1, col))
        elif movekey == DOWN_MOVE:
            result.append((row + self.__length + 1, col))
        elif movekey == LEFT_MOVE:
            result.append((row, col - 1))
        else:
            result.append((row, col + self.__length + 1))
        return result

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False
        delta_row, delta_col = DIRECTION_TO_DELTA[movekey]
        self.__location = (self.__location[0] + delta_row,
                           self.__location[1] + delta_col)
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
