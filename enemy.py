"""enemy module creating, managing and monitoring enemy's moves"""

# ------
# neccessary imports
import random as rd  # randomize moves on easy difficulty
import enemy_medium as em  # creates moves on medium and hard difficulty
import save  # used to load and save moves between app starts
import chat  # used to display eror messages


# ------
# initialization
def reset_hit_list(field_count):
    """
    returns a new hit list used to avoid doubling moves
    :param field_count: list[int, int]; board's size
    :return: list[list[0, ...], ...]; new hit_list
    """
    hit_list = [[False for _ in range(field_count[1])] for _ in range(field_count[0])]
    return hit_list


def _enemy_easy(field_count):
    """
    adds the enemy's moves to shots

    takes random fields and puts them in the shots list, until all fields can be found in the shot list so that no
        matter when the last ship is destroyed, there will be a move to do so

    the shots list is later filled with all shots needed for hte enemy to play the game,
        and the shots will then be played from [0] to [-1]

    :param field_count: list[int, int]; size of one playfield in small fields
    """
    global shots
    hit_list = reset_hit_list(field_count)  # creates list to avoid doubling moves

    field_count_x, field_count_y = field_count
    xcoord, ycoord = ("x", "y")

    while shots.__len__() < (field_count_y * field_count_x + 1):  # enough shots to cover the whole board are created
        field_selected = False
        # selects a random field, that has npt been selected before
        while not field_selected:
            field_selected = True
            # selects a random field
            xcoord = rd.randint(0, 9)
            ycoord = rd.randint(0, 9)
            if hit_list[xcoord][ycoord] == 1:  # checks, whether that field was already selected before
                field_selected = False

        hit_list[xcoord][ycoord] = 1  # refreshes checklist
        shots.append([xcoord, ycoord][:])  # adds that field to the shots list


def _enemy_impossible(ship_coordinates):
    """
    adds the enemies moves to shots

    adds all coordiantes an allied ship is placed on to the list shots

    the shots list is later filled with all shots needed for hte enemy to play the game,
        and the shots will then be played from [0] to [-1]

    :param ship_coordinates: list[list[int, int], list, ...]; coordinates of allied ship parts
    """
    global shots
    for ship_coordinate in ship_coordinates:  # geos through the coordiantes a ship is placed on
        shots.append([ship_coordinate[0], ship_coordinate[1]])  # adds that field to the shots list


def _create_moves_enemy(difficulty, field_count, ship_coordinates, ships):
    """
    creates enemy's moves

    :param difficulty: str; difficulty the palyer has chosen
    :param field_count: list[int, int]; size of the board
    :param ship_coordinates: list[list[int, int], list, ...]; list with all coordiantes inhabiting a ship
    :param ships: list[list[list[Ship, ...], ...], ...]; list containing all ships
    """
    global shots
    if difficulty == "easy":
        _enemy_easy(field_count)  # creates random moves

    elif difficulty == "medium" or difficulty == "hard":
        shots += em.enemy_mediumhard(ships, field_count, reset_hit_list, difficulty)  # creates moves less random

    elif difficulty == "impossible":
        _enemy_impossible(ship_coordinates)  # creates moves that hit everytime


def __init__enemy(load, language, resource_path, length_x, length_y, ship_coordinates=[[[0]]], difficulty="easy",
                  ships=[[[0]]], add_dir=""):
    """
    initializes enemy module and enemy's move

    :param load: bool; game is loaded and not newly created
    :param language: str; language all texts are currently displayed in
    :param resource_path: Func; returns a resoucre path to a relative path
    :param length_x: int; board size in x direction
    :param length_y: int; board size in y direction
    :param ship_coordinates: list[list[int, int], ...]; list with all coordiantes inhabiting a ship
    :param difficulty: str; easy/medium/hard/impossible
    :param ships: list[list[list[Ship, ...], ...], ...]; list containing all ships
    :param add_dir: str; additional directory used to save game sfrom different difficulties
    :return: bool or None; loading failed
    """
    global shots
    if load:  # game is laoded
        try:
            shots = save.load('lis', 'enemy', 1, resource_path, add_dir)  # shots are loaded
        except FileNotFoundError:
            chat.add_missing_message("enemy1.lis", resource_path("saves/"), language)  # adds message to chat
            return True  # interrupts loading and creates new game

    else:  # game is newly created

        shots = [[2, 2]]  # sets a start value so that in game function can be more easily readable

        _create_moves_enemy(difficulty=difficulty, field_count=(length_x, length_y), ship_coordinates=ship_coordinates,
                            ships=ships)  # creates enemy's moves


# ------
# in game
def get_enemy_move():
    """
    returns the next move of the enemy

    also returns the last move of the nemy and deletes it from shots

    the shots list is later filled with all shots needed for hte enemy to play the game,
        and the shots will then be played from [0] to [-1]

    :return: list[int, int, list[int, int]]; enemies last move, enemies next move
    """
    try:
        shot = shots[1]  # gets the next shot of the enemy
    except IndexError:
        shot = [2, 2]
    oldx, oldy = shots[0]  # gets the last shot of the enemy
    del shots[0]  # deletes it
    return oldx, oldy, shot  # returns both shots


# ------
# between games (technically in game)
def save_enemy(resource_path, language, add_dir):
    """
    saves enemy's remaining moves

    :param resource_path: Func; returns a resource path to a relative path
    :param language: str; language all texts are currently displayes in
    :param add_dir: str; additional directory used to save game sfrom different difficulties
    """
    try:
        save.save(shots, 'lis', 'enemy', 1, resource_path, add_dir)  # saves reamining shots of the enemy
    except FileNotFoundError:
        chat.add_missing_message("", resource_path("saves/"), language, False)  # displays error message
