import random
"""
module imported by enemy used to create medium and hard difficulties, currently only "medium"
"""


class Target:

    """
    used to control targets, not used in any other module
    """

    def __init__(self, location, ship_number):
        """
        :param location: list[int, int]; target's location
        :param ship_number: int or None; number of ship on the same location
        """
        self.location = location
        self.ship_number = ship_number

    def get_surrounding_locations(self):
        """
        creates surrounding locations to target's location

        :return: list[list[int, int], list, ...]; 4 surrounding targets
        """
        x_coord, y_coord = self.location  # unpacks location
        # calculates surrounding locations
        moves = [[x_coord - 1, y_coord], [x_coord + 1, y_coord], [x_coord, y_coord - 1], [x_coord, y_coord + 1]]
        return moves  # returns surrounding locations

    def convert(self):
        """
        converts itself into usable targets in enemy module
        :return: list[int, int]; targets location
        """
        return self.location


def _create_hit_list(board_size):
    """
    creates a control list used to monitor doubling targets and eliminating them

    :param board_size: list[int, int]; size of the game board
    """
    global hit_list
    hit_list = []
    for i in range(board_size[0]):  # goes through horizontal size
        hit_list.append([])
        for j in range(board_size[1]):  # goes through vertical size
            hit_list[i].append(False)  # adds False, because no target has been chosen yet


def _get_ship_positions(ships):
    """
    creates a list with every postion of allied ships

    also adds the fitting ship number to allow harder difficulties

    :param ships: list[list[Ship, Ship, ...], list]; all ships on the board
    :return: list[list[int, int, int, int], list...]; x-coordinate, y-coordinate, is hit?, ship_number
    """
    ship_positions = []
    for ship in ships[0]:  # goes through every allied ship
        next_positions = ship.list_pos()  # gets all positions of that ship
        for position in next_positions:  # goes through every of these positions
            position += [ship.identification_number]  # adds the ship number to that position
        ship_positions += next_positions  # adds these positions to the final list
    return ship_positions  # returns every allied ship's positions


def _is_hit(ship_positions, move):
    """
    checks which ship is on that move's location

    :param ship_positions: list[list[int, int, int, int], list...]; every allied ship's positions
    :param move: list[int, int]; next move, location that is inspected
    :return: int or None; hit ship's number or None if no ship will be hit
    """
    for position in ship_positions:  # goes through every location a ship is on
        if position[:2] == move:  # checks whether it is the same as the inspected location
            return position[-1]  # returns the hit ship's number


def _get_random_hit(board_size):
    """
    gets a random hit, updates control list

    :param board_size: list[int, int]; size of the board
    :return: list[list[int, int]; random move and
    """
    global hit_list
    move = None  # removes move might not be referenced
    searching = True  # sets a check
    while searching:  # starts a loop to search for an open, random spot
        searching = False  # sets the check to False to end loop if an open sopt is found
        move = [random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1)]  # sets a random spot
        if hit_list[move[0]][move[1]]:  # checks whether field is already targeted
            searching = True  # repeats loop
        else:
            hit_list[move[0]][move[1]] = True  # updates control list
    return move  # returns values


def _get_surrounding_hits(target, board_size):
    """
    gets the surrounding hits of a succesful hit

    checks whether these targets are on the board and available, updates control list

    :param target: Target; succesful hit
    :param board_size: list[int, int]; size of the board
    :return: list[list[list[int, int], ...]; available surrounding targets
    """
    global hit_list
    moves = target.get_surrounding_locations()  # gets the surrounding targets
    adjustment = 0  # used to cope with deleted moves
    for i in range(4):  # goes through all 4 targets
        # they are on the board
        if 0 <= moves[i + adjustment][0] < board_size[0] and 0 <= moves[i + adjustment][1] < board_size[1]:
            if hit_list[moves[i + adjustment][0]][moves[i + adjustment][1]]:  # they are already targeted
                del moves[i + adjustment]  # deletes thet target
                adjustment -= 1  # updates adjustment
            else:
                hit_list[moves[i + adjustment][0]][moves[i + adjustment][1]] = True  # updates control list
        else:
            del moves[i + adjustment]  # deletes thet target
            adjustment -= 1  # updates adjustment
    return moves  # available surrounding moves


def _medium_decision(ship_number, ship_positions, target_list, board_size, recursion):
    """
    decides to target succesful target's surroundings instead of a random one if given the chance

    !potentially recurses itself! this is intended behavior and gets handled accordingly

    used functions update control list

    :param ship_number: int or None; hit ship's number or None if no ship will be hit
    :param ship_positions: list[list[int, int, int, int], list...]; x-coordinate, y-coordinate, is hit?, ship_number
    :param target_list: list[Target, ...]; list with targets
    :param board_size: list[int, int]; size of the board
    :param recursion: bool; whether this is a recursion of itself
    :return: list[int or None, list[Target, ...]; last targets ship number and updated target list
    """
    if ship_number is not None:  # a ship was hit
        next_moves = _get_surrounding_hits(target_list[-1], board_size)  # gets surrounding hits
        ship_number = None  # removes infinte recursion
        for move in next_moves:  # goes through all available surrounding targets
            ship_number = _is_hit(ship_positions, move)  # updates target's ship numebr
            target_list.append(Target(move, ship_number))  # adds that target to the according list
            # recurses itself to check for surrounding targets in case of a successful hit
            ship_number, target_list = _medium_decision(ship_number, ship_positions, target_list, board_size,
                                                        recursion=True)
    elif not recursion:  # this is not a recursion, thus a random target is welcomed if no other optionp presents itself
        next_move = _get_random_hit(board_size)  # gets a random target and updates control list
        ship_number = _is_hit(ship_positions, next_move)  # gets target's ship number
        target_list.append(Target(next_move, ship_number))  # adds a random target to the according list
    return ship_number, target_list  # updated ship number, updated list with targets


def _convert_targets(targets):
    """
    converts a list of Target objects into a list of list[int, int]
    :param targets: list[Target, ...]; list with targets
    :return: list[list[int, int], ...]; list wit lists enemy module can deal with
    """
    play_list = []
    for target in targets:  # goes through every target
        play_list += [target.convert()]  # converts the target
    return play_list


def enemy_medium(ships, board_size):
    """
    creates the enemy's moves fro medium difficulty using Func _medium_decision and Target

    :param ships: list[list[Ship, ...], list]; lsit with all ships on the board
    :param board_size: list[int, int]; size of the board
    :return: list[list[int, int], list, ...]; play_list, global shots in enemy module
    """
    target_list = []  # creates a list that later contains all targets as Target
    _create_hit_list(board_size)  # creates a control list to eliminate doubling targets
    ship_positions = _get_ship_positions(ships)  # gets all postions a ship is on
    first_move = _get_random_hit(board_size)  # makes a random first move
    ship_number = _is_hit(ship_positions, first_move)  # gets that target's ship number
    target_list.append(Target(first_move, ship_number))  # adds the target to the according list

    # creation loop creating list with targets that are later converted to usable moves
    creating = True
    while creating:
        # decides to target succesful target's surroundings instead of a random one if given the chance
        ship_number, target_list = _medium_decision(ship_number, ship_positions,
                                                    target_list, board_size, recursion=False)
        if target_list.__len__() >= board_size[0] * board_size[1]:  # all fields are targeted
            creating = False  # ands creation loop

    play_list = _convert_targets(target_list)  # converts the Target objects to list[int, int]
    return play_list  # returns play_list, global shots in enemy module
