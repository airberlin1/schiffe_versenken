# ------
# neccessary imports
import random as rd  # used to set colors and ships' locations randomly
import pygame  # used to display ships
import save  # used to save ships
import chat  # used to display error messages
import math  # used to round numbers
import copy  # idk why but it has to stay
from playfield import hit_small_field  # used to interact with board
from constants import DIFFICULTIES, SHIPNAMES, RED, DEFAULTPOSITIONS, DIRECTIONS
from translation import get_dict  # used to translate error messages


# ------
# class ship
class Ship:
    """
    Ship with length and color, that can be displayed on the GUI

    Subclasses: Kreuzer5, ContainerShip4, ShipShip3, FisherShip2
    """

    def __init__(self, positions, length, color, identification_number, player, field_size):
        """
        initialises a Ship
        :param positions: list[list[int, int, int], list, ...]; x field coordiante, y field coordiante,
                                                                ship sgement status (3 intact, 1 destroyed)
        :param length: int; number of segments on one ship
        :param color: tuple(int, int, int); color in RGB the ship is displayed in when not destroyed
        :param identification_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; palyer this ship is assigned to, used to determine whether it has to be shown
        :param field_size: float; size of one virtual field
        """
        self.length = length
        self.color = color
        self.identification_number = identification_number
        self.player = player
        self.placed = False
        self.hit = False
        self.positions = positions
        self.name = SHIPNAMES[length]
        self.rects = [pygame.Surface((int(field_size), int(field_size))).get_rect() for _ in range(length)]
        self.direction = DIRECTIONS[0]  # "horizontalright"
        self.hit_tile = 0

    def draw(self, screen, field_size, orientation, small_field_count_x, small_field_count_y, zustand):
        """
        displays the Ship on the GUI

        :param screen: Surface; background the ship is displayed on
        :param field_size: float; size of one virtual field, that is determined by the size of the GUI
        :param orientation: str; width/height, depending on what side of the window is bigger
        :param small_field_count_x: int; number of small fields in one big field in the x direction
        :param small_field_count_y: int; number of small fields in one big field in the y direction
        :param zustand: str; loop the program is currently in
        """
        poslist = self.list_pos()  # lists all positions of the ship to later display them
        for pos in poslist:  # goes through every position of the ship

            if pos[2] == 1:  # checks, whether the ship was hit
                color = RED  # sets the color to red to indicate that segment as destroyed
                draw_ship = True  # ship gets drawn later, without needing to know which player it was assigned to
            else:
                color = self.color  # sets the color to its own color to indiacte the ship being intact
                if self.player == 0:  # checks which player the ship is assigned to, does not show enemy's intact ships
                    draw_ship = True
                else:
                    draw_ship = False

            if draw_ship:  # checks, whether this ship is supposed to be shown
                if self.player == 0 and zustand == "ingame":  # ships belongs to player
                    # checks, how window is currently shown to show the ships on the correct places
                    if orientation == "width":
                        # sets the coordiante for the ship segment
                        x_coord = pos[0] * field_size + 2.5 * field_size + small_field_count_x * field_size
                        y_coord = pos[1] * field_size + 1.5 * field_size
                    else:
                        # sets the coordiante for the ship segment
                        x_coord = pos[0] * field_size + 1.5 * field_size
                        y_coord = pos[1] * field_size + 2.5 * field_size + small_field_count_y * field_size

                else:
                    # sets the coordiante for the ship segment
                    x_coord = pos[0] * field_size + 1.5 * field_size
                    y_coord = pos[1] * field_size + 1.5 * field_size
                pygame.draw.rect(screen, color,  # displays the ship segment on the GUI
                                 (x_coord, y_coord, field_size, field_size), 0)

    def update_rects(self, field_size):
        """
        updates ship's pygame.Rect objects
        :param field_size: float; sizeof one virtual field
        """
        for i in range(self.length):  # goes through length
            # updates Rect's position
            self.rects[i].x = int(self.positions[i][0] * field_size + 3 / 2 * field_size)
            self.rects[i].y = int(self.positions[i][1] * field_size + 3 / 2 * field_size)
            # updates Rect's size
            self.rects[i].inflate(field_size, field_size)

    def is_destroyed(self):
        """
        determines, whether ship is destroyed
        :return: bool; ship is destroyed
        """
        count = 0  # starts count to check number of destroyed pieces
        for position in self.positions:  # goes through every piece
            if position[2] != 3:  # piece has been hit
                count += 1

        if count == self.length:  # ship is destroyed
            return True
        return False

    def list_pos(self):
        """
        returns ship's positions, used to keep older code working
        :return: list[list[int, ...], ...]; list with positions
        """
        return self.positions

    def change_pos(self, poslist):
        """
        updates ship's position, used to keep older code working
        :param poslist: list[list[int, ...], ...]; list with updated positions
        """
        self.positions = poslist

    # ------
    # methods to allow player controlled palycement in the beginning
    def turn_right(self):
        """
        turns the ship by 90 degrees to the right
        """
        i = DIRECTIONS.index(self.direction)  # gets current direction the ship is facing
        # calculates new direction's index
        i -= 1
        if i < 0:
            i = 3
        self.direction = DIRECTIONS[i]  # updates direction
    
    def turn_left(self):
        """
        turns the ship by 90 degrees to the left
        """
        i = DIRECTIONS.index(self.direction)  # gets current direction the ship is facing
        # calculates new direction's index
        i += 1
        if i > 3:
            i = 0
        self.direction = DIRECTIONS[i]  # updates direction

    def move_whole_ship(self):
        """
        moves the parts of the ship, that were not initially moved
        """

        start_pos = self.positions[self.hit_tile]  # gets position of moved tile
        start_ind = self.hit_tile  # gets number of moved tile
        direction = self.direction  # gets direction the ship is currently facing

        if direction == "horizontalright":  # ship is facing right
            addright_change = 1
            adddown_change = 0
            addright = start_ind * -1
            adddown = 0
        elif direction == "verticalup":  # ship is facing up
            addright_change = 0
            adddown_change = -1
            addright = 0
            adddown = start_ind
        elif direction == "horizontalleft":  # ship is facing left
            addright_change = -1
            adddown_change = 0
            addright = start_ind
            adddown = 0
        elif direction == "verticaldown":  # ship is facing down
            addright_change = 0
            adddown_change = 1
            addright = 0
            adddown = start_ind * -1
        else:  # removes variable might not be assigned warning
            addright_change = adddown_change = addright = adddown = None

        new_positions = []  # list used to save updated positions
        for position in self.positions:  # goes through ship's positions
            # recalculates position
            position = [round(start_pos[0] + addright, 2), round(start_pos[1] + adddown, 2), position[2]]
            # updates change values
            addright += addright_change
            adddown += adddown_change
            # saves updated position
            new_positions.append(position)

        self.positions = new_positions  # saves updated positions

    def move(self, field_size):
        """
        reacts to movement of ship by mouse

        :param field_size: float; size of one virtual field
        """
        for i in range(2):  # updates coordinate of hit tile
            self.positions[self.hit_tile][i] = pygame.mouse.get_pos()[i] / field_size - 3 / 2
        self.move_whole_ship()  # moves the other parts

    def set_default_pos(self, field_size, resource_path):
        """
        sets ship's position back to default positions not on the board
        """
        # loads default positions
        self.positions = save.load("lis", "ship", self.identification_number - 1, resource_path, "placement/")
        self.direction = DIRECTIONS[0]  # "horizonatlright", default direction
        self.update_rects(field_size)  # updates ship's pygame.Rect objects

    def set_position(self, field_size, resource_path):
        """
        sets ship to a position when ship is no longer selected
        """
        for position in self.positions:  # goes through ship's positions
            for i in range(2):  # goes through x and y coordinate
                position[i] = round(position[i])  # rounds position
                if not 0 <= position[i] <= 9:  # ship is not on the board
                    self.set_default_pos(field_size, resource_path)  # sets the ship back to its default position
                    return
        self.placed = True  # ship is placed
        self.update_rects(field_size)  # updates ship's pygame.Rect objects


