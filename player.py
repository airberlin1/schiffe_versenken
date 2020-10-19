# commented english
# module player that looks over the player's plays
import save
import chat


# ------
# initializes player
def __init__player(load, resource_path, language, add_dir):
    """
    initializes player and its required lists to check for doublicating inputs

    :param load: bool; whether the game is loaded or newly created
    :param resource_path: Func; returns the resource path to a relative path
    :param language: str; lnguage all texts are currently displayed in
    :param add_dir: str; additional directory where loaded game is found
    """
    global hit_list
    global feld
    global done_clicks
    feld = [-1, -1]  # creates a list that contains the currently clicked field with a control value
    done_clicks = [[0, 0]]  # creates control to undo clicks when another field is clicked instead
    if load:
        # loads control for already targeted fields
        try:
            hit_list = save.load('lis', 'player', 1, resource_path, add_dir)
        except FileNotFoundError:
            chat.add_missing_message("player1.lis", resource_path("saves/"), language)
            return True
    else:
        # creates control for already targeted fields
        hit_list = [[0 for _ in range(10)] for _ in range(10)]


# ------
# refreshes check lists
def _add_field(xcoord, ycoord):
    """
    adds a field to the list with previously done clicks
    :param xcoord: int; x coordiante of the selected field
    :param ycoord: int; y coordiante of the selected field
    """
    done_clicks.append([xcoord, ycoord])


def set_angeklicktes_feld(xcoord, ycoord):
    """
    refreshes the clicked field
    :param xcoord: int; x coordiante of the selected field
    :param ycoord: int; y coordiante of the selected field
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


def save_player(resource_path, language, add_dir):
    """
    saves the list required to continue a game without the player being able to click previously hit fields

    :param resource_path: Func; returns the resource path to a relative path
    :param language: str; langauge all texts are currently displayed in
    :param add_dir: str; additional directory where loaded game is found
    """
    try:
        save.save(hit_list, 'lis', 'player', 1, resource_path, add_dir)  # saves the hit list [[0, 1,...], [], ...]
    except FileNotFoundError:
        chat.add_missing_message("", resource_path("saves/"), language, False)
