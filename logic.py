import input as ip  # converts input into usable data
import chat
import visual_output as vo  # GUI
import pygame  # used to recieve player input and create GUI
import save  # used to save/load settings
import os  # used to open pdf

from pygame.locals import *  # used for pygame constants such as RESIZABLE for window settings
from playfield import hit_small_field  # lets the game hit a small field
# TODO Regeln aendern ermoeglichen


def _get_button_return(x_coord, y_coord, inputtype, resource_path, clicked_field="string"):
    """
    returns, what is supposed to be returned to the main module from do_button_mouse_ingame
    :param x_coord: int; x coord of the clicked field
    :param y_coord: int; y coord of the clicked field
    :param inputtype: str; mouse/keyboard
    :param resource_path: Func; returns a resource path to a relative path
    :param clicked_field: list[int, int]; previously clicked field
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    if inputtype == "keyboard":
        return x_coord, y_coord

    if x_coord == clicked_field[0] and y_coord == clicked_field[1]:
        # returns the new clicked field, whether a field was hit, and the hit field
        return -1, -1, True, x_coord, y_coord

    else:
        hit_small_field(1, x_coord, y_coord, resource_path, sound_volume, get_language())  # clicks a new field
        # returns the new clicked field, whether a field was hit, and the hit field
        return x_coord, y_coord, False, -1, -1


def _get_button_return_ingame(button, inputtype, resource_path, clicked_field="string", save_game=()):
    """
    evaluates return values getting returned to the main module

    when button is pressed, executes its feature

    :param button: list[str, str] or list[str, int, int]; button/field and the pressed button/field
    :param inputtype: str; mouse/keyboard, depending on input leading here
    :param resource_path: Func; returns the resource path to a relative path
    :param clicked_field: list[int, int]; previously clicked field
    :param save_game: Func; saves the game
    :return: list[int, int, bool, int, int] or None; clicked field, whether a field is targeted, targeted field
     or control values
    """
    if button:  # checks whether something was pressed
        # checks whether a field or button was pressed
        if str(button[0]) == "field":
            # returns the new clicked field, whether a field was hit, and the hit field
            return _get_button_return(button[1], button[2], inputtype, resource_path, clicked_field)

        elif str(button[0]) == "button":
            # checks type of button
            if str(button[1]) == "end":
                return "end"  # ends the game
            elif str(button[1]) == "settings":
                return "settings"
            elif str(button[1]) == "save":
                save_game()


def _play_click_sound(resource_path):
    """
    plays a clicking sound everytime mouse input is recognized

    :param resource_path: Func; returns the resource path to a relative path
    """
    channel = pygame.mixer.Channel(1)  # chooses channel for mouse sound
    try:
        sound = pygame.mixer.Sound(resource_path("assets/sounds/click.wav"))  # takes the mouse sound
    except FileNotFoundError:
        chat.add_missing_message("click.wav", resource_path("assets/sounds/"), get_language())
    else:
        sound.set_volume(sound_volume)  # sets the volume to the current sound volume
        channel.play(sound)  # plays mouse sound


def do_button_mouse_ingame(xcoord, ycoord, field_size, end_buttons, clicked_field, resource_path,
                           save_game):
    """
    executes feature of a button or clicks/hits a field

    :param xcoord: int; x coordinate of the click
    :param ycoord: int; y coordinate of the click
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param end_buttons: list[Button, Button]; Liste mit den Endknoepfen
    :param clicked_field: list[int, int]; previously clicked field
    :param resource_path: Func; returns the resource path to a relative path
    :param save_game: Func; saves the game
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    button = ip.get_button_ingame_mouse(xcoord, ycoord, field_size, end_buttons)  # gets pressed thing
    _play_click_sound(resource_path)
    # returns the new clicked field, whether a field was hit, and the hit field
    return _get_button_return_ingame(button, "mouse", resource_path, clicked_field, save_game)


def _play_tastatur_sound(resource_path):
    """
    plays a clicking sound everytime keyborad input is recognized

    :param resource_path: Func; returns the resource path to a relative path
    """
    channel4 = pygame.mixer.Channel(3)  # chooses channel for keyboard sound
    try:
        sound = pygame.mixer.Sound(resource_path("assets/sounds/tastatur.wav"))  # takes the keyboard sound
    except FileNotFoundError:
        chat.add_missing_message("tastatur.wav", resource_path("assets/sounds/"), get_langauge())
    else:
        sound.set_volume(sound_volume)  # sets the volume to the current sound volume
        channel4.play(sound)  # plays keyboard sound