# ------
# ship initialization
def set_ship_count(count):
    """
    sets the number of ships

    used to create ships and their positions as well as checking for win
    """
    global ship_count
    ship_count = count


def __init__shipcheck():
    """
    creates a list that checks where a ship has been placed
     to disallow two ship segemnts being placed on the same field
    """
    global ship_check
    ship_check = []
    for t in range(2):
        ship_check.append([])
        for x in range(10):
            ship_check[t].append([])
            for y in range(10):
                ship_check[t][x].append(0)


def __init__ship(load, get_dif_number):
    """
    initializes ship method

    :param load: bool; whether game is loaded or a new one is created
    :param get_dif_number: Func; returnd number of current difficulty
    """
    set_ship_count(10)  # sets the ship count to ten, because curretly ten ships are created
    global get_dif_ind
    get_dif_ind = get_dif_number
    # creates lists used to update stats
    global hit  # number of times a ship was hit by the player
    global destroyed  # number of times a ship was destroyed by the player
    hit = []
    destroyed = []
    for _ in DIFFICULTIES:  # goes through difficulties
        # adds individual value for each difficulty
        hit.append(0)
        destroyed.append(0)
    if not load:  # game is newly created
        __init__shipcheck()  # inititalizes a list to check where a ship has been placed


# ------
# ship placement
def _get_rand_pos(y, x, length):
    """
    creates a random position for the ship and teh direction the ship is facing

    the first position of the ship is set into the ship instantly, direction is returned

    :param y: int; player the shipis assigned to, used in ship[y]
    :param x: int; ship's number, used in ship[][x]
    :param length: int; number of segments in the ship

    :return: int; direction the ship is facing (1, 2, 3, 4 as North, East, South , West),
                or False, when no viable direction is found
    """
    ship[y][x].positions[0] = [rd.randint(0, 9), rd.randint(0, 9), 3]  # sets a random start position
    # creates a check, that is used to break the loop, when all directions were tried and no viable one was found
    check = 0
    while check < 4:
        # sets a random direction
        direction = rd.randint(1, 4)
        if direction == 1:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].positions[0][1] - length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 2:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].positions[0][0] + length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 3:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].positions[0][1] + length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 4:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].positions[0][0] - length <= 9:
                return direction  # returns the direction
            check += 1
    return False  # returns False when no viable direction was found


