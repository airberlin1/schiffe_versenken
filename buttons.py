"""module containing buttons and their content, displaying themselves"""
# TODO Sprachen mit Flaggen kennzeichenen
# ------
# imports pygame and the writing to display buttons and writings
from writing import Writing
from translation import get_dict
import pygame


# -------
# list with buttons' contents
# one whole row is shown simultaniously from top to bottom
intention_list = [
        ["Start", "Leicht", "Vollbild", "Ozean", "Deutsch", "Zurueck", None, "Zurueck", "Normal"],
        ["Schwierigkeit", "Mittel", "Fenster", "Weltall", "English", None, None, None, "Kontrast"],
        ["Bildeinstellungen", "Unmoeglich", "Hintergrund", "Gezeichnet", "Latinum", None, None, None, "Weihnachten"],
        ["Sprache", "Zurueck", "Theme", "Zurueck", "Zurueck", None, None, None, "Zurueck"],
        ["Hilfe", None, "Zurueck"],
        ["Beenden"]
]
intention_list_settings = [
    ["Weiter",            None, "Vollbild",    "Ozean",      "Deutsch", "Zurueck", None, "Zurueck", "Normal"],
    ["Bildeinstellungen", None, "Fenster",     "Weltall",    "English", None, None, None, "Kontrast"],
    ["Sprache",           None, "Hintergrund", "Gezeichnet", "Latinum", None, None, None, "Weihnachten"],
    ["Hilfe",             None, "Theme",     "Zurueck",    "Zurueck", None, None, None, "Zurueck"],
    ["Lautstärke",  None, "Zurueck"],
    ["Aufgeben"]
]


# -------
# classes "Button" and "ButtonWriting"
class Button:
    """Knoepfe auf der Oberflaeche"""

    def __init__(self, location_top_left, size_x, size_y, field_size_x, field_size_y, field_coords, intention,
                 liste, active, color_local, number):
        """
        :param location_top_left: list[int, int]; top left corner's coordiantes
        :param size_x: float; horizontal size of button
        :param size_y: float; vertical size of button
        :param field_size_x: int; horizontal size of button in quantity of fields
        :param field_size_y: int; vertical size of button in quantity of fields
        :param field_coords: list[list[int, int], list,...]; field coordaintes the button is on,
         used to recognize clicks on it
        :param intention: str; intention and text on button that is translated
        :param liste: str; lsit the button is in
        :param active: bool; button is displayed
        :param color_local: tuple(int, int, int); color the button's background is dispalyed in
        :param number: numberused to differ between buttons
        """
        self.location_top_left = location_top_left
        self.size_x = size_x
        self.size_y = size_y
        self.field_size_y = field_size_y
        self.field_size_x = field_size_x
        self.field_coords = field_coords
        self.intention = intention
        self.active = active
        self.liste = liste
        self.color = color_local
        self.number = number

    def change_loc_coords(self, field_size):
        """
        updates button's coordinates, used when changes to the window are made
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        # gets the top left field coordiante
        fieldcoord_top_left = self.field_coords[0]
        # calculates new coordiante for top left corner
        self.location_top_left = [int((fieldcoord_top_left[0] + (3 / 2)) * field_size),
                                  int((fieldcoord_top_left[1] + (3 / 2)) * field_size)]
        # updates button's size
        self.size_x = self.field_size_x * field_size
        self.size_y = self.field_size_y * field_size

    def get_active_end_b(self, orientation):
        """
        gets whether in game button is displayed
        :param orientation: str; width/height depending on what is bigger
        :return: bool; whether button is displayed
        """
        if orientation == "height":
            # first button is not displayed, second is
            if self.number % 2 == 1:
                return True
            else:
                return False
        else:
            # first button is displayed, second is not
            if self.number % 2 == 0:
                return True
            else:
                return False

    def change_intention(self, task_number, orientation, zustand):
        """
        changes whether a button is displayed and also updates its intention
        :param task_number: int; number of the task the menu has to fulfill
        :param orientation: str; width/height, depending on what is bigger
        :param zustand: str; start/ingame/settings, what the program is currently doing
        """
        if self.number > 98:  # button is not a start button
            if task_number == 6:  # program is currently in game
                # only half of end buttons are displayed depending on orientation
                self.active = self.get_active_end_b(orientation)
            else:
                self.active = False  # no in game button is displayed while not in game

        elif task_number != 6:  # program is at start or in settings
            try:
                # updates buttons intention
                if zustand == "start":  # program is at start
                    # gets intention from list
                    self.intention = intention_list[self.number][task_number]
                elif zustand == "settings":  # program is in settings
                    # gets intention from list
                    self.intention = intention_list_settings[self.number][task_number]
                if self.intention is None:  # no intention for this button at this moment
                    self.active = False  # button is not displayed
                else:
                    self.active = True  # button is displayed

            except IndexError:
                # no intention so that button is not displayed
                self.intention = None
                self.active = False

        else:  # game is in game and button is start button
            # button is not displayed
            self.intention = None
            self.active = False

    def draw(self, screen):
        """
        displays button in the game window
        :param screen: Surface; surface covering whole window
        """
        pygame.draw.rect(screen, self.color,
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 0)


class ButtonWriting(Writing):
    """writing on buttons displaying itself on button's center and getting content from button's intention"""

    def __init__(self, content, font, color_local, top_left_corner, button, background, active):
        """
        :param content: str; dispalyed text
        :param font: SysFont; font the text is dispalyed in
        :param color_local: tuple(int, int, int); writing's color
        :param top_left_corner: list[int, int]; coordiantes of writing's center
        :param button: Button; button the writing is on
        :param background: tuple(int, int, int); writing's background's color, usually None
        :param active: bool; writing is currently displayed
        """
        super().__init__(content, font, color_local, top_left_corner, background)  # initializes the writing
        self.button = button
        self.active = active

    def change_loc_coords(self, field_size):
        """
        refreshes writing's size and center
        :param field_size: float; size of one virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        self.top_left_corner = _get_center_writing(self.button)  # sets new center
        font_size = int(field_size * 2)  # resizes font
        self.font = pygame.font.SysFont(None, font_size)  # updates font

    def refresh_content(self, language):
        """
        updates content of writing and if writing is dispalyed
        :param language: str; language all text is currently displayed in
        """
        self.content = _get_writing_content(self.button.liste, language, self.button.number)  # updates content
        self.active = self.button.active  # writing is dispalyed if button is displayed


