# commented english
# module input, used to convert an action into an input the program can deal with
from pygame.locals import *

# ------
# important variables
# a few letters of the alphabet, used to convert letters into numbers
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# dicitonary used to convert keys into letters and numbers
key_dict_letters_digits = {
    K_a: "A",
    K_b: "B",
    K_c: "C",
    K_d: "D",
    K_e: "E",
    K_f: "F",
    K_g: "G",
    K_h: "H",
    K_i: "I",
    K_j: "J",
    K_1: 1, K_KP1: 1,
    K_2: 2, K_KP2: 2,
    K_3: 3, K_KP3: 3,
    K_4: 4, K_KP4: 4,
    K_5: 5, K_KP5: 5,
    K_6: 6, K_KP6: 6,
    K_7: 7, K_KP7: 7,
    K_8: 8, K_KP8: 8,
    K_9: 9, K_KP9: 9,
    K_0: 0, K_KP0: 0
}
# dictionary used to convert the order of end_buttons into their use
end_button_dic = {
    0: "end",
    1: "settings"
}


# ------
# initialising the modul
def __init__input():
    """
    initializes the module input
    :return: nothing
    """
    global key_list
    key_list = []  # creates an empty list, where keys of a selcted field are stored


# ------
# input by mouseclick
def _get_field_count(coord, field_size):
    """
    returns the field coordinate of a coordiante
    :param coord: int; half a coordinate
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :return: int; field coordiante of the coordinate
    """

    field_coord = -1  # sets the field coordiante to -1
    next_field_border = 3 / 2.0 * field_size  # calculates the first field boarder

    while coord > next_field_border:  # checks, whether the coordiante is farther right/down than the field boarder
        field_coord += 1  # adds one to the field coordinate
        next_field_border += field_size  # calculates the next field boarder

    return field_coord  # returns the field coordiante of the coordinate


def _get_square_mouse(xcoord, ycoord, field_size):
    """
    :param xcoord: int; x coordinate
    :param ycoord: int; y coordinate
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :return: list[int, int]; field coordinate of the mouseclick
    """
    # gets the field coordinates
    field_coord_x = _get_field_count(xcoord, field_size)
    field_coord_y = _get_field_count(ycoord, field_size)

    if field_coord_x != -1 and field_coord_y != -1:  # checks for mistakes
        return field_coord_x, field_coord_y  # returns the field coordinate of the mouseclick


def _get_button_boundaries(button_list):
    """
    returns the button boundaries of the one button list's buttons
    :param button_list: list[Button, ...]; list that holds buttons
    :return: lsit[list[list[int, int], list[int, int]], list, ...]; list that holds the button boundaries
    """
    button_boundaries = []  # creates an empty list
    for button in button_list:  # goes through the buttons of the button_list
        if button.active:  # checks, whether the button is currently active
            button_coords = button.field_coords  # gets the button's coordinates
            boundary_x_small, boundary_y_small = button_coords[0]  # sets the first coordiante
            boundary_x_big, boundary_y_big = button_coords[-1]  # sets the last coordinate
            # adds those boundaries to the list
            button_boundaries.append([[boundary_x_small, boundary_x_big], [boundary_y_small, boundary_y_big]][:])
    return button_boundaries  # returns the list that holds the button boundaries


def get_button_start_mouse(xcoord, ycoord, field_size, start_buttons):
    """
    gibt den angeklickten Knopf in den Einstellungen zurueck
    :param xcoord: int; x-Koordinate des Mausklicks
    :param ycoord: int; y-Koordinate des Mausklicks
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param start_buttons: list[Button, Button, ...]; list that holds start buttons
    :return: int; button's number of the clicked button
    """
    square = _get_square_mouse(xcoord, ycoord, field_size)  # gets the klicked field
    button_boundaries = _get_button_boundaries(start_buttons)  # gets the boundarios of the active buttons

    count = 1  # creates a counter that counts the active buttons
    for boundaries in button_boundaries:  # goes through the buttons
        # checks, whether that button was clicked
        if boundaries[0][0] <= square[0] <= boundaries[0][1] and boundaries[1][0] <= square[1] <= boundaries[1][1]:
            return count  # returns the button's number
        count += 1  # adds 1

    return False  # returns False if no button was clicked


