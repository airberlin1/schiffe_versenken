"""module making things visible for user"""

# TODO ships as pictures
# TODO animate hits

# -------
# imports pygame, used to display things
# and modules displaying things
import time  # wait 3 seconds in end screen
import pygame  # display things
from pygame.locals import *  # constants used in pygame
from constants import DARKGREEN, DARKRED, BLACK  # colors used
import buttons as bu  # display buttons
import playfield as pf  # dispaly boards
import slider as sl  # display sliders
import chat as ch  # display chat
import tables as ta  # display table


# ------
# returns sizes
def get_screen_size_full_screen():
    """
    :return: list[int, int]; width, height in full screen
    """
    display_info = pygame.display.Info()
    height = display_info.current_h  # gets display's height
    width = display_info.current_w  # gets display's width
    return width, height  # returns display's size


def get_window_size(width, height):
    """
    calculates size of one virtual field and orientation

    :param width: int; window's width
    :param height: int; window's height
    :return: list[int, int, float, str]; window's height, window's width, size  of one virtual field, orientation
    """
    if height > width:  # window's height is bigger than its width
        field_size = width / 22  # updates size if one virtual field
        orientation = "height"  # updates orientation
    else:  # window's width is bigger than its height
        field_size = height / 20  # updates size of one virtual field
        orientation = "width"  # updates orientation
    return height, width, field_size, orientation  # returns values


def set_screen_size(width, height):
    """
    updates window's size, used when window's size has been adjusted

    :param width: int; new width
    :param height: int; new height
    """
    # updates both values
    global global_width
    global global_height
    global_width = width
    global_height = height


def get_screen_size():
    """
    :return: list[int; int]; wwindow's size
    """
    return global_width, global_height


def get_small_field_count():
    """
    :return: list[int; int]; number of tiles on one board
    """
    return pf.get_big_fields()[0].field_count_x, pf.get_big_fields()[0].field_count_y


def _init_window(resource_path, language):
    """
    initializes the window the game is played in

    :param resource_path: Func, returns a path to pictures and sounds
    :param language: str; language all texts are currently displayed in
    """
    global g_screen
    try:
        icon = pygame.image.load(resource_path("assets/images/icon.jpg"))  # loads icon
    except pygame.error:  # file is not found
        ch.add_missing_message("icon.jpg", resource_path("assets/images/"), language)
    else:  # file is found
        pygame.display.set_icon(icon)  # creates an icon
    pygame.display.set_caption("schiffe_versenken      v.alpha.4")  # creates a caption
    g_screen = pygame.display.set_mode(get_screen_size(), resizable)


# -------
# initializes visible things
def __init__chat():
    pygame.init()
    field_size, orientation = 50, "height"
    ch.__init__chat(field_size, orientation)  # initializes chat


def __init__visual_output(resource_path, language, color_writing_start, sound_volume, music_volume, bu_bg_color):
    """
    initializes game window and buttons

    :param resource_path: Func; returns a resource path to a relative path
    :param language: str; language all texts are currently displayed in
    :param color_writing_start: tup(int, int, int); color of start buttons' writings
    :param sound_volume: float; 0-1, volume the sounds are currently played in
    :param music_volume: float; 0-1, volume the music is currently playing in
    :param bu_bg_color: tup(int, int, int); background color of start buttons
    """
    global resizable
    global space_new
    global ocean_new
    global drawn_new
    space_new = drawn_new = ocean_new = True
    resizable = pygame.constants.FULLSCREEN  # starts game in full screen
    color_writing_end_b = (125, 125, 255)  # sets color on end buttons to blue
    set_screen_size(get_screen_size_full_screen()[0], get_screen_size_full_screen()[1])  # sets size of window
    _init_window(resource_path, language)  # initializes the window the game is played in
    field_size, orientation = get_window_size(global_width, global_height)[2:]  # gets size of one virtual field
    # initializes buttons
    bu.__init__buttons(language, color_writing_start, color_writing_end_b, field_size, bu_bg_color)
    sl.create_slider(field_size, sound_volume, music_volume)  # intializes slider
    ta.create_stats_table(field_size, resource_path)  # creates stats table


def __init__playfield(resource_path, load, language, orientation="height", add_dir="", field_count_x=10,
                      field_count_y=10):
    """
    creates boards in playfield module and remaining ships table in tables module

    :param resource_path: Func; returns resource path to a relative path
    :param load: bool; game is loaded and not newly created
    :param orientation: width/height depending on what is bigger
    :param add_dir: str; additional directory where loaded game is found
    :param field_count_x: int; number of tiles per board in horizontal direction
    :param field_count_y: int; number of tiles per board in vertical direction
    """
    field_size = get_window_size(global_width, global_height)[2]  # gets size of one virtual field
    # initializes board
    pf.__init__playfield(load, language, orientation, field_size, field_count_x, field_count_y, resource_path, add_dir)
    ta.create_remainings_table(field_size)  # initializes table displaying remaining ships


