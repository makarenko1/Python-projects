#############################################################################
# FILE: wave_editor.py
# EXERCISE: intro2cs1 ex6 2020
# DESCRIPTION: A simple program that creates or changes .wav files
#############################################################################
import wave_helper
import copy
import math
import sys
import os.path

MAX_VOLUME = 32767
MIN_VOLUME = -32768
SAMPLE_RATE = 2000
FREQUENCY_A = 440
FREQUENCY_B = 494
FREQUENCY_C = 523
FREQUENCY_D = 587
FREQUENCY_E = 659
FREQUENCY_F = 698
FREQUENCY_G = 784
FREQUENCY_Q = 0


def main_menu():
    """This function prints the main menu. The user can choose either to edit
    a .wav file or to create a new melody or to exit from a program."""
    user_input = input("1. EDIT FILE WAV\n2. CREATE A NEW MELODY"
                       "\n3. EXIT FROM A PROGRAM\nYOUR CHOICE: ")
    while user_input != "1" and user_input != "2" and user_input != "3":
        print("SOMETHING WENT WRONG!")
        user_input = input("1. EDIT FILE WAV\n2. CREATE A NEW MELODY"
                           "\n3. EXIT FROM A PROGRAM\nYOUR CHOICE: ")
    if user_input == "1":
        edit_melody_main()
    elif user_input == "2":
        create_melody_main()
    else:
        sys.exit()


def edit_melody_main():
    """This function opens a user file and calls for necessary function if
    the user chooses 1."""
    filename = input("CHOOSE A FILE: ")
    melody_list_freq = wave_helper.load_wave(filename)
    while melody_list_freq == -1:
        print("SOMETHING WENT WRONG!")
        filename = input("CHOOSE A FILE: ")
        melody_list_freq = wave_helper.load_wave(filename)
    frame_rate = melody_list_freq[0]
    melody_list = melody_list_freq[1]
    return editor_menu(frame_rate, melody_list)


def create_melody_main():
    """This function opens a user file and calls for necessary function if
    the user chooses 2."""
    filename = input("CHOOSE A FILE: ")
    while not os.path.isfile(filename):
        print("SOMETHING WENT WRONG!")
        filename = input("CHOOSE A FILE: ")
    print("A MELODY WAS CREATED")
    return editor_menu(SAMPLE_RATE, create_melody(read_notes_list(filename)))


def print_editor_menu():
    """This function prints an editor menu for the first option in the main
    menu. The user can choose to make a reversed melody, a negative melody,
    speed a melody up, slow it down, increase the volume, decrease the volume,
    make a low pass filter. Or he can save the current progress."""
    user_input = input("1. REVERSE A MELODY\n2. NEGATIVE MELODY"
                       "\n3. SPEED UP\n4. SLOW DOWN\n5. VOLUME UP"
                       "\n6. VOLUME DOWN\n7. LOW PASS FILTER"
                       "\n8. FINISH MENU\nYOUR CHOICE: ")
    while user_input != "1" and user_input != "2" and user_input != "3" \
            and user_input != "4" and user_input != "5" and user_input != "6" \
            and user_input != "7" and user_input != "8":
        print("SOMETHING WENT WRONG!")
        user_input = input("1. REVERSE A MELODY\n2. NEGATIVE MELODY"
                           "\n3. SPEED UP\n4. SLOW DOWN\n5. VOLUME UP"
                           "\n6. VOLUME DOWN\n7. LOW PASS FILTER"
                           "\n8. FINISH MENU\nYOUR CHOICE: ")
    return user_input


def limit_checking(number):
    """This function checks if a number is in the limit of volume."""
    if number > MAX_VOLUME:
        number = MAX_VOLUME
        return number
    elif number < MIN_VOLUME:
        number = MIN_VOLUME
        return number
    return number


def reverse_a_melody(melody_list):
    """This function returns a melody_list vice versa."""
    return melody_list[::-1]


def negative_melody(melody_list):
    """This function returns a melody_list with all its values negative."""
    for pair in range(len(melody_list)):
        melody_list[pair][0] *= -1
        melody_list[pair][0] = limit_checking(melody_list[pair][0])
        melody_list[pair][1] *= -1
        melody_list[pair][1] = limit_checking(melody_list[pair][1])
    return melody_list


def speed_up(melody_list):
    """This function returns a melody_list with only odd elements."""
    update_melody_list = []
    for pair in range(0, len(melody_list), 2):
        update_melody_list.append(melody_list[pair])
    return update_melody_list


def slow_down(melody_list):
    """This function returns a melody_list with a new pair of elements added
    between every two elements."""
    edited_melody_list = []
    for pair in range(len(melody_list)-1):
        edited_melody_list.append(melody_list[pair])
        edited_melody_list.append([int((melody_list[pair][0] +
                                  melody_list[pair+1][0])/2),
                                   int((melody_list[pair][1] +
                                        melody_list[pair+1][1])/2)])
    edited_melody_list.append(melody_list[len(melody_list)-1])
    return edited_melody_list


