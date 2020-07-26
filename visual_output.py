# commented, partly german
# Modul, das Bilder auf den Bildschirm bringt und fuer die visuelle Ausgabe zustaendig ist

# TODO Ausgabe der Schiffe verbessern, Bilder (Turtle??)
# TODO Treffer als Animation ausgeben

# -------
# importiert pygame, mit dem alles in einem Fenster ausgegebn wird,
# sowie die Module, mit denen weiteren Dingen die ausgegen werden
import time
import pygame
from pygame.locals import *
import buttons as bu
import playfield as pf
import slider as sl


# ------
# gibt Groessen der Oberflaeche zurueck
def get_screen_size_full_screen():
    """
    gibt die Groesse des Bildschirms bei Vollbild zurueck
    :return: list[int, int]; Breite und Hoehe des Bildschirms bei Vollbild
    """
    pygame.init()
    display_info = pygame.display.Info()  # erhaelt Information ueber den Bildschirm
    # entnimmt daraus die Breite und Hoehe des Bildschirms zurueck
    height = display_info.current_h
    width = display_info.current_w
    return width, height  # gibt die beiden Werte zurueck


def get_window_size(width, height):
    """
    laesst Hoehe und breite des bildschirms sowie die Groesse eines Feldes auslesen und den Bildschirmzustand auslesen
    :param width: int; aktuelle Breite des Bildschirms
    :param height: int; aktuelle Breite des Bildschirms
    :return: list[int, int, int, str]; die Breite und Hoehe sowie die Groesse eines Feldes und der Bildschirmzustand
    """
    if height > width:  # ueberprueft, ob der Bildschirm weiter in die Breite oder weiter in die Hoehe geht
        field_size = width / 20  # setzt die Groesse eines Feldes abhaengig von der kleineren Groesse
        orientation = "height"  # setzt den Bildschirmzustand auf die groessere Groesse
    else:
        field_size = height / 20  # setzt die Groesse eines Feldes abhaengig von der kleineren Groesse
        orientation = "width"  # setzt den Bildschirmzustand auf die groessere Groesse
    return height, width, field_size, orientation  # gibt alle Werte zurueck


def set_screen_size(width, height):
    """
    setzt die Groesse der Oberflaeche neu
    :param width: int; neue Breite der Oberflaeche
    :param height: int; neue Hoehe der Oberflaeche
    :return:
    """
    # setzt die neuen Werte ein
    global global_width
    global global_height
    global_width = width
    global_height = height


def get_screen_size():
    """
    gibt die aktuelle Groesse der Oberflaeche zurueck
    :return: list[int; int]; die Breite und Hoehe der Oberflaeche
    """
    return global_width, global_height  # gibt die aktuelle Groesse der Oberflaeche zurueck


def get_small_field_count():
    """
    gibt die Anzahl der kleinen Felder innerhalb eines Spielfeldes zurueck
    :return: list[int; int]; Anzahl der kleine Felder innerhalb eines Spielfeldes
    """
    # gibt die Anzahl der Felder in die Breite und in die Hoehe zurueck
    return pf.get_big_fields()[0].field_count_x, pf.get_big_fields()[0].field_count_y


def _init_window(resource_path):
    """
    initializes the window the game is played in
    :param resource_path: Func, returns a path to pictures and sounds
    :return: nothing
    """
    global g_screen
    icon = pygame.image.load(resource_path("assets/images/icon.jpg"))
    pygame.display.set_icon(icon)  # creates an icon
    pygame.display.set_caption("schiffe_versenken      v.alpha.3")  # creates a caption
    g_screen = pygame.display.set_mode(get_screen_size(), resizable)


# -------
# initialisiert das Modul 'visual_output'
def __init__visual_output(resource_path, language, color_writing_start, sound_volume, music_volume, bu_bg_color,
                          orientation="height", field_count_x=10, field_count_y=10):
    """
    initialisiert die Methode visual output
    :param language: str; Sprache, in der die Schrift ausgegeben wird
    :param orientation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    :param field_count_x: int; Anzahl der kleinen Felder eines großen Spielfelds in die Breite
    :param field_count_y: int; Anzahl der kleinen Felder eines großen Spielfelds in die Hoehe
    :return: nothing
    """
    global resizable
    resizable = pygame.constants.RESIZABLE
    color_writing_end_b = (125, 125, 255)  # setzt die Farbe der Schrift auf den Endknoepfen auf grau
    # setzt die Groesse der Oberflaeche auf die Groesse des Bildschirms
    set_screen_size(get_screen_size_full_screen()[0], get_screen_size_full_screen()[1])
    _init_window(resource_path)  # initializes the window the game is played in
    field_size = get_window_size(global_width, global_height)[2]  # erhaelt die Groesse eines Feldes
    pf.__init__playfield(orientation, field_size, field_count_x, field_count_y)  # initialisiert das Spielfeld
    bu.__init__buttons(language, color_writing_start, color_writing_end_b, field_size, bu_bg_color)  # initialisiert die Knoepfe
    sl.create_slider(field_size, sound_volume, music_volume)


# -------
# gibt alle zu sehenden Dinge aus und laesst sie in einem Fenster sichtbar werden
def _draw_background(screen, background, resource_path):
    """
    gibt den Hintergrund auf der Oberflaeche aus
    :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
    :param background: str; gibt an, welches Bild als Hintergrundbild angezeigt wird
    :param resource_path: Func; returns the full resource path when given a relative path
    :return: nothing
    """
    if background == "ocean":  # ueberprueft, welches Hintergrundbild angezeigt werden soll
        bg = pygame.image.load(resource_path("assets/images/ocean.jpg"))
    elif background == "space":
        bg = pygame.image.load(resource_path("assets/images/space.jpg"))
    else:
        bg = pygame.image.load(resource_path("assets/images/drawn.jpg"))  # laedt das gezeichnete Bild
    screen.blit(bg, (0, 0))  # gibt das geladene Bild auf der Oberflaeche aus


