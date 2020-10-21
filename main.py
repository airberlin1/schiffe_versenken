# main module
# TODO fix imports where possible
# ------
# import of neccessary modules
import logic as lg  # game logic, button execution
import ship as sh  # ships and ship interaction
import enemy as en  # enemy and its moves
import player as pl  # player and move control
import chat  # displays errors
import save  # updates stats
from player import get_angeklicktes_feld as gaf  # shortening function name to fit into character limit
import visual_output as vo  # visual outout, managing of buttons and playfield
from playfield import hit_small_field  # hits one field
from translation import get_dict  # transates errors
from constants import DIFFICULTIES, STATS
import pygame as pg  # used for GUI and input management
from pygame.locals import *  # constants inputs are compared to
import time  # used to slow enemy's moves/to get time palyed for stats
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
    global move
    global gwon
    global glost
    global start_time
    move = []
    gwon = []
    glost = []
    start_time = []
    for _ in DIFFICULTIES:
        move.append(0)
        gwon.append(0)
        glost.append(0)
        start_time.append(0)
    if aufgabe == "start":  # program is currently starting
        # sets variables used to control game and settings loops
        player = 0  # sets player to 0, which is the player
        pg.mixer.init()  # initializes sound output
        _play_music(lg.get_music_volume())  # plays music


# ------
# displays system messages
def add_system_message(message):
    """
    adds a system message to be displayed in chat
    :param message: str; message that i sdisplayed
    """
    dictionary = get_dict(lg.get_language(), "message")  # gets the correcct dictionary to translate message
    message = dictionary["System"] + dictionary[message]  # translates message
    chat.add_message(message, (50, 50, 0))  # displays message in dark yellow


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
    global move
    player = play  # refreshes current player
    if player == 1:  # checks whether this is the enemy's move
        move[get_dif_number()] += 1
        # displays the game on the game window
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                       lg.get_task_number())
        time.sleep(0.75)  # waits 2 seconds to simulate the enemy thinking
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
        add_system_message("againhit")


# ------
# saves the game/stats
def save_game():
    """
    saves the game to the saves directory
    """
    en.save_enemy(resource_path, lg.get_language(), lg.get_difficulty() + "/")  # saves the remaining moves of the enemy
    pl.save_player(resource_path, lg.get_language(), lg.get_difficulty() + "/")  # saves already targeted fields
    sh.save_ship(resource_path, lg.get_language(), lg.get_difficulty() + "/")  # saves the ships
    vo.save_playfield(resource_path, lg.get_language(), lg.get_difficulty() + "/")  # saves the playfield
    add_system_message("save")  # shows confirmation in chat


def update_stats(games, won, lost, moves, hit, destroyed, time_spent):
    """
    updates stats when stats are looked up ore game is closed

    :param games: int; games played since stats have been updated
    :param won: int; games won since stats have been updated
    :param lost: int; games lost since stats have been updated
    :param moves: int; moves done since stats have been updated
    :param hit: int; ships hit since stats have been updated
    :param destroyed: int; ships destroyed since stats have been updated
    :param time_spent: int; time spent since stats have been updated in minutes
    """
    stat_vals = [games, won, lost, time_spent, moves, hit, destroyed]  # new stats
    count = 0
    for difficulty in DIFFICULTIES:  # goes through all difficulties
        for i in range(7):  # goes through all stats
            stat_val = save.load("int", STATS[i], 1, resource_path, "stats/" + difficulty)  # loads stat's value
            stat_val += stat_vals[i][count]  # adds new value
            save.save(stat_val, "int", STATS[i], 1, resource_path, "stats/" + difficulty)  # saves updated value
        count += 1


def update_statistics():
    """updates stats from main module"""
    global start_time
    global gwon
    global glost
    global move
    global game
    hits, destroyed = sh.get_hit_des()  # gets stats handled in ship module
    spent_time = []
    count = 0
    for difficulty in DIFFICULTIES:  # goes through difficulties
        spent_time.append(0)
        if difficulty[:-1] == lg.get_difficulty() and lg.get_zustand() != "start":  # current difficulty
            spent_time[count] = int(time.time() / 60) - start_time[count]  # calculates spent time since last update
        else:
            spent_time[count] = 0
        count += 1
    # updates stats
    update_stats(moves=move, hit=hits, destroyed=destroyed, time_spent=spent_time, won=gwon, lost=glost, games=game)
    # resets stats
    move = []
    gwon = []
    glost = []
    game = []
    start_time = []
    for _ in DIFFICULTIES:
        move.append(0)
        gwon.append(0)
        glost.append(0)
        game.append(0)
        start_time.append(int(time.time() / 60))  # resets time


