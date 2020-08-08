# import fixed
import random as rd
import enemy_medium as em
import save
import chat
# TODO Modul sortieren
# TODO kommentieren


def get_play_list():
    return ps.get_play_list_ps()


def __init__enemy(load, language, resource_path, length_x, length_y, ship_coordinates, difficulty, ships):
    global hit_list
    global known_hits
    global shots
    if load:
        try:
            shots = save.load('lis', 'enemy', 1, resource_path)
        except FileNotFoundError:
            chat.add_missing_message("enemy1.lis", resource_path("saves/"), language)
            return True
    else:
        # initialisiert den Gegner und eine Kontrollliste, um doppelte Eingaben zu vermeiden

        shots = [[2, 2]]

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

        create_moves_enemy(difficulty=difficulty, field_count=(length_x, length_y), ship_coordinates=ship_coordinates,
                           ships=ships)


def _enemy_easy(field_count):
    """
    adds the enemy's moves to shots

    takes random fields and puts them in the shots list, until all fields can be found in the shot list so that no
        matter when the last ship is destroyed, there will be a move to do so

    the shots list is later filled with all shots needed for hte enemy to play the game,
        and the shots will then be played from [0] to [-1]

    :param field_count: list[int, int]; size of one playfield in small fields
    """
    field_count_x, field_count_y = field_count
    xcoord, ycoord = ("x", "y")

    while shots.__len__() < (field_count_y * field_count_x + 1):
        field_selected = False
        # selects a random field, that wasn't selected before
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
    for ship_coordinate in ship_coordinates:  # geos through the coordiantes a ship is placed on
        hit_list[ship_coordinate[0]][ship_coordinate[1]] = 1  # refreshes checklist
        shots.append([ship_coordinate[0], ship_coordinate[1]])  # # adds that field to the shots list


def create_moves_enemy(difficulty, field_count, ship_coordinates, ships):
    """"""
    global shots
    if difficulty == "easy":
        _enemy_easy(field_count)

    elif difficulty == "medium":
        shots += em.enemy_medium(ships, field_count)

    elif difficulty == "hard":
        shots += em.enemy_hard()  # TODO implement hard enemy

    elif difficulty == "impossible":
        _enemy_impossible(ship_coordinates)


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


def get_random_field(length_x, length_y):
    rand_field = ps.add_random_target(length_x, length_y)
    return rand_field


def get_hit_list_enemy():
    # gibt die Liste der bereits beschossenen Felder zurueck
    return hit_list


def save_enemy(resource_path, language):
    # saves remaining enemy moves for this game
    try:
        save.save(shots, 'lis', 'enemy', 1, resource_path)
    except FileNotFoundError:
        chat.add_missing_message("", resource_path("saves/"), language, False)