# -------
# buttons' creation
def _get_field_coords_from_start(xcoord_count, start_coord):
    """
    creates list with all fields a button is on depending on its size and location

    :param xcoord_count: int; number of fields in x direction the button is covering
    :param start_coord: list[int, int]; top left coordiante of the button
    :return: list[list[int, int], list[int, int], ...]; coordiantes the button is on
    """
    field_coords = []  # creates a list that is going to hold the field coords
    next_coord = start_coord[:]
    for j in range(2 * xcoord_count):
        field_coords.append(next_coord[:])  # adds the coordinate to the list of coordinates

        # sets the y coordiante to the same as the start y coordinate, if the first line of coordinates is added
        if j < (xcoord_count - 1):
            next_coord[1] = start_coord[1]
        elif j == (xcoord_count - 1):
            # sets the y coordiante to one plus the start y coordinate, if the second line of coordinates is added
            next_coord[1] = start_coord[1] + 1
            # sets the x coordiante to the same as the start x coordinate when the second line begins
            next_coord[0] = start_coord[0]
        else:
            # sets the y coordiante to one plus the start y coordinate, if the second line of coordinates is added
            next_coord[1] = start_coord[1] + 1

        # adds 1 to the x-coordinate, so that the field coord next to the one before can be added
        next_coord[0] += 1
    return field_coords  # returns all field coords the button is on


def _create_start_buttons(field_size, button_bg_color):
    """
    creates buttons displayed while settings and in the beginning
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param button_bg_color: tup(int, int, int); background color of buttons, RGB
    """
    # creates lsit later containing all in game buttons
    global start_buttons
    start_buttons = []
    loc_tl = [int(3 / 2 * field_size), int(3 / 2 * field_size)]  # sets top left corner for first button
    # sets buttons' size
    size_x = field_size * 10
    size_y = field_size * 2
    for i in range(6):  # currently there are six start buttons
        # gets all coordinates
        field_coords = _get_field_coords_from_start(xcoord_count=10, start_coord=[0, i * 3])
        # creates button
        start_buttons.append(0)
        start_buttons[i] = Button(loc_tl, size_x, size_y, 11, 2, field_coords, None, "start_buttons", True,
                                  button_bg_color, i)
        # puts the top left corner 3 field sizes down
        loc_tl[1] += 3 * field_size