def get_dif_number():
    """returns difficulty's index"""
    count = 0
    for difficulty in DIFFICULTIES:
        if difficulty[:-1] == lg.get_difficulty():
            return count
        count += 1


# ------
# loops
def video_resize(size, ship=[[[0]]], draw=True):
    vo.set_screen_size(size[0], size[1])  # refreshes window size
    # refreshes location of visible assets and the game itself
    vo.refresh_loc_coords(vo.get_window_size(size[0], size[1])[2],
                          vo.get_window_size(size[0], size[1])[3], lg.get_zustand())
    if draw:
        # displays the menu on the game window
        vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), ship, resource_path,
                       lg.get_task_number(), lg.get_settings())


def begins(begin, request, running, settings, win, again):
    """
    loop running at the beginning of the game

    shows a menu,
    settings can be changed that impact the next game and are saved for future games

    :param begin: bool; setings loop is running
    :param request: bool; request loop will run
    :param running: bool; game loop will run
    :param settings: bool; settings loop in game will run
    :param win: int; current winner of the game
    :param again: bool; game is repeated from the begin loop to allow for another game to b played
    :return: bool, bool, bool, int, bool; updated bools for loop management
    """
    global start_time
    # displays the menu on the game window
    vo.refresh_loc_coords(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                          vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3], lg.get_zustand())
    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]], resource_path,
                   lg.get_task_number(), lg.get_settings())
    num = 0
    other_num = 0
    while begin and lg.get_zustand() != "end":  # begin loop is running and settings can be changed

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
                                   lg.get_task_number(), lg.get_settings())
                if lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
                    for slider in vo.get_slides():  # goes through every slider
                        try:
                            if slider.button_rect.collidepoint(event.pos):  # checks whether the slider is pressed
                                slider.hit = True  # sets hit to true, so that it will be moved
                        except AttributeError:
                            pass
                    other_num = num  # refreshes control number used to fix bug with sliders

            elif event.type == MOUSEBUTTONUP and num != other_num + 1:  # checks whether a mouse button was lifted
                for slider in vo.get_slides():  # goes through every slider
                    slider.hit = False  # sets hit to false, so that it won't be moved
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]],
                               resource_path, lg.get_task_number(), lg.get_settings())

            elif event.type == VIDEORESIZE:  # window size has been adjusted
                video_resize(event.size)

            elif event.type == pg.QUIT:  # window was closed
                # ends the program
                running = begin = settings = request = again = False
                win = 2

        if lg.get_aufgabe() == "stats":
            update_statistics()
            # displays the statistics on the game window
            vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]],
                           resource_path, lg.get_task_number(), lg.get_settings())
            lg.set_aufgabe("statistics")

        elif lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
            for slider in vo.get_slides():  # goes through every slider
                if slider.hit:  # checks, whether it is hit
                    # moves the slider and thus changes the value of it
                    slider.move(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2])
                    # displays the volume settings on the game window
                    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), [[[0]]],
                                   resource_path, lg.get_task_number(), lg.get_settings())

        # continues counting, used to fix a bug instantly having a mousebuttonup event after mousebuttondown
        num += 1
        if num > 254:
            num = 0

        if lg.get_zustand() == "request":  # game has been started
            begin = False  # starts the game

        try:
            music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing
        except NameError:  # music could not be found
            pass

    return request, running, settings, win, again


