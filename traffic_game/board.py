SIZE = 7
FINISH = (3, 7)


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        self.__cars_on_board = dict()

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        result = ""
        for row in range(SIZE):
            for col in range(SIZE + 1):
                if col == SIZE and (row, col) != FINISH:
                    result += "#"
                else:
                    car_name = self.cell_content((row, col))
                    if car_name is None:
                        if (row, col) == FINISH:
                            result += "E"
                        else:
                            result += "_"
                    else:
                        result += car_name
            result += "\n"
        return result

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        result = list()
        for row in range(SIZE):
            for col in range(SIZE):
                result.append((row, col))
        result.append(FINISH)
        return result

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        result = list()
        for car_name in self.__cars_on_board:
            car_possible_moves = self.__cars_on_board[car_name].possible_moves()
            for movekey, description in car_possible_moves.items():
                for coordinate in self.__cars_on_board[
                        car_name].movement_requirements(movekey):
                    if coordinate in self.cell_list() and \
                            self.cell_content(coordinate) is None:
                        result.append((car_name, movekey, description))
        return result

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return FINISH

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for car_name in self.__cars_on_board:
            car_coordinates = self.__cars_on_board[car_name].car_coordinates()
            if coordinate in car_coordinates:
                return car_name
        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_name = car.get_name()
        if car_name in self.__cars_on_board:
            return False
        for car_coordinate in car.car_coordinates():
            if car_coordinate not in self.cell_list() or \
                    self.cell_content(car_coordinate) is not None:
                return False
        self.__cars_on_board[car_name] = car
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars_on_board or movekey not in \
                self.__cars_on_board[name].possible_moves():
            return False
        for coordinate in self.__cars_on_board[name].movement_requirements(
                movekey):
            if coordinate not in self.cell_list() or \
                    self.cell_content(coordinate) is not None:
                return False
        if not self.__cars_on_board[name].move(movekey):
            return False
        return True
