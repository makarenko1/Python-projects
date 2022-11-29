############################################################################
# FILE: asteroid.py
# EXERCISE: intro2cs1 ex10 2021
# DESCRIPTION: A file with the Asteroid class for the Asteroids game.
############################################################################
import math
START_SIZE = 3


class Asteroid:
    """A class that defines, updates and provides data about asteroids."""
    def __init__(self, coordinate_x, coordinate_y, speed_x, speed_y,
                 size=START_SIZE):
        """
        This is a constructor which gives an asteroid coordinates, start speed
        and size. An asteroid can be initialized either when a big one is
        broken or at the start of the game.
        :param coordinate_x: coordinate x of the start position
        :param coordinate_y: coordinate y of the start position
        :param speed_x: start speed by the x coordinate
        :param speed_y: start speed by th y coordinate
        :param size: size (at the start is 3)
        """
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__coordinate_x = coordinate_x
        self.__coordinate_y = coordinate_y
        self.__size = size

    def has_intersection(self, obj):
        """
        This function checks if an asteroid has an intersection with
        another object.
        :param obj: another object that an asteroid can collide with
        :return: True if there is an intersection, False if there isn't
        """
        distance = math.sqrt((obj.get_x() - self.__coordinate_x)**2 +
                             (obj.get_y() - self.__coordinate_y)**2)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False

    def get_size(self):
        """This function returns a size of an asteroid."""
        return self.__size

    def get_radius(self):
        """This function returns a radius of an asteroid."""
        return self.__size * 10 - 5

    def get_x(self):
        """This function returns an x-coordinate of an asteroid."""
        return self.__coordinate_x

    def get_y(self):
        """This function returns an y-coordinate of an asteroid."""
        return self.__coordinate_y

    def get_speed_x(self):
        """This function returns a speed of an asteroid by the x-coordinate."""
        return self.__speed_x

    def get_speed_y(self):
        """This function returns a speed of an asteroid by the y-coordinate."""
        return self.__speed_y

    def set_x(self, x):
        """This function sets a new x-coordinate."""
        self.__coordinate_x = x

    def set_y(self, y):
        """This function sets a new y-coordinate."""
        self.__coordinate_y = y