def _is_used(i, j):
    """
    checks, whether a certain position is already occupied by a ship segment

    if it is not, all ship segment's positions are marked as occupied

    used when setting the ships to certain or random locations on the play field

    :param i: int; number of the ship which positions ahould be checked
    :param j: int; player the ship was assigned to

    :return: bool; wether one of the ships new positions are already occupied
    """
    positions = ship[j][i].list_pos()  # gets all positions of one ship
    length = ship[j][i].length  # gets the length of that ship

    for h in range(length):  # goes through every position of that ship
        if ship_check[j][positions[h][0]][positions[h][1]]:  # checks whether the ships position is already occupied
            return True  # returns True to show that one of the ship's positions was already occupied

    for h in range(length):  # goes through every position of that ship
        ship_check[j][positions[h][0]][positions[h][1]] = 1  # marks the position as occupied

    return False  # returns False to show that none of the ship's positions was occupied previously


def _set_default_pos(field_size, resource_path):
    """
    sets all player's ships to their default position for player controlled placement
    :param field_size: float; number of one virtual field
    :param resource_path: Func; returns the resource path to a relative path
    """
    for one_ship in ship[0]:  # goes throug player's ships
        one_ship.set_default_pos(field_size, resource_path)  # sets it to its default position


def _set_rand_pos():
    """
    sets every ship to a random postion on the play field

    ships are located in global list ship as Ship

    used once in the beginning of the game
    """
    # goes through every ship
    for player in range(2):
        for one_ship_number in range(ship_count):

            testing = True  # sets testing to True, so that the loop trying to find a spot for that ship continues
            while testing:
                testing = False
                # gets the direction the ship could be facing in and sets the first segment's location
                direction = _get_rand_pos(player, one_ship_number, ship[player][one_ship_number].length)
                x = 0  # sets x to 0 to circumvent var could not be assigned before reference

                if direction:  # checks, whether a direction was found
                    positions = ship[player][one_ship_number].positions  # gets all positions of one ship
                    length = ship[player][one_ship_number].length  # gets the length of that ship

                    for i in range(2):
                        for j in range(length):
                            if direction == 1:  # up
                                # calculates the summand used to adjust the segments location after the first one
                                x = -i * j
                                directionn = 1
                            elif direction == 2:  # right
                                # calculates the summand used to adjust the segments location after the first one
                                x = j - (i * j)
                                directionn = 0
                            elif direction == 3:  # down
                                # calculates the summand used to adjust the segments location after the first one
                                x = i * j
                                directionn = 3
                            elif direction == 4:  # left
                                # calculates the summand used to adjust the segments location after the first one
                                x = -(j - (i * j))
                                directionn = 2
                            if j > 0:
                                # calculates the location based on the previously retrieved summand
                                positions[j][i] = positions[0][i] + x

                    # renews the ship's positions to the just created ones
                    ship[player][one_ship_number].positions = positions
                    ship[player][one_ship_number].direction = DIRECTIONS[directionn]
                    if _is_used(one_ship_number, player):
                        # sets testing to True, so that the loop trying to find a spot for that ship continues
                        testing = True
                else:
                    # sets testing to True, so that the loop trying to find a spot for that ship continues
                    testing = True


