"""module containing translation to different languages, currently german, english and latin"""

# -------
# button intentions
# to english
intention_dict_english = {
    "new": "New Game",
    "load": "Load Game",
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
    "Menue": "Settings",
    "Speichern": "Save",
    None: None
}
# to german
intention_dict_german = {
    "new": "Neues Spiel",
    "load": "Spiel Laden",
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
    "Menue": "Menü",
    "Speichern": "Speichern",
    None: None
}
# to latin
intention_dict_latin = {
    "new": "Nova Alea",
    "load": "Condita Alea",
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
    "Menue": "Mora",
    "Speichern": "Condo",
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
    "success": "succesful hit on ",
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


def get_dict(language, dict_type):
    """
    gets dictionary used to translate things
    :param language: str; language all texts are curretnly displayed in
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
    else:
        dictionary = None  # erases might not be refrenced marking
    return dictionary