def get_button_ingame_mouse(xcoord, ycoord, field_size, end_buttons):
    """
    returns the clicked thing if something was clicked
    :param xcoord: int; x coordinate of the mouseclick
    :param ycoord: int; y coordinate of the mouseclick
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param end_buttons: list[Button, ...]; list that holds the end buttons
    :return: list[str, int, int] or list[str, str]; type of clicked thing and it's identification
    """
    square = _get_square_mouse(xcoord, ycoord, field_size)  # gets the clicked field

    # returns a field, if a field on the playfield was clicked
    if 0 <= square[0] <= 9 and 0 <= square[1] <= 9:
        return "field", square[0], square[1]

    button_boundaries = _get_button_boundaries(end_buttons)  # gets the boundaries of the active buttons

    count = 0  # creates a counter that counts the active buttons
    for boundaries in button_boundaries:  # goes through the buttons
        # checks, whether that button was clicked
        if boundaries[0][0] <= square[0] <= boundaries[0][1] and boundaries[1][0] <= square[1] <= boundaries[1][1]:
            return "button", end_button_dic[count]  # returns that button
        count += 1  # adds 1

    return False  # returns False if no button was clicked


# ------
# input by keyboard presses
def _get_square_keyboard():
    """
    returns the selected square from pressed keys
    :return: bool, int, int; whether a valid field was selected, selected square
    """
    if not key_list:  # checks, whether the key_list is empty
        key_list.append(0)  # adds a zero, so that the list can be iterated through
    # counts the keys that were pressed before they were submitted
    key_count = 0
    # noinspection PyUnusedLocal
    for key in key_list:
        key_count += 1

    x_coord, y_coord = -1, -1  # declares values for the square, that will get changed when the input is valid

    if key_count >= 2:  # checks, whether at least two keys got pressed, because two are needed for a valid input
        if key_list[0] in letters:  # checks, whether the letter input is valid
            # converts the pressed letter into a x-coordinate
            x_coord = 0
            for letter in letters:
                if letter == key_list[0]:
                    break
                x_coord += 1

        if key_count >= 3:  # checks how many keys were pressed
            # calculates the y-coordinate and ignores all keys past the third
            y_coord = key_list[1] * 10 + key_list[2] - 1
        elif key_count == 2:
            y_coord = key_list[1] - 1  # calculates the y-coordinate

    if 0 <= x_coord <= 9 and 0 <= y_coord <= 9:
        return True, [x_coord, y_coord]  # returns that a valid field was selected, and the selected square
    return False, [-1, -1]  # returns that no valid field was seleccted


def _get_keyboard_input(key):
    """
    :param key: pressed  key on keyboard
    :return: pressed number or letter
    """
    if key in key_dict_letters_digits:  # checks, whether the key is used to select a field
        return key_dict_letters_digits[key]  # returns the pressed number or letter
    else:
        return None  # returns None, so that it can be handeled as somethign that is not a valid key


def get_button_ingame_keyboard(pressed_key):
    """
    returns a selected field, if a field was selcted
    :param pressed_key: Key; pressed key
    :return: list[str, int, int]; type of selected field, selected field
    """
    if pressed_key == K_KP_ENTER or pressed_key == K_RETURN:  # checks, whether an enter key was pressed
        if _get_square_keyboard()[0]:  # checks, whether a valid field was selected
            xcoord, ycoord = _get_square_keyboard()[1]  # gets the selected field
            key_list.clear()  # clears the list with the selected field
            return "field", xcoord, ycoord  # returns the selected field
        else:
            key_list.clear()  # clears the list with the selected field
    else:
        if _get_keyboard_input(pressed_key) is not None:  # checks, whether a valid key was pressed
            key_list.append(_get_keyboard_input(pressed_key))  # appends the key to the list with the selected field