def request_load(request, running, settings, win, again):
    """
    displays a request asking to load a game instead of creating a new one

    :param request: bool; request loop is running
    :param running: bool; game loop will be running
    :param settings: bool; in game settings loop will be running
    :param win: int; player that is currently winning the game
    :param again: bool; game will be starting again after this game
    :return: bool, bool, bool, int, bool; updated bools for loop management
    """
    load = False
    random = False
    # creates request buttons
    vo.create_request_buttons(lg.get_background_color_start(), lg.get_writing_color_start(), lg.get_language())
    if request:  # displays the request screen
        vo.draw_request(lg.get_writing_color_start())
    while request:  # request for loading the game

        for event in pg.event.get():  # goes through every input occuring while game window is in focus

            if event.type == MOUSEBUTTONDOWN:  # mouse button was clicked
                # gets size of one field and orientation
                field_size, orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2:]
                load = lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_request_buttons(),
                                          resource_path)
                if load != -1:  # one button is hit
                    request = False  # ends request loop
                    if load == 1:  # ships are randomly set
                        random = True
                        load = False
                    else:  # ships are not set randomly
                        random = False

            elif event.type == pg.QUIT:  # window was closed
                # ends the program
                settings = again = request = running = False
                win = 2
    lg.set_zustand("ingame")
    return random, load, running, settings, win, again


def load_game(load, random):
    """
    loads the game and thus all ships and control lists
    when game is not newly created, skips creation steps and loading from saves instead

    :param load: bool; game is loaded and not newly created
    :param random: bool; ships are set randomly and not by the player
    """
    if load:
        random = True
    check_list = [True]  # creates a check list to prevent a failed loading attempt to break the game
    while True in check_list:  # game has not been loaded successfully yet
        if check_list.__len__() > 1:  # loop is running for a second time, thus loading has failed
            load = False  # game is newly created
            add_system_message("loadingfailure")  # displays system message informing about missing file when loading

        check_list = [  # updates list to check for failed loadings; [False, False, False, False] when successful
            # loads/creates player's check lists
            pl.__init__player(load, resource_path, lg.get_language(), lg.get_difficulty() + "/"),
            sh.__init__ship(load, get_dif_number),  # loads/creates ships
            vo.__init__playfield(resource_path, load, lg.get_language(),  # loads/creaetes board
                                 vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3],
                                 lg.get_difficulty() + "/")
        ]
        # sets ships to corect locations
        if random:
            check_list.append(sh.set_ships(load, resource_path, lg.get_language(), lg.get_difficulty() + "/",
                                           vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2]))
        else:
            sh.set_ships(load, resource_path, lg.get_language(), lg.get_difficulty() + "/",
                         vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                         False)
            return True
        # loads/creates enemy's moves
        check_list.append(en.__init__enemy(load, lg.get_language(), resource_path, 10, 10,
                                           ship_coordinates=sh.get_ship_positions(), ships=sh.get_ship(),
                                           difficulty=lg.get_difficulty(), add_dir=lg.get_difficulty() + "/"))


