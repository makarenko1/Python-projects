############################################################################
# FILE: torpedo.py
# EXERCISE: intro2cs1 ex10 2021
# DESCRIPTION: A file with the Torpedo class for the Asteroids game.
############################################################################
import math
RADIUS = 4
START_LIFE = 200


class Torpedo:
    """A class that defines, updates and provides data about torpedoes."""
    def __init__(self, speed_x, speed_y, coordinate_x, coordinate_y, heading):
        """
        This is a constructor that assigns the start parameters to a
        torpedo.
        :param speed_x: the speed of the ship by the x-coordinate
        :param speed_y: the speed of the ship by the y-coordinate
        :param coordinate_x: the x-coordinate of the ship
        :param coordinate_y: the y-coordinate of the ship
        :param heading: the heading angle of the ship
        """
        self.__speed_x = speed_x + 2 * math.cos(math.radians(heading))
        self.__speed_y = speed_y + 2 * math.sin(math.radians(heading))
        self.__coordinate_x = coordinate_x
        self.__coordinate_y = coordinate_y
        self.__heading = heading
        self.__radius = RADIUS
        self.__life = START_LIFE

    def get_radius(self):
        """This function returns a radius of a torpedo."""
        return self.__radius

    def get_x(self):
        """This function returns an x-coordinate of a torpedo."""
        return self.__coordinate_x

    def get_y(self):
        """This function returns an y-coordinate of a torpedo."""
        return self.__coordinate_y

    def get_heading(self):
        """This function returns an angle of movement of a torpedo."""
        return self.__heading

    def get_speed_x(self):
        """This function returns a speed of a torpedo by the x-coordinate."""
        return self.__speed_x

    def get_speed_y(self):
        """This function returns a speed of a torpedo by the y-coordinate."""
        return self.__speed_y

    def set_x(self, x):
        """This function sets a new x-coordinate."""
        self.__coordinate_x = x

    def set_y(self, y):
        """This function sets a new y-coordinate."""
        self.__coordinate_y = y

    def update_life(self):
        """
        This function updates the number of remaining loops to live of the
        torpedo.
        :return: True if number of the remaining number of loops is bigger
        than 0, False otherwise
        """
        if self.__life > 0:
            self.__life -= 1
            return True
        return False