def set_ships(load, resource_path, language, add_dir, field_size, random_placement=True):
    """
    creates ships as Ship, in a way that the player's ships are in ship[0] and the enemy's ships are in ship[1]
    and places all ships on random locations on the playfield

    Ship is a ship that can be hit, located on the playfield and shown in the GUI

    used once in the beginning of the game

    :param load: bool; whether game is loaded or a new one is created
    :param resource_path: Func; returns the resource_path to a relative_path
    :param language: str; language all texts are currently displayed in
    :param add_dir: str; additional directory where loaded game is found
    :param field_size: float; size of one virtual field
    :param random_placement: bool; ships are placed randomly and not by the player
    """
    global ship
    if load:  # game is loaded
        try:
            ship = save.load('lis', 'ship', 1, resource_path, add_dir)  # loads ships
        except FileNotFoundError:  # ships file has not been found
            chat.add_missing_message("ship1.lis", resource_path("saves/"), language)  # adds message to chat
            return True  # interrupts loading and creates new game
    else:  # game is newly created
        ship = []  # creates list later holding all ships
        for i in range(2):  # creates individual list for each palyer
            ship.append([])
            for j in range(ship_count):  # goes through number of ships
                ship[i].append(0)
            # creates ten ships for each player that are intact, but are not yet located anywhere on the playfield
            for j in range(4):  # creates four ships as FisherShip2, a Ship with two segments
                ship[i][j] = Ship([[-1, -1, 3], [-1, -1, 3]], identification_number=j + 1, player=i,
                                  color=(255, 50 * j, 255), length=2, field_size=field_size)
            for j in range(3):  # creates three ships as FisherShip2, a Ship with three segments
                d = j + 4
                ship[i][d] = Ship([[-1, -1, 3], [-1, -1, 3], [-1, -1, 3]], identification_number=d + 1, player=i,
                                  color=(50 * j, 100, 255), length=3, field_size=field_size)
            # creates two ships as ContainerShip4, a Ship with four segments
            ship[i][7] = Ship([[-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3]],
                              identification_number=8, player=i, color=(100, 255, 50), length=4, field_size=field_size)
            ship[i][8] = Ship([[-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3]],
                              identification_number=9, player=i, color=(100, 255, 100), length=4, field_size=field_size)
            # creates one ship as Kreuzer5, a ship wih five segments
            ship[i][9] = Ship([[-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3]],
                              identification_number=10, player=i, color=(255, 100, 0), length=5, field_size=field_size)
        if random_placement:
            _set_rand_pos()  # sets all ships to random positions
        else:
            _set_default_pos(field_size, resource_path)