def do_button_ingame_keyboard(pressed_key, resource_path):
    """
    carries out use of a button or hits a small field
    :param pressed_key: Key; pressed key
    :param resource_path: Func; return the resource path to a relative path
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    button = ip.get_button_ingame_keyboard(pressed_key)
    _play_tastatur_sound(resource_path)
    # returns the new clicked field, whether a field was hit, and the hit field
    return _get_button_return_ingame(button, "keyboard", resource_path)


def goto_volume():
    """
    enabels volume adjustments
    """
    global aufgabe
    aufgabe = "volume"


def do_button_start(xcoord, ycoord, field_size, start_buttons, resource_path):
    """
    fuhrt einen Knopf am Start aus
    :param xcoord: int; x-Koordinate des Mausklicks
    :param ycoord: int; y-Koordiante des Mausklicks
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param start_buttons: list[Button, Button, ...]; Liste mit den Startknoepfen
    :param end: Function; beendet das Spiel
    :param resource_path: Func; returns resource path to a relative path
    """
    _play_click_sound(resource_path)
    # erhaelt den angeklickten Knopf in den Einstellungen
    button = ip.get_button_start_mouse(xcoord, ycoord, field_size, start_buttons)

    if aufgabe == "main" and zustand == "start":  # Aufgabe ueberpruefen, dementsprechend handeln
        # ueberprueft die Nummer des Knopfes
        if button == 1:
            set_game_start()  # Spiel startet
        elif button == 2:
            goto_difficulty()  # Schwierigkeit kann geaendert werden
        elif button == 3:
            goto_videosettings()  # Bild kann geaendert werden
        elif button == 4:
            goto_choose_rules()  # Regeln koennen geaendert werden
        elif button == 5:
            try:
                os.startfile(resource_path('assets/help.pdf'))  # opens the pdf that explains the game
            except FileNotFoundError:
                chat.add_missing_message("help.pdf", resource_path('assets/'), get_language())
        elif button == 6:
            return "end"

    elif aufgabe == "main" and zustand == "settings":
        if button == 1:
            set_game_start()  # Spiel startet
        elif button == 2:
            goto_videosettings()  # Bild kann geaendert werden
        elif button == 3:
            goto_choose_rules()  # Regeln koennen geaendert werden
        elif button == 4:
            try:
                os.startfile(resource_path('assets/help.pdf'))  # opens the pdf that explains the game
            except FileNotFoundError:
                chat.add_missing_message("help.pdf", resource_path('assets/'), get_language())
        elif button == 5:
            goto_volume()
        elif button == 6:
            return "end"

    elif aufgabe == "difficulty":
        # wenn die Schwierigkeit ausgewaehlt wird, Schwierigkeit auf neue Schwierigkeit umstellen
        if button == 1:
            set_difficulty("easy", resource_path)
        elif button == 2:
            set_difficulty("medium", resource_path)
        elif button == 3:
            set_difficulty("impossible", resource_path)
        elif button == 4:
            set_aufgabe("main")

    elif aufgabe == "videosettings":
        # wenn das Hintergrundbild geaendert wird, dieses aendern, wenn Art der Oberflaeche geaendert
        # wird, diese veraendern
        if button == 1:
            vo.set_windowed(pygame.FULLSCREEN, resource_path, get_language())
            set_aufgabe("main")
        elif button == 2:
            vo.set_windowed(pygame.RESIZABLE, resource_path, get_language())
            set_aufgabe("main")
        elif button == 3:
            set_aufgabe("background")
        elif button == 4:
            set_aufgabe("theme")
        elif button == 5:
            set_aufgabe("main")

    elif aufgabe == "background":
        if button == 1:
            set_background("ocean", resource_path)
        elif button == 2:
            set_background("space", resource_path)
        elif button == 3:
            set_background("drawn", resource_path)
        elif button == 4:
            set_aufgabe("videosettings")

    elif aufgabe == "language":
        # wenn die Regeln geaendert werden, Regeln aendern
        if button == 1:
            set_language("german", resource_path)
        elif button == 2:
            set_language("english", resource_path)
        elif button == 3:
            set_language("latin", resource_path)
        elif button == 4:
            set_aufgabe("main")

    elif aufgabe == "help":
        pass

    elif aufgabe == "volume":
        if button == 1:
            set_aufgabe("main")
            set_music_volume(vo.get_slides()[0].val, resource_path)
            set_sound_volume(vo.get_slides()[1].val, resource_path)

    elif aufgabe == "theme":
        if button == 1:
            set_theme(resource_path, 1)
        elif button == 2:
            set_theme(resource_path, 2)
        elif button == 3:
            set_theme(resource_path, 3)
        elif button == 4:
            set_aufgabe('main')

    return button - 1


def get_task_number():
    """gibt je nach Aufgabe die dazu passende Nummer zurück"""
    task_list = ["main", "difficulty", "videosettings", "background", "language", "help", "ingame", "volume", "theme"]
    task_number = 0
    for task in task_list:
        if aufgabe == task:
            return task_number
        task_number += 1
    return -1


# def set_confirmation(ex):
    # setzt die Bestaetigung auf neuen Wert
    # global confirmation
    # confirmation = ex
    # return


def set_background(bg, resource_path):
    global background
    background = bg
    try:
        save.save(background, "str", "logic", 1, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic1.str", resource_path("saves/settings/"), get_language(), False)
    set_aufgabe('main')


def load_background(resource_path):
    global background
    try:
        background = save.load("str", "logic", 1, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic1.str", resource_path("saves/settings/"), get_language())
        background = "space"


def get_background():
    return background


def get_confirmation():
    # laesst andere Systeme die bestaetigung auslesen
    return confirmation


def set_rule(rules, resource_path):
    # setzt die Regeln auf das Angeklickte
    global rule
    rule = rules
    try:
        save.save(rule, "int", "logic", 6, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic6.int", resource_path("saves/settings/"), get_language(), False)
    set_aufgabe("main")


def load_rule(resource_path):
    global rule
    try:
        rule = save.load("int", "logic", 6, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic6.int", resource_path("saves/settings/"), get_language())
        rule = 1


def get_rule():
    # gibt die Regeln zurueck
    return rule


def set_language(sprache, resource_path):
    """
    sets a new language when the user changes the language

    :param sprache: str; german/english/latin, language the program is now displaying its texts in
    :param resource_path: Func; returns the resource path to a relative path
    """
    global language
    language = sprache
    try:
        save.save(language, "str", "logic", 5, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic5.str", resource_path("saves/settings/"), get_language(), False)
    set_aufgabe('main')


def load_language(resource_path):
    global language
    try:
        language = save.load("str", "logic", 5, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic5.str", resource_path("saves/settings/"), "english")
        language = "english"


def get_language():
    # gibt die Sprache zurueck
    return language


def goto_choose_rules():
    # oeffnet neues Fenster
    set_aufgabe("language")


def goto_videosettings():
    # oeffnet neues Fenster
    set_aufgabe("videosettings")


def goto_help():
    # oeffnet neues Fenster
    set_aufgabe("help")


def set_zustand(now):
    # setzt den zustand (ingame etc.) auf das Angeklickte
    global zustand
    zustand = now


def get_zustand():
    # laesst andere modules den Zustand auslesen
    return zustand


def set_difficulty(difficult, resource_path):
    # setzt die neue Schwierigkeit
    global difficulty
    difficulty = difficult
    try:
        save.save(difficulty, "str", "logic", 4, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic4.str", resource_path("saves/settings/"), get_language(), False)
    set_aufgabe("main")


def load_difficulty(resource_path):
    global difficulty
    try:
        difficulty = save.load("str", "logic", 4, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic4.str", resource_path("saves/settings/"), get_language())
        difficulty = "medium"


def get_difficulty():
    # laesst andere Systeme die Schwierigkeit auslesen
    return difficulty


def set_sound_volume(volume, resource_path):
    global sound_volume
    sound_volume = volume
    try:
        save.save(sound_volume, "flo", "logic", 3, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic3.flo", resource_path("saves/settings/"), get_language(), False)


def set_music_volume(volume, resource_path):
    global music_volume
    music_volume = volume
    try:
        save.save(music_volume, "flo", "logic", 2, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic2.flo", resource_path("saves/settings/"), get_language(), False)


def load_music_volume(resource_path):
    global music_volume
    try:
        music_volume = save.load("flo", "logic", 2, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic2.flo", resource_path("saves/settings/"), get_language())
        music_volume = 0.4


def load_sound_volume(resource_path):
    global sound_volume
    try:
        sound_volume = save.load("flo", "logic", 3, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic3.flo", resource_path("saves/settings/"), get_language())
        sound_volume = 0.4


def get_music_volume():
    return music_volume


def get_sound_volume():
    return sound_volume


def set_writing_color_start(resource_path, number):
    global writing_color_start
    try:
        writing_color_start = save.load("tup", "logiccol", number, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logiccol" + str(number) + ".tup", resource_path("saves/settings/"), get_language())
        writing_color_start = (0, 0, 0)


def get_writing_color_start():
    return writing_color_start


def set_background_color_start(resource_path, number):
    global writing_color_bg
    try:
        writing_color_bg = save.load("tup", "logicbac", number, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logicbac" + str(number) + ".tup", resource_path("saves/settings/"), get_language())
        writing_color_bg = (255, 255, 255)


def get_background_color_start():
    return writing_color_bg


def set_theme(resource_path, number):
    try:
        save.save(number, 'int', 'logic', 7, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic7.int", resource_path("saves/settings/"), get_language(), False)
    load_theme(resource_path, number)
    vo.change_button_color(writing_color_start, writing_color_bg)


def load_theme(resource_path, number):
    set_writing_color_start(resource_path, number)
    set_background_color_start(resource_path, number)


def set_game_start():
    # startet das Spiel
    set_zustand("ingame")
    set_aufgabe("ingame")


def set_fullscreen():
    global resizable
    global fullscreen
    resizable = 0
    fullscreen = FULLSCREEN


def get_fullscreen():
    return fullscreen


def get_resizable():
    return resizable


def get_aufgabe():
    # laesst andere Systeme die Aufgabe auslesen
    return aufgabe


def set_aufgabe(task):
    # setzt die Aufgabe, wodurch neue Oberflaeche entsteht
    global aufgabe
    aufgabe = task


def goto_difficulty():
    # oeffnet neues Fenster
    set_aufgabe("difficulty")


def __init__logic(resource_path):
    global aufgabe
    global zustand
    load_language(resource_path)
    try:
        theme_number = save.load('int', 'logic', 7, resource_path, 'settings/')
    except FileNotFoundError:
        chat.add_missing_message("logic7.int", resource_path("saves/settings/"), get_language())
        theme_number = 1
    load_theme(resource_path, theme_number)
    load_background(resource_path)
    load_music_volume(resource_path)
    load_sound_volume(resource_path)
    load_difficulty(resource_path)
    load_rule(resource_path)
    aufgabe = "main"
    zustand = "start"
    ip.__init__input()


# def begin():
    # Beginn des Programs
    # vw.draw_start(get_but_count(aufgabe), aufgabe)
    # return


def get_but_count(aufgab):
    if aufgab == "main":
        return 6
    elif aufgab == "videsettings":
        return 5
    elif aufgab == "difficulty" or aufgab == "language" or aufgab == "theme":
        return 4
    elif aufgab == "help" or aufgab == "volume":
        return 1
    else:
        return 30


def _check_player_change(hit, ship_count, check_ship_pos, ship):
    # TODO andere Regeln ermoeglichen
    """in Bearbeitung, wichtig bei Änderung der Regeln"""
    while True:
        if rule == 1:
            hi = 1
        elif rule == 2:
            hi = 1
        elif rule == 3:
            hi = ship_count
        else:
            hi = 0
        x = 0
        while x < hi:
            x += 1
            if rule == 2:
                # bei Wechsel des Spielers nach nicht getroffenem Schiff, wird ueberprueft, ob Schiff getroffen und
                # dementsprechend Schleife beendet oder auch nicht
                for x in range(10):
                    if check_ship_pos(ship[0][x], hit)[0]:
                        hi += 1
            yield
        # set_player(1)
