# commented, partly german
# Main Modul, das alles organisiert und die anderen Module ueberwacht und steuert

# TODO speichern ermoeglichen
# ------
# Import der verwendeten Module sowie von pygame
import pygame as pg
import logic as lg
from pygame.locals import *
import ship as sh
import enemy as en
import player as pl
import visual_output as vo
from playfield import hit_small_field
import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# -------
# Deklaration von Variablen und Funktionen
begin = False
running = False
settings = False
csp = sh.check_ship_pos


# ------
# Initialisierung des main-Moduls
def _play_music(volume):
    global channel5
    global music
    channel5 = pg.mixer.Channel(4)
    music = pg.mixer.Sound(resource_path("assets/music/deepblue.wav"))
    music.set_volume(volume)
    channel5.play(music, loops=-1)


def __init__main(aufgabe):
    """
    # initialisiert das main module
    :param aufgabe: str; aktuelle Aufgabe des Programms, meist "start"
    :return: nothing
    """
    global player
    global begin
    global running
    global settings
    global zug
    if aufgabe == "start":  # ueberprueft, ob das Programm gerade startet
        # setzt begin auf True, was den Start der Oberflaeche und spielergesteuerte Einstellungen ermoeglicht
        begin = True
        running = True  # setzt running auf True, was das Spielen des Spiels ermoeglicht
        settings = False
        zug = 0  # setzt die Anzahl der Zuege auf 0, da noch kein Zug durchgefuehrt wurde
        player = 0  # setzt den Spieler auf 0, da der Gegner erst als zeites spielen darf
        # initialisiert das Modul ship
        sh.__init__shipcheck()
        sh.__init__ship()
        sh.set_ships()
        pg.mixer.init()
        _play_music(lg.get_music_volume())


# ------
# Ausfuehrung des gegnerischen Zuges
def _get_play_list_enemy():
    """
    gibt den naechsten Schuss des Gegners zurueck
    :return: list[int, int]; Koordinaten des naechsten Schuss' des Gegners
    """
    try:
        # ueberprueft, ob ein naechstes Feld in der Liste der naechsten Treffer vorhanden ist
        next_play = en.get_play_list()[0]
    except IndexError:
        # erstellt ein zufaelliges Feld als naechstes zu treffendes Feld
        next_play = [en.get_random_field(vo.get_small_field_count()[0], vo.get_small_field_count()[1])]
    return next_play  # gibt die Koordinaten dieses Feld zurueck


def _get_check_hit(next_play):
    """
    uberprueft, ob der naechste Schuss des Gegners trifft
    :param next_play: list[int, int]; naechster Schuss des Gegners
    :return: int; Nummer des getroffenen Schiffes, wenn dort eines vorhanden ist
    """
    try:
        # ueberprueft, ob ein Schiff getroffen werden wird
        return sh.check_hit(1, next_play)[1]  # gibt die Nummer des Schiffes zurueck
    except IndexError:
        return -1  # gibt -1 als Kontrollwert zurueck
    except TypeError:
        return -1  # gibt -1 als Kontrollwert zurueck


def set_player(play):
    """
    setzt den Spieler am Zug neu
    :param play: int; Spieler, der nun am Zug ist
    :return: nothing
    """
    global player
    global zug
    player = play  # setzt den Spieler am Zug auf den Spieler, der am Zug sein soll
    if player == 1:  # ueberprueft, ob nun der Gegner am Zug ist
        _do_enemy_move()  # fuehrt den Zug des Gegners aus
        zug += 1  # zaehlt einen Zug weiter
    player = 0  # setzt den Spieler am Zug wieder auf den Spieler


def _do_enemy_move():
    """
    fuehrt den gegnerischen Zug aus
    :return: nothing
    """
    old_xcoord, old_ycoord, hit = en.get_enemy_move()
    sh.hit_something(hit[0], hit[1], 1, resource_path, lg.get_sound_volume(), old_xcoord,
                     old_ycoord)  # trifft etwas an der getroffenen Stelle

    if lg.get_rule() == 2:  # ueberprueft, ob Treffer Anzahl der Schuesse je Zug bestimmt
        for x in range(sh.get_ship_count()):  # ueberprueft, ob ein Schiff getroffen wurde
            if sh.check_ship_pos(sh.get_ship()[0][x], hit)[0]:
                set_player(1)  # fuehrt einen weiteren gegnerischen Zug aus

    elif lg.get_rule() == 3:  # ueberprueft, ob Anzahl der SChiffe Anzahl der SChuesse bestimmt
        # TODO Anzahl der intakten SChiffe ermitteln, sh.check_ship_status veraendern?
        pass