def _get_loc_top_left_end_b(end_button_number):
    """
    returns the top left field coordinate of the end button
    :param end_button_number: int; end button's number
    :return: list[int, int]; coordinate of the button's top left corner
    """
    if end_button_number == 0:
        return 19 / 2, 25 / 2  # 0 is the end button while orientation == "width"

    elif end_button_number == 1:
        return 25 / 2, 23 / 2  # 1 is the end button while orientation == "height"

    elif end_button_number == 2:
        return 3 / 2, 25 / 2  # 2 is the settings button while orientation == "width"

    elif end_button_number == 3:
        return 25 / 2, 17 / 2  # 3 is the settings button while orientation == "height"

    elif end_button_number == 4:
        return 35 / 2, 25 / 2  # 4 is the save button while orientation == "width"

    elif end_button_number == 5:
        return 25 / 2, 29 / 2  # 5 is the save button while orientation == "height"


def _get_field_coords_end_b(end_button_number):
    """
    returns a list with an end button's coordiantes.
    This list than holds all the coordinates on which the button can be clicked
    :param end_button_number: int; end button's number
    :return: list[list[int, int], list[int, int], ...]; coordiantes the button is on
    """
    # calculates first coordinate
    start_coord = list(_get_loc_top_left_end_b(end_button_number))
    start_coord[0] -= 1.5
    start_coord[1] -= 1.5
    # returns the coordinates the button is on
    return _get_field_coords_from_start(xcoord_count=7, start_coord=start_coord)


def _create_end_buttons(field_size):
    """
    creates buttons to end the game, to go to the settings in game and to save the game
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    # creates list later holding all in game buttons
    global end_buttons
    end_buttons = []
    for i in range(6):  # currently 3 buttons, both twice for different orientation
        loc_tl = _get_loc_top_left_end_b(i)  # gets coordinates for top left corner
        field_count_x = 7  # sets button's width
        # calculates button's size
        size_x = field_count_x * field_size
        size_y = 2 * field_size + (1 - (i % 2)) * field_size
        field_coords = _get_field_coords_end_b(i)  # gets coordiantes on which the button can be clicked
        # sets button's background color according to usage
        if i < 2:  # surrender button
            color = (170, 0, 0)
        elif i < 4:  # settings button
            color = (0, 50, 0)
        else:  # save button
            color = (0, 0, 100)
        # creates button
        end_buttons.append(0)
        end_buttons[i] = Button(loc_tl, size_x, size_y, field_count_x, 2, field_coords, "Beenden", "end_buttons",
                                False, color, i + 100)


def _create_buttons(field_size, button_bg_color):
    """
    creates buttons apart from request button (under writing initialization)
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    _create_start_buttons(field_size, button_bg_color)  # creates list with buttons displayed at the start
    _create_end_buttons(field_size)  # creaets list with buttons displayed in game


# -------
# initializes buttons' writings
def _get_writing_content(button_list, language, button_number):
    """
    retunrs content for a writing
    :param button_list: str; list the button is in
    :param language: str; language all tect is currentöy displayed in
    :param button_number: int; number of button
    :return: str; content of button
    """
    dictionary = get_dict(language, "button")  # gets dictionary used to translate button's intention
    if button_list == "start_buttons":  # button is displayed in the beginning
        # translates button's intention
        return dictionary[start_buttons[button_number].intention]
    else:  # button is displayed in game
        if button_number < 102:  # surrender button
            intention = "Aufgeben"
        elif button_number < 104:  # settings button
            intention = "Menue"
        else:  # save button
            intention = "Speichern"
        return dictionary[intention]  # translates button


def _get_font_button(field_size):
    """
    gets font for a button's writing
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :return: SysFont; font the writing is displayed in
    """
    font_size = int(field_size * 2)  # calculates font's size
    return pygame.font.SysFont(None, font_size)   # returns font