def create_request_buttons(bg_color, writing_color, language):
    """
    creates request buttons labeled with 'New Game' and 'Load Game'

    those buttons are used once after the beginning and before the actual game start

    :param bg_color: tup(int, int, int); color of the buttons' backgrounds
    :param writing_color: tup(int, int, int); writings' colors
    :param language: str; language the program currently displays all writing in
    """
    bu.create_request_buttons(get_window_size(global_width, global_height)[2], bg_color, writing_color, language)
    bu.create_placement_buttons(get_window_size(global_width, global_height)[2], language)


# -------
# displays all visible things
def _draw_background(screen, background, resource_path, language):
    """
    displays background

    :param screen: Surface; surface covering the whole window
    :param background: str; picture displayed as background
    :param resource_path: Func; returns the full resource path when given a relative path
    :param language: str; language all texts are currently dispalyed in
    """
    global ocean_new
    global space_new
    global drawn_new
    if background == "ocean":
        try:
            bg = pygame.image.load(resource_path("assets/images/ocean.jpg"))  # loads ocean picture
        except pygame.error:  # picture flle is not found
            if ocean_new:
                ch.add_missing_message("ocean.jpg", resource_path("assets/images/"), language)
                ocean_new = False
    elif background == "space":
        try:
            bg = pygame.image.load(resource_path("assets/images/space.jpg"))  # loads space picture
        except pygame.error:  # picture file is not found
            if space_new:
                ch.add_missing_message("space.jpg", resource_path("assets/images/"), language)
                space_new = False
    else:  # background == "drawn"
        try:
            bg = pygame.image.load(resource_path("assets/images/drawn.jpg"))  # loads ugly picture
        except pygame.error:  # pictue file is not found
            if drawn_new:
                ch.add_missing_message("drawn.jpg", resource_path("assets/images/"), language)
                drawn_new = False
    try:
        screen.blit(bg, (0, 0))  # displays loaded picture
    except NameError:  # loading a picture failed
        screen.fill(BLACK)  # fills screen black


def _draw_ships(ship, screen, field_size, orientation, zustand):
    """
    displays all ships

    :param zustand: str; start/ingame/settings, loop the program is curretnly in
    :param ship: list[list[Ship, ...], list]; lsit with all ships
    :param screen: Surface; surface covering the whole window
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height depending on what is bigger
    """
    if zustand == "ingame" or zustand == "placement":  # game is currently played and boards are displayed
        # gets number of tiles per board
        small_field_count_x, small_field_count_y = pf.get_small_fieldcounts()
        for shiplist in ship:
            for realship in shiplist:  # goes through every ship
                # displays it
                realship.draw(screen, field_size, orientation, small_field_count_x, small_field_count_y, zustand)


def draw_screen(zustand, background, language, ship, resource_path, task_number=-1):
    """
    displays all visible things on the game window

    used in every occasion when window is changed except for request screens

    :param zustand: str; start/ingame/settings, loop the program is curretnly in
    :param background: str; picture currently used as background
    :param language: str; language all texts are currently displayed in
    :param ship: list[list[Ship, Ship, ...], list]; list with all ships on the board
    :param resource_path: Func; returns the full resource path when given a relative path
    :param task_number: int; number referring to curretn task, for example volume
    """
    screen = g_screen
    screen.fill((0, 0, 0))  # fills the screen black
    field_size, orientation = get_window_size(global_width, global_height)[2:]  # gets values

    _draw_background(screen, background, resource_path, language)  # displays background
    _draw_ships(ship, screen, field_size, orientation, zustand)  # displays ships
    pf.draw_playfield(screen, field_size, zustand)  # displays board
    ch.draw_chat(screen, zustand)  # shows the chat
    if orientation == "width" and zustand == "ingame":  # game is currently played
        ta.draw_remainings(language, screen, ship)  # shows remaining ships table
    if task_number == 9:  # stats option in menu has been selected
        ta.draw_stats(language, screen)  # shows stats
    bu.refresh_buttons(task_number, orientation, language, zustand)  # updates buttons' writings
    bu.draw_buttons(screen)  # displays buttons
    sl.refresh_slides(task_number)  # refreshes active of slides
    sl.draw_slides(screen, field_size)  # displays sliders on the GUI
    pygame.display.flip()  # updates display to display displayed things


def draw_ship_placement(zustand, language, background, resource_path, ship):
    """
    displays player's board and player's ships

    :param zustand: str; ingame/placement
    :param language: str; language all texts are currently dispalyed in
    :param background: str; currently used background picture
    :param resource_path: Func; returns a resource path to a relative path
    :param ship: list[list[Ship, ...], ...]; list containing all ships
    """
    screen = g_screen
    field_size, orientation = get_window_size(global_width, global_height)[2:]
    _draw_background(screen, background, resource_path, language)  # displays background
    _draw_ships(ship, screen, field_size, orientation, zustand)  # displays ships
    pf.draw_playfield(screen, field_size, zustand, True)  # displays board
    bu.draw_placement_buttons(screen)  # displays button
    pygame.display.flip()  # updates display to display displayed things