# ------
# Ausfuehren des spielergesteuerten Zuges
def do_hit_player_input(xcoord_local, ycoord_local):
    """
    does a hit enforced by a player input

    :param xcoord_local: int; x coordinate of the hit
    :param ycoord_local: int; y coordiante of the hit
    """
    # hits something on the coordiantes of the hit
    sh.hit_something(xcoord_local, ycoord_local, 0, resource_path, lg.get_sound_volume())
    if pl.change_hit_list(xcoord_local, ycoord_local):  # changes the lsit with hit fields
        set_player(1)  # does the enemies move and sets the player back to the player


# ------
# Zurueckgabe von Werten
def get_player():
    """
    gibt den Spieler zurueck, der gerade am Zug ist
    :return: int; Spieler, der am Zug ist (0 = Spieler; 1 = Gegner)
    """
    return player


# ------
# enables change of settings
def do_settings():
    """
    enables a change of settings
    :return: nothing
    """
    global running
    global settings
    running = False  # ends the ingame loop
    settings = True  # activates the start loop
    lg.set_zustand("settings")  # sets the things that is done to "start"
    lg.set_aufgabe("main")  # sets the task to "main"


# ------
# Beendigung des Spiels
def end(winner):
    """
    beendet das Spiel und damit das Programm
    :param winner: int; Spieler, der das Spiel gewinnt
    :return: nothing
    """
    global win
    global running
    global begin
    global settings
    win = winner
    lg.set_zustand("end")  # setzt den Zustand des Programms auf "end"
    begin = False  # beendet die Moeglichkeit fuer spielergesteuerte Einstellungen
    running = False  # beendet die Moeglichkeit das Spiel zu spielen
    settings = False


# ------
# Initialisierung des Programms
pl.__init__player()  # initialisiert den Spieler
lg.__init__logic(resource_path)  # initialisiert das Modul logic
vo.__init__visual_output(resource_path, lg.get_language,
                         lg.get_writing_color_start(), lg.get_sound_volume(),
                         lg.get_music_volume(), lg.get_background_color_start())  # initialisiert die Ausgabe auf dem Bildschirm

__init__main(lg.get_zustand())  # initialisiert das main Modul
# displays the menu on the game window
vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
               lg.get_task_number())
# ------
# start, settings
while begin and lg.get_zustand() != "end":

    for event in pg.event.get():  # geht alle Eingaben in das Programm durch

        if event.type == MOUSEBUTTONDOWN:  # ueberprueft, ob mithilfe der Maus auf die Oberflache geklickt wurde
            # erhaelt die Groesse eines Feldes
            field_size = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2]
            # erhaelt die Bildschirmausrichtung
            orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[3]
            # fuehrt die Funktion des Kopfes aus, wenn ein Knopf gedrueckt wurde
            lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_buttons()[0], end, resource_path)
            # displays the menu on the game window
            vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                           lg.get_task_number())

        elif event.type == VIDEORESIZE:  # ueberprueft, ob die Groesse des Fenster veraendert wurde
            vo.set_screen_size(event.size[0], event.size[1])  # aktualisiert die Groesse des Fensters
            # aktualisiert die Koordinaten der Dinge, die auf der Oberflaeche ausgegeben werden
            vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                  vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
            # displays the menu on the game window
            vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                           lg.get_task_number())

        elif event.type == pg.QUIT:  # ueberprueft, ob das Fenster geschlossen wurde
            # beendet das Programm
            running = False
            begin = False
            win = 2

    if lg.get_zustand() == "ingame":  # ueberprueft, ob das Spiel getstartet wurde
        begin = False  # startet das Spiel
        running = True
        settings = False

    music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing

en.__init__enemy(vo.get_small_field_count()[0], vo.get_small_field_count()[1], sh.get_ship_positions(),
                 lg.get_difficulty())  # initialisiert den GEgner
num = 0
other_num = 0

