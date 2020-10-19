from random import randint

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
        self.success = True if ship_number else False

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


def _create_hit_list(board_size, reset_hit_list):
    """
    creates a control list used to monitor doubling targets and eliminating them

    :param board_size: list[int, int]; size of the game board
    :param reset_hit_list: Func; creates new hit list
    """
    global hit_list
    hit_list = reset_hit_list(board_size)


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
        move = [randint(0, board_size[0] - 1), randint(0, board_size[1] - 1)]  # sets a random spot
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
    for i in range(4):  # goes through all 4 targets
        # they are on the board
        if not 0 <= moves[i][0] < board_size[0] or not 0 <= moves[i][1] < board_size[1]:
            moves[i] = "no"  # deletes thet target
    return moves  # available surrounding moves


def _medium_decision(ship_number, ship_positions, target_list, board_size, recursion, directions, ships, last_ship,
                     targeted, finished):
    """
    decides to target succesful target's surroundings instead of a random one if given the chance

    !potentially recurses itself! this is intended behavior and gets handled accordingly

    :param ship_number: int or None; hit ship's number or None if no ship will be hit
    :param ship_positions: list[list[int, int, int, int], list...]; x-coordinate, y-coordinate, is hit?, ship_number
    :param target_list: list[Target, ...]; list with targets
    :param board_size: list[int, int]; size of the board
    :param recursion: bool; whether this is a recursion of itself
    :param directions: list[str, str, ...]; only used in hard decision
    :param ships: list[list[Ship, Ship, ...], list]; only used in hard decision
    :param last_ship: list[int, ...]; only used in hard decision
    :param targeted: None; only used in hard decision
    :param finsished: None, only used in hard decision
    :return: int, list[Target, ...], list[str, ...], list[int, ...], None, None; updated lists/values
    """
    ship_pos = ship_positions  # used to make line shorter than 120 characters
    if ship_number is not None:  # a ship was hit
        next_moves = _get_surrounding_hits(target_list[-1], board_size)  # gets surrounding hits
        ship_number = None  # removes infinte recursion
        for move in next_moves:  # goes through all available surrounding targets
            if move != "no":
                if not hit_list[move[0]][move[1]]:
                    hit_list[move[0]][move[1]] = True
                    ship_number = _is_hit(ship_positions, move)  # updates target's ship number
                    target_list.append(Target(move, ship_number))  # adds that target to the according list
                    # recurses itself to check for surrounding targets in case of a successful hit
                    ship_number, target_list, directions, last_ship, targeted, finished = _medium_decision(ship_number,
                                                                                                           ship_pos,
                                                                                                           target_list,
                                                                                                           board_size,
                                                                                                           recursion=
                                                                                                           True,
                                                                                                           directions=
                                                                                                           directions,
                                                                                                           ships=ships,
                                                                                                           last_ship=
                                                                                                           last_ship,
                                                                                                           targeted=
                                                                                                           None,
                                                                                                           finished=None
                                                                                                           )
    elif not recursion:  # this is not a recursion, thus a random target is welcomed if no other optionp presents itself
        next_move = _get_random_hit(board_size)  # gets a random target and updates control list
        ship_number = _is_hit(ship_positions, next_move)  # gets target's ship number
        target_list.append(Target(next_move, ship_number))  # adds a random target to the according list
    return ship_number, target_list, directions, last_ship, targeted, finished  # updated lists


def update_dir(dire, ship_num, ship):
    """
    updates list of known directions, used in hard enemy
    :param dire: list[str, str, ...]; list with known directions
    :param ship_num: int; number of targeted ship
    :param ship: list[list[Ship, Ship, ...], list]; list containing all ships
    :return: list[str, str, ...]; updated list with known directions
    """
    ind = ship_num - 1
    if dire[ind] is None:  # this ship has not been hit before
        dire[ind] = "here"
    elif dire[ind] == "here":  # this ship has been hit once, so that the direction can now be determined
        # this is not te way a user would get information about the ship's diredtion
        dire[ind] = "up" if ship[0][ind].direction == "verticalup" or ship[0][ind].direction == "verticaldown" \
            else "right"
    return dire