def draw_request(writing_color):
    """
    draws a request screen, currently only used to request for a game load

    :param writing_color: tup(int, int, int); current writing_color of used theme
    """
    screen = g_screen
    screen.fill(writing_color)  # fills the screen with the writing_color
    bu.draw_request_buttons(screen)  # draws the buttons
    pygame.display.flip()


def draw_end(winner, resource_path, language):
    """
    shows the end screen

    :param winner: int; player who won the game, 1 is the enemy and 0 is the player
    :param resource_path: Func; return teh reource path of a relative path
    :param language: str; language all texts are currently displayed in
    """
    try:
        sound = pygame.mixer.Sound(resource_path("assets/sounds/windowsxp.wav"))  # gets windows xp shut down sound
    except FileNotFoundError:  # sound file is not found
        ch.add_missing_message("windowsxp.wav", resource_path("assets/sounds/"), language)
    else:  # sound file is found
        sound.play()  # plays windows xp shut down sound
    if winner == 1 or winner == 0:  # checks, whether a winner was determined
        screen = pygame.display.set_mode((0, 0), FULLSCREEN)  # sets new surface
        field_size = get_window_size(global_width, global_height)[2]  # gets size of one virtual field
        screen.fill((0, 0, 0))  # draws a black background
        if winner == 0:  # player has won
            screen.blit(pygame.font.SysFont(None, int(field_size * 3)).render("You won!!!", False, DARKGREEN),
                        (field_size * 3, field_size * 5))  # shows "You won!!!" in green
        elif winner == 1:  # enemy has won
            screen.blit(pygame.font.SysFont(None, int(field_size * 3)).render("You lost :´(", False, DARKRED),
                        (field_size * 3, field_size * 5))  # shows "You lost :´(" in red
        pygame.display.flip()  # updates the window
    time.sleep(3)  # waits 3 seconds


# -------
# updates locations of visible things
def refresh_loc_coords(field_size, orientation, zustand):
    """
    refreshes the locations of visible things shown in the GUI

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :param zustand: str; ingame/start/settings, depending on what the program is doing
    """
    if zustand == "ingame":  # game is currently played
        pf.refresh_loc_small_fields(field_size, orientation)  # refreshes the small-fields' coordiantes
        pf.refresh_loc_big_fields(field_size, orientation)  # refreshes the big-fields' coordiantes
        pf.refresh_loc_writings(field_size, orientation)  # refreshes the writings' coordinates
        ch.refresh_loc(field_size, orientation)  # refreshes the chat's coordinates
        ta.refresh_loc(field_size)  # refreshes table's coordinates
    bu.refresh_loc_buttons(field_size, orientation, zustand)  # refreshes the buttons' coordinates
    bu.refresh_loc_writing(field_size, zustand)  # refreshes the button-writings' coordinates
    sl.refresh_loc_sliders(field_size)  # refreshes the sliders' coordiantes


def set_windowed(l_resizable, resource_path, language):
    """
    updates to game to either be windowed or fullscreen
    :param l_resizable: int; pg.FULLSCREEN or pg.RESIZABLE
    :param resource_path: Func; returns a resource path to a relative path
    :param language: str; language all texts are curently displayed in
    """
    global resizable  # global variable keeping ttrack of window type
    pygame.display.quit()  # closes window
    resizable = l_resizable  # updates window's attribute
    _init_window(resource_path, language)  # opens a new window with updated attribute


def unclick(field):
    """
    unclicks a field
    :param field: list[int, int]; coordiantes of the field
    """
    pf.unclick(field)


def change_button_color(writing_color, bg_color):
    """
    updates in game buttons' appearance

    :param writing_color: tup(int, int, int); new writing color for the buttons
    :param bg_color: tup(int, int, int); new background color for the buttons
    """
    bu.change_button_color(writing_color, bg_color)


def get_small_fields():
    """
    returns the boards' tiles
    :return: list[list[SmallField, ...], list, ...]; list with the small fields
    """
    return pf.get_small_fields()


def get_buttons():
    """
    returns start and in game buttons
    :return: list[list[Button, ...], list[Button, ...]; list with all buttons
    """
    return bu.get_buttons()


def get_request_buttons():
    """
    returns request buttons
    used to determine a click on them while request loop is running

    :return: list[Button, Button]; list with request buttons
    """
    return bu.get_request_buttons()


def get_placement_buttons():
    """
    returns placement buttons
    used to determine a click on them while placement loop is running

    :return: list[Button, Button]; list with placement buttons
    """
    return bu.get_placement_buttons()


def get_slides():
    """"
    :return: list[Slider, Slider]; lsit with volume sliders, used to determine change to volume
    """
    return sl.get_sliders()


def save_playfield(resource_path, language, add_dir):
    """
    saves the playfield, used to continue games after closing the program

    :param resource_path: Func; returns the resource path to a relative path
    :param language: language all texts are currently displayed in
    :param add_dir: str; additional directory where loaded game is found
    """
    pf.save_playfield(resource_path, language, add_dir)