# ------
# game loop
while settings or running:
    # ------
    # settings
    while settings and lg.get_zustand() != "end":

        for event in pg.event.get():  # geht alle Eingaben in das Programm durch

            if event.type == MOUSEBUTTONDOWN:  # ueberprueft, ob mithilfe der Maus auf die Oberflache geklickt wurde
                # erhaelt die Groesse eines Feldes
                field_size, orientation = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2:]
                # fuehrt die Funktion des Kopfes aus, wenn ein Knopf gedrueckt wurde
                lg.do_button_start(event.pos[0], event.pos[1], field_size, vo.get_buttons()[0], end, resource_path)

                if lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
                    for slider in vo.get_slides():  # goes through every slider
                        try:
                            if slider.button_rect.collidepoint(event.pos):  # checks whether the slider is pressed
                                slider.hit = True  # sets hit to true, so that it will be moved
                        except AttributeError:
                            pass
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                               lg.get_task_number())
                other_num = num

            elif event.type == MOUSEBUTTONUP and num != other_num + 1:  # checks whether a mouse button was lifted
                for slider in vo.get_slides():  # goes through every slider
                    slider.hit = False  # sets hit to false, so that it won't be moved
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == VIDEORESIZE:  # ueberprueft, ob die Groesse des Fenster veraendert wurde
                vo.set_screen_size(event.size[0], event.size[1])  # aktualisiert die Groesse des Fensters
                # aktualisiert die Koordinaten der Dinge, die auf der Oberflaeche ausgegeben werden
                vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                      vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
                # displays the menu on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                               lg.get_task_number())

            elif event.type == pg.QUIT:  # ueberprueft, ob das Fenster geschlossen wurde
                # beendet das Programm
                running = False
                settings = False
                win = 2

        if lg.get_aufgabe() == "volume":  # checks whether a slider is on the screen
            for slider in vo.get_slides():  # goes through every slider
                if slider.hit:  # checks, whether it is hit
                    # moves the slider and thus changes the value of it
                    slider.move(vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2])
                    # displays the volume settings on the game window
                    vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                                   resource_path,
                                   lg.get_task_number())

        if lg.get_zustand() == "ingame":  # ueberprueft, ob das Spiel getstartet wurde
            settings = False  # startet das Spiel
            running = True

        num += 1
        if num > 254:
            num = 0

        music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing

    # ------
    # Spiel, spielergestuerte Eingabe eines Spielers
    while running and lg.get_zustand() != "end":  # fuehrt das Programm aus, waehrend das Spiel gespielt wird

        for event in pg.event.get():  # geht alle Eingaben in das Programm durch

            if event.type == MOUSEBUTTONDOWN:  # button on  mouse was pressed
                try:
                    # gets the size of one virtual field
                    field_size = vo.get_window_size(vo.get_screen_size()[0], vo.get_screen_size()[1])[2]
                    # gets coordiantes of the clcked field, whether a field was hit, and the hit field
                    xcoord, ycoord, hit_check, xcoord_2, ycoord_2 = lg.do_button_mouse_ingame(event.pos[0],
                                                                                              event.pos[1], field_size,
                                                                                              vo.get_buttons()[1], end,
                                                                                              do_settings,
                                                                                              pl.get_angeklicktes_feld(),
                                                                                              resource_path
                                                                                              )
                except TypeError:
                    # gets coordiantes of the clcked field, whether a field was hit, and the hit field
                    xcoord, ycoord, hit_check, xcoord_2, ycoord_2 = (-1, -1, False, -1, -1)

                if hit_check:
                    # setzt den Treffer nach Spielereingabe um, wenn ein Feld angeklickt wurde
                    do_hit_player_input(xcoord_2, ycoord_2)
                vo.unclick(pl.get_last_click())
                pl.set_angeklicktes_feld(xcoord, ycoord)  # setzt das angeklickte Feld neu
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                               lg.get_task_number())

            elif event.type == KEYDOWN:  # button on keyboard was pressed
                if event.key == K_ESCAPE:
                    do_settings()
                else:
                    try:
                        # gets coordinates of the selected field
                        xcoord, ycoord = lg.do_button_ingame_keyboard(event.key, end, do_settings, resource_path)
                    except TypeError:
                        # sets coordinates to -1 when no field is selected yet
                        xcoord, ycoord = -1, -1

                    if xcoord != -1 and ycoord != -1:
                        hit_small_field(1, xcoord, ycoord, resource_path, lg.get_sound_volume())  # clicks a new field
                        do_hit_player_input(xcoord, ycoord)  # hits a field from a player input
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(),
                               resource_path, lg.get_task_number())

            elif event.type == VIDEORESIZE:  # checks whether the size of the window got adjusted
                vo.set_screen_size(event.size[0], event.size[1])  # aktualisiert die Groesse des Fensters
                # aktualisiert die Koordinaten der Dinge, die auf der Oberflaeche ausgegeben werden
                vo.refresh_loc_coords(vo.get_window_size(event.size[0], event.size[1])[2],
                                      vo.get_window_size(event.size[0], event.size[1])[3], lg.get_zustand())
                # displays the game on the game window
                vo.draw_screen(lg.get_zustand(), lg.get_background(), lg.get_language(), sh.get_ship(), resource_path,
                               lg.get_task_number())

            elif event.type == pg.QUIT:  # checks whether the wndow has been closed
                running = False  # ends the program
                settings = False
                win = 2  # sets win to 2, what is used to mark that no player has won the game

        sh.check_ship_status(end)  # checks whether all ships of one player have been destroyed

        music.set_volume(lg.get_music_volume())  # adjusts the volume of the music playing

# ------
# End of Program
channel5.stop()  # stops the music
vo.draw_end(win, resource_path)  # shows an end screen if a winner is determined and plays windows xp shut down sound
pg.mixer.quit()  # closes all sound channels
pg.quit()  # closes the window
sys.exit()  # ends the program