def ship_placement(settings, again, running, win):
    """
    loop that allows ships to be set to correct location

    :param settings: bool; settings loop is running
    :param again: bool; game will be starting again after this game
    :param running: bool; game loop will be running
    :param win: int; player that is currently winning
    :return: bool, bool, bool, int; updated bools for loop management
    """

    def try_start():
        """
        tries to start the game, only allows start if all ships have been placed
        :return: bool; ship placement continues
        """
        start = True
        for ship_l in sh.get_ship()[0]:  # goes through player's ships
            if not ship_l.placed:  # ship has not been placed yet
                start = False  # game cannot be started
        return bool(1 - int(start))  # returns inverted start

    lg.set_zustand("placement")  # starts placement loop
    video_resize(vo.get_screen_size(), sh.get_ship(), False)  # updates window's size
    vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                           sh.get_ship())  # displays updated window
    place_ships = True  # starts placement loop
    clock = pg.time.Clock()  # initializes clock to limit frames/second
    while place_ships:  # loop for ships' player controlled placements

        for event in pg.event.get():  # goes through all input events

            if event.type == MOUSEBUTTONDOWN:  # button on mouse is pressed*

                for ship in sh.get_ship()[0]:  # goes through player's ships
                    for i, rect in enumerate(ship.rects):  # goes through ship's Rects
                        if rect.collidepoint(event.pos):  # ship was clicked
                            ship.hit = True  # ship is hit
                            ship.placed = False  # ship is not placed
                            ship.hit_tile = i  # updates hit tile

                vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                                       sh.get_ship())  # displays updated placement
                # gets button, important when button was pressed
                button = lg.do_button_mouse_ingame(event.pos[0], event.pos[1],
                                                   vo.get_window_size(vo.get_screen_size()[0],
                                                                      vo.get_screen_size()[1])[2],
                                                   vo.get_placement_buttons(), [-1, -1], resource_path, save_game)

                if button == "start":  # start button was pressed
                    place_ships = try_start()

                elif button == "end":  # abort button was pressed
                    settings = running = place_ships = False  # restarts program

            elif event.type == MOUSEBUTTONUP:  # button on mouse is lifted
                for ship in sh.get_ship()[0]:  # goes through palyer's ships
                    if ship.hit:  # ship is clicked
                        ship.hit = False  # ship is not clicked anymore
                        ship.set_position(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                                          resource_path)  # sets ship to a position on the board or back to default
                vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                                       sh.get_ship())  # dispalys updated ship placement

            elif event.type == KEYDOWN:  # key on keyboard was pressed

                if event.key == K_LEFT or event.key == K_d:
                    # turns ship by 90 degrees to the left
                    for ship in sh.get_ship()[0]:
                        if ship.hit:
                            ship.turn_left()

                elif event.key == K_RIGHT or event.key == K_a:
                    # turns ship by 90 degrees to the right
                    for ship in sh.get_ship()[0]:
                        if ship.hit:
                            ship.turn_right()

                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    place_ships = try_start()  # starts game if all ships have been placed

                vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                                       sh.get_ship())  # updates output

            elif event.type == VIDEORESIZE:  # window's size has been changed
                video_resize(event.size, sh.get_ship(), False)  # updates window's size
                vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                                       sh.get_ship())  # displays updated window

            elif event.type == pg.QUIT:  # game window has been closed
                # ends program
                settings = again = running = place_ships = False
                win = 2

        for ship in sh.get_ship()[0]:
            # goes through player's ships
            if ship.hit:  # ship is clicked on
                # moves ship to current cursor position
                ship.move(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2])
                vo.draw_ship_placement(lg.get_zustand(), lg.get_language(), lg.get_background(), resource_path,
                                       sh.get_ship())  # displays updated ship placement

        clock.tick(40)  # limits frames/seconds to 40

    lg.set_zustand("ingame")  # starts game
    en.__init__enemy(False, lg.get_language(), resource_path, 10, 10,
                     ship_coordinates=sh.get_ship_positions(), ships=sh.get_ship(),
                     difficulty=lg.get_difficulty(), add_dir=lg.get_difficulty() + "/")
    sh.set_ships(False, resource_path, lg.get_language(), lg.get_difficulty() + "/",
                 vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2], normal=True)
    return settings, again, running, win  # returns updated bools for loop management


def setting(settings, running, win, again):
    """
    settings loop in game, allowing for settings to change that only effect the game visually

    :param settings: bool; settings loop is running
    :param running: bool; game loop will be running
    :param win: int; player that is currently winning
    :param again: bool; game will be starting again after this game
    :return: bool, bool, int, bool; updated bools for loop management
    """
    num = 0
    other_num = 0
    while settings and lg.get_zustand() != "end":  # settings loop enabling setting changes in game

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
                               resource_path, lg.get_task_number(), lg.get_settings())
                other_num = num  # refreshes control number used to fix bug with sliders

            elif event.type == MOUSEBUTTONUP and num != other_num + 1:  # checks whether a mouse button was lifted
                for slider in vo.get_slides():  # goes through every slider
                    slider.hit = False  # sets hit to false, so that it won't be moved
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number(), lg.get_settings())

            elif event.type == VIDEORESIZE:  # window size has been adjusted
                video_resize(event.size, sh.get_ship())

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
                                   resource_path, lg.get_task_number(), lg.get_settings())

        elif lg.get_aufgabe() == "stats":
            update_statistics()
            # displays the statistics on the game window
            vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                           resource_path, lg.get_task_number(), lg.get_settings())
            lg.set_aufgabe("statistics")

        if lg.get_zustand() == "ingame":  # game has been started
            settings = False  # continues the game
            running = True
        # continues counting, used to fix a bug instantly having a mousebuttonup event after mousebuttondown
        num += 1
        if num > 254:
            num = 0

        try:
            music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing
        except NameError:  # music has not been found
            pass

    return settings, running, win, again