def _get_center_writing(button):
    """
    gets top left corner for button writings
    :param button: Button; button the writing is on
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :return: list[int, int]; coordiantes of writings center
    """
    xcoord, ycoord = button.location_top_left  # buttons top left corner
    xcoordadd, ycoordadd = button.size_x / 2, button.size_y / 2  # gets buttons center
    xcoord += xcoordadd  # adds half of button's size to x-coordinate
    ycoord += ycoordadd  # adds half of button's size to y-koordinate
    return xcoord, ycoord  # returns writing's center


def __init__button_writings(language, color_writing, color_end_b_writing, field_size):
    """
    creates writings on buttons

    :param language: str; language the program is currently displaying its writings in
    :param color_writing: tuple(int, int, int); color of start buttons' writings
    :param color_end_b_writing: tuple(int, int, int); color of end buttons' writings
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    # creates a list later holding all writings on start buttons
    global button_writings_start
    button_writings_start = []
    for button in start_buttons:
        # creates a wrtiting for that button
        button_writings_start.append(ButtonWriting(_get_writing_content("start_buttons", language, button.number),
                                                   _get_font_button(field_size), color_writing,
                                                   _get_center_writing(button),
                                                   button, None, True))
    # creates a list later holding all writings on in game buttons
    global button_writings_end
    button_writings_end = []
    for button in end_buttons:  # goes through every in game button
        # creates a writing for that button
        button_writings_end.append(ButtonWriting(_get_writing_content("end_buttons", language, 0),
                                                 _get_font_button(field_size), color_end_b_writing,
                                                 _get_center_writing(button), button, None, False))


def __init__buttons(language, color_writing, color_end_b_writing, field_size, button_bg_color):
    """
    initializes buttons by creating buttons

    :param language: str; language the program is currently displaying its writings in
    :param color_writing: color_writing: tuple(int, int, int); color of start buttons' writings
    :param color_end_b_writing: color_end_b_writing: tuple(int, int, int); color of end buttons' writings
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    _create_buttons(field_size, button_bg_color)  # creates buttons
    __init__button_writings(language, color_writing, color_end_b_writing, field_size)  # creates writings


def create_request_buttons(field_size, bg_color, writing_color, language):
    """
    creates request buttons labeled with 'New Game' and 'Load Game'

    those buttons are used once after the beginning and before the actual game start

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param bg_color: tup(int, int, int); color of the buttons' backgrounds
    :param writing_color: tup(int, int, int); writings' colors
    :param language: str; language the program currently displays all writing in
    """
    global request_buttons
    global button_writings_request
    request_buttons = []  # creates a list that later holds the request buttons
    button_writings_request = []  # creates a list that later holds the writings to the request buttons
    for i in range(2):
        # determines the correct intention for the button
        intention = 'new' if i == 0 else 'load'
        # calculates button's size
        size_x = field_size * 10
        size_y = field_size * 2
        # determines the correct dict to show request in correct language
        lang_dict = get_dict(language, "button")
        if i:
            location_top_left = [35 / 2 * field_size, 15 / 2 * field_size]
            start_coord = [16, 6]
        else:
            location_top_left = [11 / 2 * field_size, 15 / 2 * field_size]
            start_coord = [4, 6]
        xcoord_count = 10

        # creates a button
        request_buttons.append(Button(size_x=size_x, size_y=size_y, number=i + 200, location_top_left=location_top_left,
                                      liste='request_buttons', intention=intention, field_size_x=8, field_size_y=2,
                                      field_coords=_get_field_coords_from_start(xcoord_count, start_coord),
                                      color_local=bg_color, active=False))
        # creates a writing to the button
        button_writings_request.append(ButtonWriting(top_left_corner=_get_center_writing(request_buttons[i]),
                                                     font=_get_font_button(field_size),
                                                     content=lang_dict[intention], color_local=writing_color,
                                                     button=request_buttons[i], background=None, active=False))


# -------
# refreshes buttons' and their writings' coordinates
def refresh_loc_buttons(field_size, orientation, zustand):
    """
    refreshes coordinates of buttons, used when window's size is adjusted

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :param zustand: str; ingame/start/settings, depending on what the program is doing
    """
    for start_button in start_buttons:  # goes through start buttons
        start_button.change_loc_coords(field_size)  # refreshes its coordinates
    button_number = 0  # starts to count to count to determine number of button
    for end_button in end_buttons:  # goes through end buttons
        end_button.change_loc_coords(field_size)  # refreshes its coordinates
        if zustand == "ingame":  # refreshes button's visibility
            end_button.active = end_button.get_active_end_b(orientation)
        button_number += 1  # continues counting


