# import fixed
import random as rd
import player_smart as ps
# TODO Modul sortieren
# TODO kommentieren


def get_play_list():
    return ps.get_play_list_ps()


def __init__enemy(length_x, length_y):
    ps.__init__player_smart(length_x, length_y)
    # initialisiert den Gegner und eine Kontrollliste, um doppelte Eingaben zu vermeiden
    global hit_list
    global known_hits
    global done_plays
    done_plays = [[2, 2]]
    hit_list = []
    for x in range(10):
        hit_list.append([])
        for y in range(10):
            hit_list[x].append(0)
    known_hits = []
    for x in range(10):
        known_hits.append([])
        for y in range(10):
            known_hits[x].append(0)


def _enemy_medium(hit, ship_number, destroyed):
    shot = ps.do_shot(hit, ship_number, destroyed)
    hit_list[shot[0]][shot[1]] = 1
    done_plays.append([shot[0], shot[1]])
    return shot[0], shot[1]


def do_enemy_move(rule, hit, ship_number, destroyed, dif, ship_count, ship_coordinates):
    """fuehrt den Zug des computergegners aus"""
    # TODO Regeln
    # TODO Variablennamen
    # ueberprueft die regeln, um festzustellen, wie viele Zuege erlaubt sind
    if rule == 1:
        hi = 1
    elif rule == 2:
        hi = 1
    elif rule == 3:
        hi = ship_count
    else:
        hi = 0
    x = 0
    # fuehrt diese Anzahl der Zuege aus
    while x < hi:
        x += 1
        # Schwierigkeit ueberpruefen, um den Zug je nach Schwierigkeit zu bestimmen
        if dif == "easy":
            hit = _enemy_easy()
        elif dif == "medium":
            hit = _enemy_medium(hit, ship_number, destroyed)
        elif dif == "impossible":
            hit = _enemy_impossible(ship_coordinates)
        if rule == 2:
            # bei Wechsel des Spielers nach nicht getroffenem Schiff, wird ueberprueft, ob Schiff getroffen und
            # dementsprechend Schleife beendet oder auch nicht
            pass
    return hit


def get_random_field(length_x, length_y):
    rand_field = ps.add_random_target(length_x, length_y)
    return rand_field


def _enemy_easy():
    """bestimmtden zufaellig den Zug, wenn die Schwierigkeit einfach gewaehlt wurde"""
    # TODO Vraiablennamen
    x, y = ("x", "y")
    hi = True
    while hi:
        # zufaelligen Wert waehlen
        hi = False
        x = rd.randint(0, 9)
        y = rd.randint(0, 9)
        # ueberpruefen, ob Feld bereits getroffen wurde
        if hit_list[x][y] == 1:
            hi = True
    # Checkliste aktualisieren
    hit_list[x][y] = 1
    done_plays.append([x, y])
    return x, y


def _enemy_impossible(ship_coordinates):
    """bestimmt den gegnerischen Zug aufgrund der dem Computer bereits bekannten Positionen der Schiffe"""
    for ship_coordinate in ship_coordinates:
        if hit_list[ship_coordinate[0]][ship_coordinate[1]] == 0:
            hit_list[ship_coordinate[0]][ship_coordinate[1]] = 1
            done_plays.append([ship_coordinate[0], ship_coordinate[1]])
            return ship_coordinate[0], ship_coordinate[1]


def get_last_play(zug):
    return done_plays[zug]


def get_hit_list_enemy():
    # gibt die Liste der bereits beschossenen Felder zurueck
    return hit_list