def volume_up(melody_list):
    """This function returns a melody_list multiplied by 1.2"""
    for number in range(len(melody_list)):
        melody_list[number][0] = \
            limit_checking(int(melody_list[number][0] * 1.2))
        melody_list[number][1] = \
            limit_checking(int(melody_list[number][1] * 1.2))
    return melody_list


def volume_down(melody_list):
    """This function returns a melody_list divided by 1.2"""
    for pair in range(len(melody_list)):
        melody_list[pair][0] = int(melody_list[pair][0]/1.2)
        melody_list[pair][0] = limit_checking(melody_list[pair][0])
        melody_list[pair][1] = int(melody_list[pair][1]/1.2)
        melody_list[pair][1] = limit_checking(melody_list[pair][1])
    return melody_list


def low_pass_filter(melody_list):
    """This function changes each element to the average between the previous
    element to it and the next to it. If it is the first element, the average
    is done with it and the next to it. If it is the last element, the average
    is done between it and the previous element."""
    update_melody_list = copy.deepcopy(melody_list)
    for pair in range(len(melody_list)):
        if pair == 0:
            for i in range(2):
                update_melody_list[pair][i] = \
                    int((melody_list[pair][i] +
                         melody_list[pair + 1][i]) / 2)

        elif pair == len(melody_list) - 1:
            for i in range(2):
                update_melody_list[pair][i] = \
                    int((melody_list[pair - 1][i] +
                         melody_list[pair][i]) / 2)

        else:
            for i in range(2):
                update_melody_list[pair][i] = \
                    int((melody_list[pair - 1][i] +
                         melody_list[pair][i] +
                         melody_list[pair + 1][i]) / 3)
    return update_melody_list


def finish_menu(frame_rate, melody_list):
    """This function suggests the user to choose a name of the file where they
    would like to save the result. If the name of the file is without .wav,
    the function adds it. Then it writes the result in the file. In the end it
    calls the main_menu function."""
    filename = input("CHOOSE A FILENAME TO SAVE: ")
    result = wave_helper.save_wave(frame_rate, melody_list, filename)
    while result == -1:
        print("SOMETHING WENT WRONG!")
        filename = input("CHOOSE A FILENAME TO SAVE: ")
        result = wave_helper.save_wave(frame_rate, melody_list, filename)
    main_menu()


def read_notes_list(filename):
    """This function creates a list from a file with directions for creation a
    melody."""
    notes_list = []
    notes_file = open(filename)
    for lines in notes_file:
        temp = ""
        lines = lines.upper()
        for note in lines:
            temp += " " + note + " "
        notes_list += temp.split()
    notes_file.close()
    return notes_list


def calculate_samples(time, frequency):
    """This function returns a list with samples for one note."""
    samples_list = []
    for i in range(0, int(time) * 125):
        if frequency == 0:
            sample = 0
        else:
            samples_per_cycle = SAMPLE_RATE/frequency
            sample = int(MAX_VOLUME * math.sin(math.pi*2*i/samples_per_cycle))
        samples_list.append([sample, sample])
    return samples_list


def create_melody(notes_list):
    """This function creates one list of lists with samples of each note from
    a file with notes.
    :param notes_list: list with each note and time of playing
    :return: list with audio data"""
    melody_list = []
    for note in range(0, len(notes_list)-1, 2):
        if notes_list[note] == "A":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_A)
        elif notes_list[note] == "B":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_B)
        elif notes_list[note] == "C":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_C)
        elif notes_list[note] == "D":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_D)
        elif notes_list[note] == "E":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_E)
        elif notes_list[note] == "F":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_F)
        elif notes_list[note] == "G":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_G)
        elif notes_list[note] == "Q":
            melody_list += calculate_samples(notes_list[note + 1], FREQUENCY_Q)
    return melody_list


def editor_menu(frame_rate, melody_list):
    """This function analyses the print_editor_menu function and chooses
    which task to perform. Then it prints a success message."""
    user_input = print_editor_menu()
    if user_input == "1":
        melody_list = reverse_a_melody(melody_list)
        print("THE CHANGE 'REVERSE A MELODY' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "2":
        melody_list = negative_melody(melody_list)
        print("THE CHANGE 'NEGATIVE MELODY' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "3":
        melody_list = speed_up(melody_list)
        print("THE CHANGE 'SPEED UP' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "4":
        melody_list = slow_down(melody_list)
        print("THE CHANGE 'SLOW DOWN' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "5":
        melody_list = volume_up(melody_list)
        print("THE CHANGE 'VOLUME UP' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "6":
        melody_list = volume_down(melody_list)
        print("THE CHANGE 'VOLUME DOWN' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "7":
        melody_list = low_pass_filter(melody_list)
        print("THE CHANGE 'LOW PASS FILTER' IS DONE")
        editor_menu(frame_rate, melody_list)
    elif user_input == "8":
        finish_menu(frame_rate, melody_list)
        return


if __name__ == "__main__":
    main_menu()