# ------
# ships' interaction with other modules
def check_ship_pos(schiff, feld):
    """
    checks, whether ship is at position x,y
    :param schiff: Ship; checked ship
    :param feld: list[int, int]; checked field (x,y)
    :return: bool, bool, int; ship is at position x,y, ship part is intact, hit ship's part's number
    """
    positions = schiff.positions  # gets ship's positions

    for position in positions:  # goes through every position of that ship
        if position[0] == feld[0] and position[1] == feld[1]:  # ship is at position x,y
            if position[2] > 2:  # part is intact
                return [True, True, positions.index(position)]
            else:  # part has been destroyed
                return [True, False, positions.index(position)]

    return [False, False]


def mark_destroyed(player, i, xcoord, ycoord):
    """
    changes the third value of the hit ship part, thus marking it as destroyed
    :param player: int; player the hit ship belongs to
    :param i: int; hit ship's number
    :param xcoord: int; hit location's x-coordinate
    :param ycoord: int; hit location's y-coordinate
    """
    ship_part_number = check_ship_pos(ship[player][i], (xcoord, ycoord))[2]  # gets the number of the hit ship part
    positions_local = ship[player][i].positions  # gets positions
    positions_local[ship_part_number][2] = 1  # updates positions
    ship[player][i].positions = positions_local  # sets updated positions


def update_stats_values(player, destroyed_l):
    """
    updates values used for statistics

    :param player: int; player whose ship was hit
    :param destroyed_l: bool; ship was destroyed completely
    """
    global hit
    global destroyed
    if player:  # enemy's ship was hit
        hit[get_dif_ind()] += 1  # updates number of successful hits
        if destroyed_l:  # ship was destroyed completely
            destroyed[get_dif_ind()] += 1  # updates number of successful ship eliminations


def _play_hit_sound(resource_path, sound_volume, language):
    """
    plays the sound that indicates a ship part being hit

    :param resource_path: Func; returns the resource path to a relative path
    :param sound_volume: float; 0 - 1, volume of sounds
    :param language: str; language all texts are currently displayed in
    """
    channel3 = pygame.mixer.Channel(2)  # opens a channel
    try:
        sound = pygame.mixer.Sound(resource_path("assets/sounds/hit.wav"))  # creates the sound as a Sound
    except FileNotFoundError:
        chat.add_missing_message("hit.wav", resource_path("assets/sounds/"), language)
    else:
        sound.set_volume(sound_volume)  # sets the volume
        channel3.play(sound)  # plays the sound once


def _get_hit_message(play, success, language, hit_ship="", destroyed_l=False):
    """
    evaluates displayed message based on hit and player

    :param play: int; player, 0 enemy 1 player
    :param success: bool; ship was hit
    :param language: str; language all wiritngs are currently displayed in
    :param hit_ship: Ship, hit ship
    :param destroyed_l: bool; ship was destroyed with that hit
    :return: str, tup(int, int, int)
    """
    dictionary = get_dict(language, "message")  # sets dictionary
    color = (0, 50, 125) if play else (125, 0, 0)  # sets a color based on the player
    play = "Player" if play else "Enemy"  # sets player
    player = dictionary[play]  # translates player
    # sets message
    if destroyed_l:  # a ship was destroyed
        message = "destroyed"
    elif success:  # a ship was hit
        message = "success"
    else:  # no ship was hit
        message = "failure"
    message = dictionary[message]  # translates message
    if success:  # a ship was hit
        # adds the ship and its number
        hit_ship = hit_ship.name + " " + str(hit_ship.identification_number)
    return player + message + hit_ship, color  # returns message and color