def _hard_decision(ship_number, ship_positions, target_list, board_size, targeted, finished, recursion, directions,
                   ships, last_ship):
    """
    decides to target succesful target's surroundings instead of a random one if given the chance,
    also tries to find ships direction and use it to find solution faster
     and doesn't try to destroy already destroyed ships

    !potentially recurses itself! this is intended behavior and gets handled accordingly

    :param ship_number: int or None; hit ship's number or None if no ship will be hit
    :param ship_positions: list[list[int, int, int, int], list...]; x-coordinate, y-coordinate, is hit?, ship_number
    :param target_list: list[Target, ...]; list with targets
    :param board_size: list[int, int]; size of the board
    :param targeted: list[int, ...]; number of times the ships have been targeted
    :param finished: list[bool, ...]; the ships have been targeted enough to be destroyed
    :param recursion: bool; whether this is a recursion of itself
    :param directions: list[str, str, ...]; list with known directions of ships
    :param ships: list[list[Ship, Ship, ...], list]; list containing all ships
    :param last_ship: list[int, ...]; ships that have been targeted, but have not been destroyed yet
    :return: int, list[Target, ...], list[str, ...], list[int, ...], list[int, ...], list[bool, ...]; updated lists
    """
    if ship_number is not None and last_ship:  # a ship was hit
        next_moves = _get_surrounding_hits(target_list[-1], board_size)  # gets surrounding hits
        count = 0  # count used to disallow infinite recursion when a ship was hit,
        #   might be redundant after finished list is implemented
        last_shi = last_ship[-1]
        for i, move in enumerate(next_moves):  # goes through all available surrounding targets
            if move != "no":  # hit is allowed
                if (directions[last_shi - 1] is None or directions[last_shi - 1] == "up" and i > 1
                    or directions[last_shi - 1] == "right" and i < 2
                    or directions[last_shi - 1] == "here") and not hit_list[move[0]][move[1]] \
                        and not finished[last_shi - 1]:  # hit helps to take down ship
                    hit_list[move[0]][move[1]] = True
                    ship_number = _is_hit(ship_positions, move)  # updates target's ship number
                    if ship_number is not None:  # a ship was hit
                        directions = update_dir(directions, ship_number, ships)  # updates known directions
                        if ship_number not in last_ship:  # ship has not been targeted before
                            last_ship.append(ship_number)
                        targeted[ship_number - 1] += 1  # ship was hit another time
                        if targeted[ship_number - 1] == ships[0][ship_number - 1].length:  # ship is destroyed
                            finished[ship_number - 1] = True
                            del last_ship[last_ship.index(ship_number)]  # this may cause one redundant shot

                    target_list.append(Target(move, ship_number))  # adds that target to the according list
                    # recurses itself to check for surrounding targets in case of a successful hit
                    ship_number, target_list, directions, last_ship, targeted, finished = _hard_decision(ship_number,
                                                                                                         ship_positions,
                                                                                                         target_list,
                                                                                                         board_size,
                                                                                                         targeted,
                                                                                                         finished,
                                                                                                         recursion=True,
                                                                                                         directions=
                                                                                                         directions,
                                                                                                         ships=ships,
                                                                                                         last_ship=
                                                                                                         last_ship)
                else:
                    count += 1
            else:
                count += 1
        if count == 4:  # disallows infinte recursion
            ship_number = None

    elif not recursion:  # this is not a recursion, thus a random target is welcomed if no other option presents itself
        next_move = _get_random_hit(board_size)  # gets a random target and updates control list
        ship_number = _is_hit(ship_positions, next_move)  # gets target's ship number
        if ship_number is not None:  # ship is hit
            if ship_number not in last_ship:  # ship has not been hit before
                last_ship.append(ship_number)
            targeted[ship_number - 1] += 1
            if targeted[ship_number - 1] == ships[0][ship_number - 1].length:  # will never happen
                finished[ship_number - 1] = True
                del last_ship[last_ship.index(ship_number)]
            directions = update_dir(directions, ship_number, ships)  # updates known directions
        target_list.append(Target(next_move, ship_number))  # adds a random target to the according list

    return ship_number, target_list, directions, last_ship, targeted, finished


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


def enemy_mediumhard(ships, board_size, reset_hit_list, difficulty):
    """
    creates the enemy's moves for medium and hard difficulty

    :param ships: list[list[Ship, ...], list]; list with all ships on the board
    :param board_size: list[int, int]; size of the board
    :param reset_hit_list: Func; creates new hit list
    :param difficulty: Str; difficulty the game is played on
    :return: list[list[int, int], list, ...]; play_list, global shots in enemy module
    """
    decision = _medium_decision if difficulty == "medium" else _hard_decision
    target_list = []  # creates a list that later contains all targets as Target
    _create_hit_list(board_size, reset_hit_list)  # creates a control list to eliminate doubling targets
    ship_positions = _get_ship_positions(ships)  # gets all postions a ship is on
    # additional lists used for hard enemy
    last_ship = []
    targeted = [0 for _ in ships[0]]  # list to stop targeting a ship after all
    finished = [False for _ in ships[0]]  # list with destroyed ships
    directions = [None for _ in ships[0]]  # list with known directions of ships
    first_move = _get_random_hit(board_size)  # makes a random first move
    ship_number = _is_hit(ship_positions, first_move)  # gets that target's ship number
    target_list.append(Target(first_move, ship_number))  # adds the target to the according list
    if ship_number is not None:
        directions[ship_number - 1] = "here"
        last_ship.append(ship_number)
        targeted[ship_number - 1] += 1
    number_of_ship_tiles = ship_positions.__len__()
    # creation loop creating list with targets that are later converted to usable moves
    creating = True
    while creating:
        # decides to target succesful target's surroundings instead of a random one if given the chance
        ship_number, target_list, direction, last_ship, targeted, finished = decision(ship_number, ship_positions,
                                                                                      target_list, board_size,
                                                                                      recursion=False,
                                                                                      directions=directions,
                                                                                      ships=ships,
                                                                                      last_ship=last_ship,
                                                                                      targeted=targeted,
                                                                                      finished=finished)
        # ends shot creation when every ship's tiles are targeted
        count = 0
        for target in target_list:  # counts targeted ship tiles
            if target.success:
                count += 1
        if count >= number_of_ship_tiles:  # compares targeted ship tiles to number of ship_tiles
            creating = False

    play_list = _convert_targets(target_list)  # converts the Target objects to list[int, int]
    return play_list  # returns play_list, global shots in enemy module
