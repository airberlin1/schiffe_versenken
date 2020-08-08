# import fixed
import random as rd
import pygame
import save
import chat
from playfield import hit_small_field
from translation import get_dict
# TODO Modul sortieren
RED = (255, 0, 0)


class Ship:
    """
    Ship with length and color, that can be displayed on the GUI

    Subclasses: Kreuzer5, ContainerShip4, ShipShip3, FisherShip2
    """

    def __init__(self, length, status, color, identification_number, player):
        """
        initialises a Ship

        :param length: int; number of segments on one ship
        :param status: str; not currently used
        :param color: tuple(int, int, int); color in RGB the ship is displayed in when not destroyed
        :param identification_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; palyer this ship is assigned to, used to determine whether it has to be shown
        """
        self.length = length
        self.status = status
        self.color = color
        self.identification_number = identification_number
        self.player = player

    def draw(self, screen, field_size, orientation, small_field_count_x, small_field_count_y):
        """
        displays the Ship on the GUI

        :param screen: Surface; background the ship is displayed on
        :param field_size: float; size of one virtual field, that is determined by the size of the GUI
        :param orientation: str; width/height, depending on what side of the window is bigger
        :param small_field_count_x: int; number of small fields in one big field in the x direction
        :param small_field_count_y: int; number of small fields in one big field in the y direction
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
                if self.player == 0:  # checks which player the field is assigned to and thus, where to show the ship
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

    def is_destroyed(self):
        count = 0
        for position in self.list_pos():
            if position[2] != 3:
                count += 1
        if count == self.list_pos().__len__():
            return True


class Kreuzer5(Ship):
    """
    Ship with 5 segments that can change its positions and list them

    Superclass Ship can display itself on the GUI
    """

    def __init__(self, pos1, pos2, pos3, pos4, pos5, identification_number, player):
        """
        initializes the Kreuzer5

        :param pos1: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos2: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos3: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos4: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos5: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param identifaction_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; player this ship is assigned to, used to determine whether it has to be shown
        """
        Ship.__init__(self, 5, "safe", (0, 255, 0), identification_number, player)  # initializes the super class
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.pos4 = pos4
        self.pos5 = pos5
        self.name = "CruiseShip"

    def list_pos(self):
        """
        lists the ships positions

        used to check every postion for displaying it or checking for hit ship segments

        :return: list[list[int, int, int], list, ...]; list with every postion of the ship
        """
        return [self.pos1, self.pos2, self.pos3, self.pos4, self.pos5]

    def change_pos(self, poslist):
        """
        renews the ships positions

        used to renew ship positions when hit or moved

        :param poslist: list[list[int, int, int], list, ...]; list with every postion of the ship
        """
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]
        self.pos4 = poslist[3]
        self.pos5 = poslist[4]


class ContainerShip4(Ship):
    """
    Ship with 4 segments that can change its positions and list them

    Superclass Ship can display itself on the GUI
    """

    def __init__(self, pos1, pos2, pos3, pos4, identification_number, player):
        """
        initializes the ContainerShip4

        :param pos1: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos2: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos3: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos4: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param identifaction_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; player this ship is assigned to, used to determine whether it has to be shown
        """
        Ship.__init__(self, 4, "safe", (255, rd.randint(150, 255), 0), identification_number,
                      player)  # initializes the super class
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.pos4 = pos4
        self.name = "ContainerShip"

    def list_pos(self):
        """
        lists the ships positions

        used to check every postion for displaying it or checking for hit ship segments

        :return: list[list[int, int, int], list, ...]; list with every postion of the ship
        """
        return [self.pos1, self.pos2, self.pos3, self.pos4]

    def change_pos(self, poslist):
        """
        renews the ships positions

        used to renew ship positions when hit or moved

        :param poslist: list[list[int, int, int], list, ...]; list with every postion of the ship
        """
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]
        self.pos4 = poslist[3]


class ShipShip3(Ship):
    """
    Ship with 3 segments that can change its positions and list them

    Superclass Ship can display itself on the GUI
    """

    def __init__(self, pos1, pos2, pos3, identification_number, player):
        """
        initializes the ShipShip3

        :param pos1: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos2: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos3: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param identifaction_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; player this ship is assigned to, used to determine whether it has to be shown
        """
        Ship.__init__(self, 3, "safe", (rd.randint(150, 255), 125, 0), identification_number,
                      player)  # initializes the super class
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.name = "ShipShip"

    def list_pos(self):
        """
        lists the ships positions

        used to check every postion for displaying it or checking for hit ship segments

        :return: list[list[int, int, int], list, list]; list with every postion of the ship
        """
        return [self.pos1, self.pos2, self.pos3]

    def change_pos(self, poslist):
        """
        renews the ships positions

        used to renew ship positions when hit or moved

        :param poslist: list[list[int, int, int], list, list]; list with every postion of the ship
        """
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]


class FisherShip2(Ship):
    """
    Ship with 2 segments that can change its positions and list them

    Superclass Ship can display itself on the GUI
    """

    def __init__(self, pos1, pos2, identification_number, player):
        """
        initializes the FisherShip2

        :param pos1: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param pos2: list[int, int, int]; x field coordiante, y field coordiante,
                                        ship sgement status (0 intact, 1 destroyed)
        :param identifaction_number: int; number the ship can be identificated with, used in more difficult settings
        :param player: int; player this ship is assigned to, used to determine whether it has to be shown
        """
        Ship.__init__(self, 2, "safe", (128, rd.randint(0, 128), 128), identification_number,
                      player)  # initializes the super class
        self.pos1 = pos1
        self.pos2 = pos2
        self.name = "FisherShip"

    def list_pos(self):
        """
        lists the ships positions

        used to check every postion for displaying it or checking for hit ship segments

        :return: list[list[int, int, int], list[int, int, int]]; list with every postion of the ship
        """
        return [self.pos1, self.pos2]

    def change_pos(self, poslist):
        """
        renews the ships positions

        used to renew ship positions when hit or moved

        :param poslist: list[list[int, int, int], list[int, int, int]]; list with every postion of the ship
        """
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]


def set_ship_count(count):
    """
    sets the number of ships

    used to create ships and their positions as well as checking for win
    """
    global ship_count
    ship_count = count


def __init__shipcheck():
    """
    creates a list that checks, where a ship has been placed,
     to disallow to ship segemnts being placed on the same field
    """
    global ship_check
    ship_check = []
    for t in range(2):
        ship_check.append([])
        for x in range(10):
            ship_check[t].append([])
            for y in range(10):
                ship_check[t][x].append(0)


def __init__ship(load):
    """
    initializes ship method

    :param load: bool; whether game is loaded or a new one is created
    """
    set_ship_count(10)  # sets the ship count to ten, because curretly ten ships are created
    if not load:
        __init__shipcheck()  # inititalizes a list to check where a ship has been placed


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
    ship[y][x].pos1 = [rd.randint(0, 9), rd.randint(0, 9), 3]  # sets a random start position
    # creates a check, that is used to break the loop, when all directions were tried and no viable one was found
    check = 0
    while check < 4:
        # sets a random direction
        direction = rd.randint(1, 4)
        if direction == 1:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].pos1[1] - length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 2:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].pos1[0] + length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 3:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].pos1[1] + length <= 9:
                return direction  # returns the direction
            check += 1
        elif direction == 4:
            # checks whether the ship would be completly on the play field
            if 0 <= ship[y][x].pos1[0] - length <= 9:
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
                    positions = ship[player][one_ship_number].list_pos()  # gets all positions of one ship
                    length = ship[player][one_ship_number].length  # gets the length of that ship

                    for i in range(2):
                        for j in range(length):
                            if direction == 1:
                                # calculates the summand used to adjust the segments location after the first one
                                x = -i * j
                            elif direction == 2:
                                # calculates the summand used to adjust the segments location after the first one
                                x = j - (i * j)
                            elif direction == 3:
                                # calculates the summand used to adjust the segments location after the first one
                                x = i * j
                            elif direction == 4:
                                # calculates the summand used to adjust the segments location after the first one
                                x = -(j - (i * j))
                            if j > 0:
                                # calculates the location based on the previously retrieved summand
                                positions[j][i] = positions[0][i] + x

                    # renews the ship's positions to the just created ones
                    ship[player][one_ship_number].change_pos(positions)
                    if _is_used(one_ship_number, player):
                        # sets testing to True, so that the loop trying to find a spot for that ship continues
                        testing = True
                else:
                    # sets testing to True, so that the loop trying to find a spot for that ship continues
                    testing = True


def set_ships(load, resource_path, language):
    """
    creates ships as Ship, in a way that the player's ships are in ship[0] and the enemy's ships are in ship[1]
    and places all ships on random locations on the playfield

    Ship is a ship that can be hit, located on the playfield and shown in the GUI

    used once in the beginning of the game

    :param load: bool; whether game is loaded or a new one is created
    :param resource_path: Func; returns the resource_path to a relative_path
    :param language: str; language all texts are currently displayed in
    """
    global ship
    if load:
        try:
            ship = save.load('lis', 'ship', 1, resource_path)
        except FileNotFoundError:
            chat.add_missing_message("ship1.lis", resource_path("saves/"), language)
            return True
    else:
        ship = []
        for i in range(2):
            # creates two lists, which later contain the ships
            ship.append([])
            for j in range(ship_count):
                ship[i].append(0)
            # creates ten ships for each player that are intact, but are not yet located anywhere on the playfield
            for j in range(4):  # creates four ships as FisherShip2, a Ship with two segments
                ship[i][j] = FisherShip2([-1, -1, 3], [-1, -1, 3], identification_number=j + 1, player=i)
            for j in range(3):  # creates three ships as FisherShip2, a Ship with three segments
                d = j + 4
                ship[i][d] = ShipShip3([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], identification_number=d + 1, player=i)
            # creates two ships as ContainerShip4, a Ship with four segments
            ship[i][7] = ContainerShip4([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                                        identification_number=8, player=i)
            ship[i][8] = ContainerShip4([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                                        identification_number=9, player=i)
            # creates one ship as Kreuzer5, a ship wih five segments
            ship[i][9] = Kreuzer5([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                                  identification_number=10, player=i)
        # TODO allow players to select positions
        _set_rand_pos()  # sets all ships to random positions


def check_ship_status():
    """
    ueberprueft, ob ein Schiff zerstoert ist, und ob alle Schiffe eines Spielers zerstoert sind
    """
    global ship
    for f in range(2):
        check = 0
        for y in range(get_ship_count()):
            # Schiffsteile auf Zustand ueberpruefen, wenn alle zerstoert, Schiff ist zerstoert
            if check_destroyed(y, f):
                check += 1
        # wenn alle Schiffe eines Spielers zerstoert sind, endet das Spiel
        if check == get_ship_count():
            return False, 1 - f
    return True, 2


def check_ship_pos(schiff, feld):
    """
    ueberprueftt, op Schiff schiff am Ort x,y ist
    :param schiff: aktuelles Schiff
    :param feld: Feld, das ueberprueft wird
    :return: 2 bools, wobei der Erste True ist, wenn sich dort ein Schiff befindet, und der Zweite, wenn das Schiffsteil
             an der Stelle nicht zerstoert ist und das Schiffsteil des Schiffes, wenn eines getroffen wurde
    """
    positions = schiff.list_pos()
    length = schiff.length
    # ueberpruefen, ob eine der Positionen des Schiffes an dieser Stelle ist
    for t in range(length):
        if positions[t][0] == feld[0] and positions[t][1] == feld[1]:
            # ueberpruefen, ob das Schiffsteil zerstoert ist

            if positions[t][2] > 2:
                return [True, True, t]
            else:
                return [True, False, t]
    return [False, False]


def is_ship_placed(angeklicktesfeld, schiff):
    ship_placed = False
    for f in range(10):
        if check_ship_pos(schiff()[1][f], angeklicktesfeld)[0]:
            ship_placed = True
    return ship_placed


def get_ship():
    # gibt die Liste mit den Schiffen zurueck
    return ship


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


def _get_hit_message(play, success, language, hit_ship="", destroyed=False):
    """
    evaluates displayed message based on hit and player

    :param play: int; player, 0 enemy 1 player
    :param success: bool; ship was hit
    :param language: str; language all wiritngs are currently displayed in
    :param hit_ship: Ship, hit ship
    :param destroyed: bool; ship was destroyed with that hit
    :return: str, tup(int, int, int)
    """
    dictionary = get_dict(language, "message")  # sets dictionary
    color = (0, 50, 125) if play else (125, 0, 0)  # sets a color based on the player
    play = "Player" if play else "Enemy"  # sets player
    player = dictionary[play]  # translates player
    # sets message
    if destroyed:  # a ship was destroyed
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
    for i in range(ship_count):
        # checks for every ship whether it is on the field
        if check_ship_pos(ship[player][i], (xcoord, ycoord))[0]:

            # hits the small field
            hit_small_field(player, xcoord, ycoord, resource_path, sound_volume, language, old_xcoord, old_ycoord)
            # gets the number of the hit ship part
            ship_part_number = check_ship_pos(ship[player][i], (xcoord, ycoord))[2]
            # changes the fird value of the hit ship part, thus marking it as destroyed
            positions_local = ship[player][i].list_pos()
            positions_local[ship_part_number][2] = 1
            ship[player][i].change_pos(positions_local)
            # plays the sound that indicates a ship part being hit
            _play_hit_sound(resource_path, sound_volume, language)
            destroyed = check_destroyed(i, player)
            message, color = _get_hit_message(player, True, language, ship[player][i], destroyed)
            chat.add_message(message, color)
            return
    # hits the small field regardless
    hit_small_field(player, xcoord, ycoord, resource_path, sound_volume, language, old_xcoord, old_ycoord)
    message, color = _get_hit_message(player, False, language)
    chat.add_message(message, color)


def check_destroyed(ship_number, player):
    """ueberprueft, ob das ausgewaehlte Schiff zerstoert ist"""
    length = ship[player][ship_number].length
    ship_pos = ship[player][ship_number].list_pos()
    hi = 0
    # geht jedes Schiffsteil durch und ueberprueft, ob es zerstoert ist
    for x in range(length):
        if ship_pos[x][2] < 2:
            hi += 1
    # wenn jedes Schiffsteil zerstoert ist, wird True zurueckgegeben und außerdem der Status des Schiffes aktualisiert
    if hi == length:
        ship[player][ship_number].status = "destroyed"
        return True
    return False


def check_hit(player, field):
    """ueberprueft fuer alle Schiffe, ob es getroffen wurde und gibt ggf. die Nummer des getroffenen Schiffes zurueck"""
    for i in range(get_ship_count()):
        if check_ship_pos(ship[player][i], field)[0]:
            return [True, i]
    return [False]  # brackets required


def get_ship_count():
    # gibt die Anzahl der Schiffe zurueck
    return ship_count


def get_ship_positions():
    ship_coordinates = []
    for x in ship[0]:
        ship_coordinates += x.list_pos()
    return ship_coordinates


def save_ship(resource_path, language):
    """
    saves the ship so that they can be loaded to continue the game

    :param resource_path: Func; returns the resource path to a relative path
    :param language: str; language all texts are currently displayed in
    """
    try:
        save.save(ship, 'lis', 'ship', 1, resource_path)
    except FileNotFoundError:
        chat.add_missing_message("hit.wav", resource_path("saves"), language, False)