def hit_something(xcoord, ycoord, player, resource_path, sound_volume, language, old_xcoord=-1, old_ycoord=-1):
    """
    hits whatever is on player, xcoord, ycoord

    hits a ship by destroying the part and from now on displaying it as red

    hits a field by now displaying "X" on it and marking it as hit

    :param xcoord: int; x coordinate of the field that is hit
    :param ycoord: int; y coordinate of the field that is hit
    :param player: int; player currently playing
    :param resource_path: Func; returns the resource path to a relative path
    :param sound_volume: float; 0 - 1, volume of sounds
    :param language: str; language all wiritings are currently displayed in
    :param old_xcoord: int; x coordinate of the field that was hit previously
    :param old_ycoord: int; y coordinate of the field that was hit previously
    """
    player = 1 - player  # setsthe player to the opposite of the input player
    # marks the small field as hit
    hit_small_field(player, xcoord, ycoord, resource_path, sound_volume, language, old_xcoord, old_ycoord)
    for i in range(ship_count):  # goes through every ship's number
        # checks for every ship whether it is on the field
        if check_ship_pos(ship[player][i], (xcoord, ycoord))[0]:
            mark_destroyed(player, i, xcoord, ycoord)  # marks ship's part as hit
            # plays the sound that indicates a ship part being hit
            _play_hit_sound(resource_path, sound_volume, language)
            destroyed_l = ship[player][i].is_destroyed()
            update_stats_values(player, destroyed_l)  # updates values used for statistics
            message, color = _get_hit_message(player, True, language, ship[player][i], destroyed_l)
            chat.add_message(message, color)  # displays success in chat
            return
    message, color = _get_hit_message(player, False, language)
    chat.add_message(message, color)  # displays miss in chat


# ------
# functions returning values
def check_ship_status():
    """
    checks, whether all ships have been destroyed
    :return: bool, int; there are undestroyed ships left, player that has won the game
    """
    global ship
    for f in range(2):  # goes through both players
        check = 0  # cretes counter to check for game ending
        for y in range(get_ship_count()):  # goes through number of ships
            check += int(ship[f][y].is_destroyed())  # adds 1 if ship is destroyed
        if check == get_ship_count():  # all ships of one player have been destroyed
            return False, 1 - f  # returns player that has won the game
    return True, 2  # returns that no player has won the game


def get_ship():
    """
    returns list with all sips
    :return: list[list[list[Ship, ...], ...], ...]; list with all ships
    """
    return ship


def get_ship_count():
    """
    returns number of ship one player has
    :return: int; number of ships one player has
    """
    return ship_count


def get_ship_positions():
    """
    gets all player's ships' coordinates
    :return: list[list[int, int, int], list, ...]
    """
    ship_coordinates = []
    for x in ship[0]:  # goes through every player's ship
        ship_coordinates += x.list_pos()  # adds its positions
    return ship_coordinates  # returns all positions


def get_hit_des():
    """
    returns stats handled in ship module
    :return: list[list[int, int, ...], list]; all values used for statistics
    """
    global hit
    global destroyed

    try:
        hit_des = [hit, destroyed]  # gets values used for statistics that are counted in ships module

    except NameError:  # variables have not yet been initialized
        # instead fills all values with 0
        hit_des = [[], []]
        for i in range(2):
            for _ in DIFFICULTIES:
                hit_des[i].append(0)

    # resets values
    hit = []
    destroyed = []
    for _ in DIFFICULTIES:
        hit.append(0)
        destroyed.append(0)

    return hit_des  # returns values


# ------
# saves ships
def save_ship(resource_path, language, add_dir):
    """
    saves the ship so that they can be loaded to continue the game

    :param resource_path: Func; returns the resource path to a relative path
    :param language: str; language all texts are currently displayed in
    :param add_dir: str; additional directory where loaded game is found
    """
    try:
        save.save(ship, 'lis', 'ship', 1, resource_path, add_dir)  # saves all ships to saves folder
    except FileNotFoundError:  # directory could not be found
        chat.add_missing_message("hit.wav", resource_path("saves"), language, False)  # displays error message