def _draw_ships(ship, screen, field_size, orientation, zustand):
    """
    Gibt die Schiffe auf der Oberflaeche aus
    :param zustand: str; gibt an, ob das Spiel bereits gespielt wird, oder sich noch am Start befindet
    :param ship: list[list[Ship, ...], list]; enthaelt alle Schiffe
    :param screen: Surface; Oberflaeche, auf der das Spiel ausgegebn wird
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param orientation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    """
    small_field_count_x, small_field_count_y = pf.get_small_fieldcounts()  # erhaelt die Feldgroesse eines Spielfeldes
    if zustand == "ingame":  # ueberprueft, ob das Spiel bereits gespielt wird
        for thing in ship:
            for shiplist in ship:  # geht alle Schiffe durch
                for realship in shiplist:
                    # gibt das Schiff auf der Oberflaeche aus
                    realship.draw(screen, field_size, orientation, small_field_count_x, small_field_count_y)


def draw_screen(zustand, background, language, ship, resource_path, task_number=-1):
    """
    gibt alle zu sehenden Dinge auf der Oberflaeche aus
    :param zustand: str; gibt an, ob das Spiel bereits gespielt wird, oder sich noch am Start befindet
    :param background: str; gibt an, welches Bild als Hintergrundbild angezeigt wird
    :param language: str; aktuelle Sprache, in der der text ausgegeben wird
    :param ship: list[Ship, Ship, ...]; Liste mit allen Schiffen
    :param resource_path: Func; returns the full resource path when given a relative path
    :param task_number: int; Nummer der aktuell durch das Programm zu bearbeitenden Aufgabe
    """
    screen = g_screen
    screen.fill((0, 0, 0))
    field_size, orientation = get_window_size(global_width, global_height)[2:]  # erhaelt die Groesse eines Feldes
    _draw_background(screen, background, resource_path)  # gibt den Hintergrund auf der Oberflaeche aus
    _draw_ships(ship, screen, field_size, orientation, zustand)  # gibt die Schiffe auf der Oberflaeche aus
    pf.draw_playfield(screen, field_size, zustand)  # gibt das Spielfeld auf der Oberflaeche aus
    bu.refresh_buttons(task_number, orientation, language, zustand)  # setzt die Knoepfe neu
    bu.draw_buttons(screen)  # gibt die Knoepfe auf der Oberflaeche aus
    sl.refresh_slides(task_number)  # refreshes active of slides
    sl.draw_slides(screen, field_size)  # displays sliders on the GUI
    pygame.display.flip()  # updated das Display, damit alle vorher auf der Oberflaeche ausgegeben Dinge sichtbar sind


def draw_end(winner, resource_path):
    """
    shows the end screen
    :param winner: int; player who won the game, 1 is the enemy and 0 is the player
    :param resource_path: Func; return teh reource path of a relative path
    """
    sound = pygame.mixer.Sound(resource_path("assets/sounds/windowsxp.wav"))
    sound.play()
    if winner == 1 or winner == 0:  # checks, whether a winner was determined
        screen = pygame.display.set_mode((int(global_width), int(global_height)), FULLSCREEN)  # sets new surface
        field_size = get_window_size(global_width, global_height)[2]  # gets size of one virtual field
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, global_width, global_height), 0)  # draws a black background
        if winner == 0:  # checks, whter the player has won
            screen.blit(pygame.font.SysFont(None, int(field_size * 3)).render("You won!!!", False, (0, 125, 0)),
                        (field_size * 3, field_size * 5))  # shows "You won!!!" in green
        elif winner == 1:  # checks, whter the enemy has won
            screen.blit(pygame.font.SysFont(None, int(field_size * 3)).render("You lost :´(", False, (125, 0, 0)),
                        (field_size * 3, field_size * 5))  # shows "You lost :´(" in red
        pygame.display.update()  # updates the window
    time.sleep(3)  # waits 3 seconds


# -------
# setzt die Koordinaten aller zu sehenden Dinge neu
def refresh_loc_coords(field_size, orientation, zustand):
    """
    refreshes the locations of visible things shown in the GUI
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :param zustand: str; ingame/start/settings, depending on what the program is doing
    """
    pf.refresh_loc_small_fields(field_size, orientation)  # refreshes the small-fields' coordiantes
    pf.refresh_loc_big_fields(field_size, orientation)  # refreshes the big-fields' coordiantes
    pf.refresh_loc_writings(field_size, orientation)  # refreshes the writings' coordinates
    bu.refresh_loc_buttons(field_size, orientation, zustand)  # refreshes the buttons' coordinates
    bu.refresh_loc_writing(field_size, zustand)  # refreshes the button-writings' coordinates
    sl.refresh_loc_sliders(field_size)  # refreshes the sliders' coordiantes


def set_windowed(l_resizable, resource_path):
    global resizable
    pygame.display.quit()
    resizable = l_resizable
    _init_window(resource_path)


def unclick(field):
    """
    unclicks a field
    :param field: list[int, int]; coordiantes of the field
    :return: nothing
    """
    pf.unclick(field)


def change_button_color(writing_color, bg_color):
    bu.change_button_color(writing_color, bg_color)


def get_small_fields():
    """
    returns the small fields
    :return: list[list[SmallField, ...], list, ...]; list with the small fields
    """
    return pf.get_small_fields()


def get_buttons():
    """
    returns the buttons
    :return: list[list[Button, ...], list[Button, ...]; list with all buttons
    """
    return bu.get_buttons()


def get_slides():
    return sl.get_sliders()
