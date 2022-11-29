############################################################################
# FILE: ship.py
# EXERCISE: intro2cs1 ex10 2021
# DESCRIPTION: A file with the Ship class for the Asteroids game.
############################################################################
import math
START_HEADING = 0
START_SPEED_X = 0
START_SPEED_Y = 0
START_LIFE = 3
RADIUS = 1


class Ship:
    """A class that defines, updates and provides data about a ship."""
    def __init__(self, coordinate_x, coordinate_y):
        """
        This is a constructor that assigns start parameters to a ship
        (start speed, start heading, radius and start life). Also, it
        initializes the coordinates of the ship.
        :param coordinate_x: randomly generated coord x
        :param coordinate_y: randomly generated coord y
        """
        self.__speed_x = START_SPEED_X
        self.__speed_y = START_SPEED_Y
        self.__coordinate_x = coordinate_x
        self.__coordinate_y = coordinate_y
        self.__heading = START_HEADING
        self.__radius = RADIUS
        self.__life = START_LIFE

    def change_heading(self, left_pressed=None):
        """
        This function rotates a ship left if the left key is pressed. Rotates
        right if the right one.
        :param left_pressed: True if left pressed, None otherwise
        """
        if left_pressed:
            self.__heading += 7
        else:
            self.__heading -= 7

    def speed_up(self):
        """This function speeds a ship up."""
        self.__speed_x = self.__speed_x + math.cos(math.radians(
            self.__heading))
        self.__speed_y = self.__speed_y + math.sin(math.radians(
            self.__heading))

    def get_radius(self):
        """This function returns a radius of a ship."""
        return self.__radius

    def get_x(self):
        """This function returns an x-coordinate of a ship."""
        return self.__coordinate_x

    def get_y(self):
        """This function returns an y-coordinate of a ship."""
        return self.__coordinate_y

    def get_heading(self):
        """This function returns an angle of movement of a ship."""
        return self.__heading

    def get_speed_x(self):
        """This function returns a speed of a ship by the x-coordinate."""
        return self.__speed_x

    def get_speed_y(self):
        """This function returns a speed of a ship by the y-coordinate."""
        return self.__speed_y

    def get_life(self):
        """This function returns the remaining amount of life."""
        return self.__life

    def set_life(self, life):
        """This function updates the life of a ship."""
        self.__life += life

    def set_x(self, x):
        """This function sets a new x-coordinate."""
        self.__coordinate_x = x

    def set_y(self, y):
        """This function sets a new y-coordinate."""
        self.__coordinate_y = y

