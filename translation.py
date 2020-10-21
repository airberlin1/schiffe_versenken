"""module containing translation to different languages, currently german, english and latin"""

# -------
# button intentions
intention_dict_english = {  # to english
    "new": "New Game",
    "load": "Load Game",
    "Theme": "Theme",
    "Normal": "Default",
    "Kontrast": "Contrast",
    "Weihnachten": "Christmas",
    "Lautstärke": "Volume",
    "Weiter": "Continue",
    "Start": "Start",
    "Abbrechen": "Abort",
    "Leicht": "Easy",
    "Vollbild": "Fullscreen",
    "Abwechselnd schießen": "one shot each turn",
    "Zurueck": "Back",
    "Schwierigkeit": "Difficulty",
    "Mittel": "Medium",
    "Schwer": "Hard",
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
    "Menue": "Settings",
    "Speichern": "Save",
    "Sonstiges": "Other",
    "Statistik": "Stats",
    "Reset": "Reset Stats",
    "random": "Random",
    None: None
}
intention_dict_german = {  # to german
    "new": "Neues Spiel",
    "load": "Spiel Laden",
    "Theme": "Thema",
    "Normal": "Standard",
    "Kontrast": "Kontrast",
    "Weihnachten": "Weihnachten",
    "Lautstärke": "Ton",
    "Weiter": "Fortsetzen",
    "Start": "Start",
    "Leicht": "Leicht",
    "Abbrechen": "Abbrechen",
    "Schwer": "Schwer",
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
    "Menue": "Menü",
    "Speichern": "Speichern",
    "Sonstiges": "Sonstiges",
    "Statistik": "Statistiken",
    "Reset": "Zurücksetzen",
    "random": "Zufällig",
    None: None
}
intention_dict_latin = {  # to latin
    "new": "Nova Alea",
    "load": "Condita Alea",
    "Theme": "Color",
    "Normal": "Norma",
    "Kontrast": "Diversitas",
    "Weihnachten": "Festum",
    "Lautstärke": "Sonus",
    "Weiter": "Persevero",
    "Start": "Initium",
    "Abbrechen": "Destruo",
    "Leicht": "Facilis",
    "Schwer": "Difficilior",
    "Vollbild": "Nullus fenestra",
    "Abwechselnd schießen": "Per vices",
    "Zurueck": "Retro",
    "Schwierigkeit": "Difficultas",
    "Mittel": "Difficilis",
    "Fenster": "Fenestra",
    "Fehlschuss wechseln": "Percutere",
    "Bildeinstellungen": "Facies",
    "Unmoeglich": "Non potest",
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
    "Menue": "Mora",
    "Speichern": "Condo",
    "Sonstiges": "Aliae Res",
    "Statistik": "Statisticae",
    "Reset": "Novae",
    "random": "Casu",
    None: None
}

# ------
# chat messages
message_dict_german = {  # to german
    "Player": "[Spieler]: ",
    "Enemy": "[Gegner]: ",
    "System": "[System]: ",
    "destroyed": "Schiff zerstört: ",
    "success": "erfolgreicher Treffer an ",
    "failure": "Schuss verfehlt",
    "againhit": "Feld bereits beschossen",
    "save": "Spiel gespeichert",
    "missing": "Fehlende Datei '",
    "missingdir": "Dateipfad fehlt:",
    "loadingfailure": "Laden fehlgeschlagen"
}
message_dict_english = {  # to english
    "Player": "[Player]:   ",
    "Enemy": "[Enemy]:  ",
    "System": "[System]: ",
    "destroyed": "destroyed ",
    "success": "successful hit on ",
    "failure": "missed shot",
    "againhit": "field was already targeted",
    "save": "game saved",
    "missing": "missing file '",
    "missingdir": "missing directory:",
    "loadingfailure": "game could not be loaded"
}
message_dict_latin = {  # to latin
    "Player": "[Lusor]:      ",
    "Enemy": "[Hostis]:     ",
    "System": "[Systema]: ",
    "destroyed": "navus deletus est: ",
    "success": "efficax iactus in ",
    "failure": "iactus not inventus est",
    "againhit": "locus tela coniectus est",
    "save": "ludos conservatus est",
    "missing": "deest tabularium '",
    "missingdir": "deest semita tabularii:",
    "loadingfailure": "Vitium"
}
# ------
# table contents
table_dict_german = {  # into german
    "": " ",
    "Remaining Ships": "Restliche Schiffe",
    "Enemy": "Gegner",
    "Player": "Spieler",
    "Ship": "Schiff",
    "Ships": "Schiffe",
    "Stats": "Statistik",
    "sum": "Gesamt",
    "easy": "Einfach",
    "medium": "Mittel",
    "hard": "Schwer",
    "impossible": "Unmöglich",
    "Games played": "Gespielt",
    "Games won": "Gewonnen",
    "Games lost": "Verloren",
    "Time spent": "Spielzeit",
    "Moves done": "Züge",
    "Ships hit": "Treffer",
    "Ships destroyed": "Zerstört"
}
table_dict_english = {  # into english
    "": " ",
    "Remaining Ships": "Remaining Ships",
    "Enemy": "Enemy",
    "Player": "Player",
    "Ship": "Ship",
    "Ships": "Ships",
    "Stats": "Stats",
    "sum": "Sum",
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
    "impossible": "Impossible",
    "Games played": "Games played",
    "Games won": "Games won",
    "Games lost": "Games lost",
    "Time spent": "Time spent",
    "Moves done": "Moves done",
    "Ships hit": "Ships hit",
    "Ships destroyed": "Ships destroyed"
}
table_dict_latin = {  # into latin
    "": " ",
    "Remaining Ships": "Navis Reliquae",
    "Enemy": "Hostis",
    "Player": "Lusor",
    "Ship": "Navis",
    "Ships": "Naves",
    "Stats": "Statistica",
    "sum": "Totus",
    "easy": "Facilis",
    "medium": "Difficilis",
    "hard": "Difficilior",
    "impossible": "Non Potest",
    "Games played": "Ludi",
    "Games won": "Victoriae",
    "Games lost": "Clades",
    "Time spent": "Tempus",
    "Moves done": "Iacti",
    "Ships hit": "Successi",
    "Ships destroyed": "Excidia"
}
table_dicts = [table_dict_english, table_dict_german, table_dict_latin]


