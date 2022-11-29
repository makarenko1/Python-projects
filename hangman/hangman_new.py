from hangman_helper import *

INVALID_LETTER = "The letter you entered is invalid."
REPEATED_LETTER = "The letter you entered was already chosen."
WIN_MESSAGE = "You won the game!"
LOSE_MESSAGE = "You lost the game. The word was "


# Part 1

def message_check(output, pattern, errors, score):
    if output == 0:  # Checking message parameter
        display_state(pattern, errors, score, "")
    elif output == 1:
        display_state(pattern, errors, score, INVALID_LETTER)
    elif output == 2:
        display_state(pattern, errors, score, REPEATED_LETTER)


def update_word_pattern(word, pattern, letter):
    for i in range(len(word)):
        if pattern[i] == "_" and word[i] == letter:
            pattern = pattern[:i] + word[i] + pattern[i + 1:]
    return pattern


def score_plus(pattern, pattern_new):
    open_letters = 0
    for i in range(len(pattern)):
        if pattern[i] != pattern_new[i]:
            open_letters += 1
    return open_letters * (open_letters + 1) // 2


def get_input_and_react(error_code, errors, pattern, score, word, words_list):
    user_in = get_input()
    if user_in[0] == LETTER:
        pattern, score, error_code = case_letter(errors, pattern, score,
                                                 user_in[1], word)
    elif user_in[0] == WORD:
        pattern, score = case_word(pattern, score, user_in[1], word)
    elif user_in[0] == HINT:
        score = case_hints(errors, pattern, score, words_list)
    return error_code, pattern, score


def run_single_game(words_list, score):
    word = get_random_word(words_list)
    pattern = '_' * len(list(word))
    errors = list()
    error_code = 0
    while pattern != word and score > 0:
        message_check(error_code, pattern, errors, score)
        error_code, pattern, score = get_input_and_react(error_code, errors,
                                                         pattern, score, word,
                                                         words_list)
    end_game(errors, pattern, score, word)
    return score


def case_letter(errors, pattern, score, user_letter, word):
    error_code = 0
    if len(user_letter) != 1 or ord(user_letter) < 97 \
            or ord(user_letter) > 122:
        error_code = 1
    elif user_letter in pattern or user_letter in errors:
        error_code = 2
    else:
        score -= 1
        pattern_new = update_word_pattern(word, pattern, user_letter)
        if pattern_new != pattern:
            score += score_plus(pattern, pattern_new)
            pattern = pattern_new
        else:
            errors.append(user_letter)
    return pattern, score, error_code


def case_word(pattern, score, user_word, word):
    score -= 1
    if word == user_word:
        score += score_plus(pattern, word)
        pattern = word
    return pattern, score


def case_hints(errors, pattern, score, words_list):
    score -= 1
    hints = filter_words_list(words_list, pattern, errors)
    new_hints = list()
    if len(hints) > HINT_LENGTH:
        for n in range(HINT_LENGTH):
            new_hints.append(hints[n * len(hints) // HINT_LENGTH])
        show_suggestions(new_hints)
    else:
        show_suggestions(hints)
    return score


def end_game(errors, pattern, score, word):
    if pattern == word:
        display_state(pattern, errors, score, WIN_MESSAGE)
    else:
        display_state(pattern, errors, score, LOSE_MESSAGE + word)


def ask_if_play_again(points, number_of_games):
    if points > 0:
        continue_playing = play_again(
            f"Number of games so far: {number_of_games}. Your current score: "
            f"{points}. Want to continue?")
    else:
        continue_playing = play_again(
            f"Number of games survived: {number_of_games}. Start a new series "
            f"of games?")
    return continue_playing


def main():
    list_of_words = load_words()
    score = POINTS_INITIAL
    number_of_games = 0
    continue_playing = True
    while continue_playing:
        score = run_single_game(list_of_words, score)
        number_of_games += 1
        continue_playing = ask_if_play_again(score, number_of_games)
        if score == 0:
            score = POINTS_INITIAL
            number_of_games = 0


# Part 2

def check_places_opened_letters(word, pattern):
    for i in range(len(word)):
        if word[i] in pattern and pattern[i] == "_":
            return False
        elif pattern[i] != "_" and word[i] != pattern[i]:
            return False
    return True


def check_letters_in_wrong_guesses(word, wrong_guess_lst):
    for letter in word:
        if letter in wrong_guess_lst:
            return False
    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    result = []
    for word in words:
        if len(word) != len(pattern):
            continue
        elif not check_letters_in_wrong_guesses(word, wrong_guess_lst):
            continue
        elif not check_places_opened_letters(word, pattern):
            continue
        result.append(word)
    return result


if __name__ == "__main__":
    main()
