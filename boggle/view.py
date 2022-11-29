#############################################################################
# FILE: view.py
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A helper file for the Boggle game (visual part).
#############################################################################
import tkinter as tk
import tkinter.messagebox
WINDOW_TITLE = "BOGGLE GAME"
LABELS_FONT = ("Helvetica", 15)
ALL_WORDS_FONT = ("Helvetica", 12)
OUTER_FRAME_STYLE = {"highlightbackground": "light salmon",
                     "highlightthickness": 5}
PACK_STYLE = {"fill": tk.BOTH, "expand": True}
DEFAULT_COLOR = "lemon chiffon"
ACTIVE_COLOR = "LightGoldenrod1"
MOUSE_ON_COLOR = "LemonChiffon2"
MOUSE_ON_ACTIVE_COLOR = "light goldenrod"
MAIN_EL_COLOR = "coral"
BUTTONS_ACTIVE = "tomato"
SCORE_TEXT = "SCORE: "
TIME_TEXT = "TIME: "
START_CELL_STYLE = {"fg": DEFAULT_COLOR, "bg": DEFAULT_COLOR,
                    "font": ("Helvetica", 20), "width": 6, "height": 3}
DEFAULT_CELL_CONFIG = {"fg": "black", "bg": DEFAULT_COLOR}
ACTIVE_CELL_CONFIG = {"bg": ACTIVE_COLOR}
MOUSE_ON_CELL_CONFIG = {"bg": MOUSE_ON_COLOR}
MOUSE_ON_ACTIVE_CELL_CONFIG = {"bg": MOUSE_ON_ACTIVE_COLOR}
QUESTION = ("GAME OVER", "PLAY AGAIN?")


