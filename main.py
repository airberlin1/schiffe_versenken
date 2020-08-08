# main module

# ------
# import of neccessary modules
import logic as lg  # game logic, button execution
import ship as sh  # ships and ship interaction
import enemy as en  # enemy and its moves
import player as pl  # player and move control
import chat
from player import get_angeklicktes_feld as gaf  # shortening function name to fit into character limit
import visual_output as vo  # visual outout, managing of buttons and playfield
from playfield import hit_small_field  # hits one field
from translation import get_dict
import pygame as pg  # used for GUI and input management
from pygame.locals import *  # constants inputs are compared to
import time  # used to slow enemy's moves
import sys  # used to quit the program and get resource paths
import os  # used to get resource paths
"""
main module for battleship application
"""


def resource_path(relative_path):
    """
    returns a resource path to a relative path

    :param relative_path: str; realtive path such as 'assets/images/space.jpg'
    :return: str; resource path such as 'C:\\folder\\assets/images/space.jpg'
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ------
# intialize program
def _play_music(volume):
    """
    plays the background music

    :param volume: float; volume of the music between 0 and 1
    """
    global channel5
    global music
    channel5 = pg.mixer.Channel(4)  # chooses a channel
    try:
        music = pg.mixer.Sound(resource_path("assets/music/deepblue.wav"))  # gets the music
    except FileNotFoundError:
        chat.add_missing_message("deepblue.wav", resource_path("assets/music/"), lg.get_language())
    else:
        music.set_volume(volume)  # sets the sound of the music
        channel5.play(music, loops=-1)  # plays the music


def __init__main(aufgabe):
    """
    # initializes main module

    :param aufgabe: str; current task the program has to solve
    """
    global player
    if aufgabe == "start":  # program is currently starting
        # sets variables used to control game and settings loops
        player = 0  # sets player to 0, which is the player
        pg.mixer.init()  # initializes sound output
        _play_music(lg.get_music_volume())  # plays music


# ------
# execution of enemy's move
def _get_play_list_enemy():
    """
    !!not used currently!!
    returns next move of enemy
    :return: list[int, int]; next enemy's move's coordinates
    """
    try:
        # gets the next move of the enemy
        next_play = en.get_play_list()[0]
    except IndexError:
        # creates a random field instead
        next_play = [en.get_random_field(vo.get_small_field_count()[0], vo.get_small_field_count()[1])]
    return next_play  # returns coordinates of next enemy's move


def _get_check_hit(next_play):
    """
    !!not used currently!!
    checks whether next move is hitting
    :param next_play: list[int, int]; next move of enemy
    :return: int; number of hit ship if one was hit
    """
    try:
        # checks whether a ship was hit
        return sh.check_hit(1, next_play)[1]  # returns hit ship's numebr
    except IndexError:
        return -1  # returns -1 as control number
    except TypeError:
        return -1  # returns -1 as control number


def _do_enemy_move():
    """
    executes enemy's move
    """
    old_xcoord, old_ycoord, hit = en.get_enemy_move()  # gets the old and new move from the enemy
    sh.hit_something(hit[0], hit[1], 1, resource_path, lg.get_sound_volume(), lg.get_language(), old_xcoord,
                     old_ycoord)  # hits a field

    if lg.get_rule() == 2:  # number of ships determined by proceeding hits
        for x in range(sh.get_ship_count()):  # checks whether a ship has been used
            if sh.check_ship_pos(sh.get_ship()[0][x], hit)[0]:
                set_player(1)  # executes another enemy's move

    elif lg.get_rule() == 3:  # number of ships determines number of shots per move
        # TODO get number of ships, use sh.check_ship_status?
        pass


def set_player(play):
    """
    refreshes current palyer and executes enemy's move

    :param play: int; which player has to complete a move next (0 player, 1 enemy)
    """
    global player
    player = play  # refreshes current player
    if player == 1:  # checks whether this is the enemy's move
        # displays the game on the game window
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                       lg.get_task_number())
        time.sleep(2)  # waits 2 seconds to simulate the enemy thinking
        _do_enemy_move()  # executes enemy's move
        # displays the game on the game window
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                       lg.get_task_number())
    player = 0  # sets the player back to the player


# ------
# executing player controlled move
def do_hit_player_input(xcoord_local, ycoord_local):
    """
    does a hit enforced by a player input

    :param xcoord_local: int; x coordinate of the hit
    :param ycoord_local: int; y coordiante of the hit
    """
    if pl.change_hit_list(xcoord_local, ycoord_local):  # changes the list with hit fields
        # hits something on the coordiantes of the hit
        sh.hit_something(xcoord_local, ycoord_local, 0, resource_path, lg.get_sound_volume(), lg.get_language())
        set_player(1)  # executes enemy's move and sets the player back to the player
    else:
        # displays a system message saying that the field was already targeted before
        dictionary = get_dict(lg.get_language(), "message")  # gets dictionary
        message = dictionary["System"] + dictionary["againhit"]  # translates message
        chat.add_message(message, (50, 50, 0))  # displays message


# ------
# saves the game
def save_game():
    """
    saves the game to the saves directory
    """
    en.save_enemy(resource_path, lg.get_language())  # saves the remaining moves of the enemy
    pl.save_player(resource_path, lg.get_language())  # saves already targeted fields
    sh.save_ship(resource_path, lg.get_language())  # saves the ships
    vo.save_playfield(resource_path, lg.get_language())  # saves the playfield
    # shows confirmation in chat
    dictionary = get_dict(lg.get_language(), "message")  # gets dictionary for translation
    chat_message = dictionary["System"] + dictionary["save"]  # translates message
    chat.add_message(chat_message, (50, 50, 0))  # displays message


def begins(begin, request, running, settings, win, again):
    while begin and lg.get_zustand() != "end":

        for event in pg.event.get():  # goes through every input occuring while game window is in focus

            if event.type == MOUSEBUTTONDOWN:  # mouse button was clicked
                # gets size of one field and orientation
                field_size, orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2:]
                # executes feature of pressed button if there is one
                button = lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_buttons()[0], resource_path)
                if button == "end":
                    begin = settings = running = request = again = False
                # displays the menu on the game window
                if lg.get_zustand() != "ingame":
                    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]], resource_path,
                                   lg.get_task_number())

            elif event.type == VIDEORESIZE:  # window size has been adjusted
                vo.set_screen_size(event.size[0], event.size[1])  # refreshes window size
                # refreshes location of visible assets and the game itself
                vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                      vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]], resource_path,
                               lg.get_task_number())

            elif event.type == pg.QUIT:  # window was closed
                # ends the program
                running = begin = settings = request = again = False
                win = 2

        if lg.get_zustand() == "ingame":  # game has been started
            begin = False  # starts the game
        try:
            music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing
        except NameError:
            pass
    return request, running, settings, win, again


def request_load(request, running, settings, win, again):
    load = False
    # creates request buttons
    vo.create_request_buttons(lg.get_background_color_start(), lg.get_writing_color_start(), lg.get_language())
    # displays the request screen
    if request:
        vo.draw_request(lg.get_writing_color_start())
    while request:

        for event in pg.event.get():  # goes through every input occuring while game window is in focus

            if event.type == MOUSEBUTTONDOWN:  # mousebutton was clicked
                # gets size of one field and orientation
                field_size, orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2:]
                load = lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_request_buttons(),
                                          resource_path)
                if load != -1:  # ends the request loop if one button is hit
                    request = False

            elif event.type == pg.QUIT:  # window was closed
                # ends the program
                settings = again = request = running = False
                win = 2
    return load, running, settings, win, again


def load_game(load):
    check_list = [True]
    while True in check_list:
        if check_list.__len__() > 1:
            load = False
            dictionary = get_dict(lg.get_language(), "message")
            message = dictionary["System"] + dictionary["loadingfailure"]
            chat.add_message(message, (50, 50, 0))
        check_list = []
        check_list.append(pl.__init__player(load, resource_path, lg.get_language()))  # intializes player
        # initializes ship
        check_list.append(sh.__init__ship(load))
        check_list.append(sh.set_ships(load, resource_path, lg.get_language()))
        # initializes playfield
        check_list.append(vo.__init__playfield(resource_path, load, lg.get_language(),
                                               vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3]))
        try:
            check_list.append(en.__init__enemy(load, lg.get_language(), resource_path, 10,
                                            10,
                                            sh.get_ship_positions(), lg.get_difficulty(),
                                            sh.get_ship()))  # initializes enemy
        except NameError:
            pass


def setting(settings, running, win, again):
    num = 0
    other_num = 0
    while settings and lg.get_zustand() != "end":

        for event in pg.event.get():  # goes through every input occuring while game window is in focus

            if event.type == MOUSEBUTTONDOWN:  # mouse button was clicked
                # gets size of one virtual field
                field_size, orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2:]
                # executes feature of pressed button if there is one
                button = lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_buttons()[0], resource_path)
                if button == "end":
                    settings = running = False
                    win = 1
                if lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
                    for slider in vo.get_slides():  # goes through every slider
                        try:
                            if slider.button_rect.collidepoint(event.pos):  # checks whether the slider is pressed
                                slider.hit = True  # sets hit to true, so that it will be moved
                        except AttributeError:
                            pass
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())
                other_num = num  # refreshes control number used to fix bug with sliders

            elif event.type == MOUSEBUTTONUP and num != other_num + 1:  # checks whether a mouse button was lifted
                for slider in vo.get_slides():  # goes through every slider
                    slider.hit = False  # sets hit to false, so that it won't be moved
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == VIDEORESIZE:  # window size has been adjusted
                vo.set_screen_size(event.size[0], event.size[1])  # refreshes window size
                # refreshes location of visible assets and the game itself
                vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                      vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == pg.QUIT:  # ueberprueft, ob das Fenster geschlossen wurde
                # ends the program
                settings = running = again = False
                win = 2

        if lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
            for slider in vo.get_slides():  # goes through every slider
                if slider.hit:  # checks, whether it is hit
                    # moves the slider and thus changes the value of it
                    slider.move(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2])
                    # displays the volume settings on the game window
                    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                                   resource_path, lg.get_task_number())

        if lg.get_zustand() == "ingame":  # game has been started
            settings = False  # continues the game
            running = True
        # continues counting, used to fix a bug instantly having a mousebuttonup event after mousebuttondown
        num += 1
        if num > 254:
            num = 0

        try:
            music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing
        except NameError:
            pass
    return settings, running, win, again


def game(settings, running, win, again):
    while running:
        running, win = sh.check_ship_status()  # checks whether all ships of one player have been destroyed
        for event in pg.event.get():  # goes through every input occuring while game window is in focus

            if event.type == MOUSEBUTTONDOWN:  # button on mouse was pressed
                # gets the size of one virtual field
                field_size = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2]
                button = lg.do_button_mouse_ingame(event.pos[0], event.pos[1], field_size, vo.get_buttons()[1],
                                                   gaf(), resource_path, save_game)
                try:
                    # gets coordiantes of the clicked field, whether a field was hit, and the hit field
                    xcoord, ycoord, hit_check, xcoord_2, ycoord_2 = button
                except ValueError:
                    # instead puts control values for hit fields if none were hit
                    xcoord, ycoord, hit_check, xcoord_2, ycoord_2 = (-1, -1, False, -1, -1)
                    if button == "end":
                        settings = running = False
                        win = 1
                    elif button == "settings":
                        running = False
                        settings = True
                        lg.set_aufgabe("main")
                        lg.set_zustand("settings")
                except TypeError:
                    # instead puts control values for hit fields if none were hit
                    xcoord, ycoord, hit_check, xcoord_2, ycoord_2 = (-1, -1, False, -1, -1)

                if hit_check:
                    # executes hit if a field was hit
                    do_hit_player_input(xcoord_2, ycoord_2)
                if -1 not in pl.get_last_click():  # checks for control value
                    vo.unclick(pl.get_last_click())  # unclicks previously clicked field
                pl.set_angeklicktes_feld(xcoord, ycoord)  # refreshes clicked field
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == KEYDOWN:  # button on keyboard was pressed
                if event.key == K_ESCAPE:  # escape button was pressed
                    settings = True
                    running = False
                    lg.set_zustand("settings")
                    lg.set_aufgabe("main")
                else:
                    try:
                        # gets coordinates of the selected field
                        xcoord, ycoord = lg.do_button_ingame_keyboard(event.key, resource_path)
                    except TypeError:
                        # sets coordinates to -1 when no field is selected yet
                        xcoord, ycoord = -1, -1

                    if xcoord != -1 and ycoord != -1:
                        # clicks a new field
                        hit_small_field(1, xcoord, ycoord, resource_path, lg.get_sound_volume(), lg.get_language())
                        do_hit_player_input(xcoord, ycoord)  # hits a field from a player input
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == VIDEORESIZE:  # checks whether the size of the window got adjusted
                vo.set_screen_size(event.size[0], event.size[1])  # refreshes window size
                # refreshes location of visible assets and the game itself
                vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                      vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == pg.QUIT:  # checks whether the wndow has been closed
                # ends the program
                settings = running = again = False
                win = 2  # sets win to 2, what is used to mark that no player has won the game

    return settings, running, win, again


def ingame(settings, running, win, again):
    while settings or running:
        # ------
        # settings
        settings, running, win, again = setting(settings, running, win, again)

        # ------
        # game itself
        settings, running, win, again = game(settings, running, win, again)

    return win, again


def main():
    # ------
    # inititalizing program
    again = True
    while again:
        begin = running = request = True
        settings = False
        win = 2
        vo.__init__chat()
        lg.__init__logic(resource_path)  # intializes logic
        vo.__init__visual_output(resource_path, lg.get_language,
                                 lg.get_writing_color_start(), lg.get_sound_volume(),
                                 lg.get_music_volume(), lg.get_background_color_start())  # initializes visual output
        __init__main(lg.get_zustand())  # initializes main module
        # displays the menu on the game window
        vo.refresh_loc_coords(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                              vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3], lg.get_zustand())
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]], resource_path,
                       lg.get_task_number())

        # ------
        # start, settings
        request, running, settings, win, again = begins(begin, request, running, settings, win, again)

        # ------
        # requests, whether game should be loaded or a new one should be created

        load, running, settings, win, again = request_load(request, running, settings, win, again)
        load_game(load)  # loads game
        vo.refresh_loc_coords(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                              vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3], lg.get_zustand())
        # displays the menu on the game window
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                       lg.get_task_number())

        # ------
        # game loop
        win, again = ingame(settings, running, win, again)

        vo.draw_end(win, resource_path, lg.get_language())  # shows an end screen if a winner is determined
    # ------
    # end of program
    channel5.stop()  # stops the music
    pg.mixer.quit()  # closes all sound channels
    pg.quit()  # closes the window
    sys.exit()  # ends the program


if __name__ == '__main__':  # prevents activation by import
    main()
