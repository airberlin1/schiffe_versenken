"""module containing constants used in different places all over the project"""
LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
DIFFICULTIES = ("easy/", "medium/", "hard/", "impossible/")
STATS = ("games", "won", "lost", "time", "moves", "hit", "destroyed")
SHIPNAMES = ("None", "None", "FisherShip", "ShipShip", "ContainerShip", "CruiseShip")
DIRECTIONS = ("horizontalright", "verticalup", "horizontalleft", "verticaldown")
DEFAULTPOSITIONS = ([11.5, 0, 3], [12.5, 0, 3], [13.5, 0, 3], [14.5, 0, 3], [15.5, 0, 3], [16.5, 0, 3])
# colors
LIGHTGREEN = (0, 255, 100)
DARKGREEN = (0, 110, 0)
DARKRED = (125, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
TRANS = (1, 1, 1)
RED = (170, 0, 0)
DARKERGREEN = (0, 50, 0)
DARKBLUE = (0, 0, 100)
LIGHTRED = (255, 0, 0)
LIGHTGREY = (170, 170, 170)
# button's intentions
INTENTIONSSTART = (
        ("Start", "Leicht", "Vollbild", "Ozean", "Deutsch", "Hilfe", None, "Zurueck", "Normal", "Zurueck"),
        ("Schwierigkeit", "Mittel", "Fenster", "Weltall", "English", "Statistik", None, None, "Kontrast", "Reset"),
        ("Bildeinstellungen", "Schwer", "Hintergrund", "Gezeichnet", "Latinum", "Lautstärke", None, None,
         "Weihnachten"),
        ("Sprache", "Unmoeglich", "Theme", "Zurueck", "Zurueck", "Zurueck", None, None, "Zurueck"),
        ("Sonstiges", "Zurueck", "Zurueck"),
        ("Beenden", None)
)
INTENTIONSSETTINGS = (
    ("Weiter",            None, "Vollbild",    "Ozean",      "Deutsch", "Hilfe", None, "Zurueck", "Normal", "Zurueck"),
    ("Bildeinstellungen", None, "Fenster",     "Weltall",    "English", "Statistik", None, None, "Kontrast", "Reset"),
    ("Sprache",           None, "Hintergrund", "Gezeichnet", "Latinum", "Zurueck", None, None, "Weihnachten"),
    ("Lautstärke",        None, "Theme",       "Zurueck",    "Zurueck", None, None, None, "Zurueck"),
    ("Sonstiges",  None, "Zurueck"),
    ("Aufgeben", None)
)
END_BUTTON_DICT = {
    0: "end",
    1: "settings",
    2: "save"
}