def translate_number_latin(number):
    """
    translates a number into latin numerals

    :param number: int; number that is translated
    :return: str; number in latin numebrals
    """
    latin_number = ""
    if number >= 1000000:
        latin_number = "M\u0305"
        number -= 1000000
    if number >= 900000:
        latin_number += "C\u0305M\u0305"
        number -= 900000
    if number >= 500000:
        latin_number += "D\u0305"
        number -= 500000
    if number >= 400000:
        latin_number += "C\u0305D\u0305"
        number -= 400000
    while number >= 100000:
        latin_number += "C\u0305"
        number -= 100000
    if number >= 90000:
        latin_number += "X\u0305C\u0305"
        number -= 90000
    if number >= 50000:
        latin_number += "L\u0305"
        number -= 50000
    if number >= 40000:
        latin_number += "X\u0305L\u0305"
        number -= 40000
    while number >= 10000:
        latin_number += "X\u0305"
        number -= 10000
    if number >= 9000:
        latin_number += "MX\u0305"
        number -= 9000
    if number >= 5000:
        latin_number += "V\u0305"
        number -= 5000
    if number >= 4000:
        latin_number += "MV\u0305"
        number -= 4000
    while number >= 1000:
        latin_number += "M"
        number -= 1000
    if number >= 900:
        latin_number += "CM"
        number -= 900
    if number >= 500:
        latin_number += "D"
        number -= 500
    if number >= 400:
        latin_number += "CD"
        number -= 400
    while number >= 100:
        latin_number += "C"
        number -= 100
    if number >= 90:
        latin_number += "XC"
        number -= 90
    if number >= 50:
        latin_number += "L"
        number -= 50
    if number >= 40:
        latin_number += "XL"
        number -= 40
    while number >= 10:
        latin_number += "X"
        number -= 10
    if number >= 9:
        latin_number += "IX"
        number -= 9
    if number >= 5:
        latin_number += "V"
        number -= 5
    if number >= 4:
        latin_number += "IV"
        number -= 4
    while number >= 1:
        latin_number += "I"
        number -= 1
    if not latin_number:
        latin_number = "Nihil"
    return latin_number


def get_dict(language, dict_type):
    """
    gets dictionary used to translate things
    :param language: str; language all texts are currently displayed in
    :param dict_type: str; thing that is translated
    :return: dict; dictionary translating things
    """
    if dict_type == "message":  # messages are translated
        if language == "german":  # texts are displayed in german
            dictionary = message_dict_german
        elif language == "english":  # texts are displayed in english
            dictionary = message_dict_english
        else:  # texts are displayed in latin
            dictionary = message_dict_latin
    elif dict_type == "button":  # buttons' intentions are translated
        if language == "german":  # texts are displayed in german
            dictionary = intention_dict_german
        elif language == "english":  # texts are displayed in english
            dictionary = intention_dict_english
        else:  # texts are displayed in latin
            dictionary = intention_dict_latin
    elif dict_type == "table":  # table's content is translated
        if language == "german":  # texts are displayed in german
            dictionary = table_dict_german
        elif language == "english":  # texts are displayed in english
            dictionary = table_dict_english
        else:  # texts are displayed in latin
            dictionary = table_dict_latin
    else:
        dictionary = None  # erases might not be referenced marking, doesn't alter usability
    return dictionary  # returns requested dictionary