def game_loop(settings, running, win, again):
    """
    game loop, allowing for game to be played

    :param settings: bool; settings loop will be running
    :param running: bool; game is running
    :param win: int; player that is currently winning
    :param again: bool; game will be starting again after this game
    :return: bool, bool, int, bool; bools for loop management
    """

    def set_settings():
        """
        activates settings loop allowing for visual changes to be made by the user
        """
        # updates bools to start settings loop
        nonlocal settings
        nonlocal running
        running = False
        settings = True
        lg.set_aufgabe("main")  # opens main page in menu
        lg.set_zustand("settings")  # sets current loop to current loop

    while running:  # game loop allowing the game to be played

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
                        set_settings()
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
                               resource_path, lg.get_task_number(), lg.get_settings())
                if running:
                    running, win = sh.check_ship_status()  # checks whether all ships of one player have been destroyed

            elif event.type == KEYDOWN:  # button on keyboard was pressed
                if event.key == K_ESCAPE:  # escape button was pressed
                    set_settings()
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
                               resource_path, lg.get_task_number(), lg.get_settings())
                running, win = sh.check_ship_status()  # checks whether all ships of one player have been destroyed

            elif event.type == VIDEORESIZE:  # checks whether the size of the window got adjusted
                video_resize(event.size, sh.get_ship())

            elif event.type == pg.QUIT:  # checks whether the wndow has been closed
                # ends the program
                settings = running = again = False
                win = 2  # sets win to 2, what is used to mark that no player has won the game

    return settings, running, win, again


def ingame(settings, running, win, again):
    """
    loops that are active in game

    settings loop allowing for visual changes

    game loop allowing game to be played

    :param settings: bool; settings loop is running
    :param running: bool; game loop is running
    :param win: int; player that is currently winning
    :param again: bool; game is datting from beginning after current game ends
    :return: int, bool; updated bool for loop management
    """

    vo.refresh_loc_coords(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2],
                          vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3], lg.get_zustand())
    # displays the menu on the game window
    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                   lg.get_task_number())

    while settings or running:
        # ------
        # settings loop
        settings, running, win, again = setting(settings, running, win, again)

        # ------
        # game loop
        settings, running, win, again = game_loop(settings, running, win, again)

    return win, again


def init_program():
    """
    initializes program's logic, chat and GUI
    """
    vo.__init__chat()  # initializes chat
    lg.__init__logic(resource_path)  # intializes logic
    vo.__init__visual_output(resource_path, lg.get_language,
                             lg.get_writing_color_start(), lg.get_sound_volume(),
                             lg.get_music_volume(), lg.get_background_color_start())  # initializes visual output
    __init__main(lg.get_zustand())  # initializes main module and music


def update_gwon(win):
    """updates statistics after game has ended"""
    global glost
    global gwon
    dif_num = get_dif_number()  # gets difficulty's index
    if win == 0:  # player has won
        gwon[dif_num] += 1
    elif win == 1:  # player has lost
        glost[dif_num] += 1
    update_statistics()  # updates statistics


def loops():
    """
    program managing all loops in another loop
    """
    global game
    global glost
    global gwon
    global start_time
    game = []
    for _ in DIFFICULTIES:
        game.append(0)
    again = True
    while again:  # program
        begin = running = request = True  # important loops will be running
        settings = False  # settings loop won't be activated without user input
        win = 2  # no winner is determined
        init_program()
        # ------
        # start, settings
        request, running, settings, win, again = begins(begin, request, running, settings, win, again)

        # ------
        # game creation
        # asks whether game should be loaded or created
        random, load, running, settings, win, again = request_load(request, running, settings, win, again)
        if load_game(load, random) and running:  # loads/creates game, True if ships are placed by the player
            settings, again, running, win = ship_placement(settings, again, running, win)
        # updates games played/start time stat
        dif_i = get_dif_number()
        game[dif_i] += 1
        start_time[dif_i] = int(time.time() / 60)
        # ------
        # game loop
        win, again = ingame(settings, running, win, again)

        vo.draw_end(win, resource_path, lg.get_language())  # shows an end screen if a winner is determined
        update_gwon(win)  # updates won/lost stat


def end():
    """
    ends the program
    """
    channel5.stop()  # stops the music
    pg.mixer.quit()  # closes all sound channels
    pg.quit()  # closes the window
    sys.exit()  # ends the program


def main():
    """
    main function, called at the beinning of code
    """
    loops()  # program
    end()  # end of program


if __name__ == '__main__':  # prevents activation by import
    main()  # program