class BoggleView:
    def __init__(self, time, board_command, enter_command, time_over_command):
        """
        This is a constructor for the BoggleView class.
        Stored values:
        1. The main window of the game;
        2. A command for the click on the board labels;
        3. A command for the enter button;
        4. A command for the case when the game time is over;
        5. All interface that is created and interface class variables.
        :param time: initial game time
        :param board_command: a controller function that runs when a label on
        the board is pressed
        :param command_enter: a controller function that runs when the enter
        button is pressed
        :param time_over_command: a controller function that runs when the
        game time is over.
        """
        root = tk.Tk()
        self.__main_window = self._design_root(root)
        self.__board_command = board_command
        self.__command_enter = enter_command
        self.__time_over_command = time_over_command
        self._create_interface(time)

    @staticmethod
    def _design_root(root):
        """
        This function adds a title to the root and makes it non-resizable.
        :param root: the main window of the game
        :return: root
        """
        root.title(WINDOW_TITLE)
        root.resizable(False, False)
        return root

    def _create_interface(self, time):
        """
        This function creates class vars that store game parameters and creates
        the interface.
        :return: None
        """
        self.__path = []
        self.__board = []
        self.__time = time
        self._create_frames()
        self._create_vars_and_buttons()
        self._create_labels()
        self._pack()

    def _create_frames(self):
        """
        This function divides the main window into parts by frames.
        :return: None
        """
        self.__outer_frame = tk.Frame(self.__main_window, **OUTER_FRAME_STYLE)
        self.__left_frame = tk.Frame(self.__outer_frame)
        self.__right_frame = tk.Frame(self.__outer_frame)
        self.__time_and_score_frame = tk.Frame(self.__left_frame)
        self.__board_frame = tk.Frame(self.__left_frame, bg=MOUSE_ON_COLOR)

    def _create_vars_and_buttons(self):
        """
        This function creates textvariables and buttons in the interface.
        :return: None
        """
        self.__time_display = tk.StringVar(
            value=TIME_TEXT + self._time_configure())
        self.__score_display = tk.StringVar(value=SCORE_TEXT + "0")
        self.__word_display = tk.StringVar(value="")
        self.__all_words_display = tk.StringVar(value="ALL WORDS:\n")
        self.__start_enter_button = tk.Button(self.__outer_frame, text="START",
                                              bg=MAIN_EL_COLOR,
                                              activebackground=BUTTONS_ACTIVE,
                                              command=self._start_game,
                                              font=LABELS_FONT)

    def _create_labels(self):
        """
        This function creates text fields in the interface.
        :return: None
        """
        self.__time_label = tk.Label(self.__time_and_score_frame,
                                     textvariable=self.__time_display,
                                     font=LABELS_FONT, bg=MAIN_EL_COLOR)
        self.__score_label = tk.Label(self.__time_and_score_frame,
                                      bg=MAIN_EL_COLOR, font=LABELS_FONT,
                                      textvariable=self.__score_display)
        self.__word_label = tk.Label(self.__left_frame, bg=MAIN_EL_COLOR,
                                     textvariable=self.__word_display,
                                     font=LABELS_FONT)
        self.__all_words_label = tk.Label(
            self.__right_frame, textvariable=self.__all_words_display,
            width=23, font=ALL_WORDS_FONT, bg=MOUSE_ON_COLOR, anchor="n",
            justify="center")

    def make_letter_cell(self, row, column, letter):
        """
        This function makes one cell in the board.
        :param row: a row index in the grid
        :param column: a column index in the grid
        :param letter: a letter in the cell
        :return: a label that was created
        """
        label = tk.Label(self.__board_frame, text=letter, **START_CELL_STYLE)
        self.__board.append(label)
        label.grid(row=row, column=column)
        return label

    def _pack(self):
        """
        This function places all the interface into the main window.
        :return: None
        """
        self.__outer_frame.pack(side=tk.TOP, **PACK_STYLE)
        self.__left_frame.pack(side=tk.LEFT, **PACK_STYLE)
        self.__time_and_score_frame.pack(side=tk.TOP, **PACK_STYLE)
        self.__right_frame.pack(side=tk.LEFT, **PACK_STYLE)
        self.__time_label.pack(side=tk.LEFT, **PACK_STYLE)
        self.__score_label.pack(side=tk.RIGHT, **PACK_STYLE)
        self.__word_label.pack(side=tk.TOP, **PACK_STYLE)
        self.__board_frame.pack(**PACK_STYLE)
        self.__start_enter_button.pack(side=tk.BOTTOM, **PACK_STYLE)
        self.__all_words_label.pack(**PACK_STYLE)

    def _start_game(self):
        """
        This function is a command function of the start button. It uncovers
        the letters in the board, starts the timer and changes the start
        button into the enter button.
        :return: None
        """
        for label in self.__board:
            label.configure(**DEFAULT_CELL_CONFIG)
        self._timer()
        self.__start_enter_button.configure(text="ENTER",
                                            command=self.__command_enter)
        self._animate_in_out()
        self._choose_letter()

    def _timer(self):
        """
        This function updates the game timer each second and when time is over
        asks the user whether to continue or exit the game.
        :return: None
        """
        self.__time_display.set(TIME_TEXT + self._time_configure())
        if self.__time == 0:
            self.__time_over_command()
        else:
            self.__time -= 1
            self.__left_frame.after(1000, self._timer)

    def _time_configure(self):
        """
        This function creates text from the stored time value in the clock
        format (min:sec).
        :return: time text
        """
        minutes = str(self.__time // 60)
        if self.__time % 60 < 10:
            seconds = "0" + str(self.__time % 60)
        else:
            seconds = str(self.__time % 60)
        return str(minutes) + ":" + str(seconds)

    def _animate_in_out(self):
        """
        This function animates mouse moves on cells.
        :return: None
        """
        for label in self.__board:
            label.bind("<Enter>", self._on_enter)
            label.bind("<Leave>", self._on_leave)

    @staticmethod
    def _on_enter(event):
        """
        This function changes the cell color when the mouse is on it.
        :param event: an event object
        :return: None
        """
        bg_color = event.widget["bg"]
        if bg_color != MOUSE_ON_COLOR:
            if event.widget["bg"] != ACTIVE_COLOR:
                event.widget.configure(**MOUSE_ON_CELL_CONFIG)
            else:
                event.widget.configure(**MOUSE_ON_ACTIVE_CELL_CONFIG)

    @staticmethod
    def _on_leave(event):
        """
        This function changes the cell color when the mouse is out of it.
        :param event: an event object
        :return: None
        """
        bg_color = event.widget["bg"]
        if bg_color != DEFAULT_COLOR and bg_color != ACTIVE_COLOR:
            if event.widget["bg"] != MOUSE_ON_ACTIVE_COLOR:
                event.widget.configure(**DEFAULT_CELL_CONFIG)
            else:
                event.widget.configure(**ACTIVE_CELL_CONFIG)

    def _choose_letter(self):
        """
        This function allows the user to choose a letter by clicking the
        corresponding label.
        :return: None
        """
        for label in self.__board:
            label.bind("<Button-1>", self.__board_command)

    def run(self):
        """
        This function starts the game loop.
        :return: None
        """
        self.__main_window.mainloop()

    def clear_board(self):
        """
        This function returns the board in the start game conditions.
        :return: None
        """
        self.__word_display.set("")
        for label in self.__board:
            label.configure(**DEFAULT_CELL_CONFIG)

    def set_word(self, letter):
        """
        This function updates the current word display.
        :param letter: a letter that is added to the current display
        :return: None
        """
        self.__word_display.set(self.__word_display.get() + letter)

    @staticmethod
    def animate_cell(label):
        """
        This function animates the board label that was clicked.
        :param label: the board label that was clicked
        :return: None
        """
        label.configure(**MOUSE_ON_ACTIVE_CELL_CONFIG)

    def set_all_words_and_score(self, new_word, score):
        """
        This function updates the score and all words display after the word
        was guessed.
        :param new_word: a word that was guessed
        :param score: the total game score
        :return: None
        """
        self.__all_words_display.set(self.__all_words_display.get() + "\n" +
                                     new_word)
        self.__score_display.set(SCORE_TEXT + str(score))

    @staticmethod
    def ask_question():
        """
        This function asks the user one question.
        :return: answer to the question
        """
        return tk.messagebox.askquestion(*QUESTION)

    def new_round(self, time):
        """
        This function starts a new game round.
        1. It destroys the outer frame that contains all the interface.
        2. It creates a new interface by rewriting the old one.
        :param time: initial game time
        :return: None
        """
        self.__outer_frame.destroy()
        self._create_interface(time)

    def exit(self):
        """
        This function destroys the game window and exits the game.
        :return: None
        """
        self.__main_window.destroy()
