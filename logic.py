import input as ip
from pygame.locals import *
from playfield import hit_small_field
# TODO Regeln aendern ermoeglichen


def _get_button_return(x_coord, y_coord, inputtype, clicked_field="string"):
    """
    returns, what is supposed to be returned to the main module from do_button_mouse_ingame
    :param x_coord: int; x coord of the clicked field
    :param y_coord: int; y coord of the clicked field
    :param clicked_field: list[int, int]; previously clicked field
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    if inputtype == "keyboard":
        return x_coord, y_coord

    if x_coord == clicked_field[0] and y_coord == clicked_field[1]:
        # returns the new clicked field, whether a field was hit, and the hit field
        return -1, -1, True, x_coord, y_coord

    else:
        hit_small_field(1, x_coord, y_coord)  # clicks a new field
        # returns the new clicked field, whether a field was hit, and the hit field
        return x_coord, y_coord, False, -1, -1


def _get_button_return_ingame(button, end, do_settings, inputtype, clicked_field="string"):
    if button:  # checks, whether something was pressed
        # checks, whether a field or button was pressed
        if str(button[0]) == "field":
            # returns the new clicked field, whether a field was hit, and the hit field
            return _get_button_return(button[1], button[2], inputtype, clicked_field)

        elif str(button[0]) == "button":
            # checks type of button
            if str(button[1]) == "end":
                end(1)  # ends the game, if end button was pressed
            elif str(button[1]) == "settings":
                do_settings()
    return None


def do_button_mouse_ingame(xcoord, ycoord, field_size, end_buttons, end, do_settings, clicked_field):
    """
    setzt die Anweisung eines gedrueckten Knopfes um oder trifft ein kleines Feld
    :param xcoord: int; x-Koordinate des Mausklicks
    :param ycoord: int; y-Koordinate des Mauslicks
    :param field_size: float; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param end_buttons: list[Button, Button]; Liste mit den Endknoepfen
    :param end: Function; ends the game
    :param clicked_field: list[int, int]; previously clicked field
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    button = ip.get_button_ingame_mouse(xcoord, ycoord, field_size, end_buttons)  # gets pressed thing
    # returns the new clicked field, whether a field was hit, and the hit field
    return _get_button_return_ingame(button, end, do_settings, "mouse", clicked_field)


def do_button_ingame_keyboard(pressed_key, end, do_settings):
    """
    carries out use of a button or hits a small field
    :param pressed_key: Key; pressed key
    :param end: Function; ends the game
    :return: list[int, int, bool, int, int]; new clicked field, whether a field was hit, hit field
    """
    button = ip.get_button_ingame_keyboard(pressed_key)
    # returns the new clicked field, whether a field was hit, and the hit field
    return _get_button_return_ingame(button, end, do_settings, "keyboard")


def do_button_start(xcoord, ycoord, field_size, start_buttons, end):
    """
    fuhrt einen Knopf am Start aus
    :param xcoord: int; x-Koordinate des Mausklicks
    :param ycoord: int; y-Koordiante des Mausklicks
    :param field_size: float; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param start_buttons: list[Button, Button, ...]; Liste mit den Startknoepfen
    :param end: Function; beendet das Spiel
    :return: nothing
    """
    # erhaelt den angeklickten Knopf in den Einstellungen
    button = ip.get_button_start_mouse(xcoord, ycoord, field_size, start_buttons)

    if aufgabe == "main":  # Aufgabe ueberpruefen, dementsprechend handeln
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
            goto_help()  # Die Hilfe wird angezeigt
        elif button == 6:
            end(2)

    elif aufgabe == "difficulty":
        # wenn die Schwierigkeit ausgewaehlt wird, Schwierigkeit auf neue Schwierigkeit umstellen
        if button == 1:
            set_difficulty("easy")
        elif button == 2:
            set_difficulty("medium")
        elif button == 3:
            set_difficulty("impossible")
        elif button == 4:
            set_aufgabe("main")

    elif aufgabe == "videosettings":
        # wenn das Hintergrundbild geaendert wird, dieses aendern, wenn Art der Oberflaeche geaendert
        # wird, diese veraendern
        if button == 1:
            # vw.set_full()
            set_aufgabe("main")
        elif button == 2:
            # vw.set_windowed()
            set_aufgabe("main")
        elif button == 3:
            set_aufgabe("background")
        elif button == 4:
            set_aufgabe("main")

    elif aufgabe == "background":
        if button == 1:
            set_background("ocean")
            set_aufgabe("main")
        elif button == 2:
            set_background("space")
            set_aufgabe("main")
        elif button == 3:
            set_background("drawn")
            set_aufgabe("main")
        elif button == 4:
            set_aufgabe("videosettings")

    elif aufgabe == "language":
        # wenn die Regeln geaendert werden, Regeln aendern
        if button == 1:
            set_language("german")
            set_aufgabe("main")
        elif button == 2:
            set_language("english")
            set_aufgabe("main")
        elif button == 3:
            set_language("latin")
            set_aufgabe("main")
        elif button == 4:
            set_aufgabe("main")

    elif aufgabe == "help":
        # die Hilfe anzeigen und bei zurueck zurueckgehen
        if button == 1:
            set_aufgabe("main")


def get_task_number():
    """gibt je nach Aufgabe die dazu passende Nummer zurück"""
    task_list = ["main", "difficulty", "videosettings", "background", "language", "help", "ingame"]
    task_number = 0
    for task in task_list:
        if aufgabe == task:
            return task_number
        task_number += 1
    return -1


def set_confirmation(ex):
    # setzt die Bestaetigung auf neuen Wert
    global confirmation
    confirmation = ex
    return


def set_background(bg):
    global background
    background = bg
    return


def get_background():
    return background


def get_confirmation():
    # laesst andere Systeme die bestaetigung auslesen
    return confirmation


def set_rules(rules):
    # setzt die Regeln auf das Angeklickte
    global rule
    rule = rules
    set_aufgabe("main")
    return


def get_rules():
    # gibt die Regeln zurueck
    return rule


def set_language(sprache):
    # setzt die Sprache, wenn eine andere angewaehlt wurde
    global language
    language = sprache
    return


def _set_writing_color_start(color_local):
    # setzt die Farbe der Schrift auf den Startknoepfen
    global writing_color_start
    writing_color_start = color_local
    return


def get_writing_color_start():
    # gibt die Farbe der Schrift auf den Startknoepfen zurueck
    return writing_color_start


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


def set_difficulty(difficult):
    # setzt die neue Schwierigkeit
    global difficulty
    set_aufgabe("main")
    difficulty = difficult


def get_difficulty():
    # laesst andere Systeme die Schwierigkeit auslesen
    return difficulty


def set_game_start():
    # startet das Spiel
    set_zustand("ingame")
    set_aufgabe("ingame")
    return


def set_windowed():
    global resizable
    global fullscreen
    resizable = RESIZABLE
    fullscreen = 0


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


def __init__logic():
    global difficulty
    global aufgabe
    global zustand
    global rule
    global writing_color_start
    global background
    global language
    background = "space"
    aufgabe = "main"
    zustand = "start"
    difficulty = "easy"
    writing_color_start = (0, 50, 0)
    rule = 1
    language = "english"
    set_windowed()
    ip.__init__input()


# def begin():
    # Beginn des Programs
    # vw.draw_start(get_but_count(aufgabe), aufgabe)
    # return


def get_but_count(aufgab):
    if aufgab == "main" or aufgab == "videosettings":
        return 6
    elif aufgab == "difficulty" or aufgab == "language":
        return 4
    elif aufgab == "help":
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
