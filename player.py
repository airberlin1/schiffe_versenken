# commented english
# module player that looks over the player's plays


# ------
# initializes player
def __init__player():
    """
    iniatialisiert den spieler und Kontrollisten, um doppelte Eingabe zu vermeiden
    :return: nothing
    """
    global hit_list
    global feld
    global done_clicks
    done_clicks = [[0, 0]]  # erstellt Kontrollliste fuer bereits angeklickte Felder, um dies rueckgaengig zu machen
    feld = [-1, -1]  # erstellt Liste mit aktuell angeklicktem Feld
    # erstellt Kontrolliste fuer schon getroffene Felder
    hit_list = []
    for x in range(10):
        hit_list.append([])
        for y in range(10):
            hit_list[x].append(0)


# ------
# refreshes check lists
def _add_field(xcoord, ycoord):
    """
    adds a field to the list with previously done clicks
    :param xcoord: int; x coordiante of the selected field
    :param ycoord: int; y coordiante of the selected field
    :return: nothing
    """
    done_clicks.append([xcoord, ycoord])


def set_angeklicktes_feld(xcoord, ycoord):
    """
    refreshes the clicked field
    :param xcoord: int; x coordiante of the selected field
    :param ycoord: int; y coordiante of the selected field
    :return: nothing
    """
    global feld
    feld = [xcoord, ycoord]  # refreshes the clicked field
    _add_field(xcoord, ycoord)  # adds that field to the list with previously done clicks


def change_hit_list(xcoord, ycoord):
    """
    refreshes the checklist with previously hit fields
    :param xcoord: int; x coordiante of the selected field
    :param ycoord: int; y coordiante of the selected field
    :return: bool; whether the field could be hit
    """
    if hit_list[xcoord][ycoord] == 1:  # checks, whether the field got hit previously
        return False
    else:
        hit_list[xcoord][ycoord] = 1  # refreshes the list
        return True


# ------
# returns check values
def get_angeklicktes_feld():
    """
    returns the clicked field
    :return: list[int, int]; clicked field
    """
    return feld


def get_hit_list_player():
    """
    returns the list that controls previously hit fields
    :return: list[list[int, int, ...], ...]; list that controls previously hit fields
    """
    return hit_list


def get_last_click():
    """
    returns the previously done click
    :return: list[int, int]; previously done click
    """
    return done_clicks[-1]