def refresh_loc_writing(field_size, zustand):
    """
    refreshes coordinates of writings, used when window's size is adjusted

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param zustand: str; ingame/start/settings, depending on what the program is doing
    """
    for button_writing in button_writings_start:  # goes through start writings
        button_writing.change_loc_coords(field_size)   # refreshes its coordinates
    button_number = 0  # begins counting to determine number of button
    for button_writing in button_writings_end:  # goes through in game writing
        button_writing.change_loc_coords(field_size)  # refreshes its coordinates
        if zustand == "ingame":
            button_writing.active = button_writing.button.active  # refreshes visibilty of end buttons' writings
        button_number += 1  # continues counting


# -------
# refreshes looks, intention and visibility of buttons
def _refresh_intention_buttons(task_number, orientation, zustand):
    """
    refreshes the buttons' intention and visibility

    :param task_number: int; task number referring to its current task in the settings menu
    :param orientation: str; width/heigth, depending on what is bigger
    :param zustand: str; start/ingame/settings, what the program is currently doing
    """
    for button in start_buttons:  # goes through the start buttons
        button.change_intention(task_number, orientation, zustand)  # refreshes its intention
    for button in end_buttons:  # goes through the in game buttons
        button.change_intention(task_number, orientation, zustand)  # refreshes its intention


def _refresh_content_b_writing(language):
    """
    refreshes the writings' contents

    :param language: str; language the program is currently displaying its writing in
    """
    for onewriting in button_writings_start:  # goes through the start buttons' writings
        onewriting.refresh_content(language)  # refreshes the writing's content
    for onewriting in button_writings_end:  # goes through the in game buttons' writings
        onewriting.refresh_content(language)  # refreshes the writing's content


def refresh_buttons(task_number, orientation, language, zustand):
    """
    refreshes the buttons' contents
    :param task_number: int; number of the task the menu has to fulfill
    :param orientation: str; width/height, depending on what is bigger
    :param language: str; language the program is currently running in
    :param zustand: str; start/ingame/settings, what the program is currently doing
    """
    _refresh_intention_buttons(task_number, orientation, zustand)  # refreshes intention of buttons
    _refresh_content_b_writing(language)  # refreshes the content shown on the buttons


def change_button_color(writing_color, bg_color):
    """
    refreshes start button's colors

    :param writing_color: tup(int, int, int); new writing color for the buttons
    :param bg_color: tup(int, int, int); new background color for the buttons
    """
    for button in start_buttons:  # goes through every start button
        button.color = bg_color  # refreshes its background color
    for local_writing in button_writings_start:  # goes through every start writing
        local_writing.color = writing_color  # refreshes its color


# -------
# shows buttons on screen
def draw_buttons(screen):
    """
    shows buttons on screen

    :param screen: Surface; surface covering the whole window
    """
    for button in start_buttons:  # goes through every start button
        if button.active:
            button.draw(screen)  # shows the button
    for button in end_buttons:  # goes through every start button
        if button.active:
            button.draw(screen)  # shows the button
    for onewriting in button_writings_start:  # goes through every start writing
        if onewriting.active:
            onewriting.draw(screen, True)  # shows the writing
    for onewriting in button_writings_end:  # goes through every in game writing
        if onewriting.active:
            onewriting.draw(screen, True)  # shows the writing


def draw_request_buttons(screen):
    """
    shows request buttons on screen, used when program asks a question

    :param screen: Surf; surface that covers the whole window
    """
    for button in request_buttons:  # goes through every request button
        button.draw(screen)  # shows that button
    for onewriting in button_writings_request:  # goes through every request button's writing
        onewriting.draw(screen, True)  # shows that writing


# ------
# returns the buttons
def get_buttons():
    """
    returns start and in game buttons
    :return: list[list[Button, ...], list[Button, ...]; lists with all buttons
    """
    return start_buttons, end_buttons


def get_request_buttons():
    """
    returns request buttons
    used to determine a click on them while request loop is running

    :return: list[Button, Button]; list with request buttons
    """
    return request_buttons
