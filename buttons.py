# commented, partly german
# Modul, in dem sich die Knoepfe befinden, wobei hier sowohl deren Koordinaten als auch die Ausgabe vorhanden sind
# TODO Sprachen aendern ermoeglichen
# TODO Sprachen mit Flaggen kennzeichenen
# TODO Luecke entfernen
# ------
# importiert pygame, das zur Ausgabe der Knoepfe genutzt wird und die Schrift
import pygame
import writing

# -------
# die Liste mit den Knopfbeschriftungen auf Deutsch
# Dabei sind in der obersten Reihe die Beschriftungen für den ersten Knopf zu finden, in der zweiten die des zweiten etc
# Die Spalten sind so organisiert, dass eine Spalte jeweils gleichzeitig zu sehen ist
intention_list = [
        ["Start",             "Leicht",     "Vollbild",    "Ozean",      "Deutsch", "Zurueck", None, "Zurueck", "Normal"],
        ["Schwierigkeit",     "Mittel",     "Fenster",     "Weltall",    "English", None, None, None, "Kontrast"],
        ["Bildeinstellungen", "Unmoeglich", "Hintergrund", "Gezeichnet", "Latinum", None, None, None, "Weihnachten"],
        ["Sprache",           "Zurueck",    "Theme",     "Zurueck",    "Zurueck", None, None, None, "Zurueck"],
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
# Die Uebersetzungen fuer die Knoepfe in verschiedene Sprachen
# auf Englisch
intention_dict_english = {
    "Theme": "Theme",
    "Normal": "Default",
    "Kontrast": "Contrast",
    "Weihnachten": "Christmas",
    "Lautstärke": "Volume",
    "Weiter": "Continue",
    "Start": "Start",
    "Leicht": "Easy",
    "Vollbild": "Fullscreen",
    "Abwechselnd schießen": "one shot each turn",
    "Zurueck": "Back",
    "Schwierigkeit": "Difficulty",
    "Mittel": "Medium",
    "Fenster": "Window",
    "Fehlschuss wechseln": "shoot until miss",
    "Bildeinstellungen": "Screen",
    "Unmoeglich": "Impossible",
    "Ozean": "Ocean",
    "Anzahl der Schiffe": "Number of ships determines shots",
    "Regeln": "Rules",
    "Weltall": "Space",
    "Hilfe": "Help",
    "Gezeichnet": "Drawn",
    "Beenden": "Close",
    "Hintergrund": "Background",
    "Sprache": "Language",
    "Deutsch": "Deutsch",
    "English": "English",
    "Latinum": "Latinum",
    "Aufgeben": "Give Up",
    None: None
}
# auf Deutsch
intention_dict_german = {
    "Theme": "Thema",
    "Normal": "Standard",
    "Kontrast": "Kontrast",
    "Weihnachten": "Weihanchten",
    "Lautstärke": "Ton",
    "Weiter": "Fortsetzen",
    "Start": "Start",
    "Leicht": "Leicht",
    "Vollbild": "Vollbild",
    "Abwechselnd schießen": "Abwechselnd",
    "Zurueck": "Zurück",
    "Schwierigkeit": "Schwierigkeit",
    "Mittel": "Mittel",
    "Fenster": "Fenster",
    "Fehlschuss wechseln": "Fehlschuss",
    "Bildeinstellungen": "Bild",
    "Unmoeglich": "Unmöglich",
    "Ozean": "Ozean",
    "Anzahl der Schiffe": "Schiffanzahl",
    "Regeln": "Regeln",
    "Weltall": "Weltall",
    "Hilfe": "Hilfe",
    "Gezeichnet": "Gezeichnet",
    "Beenden": "Beenden",
    "Hintergrund": "Hintergrund",
    "Sprache": "Sprache",
    "Deutsch": "Deutsch",
    "English": "English",
    "Latinum": "Latinum",
    "Aufgeben": "Aufgeben",
    None: None
}
# auf Latein
intention_dict_latin = {
    "Theme": "Color",
    "Normal": "Norma",
    "Kontrast": "Diversitas",
    "Weihnachten": "Festum",
    "Lautstärke": "Sonus",
    "Weiter": "Persevero",
    "Start": "Initium",
    "Leicht": "Facilis",
    "Vollbild": "Nullus fenestra",
    "Abwechselnd schießen": "Per vices",
    "Zurueck": "Retro",
    "Schwierigkeit": "Difficultas",
    "Mittel": "Difficilis",
    "Fenster": "Fenestra",
    "Fehlschuss wechseln": "Percutere",
    "Bildeinstellungen": "Facies",
    "Unmoeglich": "Non potes",
    "Ozean": "Oceanus",
    "Anzahl der Schiffe": "Numerus navis",
    "Regeln": "Regulae",
    "Weltall": "Universum",
    "Hilfe": "Auxilium",
    "Gezeichnet": "Delineatus",
    "Beenden": "Termino",
    "Hintergrund": "Facies",
    "Sprache": "Lingua",
    "Deutsch": "Deutsch",
    "English": "English",
    "Latinum": "Latinum",
    "Aufgeben": "Excedo",
    None: None
}
# auf Spanisch
# Hinweis: noch nicht vorhanden, weitere moegliche Sprachen: andere Sprache, Franzoesisch, Daenisch etc


# -------
# classes "Button" and "ButtonWriting"
class Button:
    """Knoepfe auf der Oberflaeche"""

    def __init__(self, location_top_left, size_x, size_y, field_size_x, field_size_y, field_coords, intention,
                 liste, active, color_local, number):
        """
        initialisiert den jeweiligen Knopf
        :param location_top_left: list[int, int]; Koordinaten der oberen linken Ecke des Knopfes
        :param size_x: int; die Groesse des Knopfes in die Breite
        :param size_y: int; die Groesse des Knopfes in die Hoehe
        :param field_size_x: int; die Anzahl der Felder, die in den Knopf in der Breite passen
        :param field_size_y: int; die Anzahl der Felder, die in den Knopf in der Hoehe passen
        :param field_coords: list[list[int, int], list,...]; alle Felder, auf denen sich der Knopf befindet
        :param intention: str; Beschriftung des Knopfs, welche gleichzeitig auch den Sinn des Knopfes darstellt
        :param liste: str; Liste, in der sich dieser Knopf befindet
        :param active: bool; gibt an, ob der Knopf gerade ausgegeben wird oder nicht
        :param color_local: tuple(int, int, int); Farbe des Knopfes
        :param number: Nummer des Knopfes, die bei den Stratknoepfen relevant ist
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
        aendert die Koordinaten der Knoepfe, was bei Veraenderung der Oberflaeche benoetigt wird
        :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
        """
        # ueberprueft die Oberflaechenausrichtung und setzt ggf. eine Koordinate weiter hoch, da die Luecke zwischen den
        # beiden Spielfeldern nicht als eigenes feld gezaelht wird
        fieldcoord_top_left = self.field_coords[0]
        # setzt die neue obere Linke Ecke des Knopfes
        self.location_top_left = [int((fieldcoord_top_left[0] + (3 / 2)) * field_size),
                                  int((fieldcoord_top_left[1] + (3 / 2)) * field_size)]
        # setzt die Groesse des Knopfes neu
        self.size_x = self.field_size_x * field_size
        self.size_y = self.field_size_y * field_size

    def change_active(self):
        """
        aendert, ob der Knopf angezeigt wird, oder nicht
        :return: nothing
        """
        if self.active:
            self.active = False
        else:
            self.active = True

    def get_active_end_b(self, orientation):
        """
        bestimmt, ob der Knopf aktiv ist, je nach Ausrichtung der Oberflaeche und des Knopfes
        :param orientation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
        :return: bool; ob der Knopf aktiv ist
        """
        # ueberprueft Bildschirmausrichtung
        if orientation == "height":
            # da der erste Knopf bei einer hochkanten Ausrichtung aktiv sein soll,
            # wird in diesem Fall fuer den ersten True zurueckgegeben, und fuer den zweiten False
            if self.number == 101 or self.number == 103:
                return True
            else:
                return False
        else:
            # da der zweite Knopf bei einer nicht hochkanten Ausrichtung aktiv sein soll, wird in diesem Fall fuer den
            # zweiten True zurueckgegeben, und fuer den ersten False
            if self.number == 100 or self.number == 102:
                return True
            else:
                return False

    def change_intention(self, task_number, orientation, zustand):
        """
        changes the use of a button
        :param task_number: int; number of the task the menu has to fulfill
        :param orientation: str; width/height, depending on what is bigger
        :param zustand: str; start/ingame/settings, what the program is currently doing
        """
        # ueberprueft, ob Knopf kein Startknopf ist
        if self.number > 98:
            # ueberprueft, ob das Spiel bereits gespielt wird
            if task_number == 6:
                # setzt den Knopf auf aktiv, falls er der Knopf der Endknoepfe ist, der zu sehen sein soll
                self.active = self.get_active_end_b(orientation)
            else:
                # setzt den Knopf auf inaktiv, falls keiner der Endknoepfe benoetigt wird
                self.active = False
        # setzt den Zweck des Startknopfes neu, wenn das Spiel sich noch am Start befindet
        elif task_number != 6:
            try:
                # setzt die Intetntion des Knopfes neu, nach der eigenen Nummer und der Nummer der aktuellen Aufgabe
                if zustand == "start":
                    self.intention = intention_list[self.number][task_number]
                elif zustand == "settings":
                    self.intention = intention_list_settings[self.number][task_number]
                # wenn sich hier nichts befindet, wird der Knopf auf inaktiv gesetzt, ansonsten auf aktiv
                if self.intention is None:
                    self.active = False
                else:
                    self.active = True
            except IndexError:
                # wenn sich hier nichts befindet, wird der Knopf auf inaktiv gesetzt, ansonsten auf aktiv
                self.intention = None
                self.active = False
        else:
            # wenn das Spiel bereits gespielt wrid, wird der Startknopf auf inaktiv gesetzt
            self.intention = None
            self.active = False

    def draw(self, screen):
        """
        gibt den Knopf auf dem Bildschirm aus
        :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
        :return: nothing
        """
        pygame.draw.rect(screen, self.color,
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 0)


class ButtonWriting(writing.Writing):
    """Schrift auf den Knoepfen"""

    def __init__(self, content, font, color_local, top_left_corner, button, background, active):
        """
        initialisiert die Schrift
        :param content: str; Inhalt der Schrift
        :param font: SysFont; Schrift
        :param color_local: tuple(int, int, int); Farbe der Schrift
        :param top_left_corner: list[int, int]; Koordinaten der oberen linken Ecke der Schrift
        :param button: Button; zugehoeriger Knopf
        :param background: tuple(int, int, int); Hintergrundfarbe der Schrift
        :param active: bool; gibt an, ob die Schrift gerade ausgegeben wird oder nicht
        """
        super().__init__(content, font, color_local, top_left_corner, background)  # initializes the writing
        self.button = button
        self.active = active

    def change_loc_coords(self, field_size):
        """
        aendert die obere linke Ecke und die Groesse der Schrift
        :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
        """
        self.top_left_corner = _get_top_left_corner_writing(self.button, field_size)  # setzt die obere linke Ecke neu
        font_size = int(field_size * 2)  # berechnet die Groesse der Schrift neu
        self.font = pygame.font.SysFont(None, font_size)  # setzt die Schrift neu

    def refresh_content(self, language):
        """
        erneuert den Inhalt der Schrift, und, ob die Schrift aktiv ist
        :param language: str; aktuelle Sprache, in der der text ausgegeben wird
        :return: nothing
        """
        self.content = _get_writing_content(self.button.liste, language, self.button.number)  # setzt den Inhalt neu
        self.active = self.button.active  # setzt sich auf inaktiv bzw. aktiv


# -------
# buttons' creation
def _create_start_buttons(field_size, button_bg_color):
    """
    erstellt die Knoepfe, die bei Beginn sichtbar sind
    :param field_size: float; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: nothing
    """
    # erstellt Liste fuer die Knoepfe
    global start_buttons
    start_buttons = []
    # setzt die obere linke Ecke zuerst auf ganz links oben und die Groesse der Knoepfe
    loc_tl = [int(3 / 2 * field_size), int(3 / 2 * field_size)]
    size_x = field_size * 9
    size_y = field_size * 2
    # erstellt sechs Startknoepfe
    for i in range(6):
        # erstellt eine Liste, in der spaeter die Koordinaten des Knopfes zu finden sind
        field_coords = []
        x = 0
        # erstellt die 16 Koordinaten der jeweiligen Startknoepfe
        for j in range(22):
            field_coords.append([0, 0])
            # setzt die zweite Koordinate auf null bzw. eins, da die Knoepfe jeweils 2 Felder hoch sind
            if j < 11:
                y = 0
            elif j == 11:
                # setzt die erste Koordinate zurueck auf 0, wenn mit der zweiten Reihe der Koordinaten begonnen wird,
                # und die zweite Koordinate um eins hoeher, um die zweite Reihe der Koordinaten zu erreichen
                y = 1
                x = 0
            else:
                y = 1
            # aendert die zweite Koordinate weiter nach oben, wenn nicht der erste Knopf erstellt wird,
            # da die anderen Knoepfe weiter unten liegen
            y += 3 * i
            # setzt die beiden Koordinaten in die Liste der Koordinaten ein
            field_coords[j][0] = x
            field_coords[j][1] = y
            # setzt die erste Koordinate nach oben, um die Koordinaten daneben zu erreichen
            x += 1
        # erstellt die Knoepfe mit den vorher ermittelten Werten und fuegtt sie in die Liste ein
        start_buttons.append(0)
        start_buttons[i] = Button(loc_tl, size_x, size_y, 11, 2, field_coords, "unfilled", "start_buttons", True,
                                  button_bg_color, i)
        # aendert die Ecke links oben um drei Felder nach unten
        loc_tl[1] += 3 * field_size


def _get_loc_top_left_end_b(end_button_number):
    """
    returns the top left field coordinate of the end button
    :param end_button_number: int; end button's number
    :return: list[int, int]; coordinate of the button's top left corner
    """
    if end_button_number == 0:
        return 25 / 2, 25 / 2  # 0 is the end button while orientation == "width"

    elif end_button_number == 1:
        return 25 / 2, 25 / 2  # 1 is the end button while orientation == "height"

    elif end_button_number == 2:
        return 9 / 2, 25 / 2  # 2 is the settings button while orientation == "width"

    elif end_button_number == 3:
        return 25 / 2, 19 / 2  # 3 is the settings button while orientation == "height"


def _get_field_coords_end_b(end_button_number):
    """
    returns a list with an end button's coordiantes.
    This list than holds all the coordinates on which the button can be clicked
    :param end_button_number: int; end button's number
    :return: list[list[int, int], list[int, int], ...]; coordiantes the button is on
    """
    if end_button_number == 0:  # 0 is the end button while orientation == "width"
        xcoord_count = 7  # sets the width of the button
        start_coord = [11, 11]  # sets the top left field coord of the button

    elif end_button_number == 1:  # 1 is the end button while orientation == "height"
        xcoord_count = 8  # sets the width of the button
        start_coord = [11, 11]  # sets the top left field coord of the button

    elif end_button_number == 2:  # 2 is the settings button while orientation == "width"
        xcoord_count = 7  # sets the width of the button
        start_coord = [3, 11]  # sets the top left field coord of the button

    else:  # 3 is the settings button while orientation == "height"
        xcoord_count = 8  # sets the width of the button
        start_coord = [11, 8]  # sets the top left field coord of the button

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
            # sets the x coordiante to the same as the start x coordinate when the second line gets started
            next_coord[0] = start_coord[0]
        else:
            # sets the y coordiante to one plus the start y coordinate, if the second line of coordinates is added
            next_coord[1] = start_coord[1] + 1

        # adds 1 to the x-coordinate, so that the field coord next to the one before can be added
        next_coord[0] += 1
    return field_coords  # returns the coordiantes the button is on


def _create_end_buttons(field_size):
    """
    creates buttons to end the game and to go to the settings ingame
    :param field_size: float; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: nothing
    """
    # erstellt eine Liste, in der spaeter die Knoepfe zum beenden des Spiels sind
    global end_buttons
    end_buttons = []
    for i in range(4):
        # setzt die Koordianten fuer die obere linke Ecke
        loc_tl = _get_loc_top_left_end_b(i)
        # setzt die Breite des Knopfes, da diese sich bei den beiden unterscheidet
        field_count_x = 8 - 1 * (1 - (i % 1))
        # setzt die Groesse des jeweiligen Knopfes
        size_x = field_count_x * field_size
        size_y = 2 * field_size + i * field_size
        # setzt die Koordinaten, auf denen der Knopf angeklickt werden kann
        field_coords = _get_field_coords_end_b(i)
        if i < 2:
            color = (170, 0, 0)
        else:
            color = (0, 50, 0)
        # erstellt die Knoepfe mit den noetigen Werten und Koordinaten
        end_buttons.append(0)
        end_buttons[i] = Button(loc_tl, size_x, size_y, field_count_x, 2, field_coords, "Beenden", "end_buttons",
                                False, color, i + 100)


def _create_buttons(field_size, button_bg_color):
    """
    erstellt die Knoepfe, die auf der Oberflaeche erscheinen
    :param field_size: float; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: nothing
    """
    # erstellt die beiden Listen
    _create_start_buttons(field_size, button_bg_color)
    _create_end_buttons(field_size)


# -------
# Initialisere die Schrift auf den Knoepfen
def _get_writing_content(button_list, language, button_number):
    """
    gibt die Schrift auf dem Knopf zurueck
    :param button_list: str; Liste, in dem sich der Knopf befindet
    :param language: str; Sprache, in der der Inhalt ausgegebn wird
    :param button_number: int; Nummer des Knopfes
    :param start_buttons: list[Button, Button, ...]; Liste mit den Startknoepfen
    :return: str; Inhalt der Schrift auf dem Knopf
    """
    # ueberprueft, in welcher Liste sich der Knopf befindet
    if button_list == "start_buttons":
        # wenn sich der Knopf in der Liste mit den Satrtknoepfen befindet, wird entweder direkt die Intention des
        # zugehoerigen Knopfes oder die Uebersetzung in die aktuelle Sprache zurueckgegeben
        if language == "german":
            return intention_dict_german[start_buttons[button_number].intention]
        elif language == "english":
            return intention_dict_english[start_buttons[button_number].intention]
        elif language == "latin":
            return intention_dict_latin[start_buttons[button_number].intention]
    else:
        # wenn sich der Knopf nicht in der Liste der Satrtknoepfe befindet, wird "Beenden" in der jeweiligen Sprache
        # zurueckgegeben, da der Knopf sich dann in der Liste der Endknoepfe befinden muss
        if button_number < 102:
            if language == "german":
                return "Beenden"
            elif language == "latin":
                return "Excedo"
            else:
                return "Give Up"
        else:
            if language == "german":
                return "Menü"
            elif language == "latin":
                return "Mora"
            else:
                return "Settings"


def _get_font_button(field_size):
    """
    ermittelt die Schrift und gibt diese zurueck
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: SysFont; Schrift
    """
    # ermittelt die Groesse der Schrift je nach Groese eines virtuellen Feldes
    font_size = int(field_size * 2)
    # gibt die Schrift zurueck
    return pygame.font.SysFont(None, font_size)


def _get_top_left_corner_writing(button, field_size):
    """
    ermittelt die obere linke Ecke der Schrift
    :param button: Button; zu der Schrift zugehoeriger Knopf
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: list[int, int]; Die Koordinate der oberen linken Ecke der Schrift
    """
    # erhaelt die obere linke Koordinate des zugehoerigen Knopfes
    xcoord, ycoord = button.location_top_left
    # addiert beide Werte mit einem zusaeetzlichen Wert, sodass die Schrift etwas weiter unten rechts beginnt,
    # als an der Stelle, an der sich die obere linke Ecke des Knopfes befindet
    distance = int(field_size / 2.5)
    xcoord += distance
    ycoord += distance
    # gibt die Koordinate der oberen linken Ecke der Scxhrift zurueck
    return xcoord, ycoord


def __init__button_writings(language, color_writing, color_end_b_writing, field_size):
    """
    erstellt die Schrift auf den Knoepfen
    :param language: str; aktuelle Sprache, in der der Inhalt ausgegeben wird
    :param color_writing: tuple(int, int, int); Farbe der Schrift auf den Startknoepfen
    :param color_end_b_writing: tuple(int, int, int); Farbe der Schrift auf den Endknoepfen
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: nothing
    """
    # erstellt eine leere Liste, in der spaeter die Schrift der Startknoepfe zu finden ist
    global button_writings_start
    button_writings_start = []
    for button in start_buttons:
        # geht alle Startknoepfe durch und erstellt fuer jeden eine Schrift,
        # die dann in die zuvor erstellte Liste eingefuegt wird
        button_writings_start.append(ButtonWriting(_get_writing_content("start_buttons", language, button.number),
                                                   _get_font_button(field_size), color_writing,
                                                   _get_top_left_corner_writing(button, field_size),
                                                   button, None, True))
    # erstellt eine leere Liste, in der spaeter die Schrift der Endknoepfe zu finden ist
    global button_writings_end
    button_writings_end = []
    for button in end_buttons:
        # geht alle Endknoepfe durch und erstellt fuer jeden eine Schrift,
        # die dann in die zuvor erstellte Liste eingefuegt wird
        button_writings_end.append(ButtonWriting(_get_writing_content("end_buttons", language, 0),
                                                 _get_font_button(field_size), color_end_b_writing,
                                                 _get_top_left_corner_writing(button, field_size), button, None, False))


# -------
# initialisiere das Modul "buttons"
def __init__buttons(language, color_writing, color_end_b_writing, field_size, button_bg_color):
    """
    initialisiert das Modul "buttons"
    :param language: str; aktuelle Sprache, in der der Inhalt ausgegeben wird
    :param color_writing: color_writing: tuple(int, int, int); Farbe der Schrift auf den Startknoepfen
    :param color_end_b_writing: color_end_b_writing: tuple(int, int, int); Farbe der Schrift auf den Endknoepfen
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :return: nothing
    """
    # erstellt die Knoepfe, die auf der Oberflaeche zu sehen sind
    _create_buttons(field_size, button_bg_color)
    # erstellt die Schrift auf den Knoepfen
    __init__button_writings(language, color_writing, color_end_b_writing, field_size)


# -------
# erneure die Koordinaten der Knoepfe und der Schrift darauf
def refresh_loc_buttons(field_size, orientation, zustand):
    """
    setzt die Koordinaten der Knoepfe neu, noetig wenn die Oberflaeche veraendert wird
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :param zustand: str; ingame/start/settings, depending on what the program is doing
    """
    for start_button in start_buttons:
        # geht alle Startknoepfe durch und aktualisiert deren Koordinaten
        start_button.change_loc_coords(field_size)
    button_number = 0
    for end_button in end_buttons:
        # geht alle Endknoepfe durch und aktualisiert deren Koordinaten
        end_button.change_loc_coords(field_size)
        # setzt den Knopf auf inaktiv oder aktiv, falls das Spiel bereits gespielt wird
        if zustand == "ingame":
            end_button.active = end_button.get_active_end_b(orientation)
        button_number += 1


def refresh_loc_writing(field_size, zustand):
    """
    setzt die Koordinaten fuer die Schrift neu, noetig bei Veraenderung der Oberflaeche
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param zustand: str; gibt an, ob das Spiel bereits gespielt wird, oder sich noch am Start befindet
    :return: nothing
    """
    for button_writing in button_writings_start:
        # geht die Liste mit der Schrift der Startknoepfe durch und aktualisiert die Koordinaten der Schrift
        button_writing.change_loc_coords(field_size)
    # erstellt eine variable, die durch die Knoepfe durchzaehlt und dabei die Nummer des aktuellen Knopfes darstellt
    button_number = 0
    for button_writing in button_writings_end:
        # geht die Liste mit der Schrift der Endknoepfe durch und aktualisiert die Koordinaten der Schrift
        button_writing.change_loc_coords(field_size)
        # aktualsiert dei Aktivitaet der Schrift auf den Endknoepfe, wenn das Spiel bereits gespielt wird
        if zustand == "ingame":
            button_writing.active = button_writing.button.active
        # zaehlt bei der Nummer der Knoepfe einen weiter, nachdem ein Knopf behandelt wurde
        button_number += 1


# -------
# erneure die Intention und dei Aktivitaet der Knoepfe
def _refresh_intention_buttons(task_number, orientation, zustand):
    """
    erneuert die Intention und Aktivitaet der Knoepfe
    :param task_number: int; Nummer der aktuellen Aufgabe des Programms
    :param orientation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    :param zustand: str; start/ingame/settings, what the program is currently doing
    """
    for button in start_buttons:  # geht alle Startknoepfe durch
        button.change_intention(task_number, orientation, zustand)  # aendert deren Intention und Aktivitaet
    for button in end_buttons:  # geht alle Endknoepfe durch
        button.change_intention(task_number, orientation, zustand)  # aendert deren Intention und Aktivitaet


def _refresh_content_b_writing(language):
    """
    erneuert den Inhalt der Schrift auf den Knoepfen
    :param language: str; aktuelle Sprache, in der der text ausgegeben wird
    :return: nothing
    """
    for onewriting in button_writings_start:  # geht die Schrift fuer die Startknoepfe durch
        onewriting.refresh_content(language)  # erneuert den Inhalt dieser Schrift
    for onewriting in button_writings_end:  # geht die Schrift fuer die Endknoepfe durch
        onewriting.refresh_content(language)  # erneuert den Inhalt dieser Schrift


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
    for button in start_buttons:
        button.color = bg_color
    for local_writing in button_writings_start:
        local_writing.color = writing_color


# -------
# gibt die Knoepfe aus
def draw_buttons(screen):
    """
    gibt die Knoepfe auf dem Bildschirm aus
    :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
    :return: nothing
    """
    for button in start_buttons:  # geht alle Startknoepfe durch
        if button.active:
            button.draw(screen)  # gibt den Knopf aus, falls dieser aktiv ist
    for button in end_buttons:  # geht alle Endknoepfe durch
        if button.active:
            button.draw(screen)  # gibt den Knopf aus, falls dieser aktiv ist
    for onewriting in button_writings_start:  # geht die Schrift fuer die Startknoepfe durch
        if onewriting.active:
            onewriting.draw(screen)  # gibt die Schrift aus, falls diese aktiv ist
    for onewriting in button_writings_end:  # geht die Schrift fuer die Endknoepfe durch
        if onewriting.active:
            onewriting.draw(screen)  # gibt die Schrift aus, falls diese aktiv ist


# ------
# returns the buttons
def get_buttons():
    """
    return all buttons
    :return: list[list[Button, ...], list[Button, ...]; lists with all buttons
    """
    return start_buttons, end_buttons
