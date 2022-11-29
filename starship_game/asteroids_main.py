############################################################################
# FILE: asteroids_main.py
# EXERCISE: intro2cs1 ex10 2021
# DESCRIPTION: A simple program that resembles the Asteroids game.
############################################################################
from screen import Screen
import sys
from asteroid import Asteroid
from torpedo import Torpedo
from ship import Ship
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
START_SCORE = 0
LEFT_PRESSED = 1
MINIMAL_SPEED = -4
MAXIMAL_SPEED = 4
LIFE_LOSS = -1
SCORE = {1: 100, 2: 50, 3: 20}
TORPEDOES_MAX_NUMBER = 10
# Messages to the user
COLLISION = ("COLLISION", "BEWARE OF THE ASTEROIDS")
VICTORY = ("VICTORY", "YOU'VE WON")
LOSE = ("LOSE", "YOU'VE LOST")
EXIT = ("EXIT", "WAITING FOR YOUR RETURN")


class GameRunner:

    def __init__(self, asteroids_amount):
        """
        This is a constructor of game object and its attributes (the graphics
        (screen) and game elements (ship, asteroids, torpedoes)).
        :param asteroids_amount: the number of asteroids in the game
        """
        self.__screen = Screen()
        # Borders initialization
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        # Ship initialization
        ship_coord_x, ship_coord_y = self._generate_random_coord()
        self.__ship = Ship(ship_coord_x, ship_coord_y)
        # Asteroids initialization
        self.__asteroids = []
        self._asteroids_initialization(asteroids_amount)
        # Torpedoes initialization
        self.__torpedoes = []
        # Score initialization
        self.__score = START_SCORE

    def _generate_random_coord(self):
        """
        This function calculates coordinates x,y randomly within the screen
        borders.
        :return: x, y
        """
        coord_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        coord_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return coord_x, coord_y

    def _asteroids_initialization(self, asteroids_amount):
        """
        This function initializes all asteroids in the game. If there is a
        collision between any asteroid and a ship, this asteroid is
        re-initialized.
        :param asteroids_amount: the number of asteroids in the game
        :return: None
        """
        speed_choices = [num for num in range(MINIMAL_SPEED, MAXIMAL_SPEED + 1)
                         if num != 0]
        asteroid_counter = 0
        while asteroid_counter < asteroids_amount:
            asteroid_coord_x, asteroid_coord_y = self._generate_random_coord()
            asteroid_speed_x = random.choice(speed_choices)
            asteroid_speed_y = random.choice(speed_choices)
            asteroid = Asteroid(asteroid_coord_x, asteroid_coord_y,
                                asteroid_speed_x, asteroid_speed_y)
            # Check for collision
            if asteroid.has_intersection(self.__ship):
                continue  # If collision, skip this configuration
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
            self.__asteroids.append(asteroid)
            asteroid_counter += 1

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        This function is a main function of the game. First it checks if the
        game can be finished. If yes, exit. If no, move all the objects with
        the start_ functions and then make changes from the keyboard. In the
        end of one loop update the torpedoes' lives.
        :return: None
        """
        if self._is_end():
            self.__screen.end_game()
            sys.exit()
        self._start_loop_asteroid()
        if self.__torpedoes:
            self._start_loop_torpedo()
        ship_coord_x, ship_coord_y, ship_heading = self._start_loop_ship()
        self._asteroid_interaction()
        if self.__torpedoes:
            self._update_torpedoes_life()
        self._keyboard_change(ship_coord_x, ship_coord_y, ship_heading)

    def _keyboard_change(self, ship_coord_x, ship_coord_y, ship_heading):
        """
        This function reads keyboard input and makes the corresponding changes.
        1. If left is pressed the ship turns left
        2. If right, turns right
        3. If up is pressed, the ship is accelerates
        4. If a space is pressed, a torpedo is created
        :param ship_coord_x: coordinate x of the ship
        :param ship_coord_y: coordinate y of the ship
        :param ship_heading: angle of movement of the ship
        :return: None
        """
        if self.__screen.is_left_pressed():
            self.__ship.change_heading(LEFT_PRESSED)
        if self.__screen.is_right_pressed():
            self.__ship.change_heading()
        if self.__screen.is_up_pressed():
            self.__ship.speed_up()
        if self.__screen.is_space_pressed() and \
                (not self.__torpedoes or len(self.__torpedoes) <
                 TORPEDOES_MAX_NUMBER):
            self._create_torpedo(ship_coord_x, ship_coord_y, ship_heading)

    def _start_loop_ship(self):
        """
        Drawing and moving ship at the start of each loop.
        :return: x, y, angle of ship for a subsequent creation of a torpedo
        """
        coord_x = self.__ship.get_x()
        coord_y = self.__ship.get_y()
        heading = self.__ship.get_heading()
        self.__screen.draw_ship(coord_x, coord_y, heading)
        self._move(self.__ship)
        return coord_x, coord_y, heading

    def _start_loop_torpedo(self):
        """
        Drawing and moving torpedoes at the start of each loop.
        :return: None
        """
        for torpedo in self.__torpedoes:
            coord_x = torpedo.get_x()
            coord_y = torpedo.get_y()
            heading = torpedo.get_heading()
            self.__screen.draw_torpedo(torpedo, coord_x, coord_y, heading)
            self._move(torpedo)

    def _start_loop_asteroid(self):
        """
        Drawing and moving asteroids at the start of each loop.
        :return: None
        """
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_x(),
                                        asteroid.get_y())
            self._move(asteroid)

    def _create_torpedo(self, ship_coord_x, ship_coord_y, ship_heading):
        """
        This function creates a Torpedo object, registers it and draws it.
        :param ship_coord_x: coordinate x of the ship
        :param ship_coord_y: coordinate y of the ship
        :param ship_heading: angle of movement of the ship
        :return: None
        """
        torpedo = Torpedo(self.__ship.get_speed_x(), self.__ship.get_speed_y(),
                          ship_coord_x, ship_coord_y, ship_heading)
        self.__screen.register_torpedo(torpedo)
        self.__torpedoes.append(torpedo)
        self.__screen.draw_torpedo(torpedo, ship_coord_x, ship_coord_y,
                                   ship_heading)

    def _update_torpedoes_life(self):
        """
        This function updates torpedoes' time to live after each loop.
        :return: None
        """
        for torpedo in self.__torpedoes:
            if not torpedo.update_life():
                self._delete_torpedo(torpedo)

    def _asteroid_interaction(self):
        """
        This function checks if there is any interaction (intersection)
        with the ship or with the torpedoes.
        :return: None
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self._intersection_with_ship(asteroid)
                return
            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self._intersection_with_torpedo(asteroid, torpedo)

    def _intersection_with_torpedo(self, asteroid, torpedo):
        """
        This function updates score and breaks an asteroid into smaller
        asteroid(s) if there was collision.
        :param asteroid: an object of class Asteroid
        :param torpedo: an object of class Torpedo
        :return: None
        """
        self._update_score(asteroid)
        new_asteroid_speed_x = (torpedo.get_speed_x() +
                                asteroid.get_speed_x()) / math.sqrt(
                                    asteroid.get_speed_x() ** 2 +
                                    asteroid.get_speed_y() ** 2)
        new_asteroid_speed_y = (torpedo.get_speed_y() +
                                asteroid.get_speed_y()) / math.sqrt(
                                    asteroid.get_speed_x() ** 2 +
                                    asteroid.get_speed_y() ** 2)
        coord_x = asteroid.get_x()
        coord_y = asteroid.get_y()
        size = asteroid.get_size() - 1
        self._create_new_asteroids(coord_x, coord_y, new_asteroid_speed_x,
                                   new_asteroid_speed_y, size)
        self._delete_torpedo(torpedo)
        self._delete_asteroid(asteroid)

    def _intersection_with_ship(self, asteroid):
        """
        This function takes life from a ship, shows a message and deletes the
        asteroid which collided with the ship.
        :param asteroid: an object of class Asteroid
        :return: None
        """
        self.__ship.set_life(LIFE_LOSS)
        self.__screen.show_message(*COLLISION)
        self.__screen.remove_life()
        self._delete_asteroid(asteroid)

    def _update_score(self, asteroid):
        """
        This function updates the user's score.
        :param asteroid: an object of class Asteroid that was broken
        :return: None
        """
        size = asteroid.get_size()
        self.__score += SCORE[size]
        self.__screen.set_score(self.__score)

    def _create_new_asteroids(self, x, y, speed_x, speed_y, size):
        """
        This function creates new asteroids that are the pieces of a broken
        one.
        :param x: coordinate x of the old asteroid
        :param y: coordinate y of the old asteroid
        :param speed_x: speed x of the old asteroid
        :param speed_y: speed y of the old asteroid
        :param size: size - 1 of the old asteroid
        :return: None
        """
        for index in range(1, size + 1):
            speed_x = speed_x * (-1) ** index
            speed_y = speed_y * (-1) ** (index + 1)
            new_asteroid = Asteroid(x, y, speed_x, speed_y, size)
            self.__screen.register_asteroid(new_asteroid, size)
            self.__asteroids.append(new_asteroid)

    def _delete_torpedo(self, torpedo):
        """
        This function removes a torpedo from the game.
        :param torpedo: an object of class Torpedo
        :return: None
        """
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes.remove(torpedo)

    def _delete_asteroid(self, asteroid):
        """
        This function removes an asteroid from the game.
        :param asteroid: an object of class Asteroid
        :return: None
        """
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def _move(self, other):
        """
        This function moves all kinds of objects.
        :param other: an object that can be moved
        :return: None
        """
        coord_x = self.__screen_min_x + (other.get_x() + other.get_speed_x()
                                         - self.__screen_min_x) % (
                self.__screen_max_x - self.__screen_min_x)
        coord_y = self.__screen_min_y + (other.get_y() + other.get_speed_y()
                                         - self.__screen_min_y) % (
                self.__screen_max_y - self.__screen_min_y)
        other.set_x(coord_x)
        other.set_y(coord_y)

    def _is_end(self):
        """
        This function checks if the game could be ended.
        :return: True if it could be, False if it couldn't be
        """
        if not self.__asteroids:  # When there are no asteroids left
            self.__screen.show_message(*VICTORY)
            return True
        if not self.__ship.get_life():  # When there is no ship lives left
            self.__screen.show_message(*LOSE)
            return True
        if self.__screen.should_end():  # When the user pressed "q"
            self.__screen.show_message(*EXIT)
            return True
        return False


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            main(int(sys.argv[1]))
        except ValueError:
            print("Illegal parameter!")
    else:
        main(DEFAULT_ASTEROIDS_NUM)
