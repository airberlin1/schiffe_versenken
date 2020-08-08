# module with the playfield, it's output on the GUI and it's coordinates

# ------
# imports pygame, that is used to build a GUI, and the writing for it being able to displayed on the GUI,
# as well as save used to save and load game and chat used to display errors
import pygame
import writing
import save
import chat

# ------
# sets tuples with used colors and the alphabet in alphabetic order to be displayed on top of the playfield
RED = (255, 0, 0)
GREY = (170, 170, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


# ------
# classes "BigField", "SmallField" and "PlayfieldWriting"
class BigField:
    """
    boards, 10x10 by default
    """

    def __init__(self, size_x, size_y, location_top_left, field_count_x=10, field_count_y=10):
        """
        :param size_x: int; horizontal size
        :param size_y: int; vertical size
        :param location_top_left: list[int, int]; top left corner coordinate
        :param field_count_x: int; number of tiles in horizontal direction
        :param field_count_y: int; number of tiles in vertical direction
        """
        self.size_x = size_x
        self.size_y = size_y
        self.field_count_x = field_count_x
        self.field_count_y = field_count_y
        self.location_top_left = location_top_left

    def change_loc_coords(self, field_size, orienation, own_field):
        """
        aendert die Koordinaten des Spielfeldes
        :param field_size: float; size of a virtual field, depending on size of the playfield and the size of the window
        :param orienation: str; width or height depending on the size and appearance of the window
        :param own_field: bool; player's board
        """
        # updates board's size
        self.size_y = self.field_count_y * field_size
        self.size_x = self.field_count_x * field_size
        if not own_field:  # board belongs to enemy
            self.location_top_left = [field_size * 3 / 2, field_size * 3 / 2]  # updates top left coordiante
        else:  # board belogs to player
            if orienation == "height":  # game window is bigger in veritcal direction
                self.location_top_left = [field_size * 3 / 2, field_size * 25 / 2]  # updates top left coordiante
            else:  # game window is bigger in horizontal direction
                self.location_top_left = [field_size * 25 / 2, field_size * 3 / 2]  # updates top left coordiante

    def draw(self, screen):
        """
        displays board with black and white outline

        :param screen: Surface; surface covering the whole game window
        """
        pygame.draw.rect(screen, BLACK,  # dispalys thick black outline
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 5)
        pygame.draw.rect(screen, WHITE,  # displays thinner white outline
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 3)


class SmallField:
    """
    tiles on boards

    displayed with clicked/hit attributes
    """

    def __init__(self, big_field, ship_on, hit_on, clicked_on, location_coord_x, location_field_x, location_field_y,
                 location_coord_y, ship_number=-1):
        """
        :param big_field: int; tile is on 0: enemy's board
                                          1: player's board
        :param ship_on: bool; there is a shi on this tile, not used curretnly
        :param hit_on: bool; tile was already targeted, should always be False
        :param clicked_on: bool; tile is clicked, should always be false
        :param location_coord_x: int; x coordinate
        :param location_field_x: int; x field coordinate
        :param location_field_y: int; y field coordinate
        :param location_coord_y: int; y cordinate
        :param ship_number: ship's number if ship is on tile, not used currently
        """
        self.big_field = big_field
        self.ship_on = ship_on
        self.hit_on = hit_on
        self.clicked_on = clicked_on
        self.location_field_x = location_field_x
        self.location_field_y = location_field_y
        self.location_coord_x = location_coord_x
        self.location_coord_y = location_coord_y
        self.ship_number = ship_number

    def change_loc_coords(self, field_size, orientation):
        """
        updates tile's coordinates

        :param field_size: float; size of a virtual field, depending on size of the playfield and the size of the window
        :param orientation: str; width or height depending on the size and appearance of the window
        """
        if self.big_field == 0:  # tile is on enemy's board
            # updates coordinates
            self.location_coord_x = 3 / 2 * field_size + self.location_field_x * field_size
            self.location_coord_y = 3 / 2 * field_size + self.location_field_y * field_size

        else:  # tile is on player's board
            if orientation == "height":  # game window is bigger in vertical direction
                if self.location_field_x > 9:  # orientation has changed since last use of method
                    # updates field coordinate
                    self.location_field_x -= 10
                    self.location_field_y += 10
                loc_field_x = self.location_field_x  # horizontal field
                loc_field_y = self.location_field_y + 1  # vertical field + 1, needed because of design flaw
            else:  # game window is bigger in horizontal direction
                if self.location_field_y > 9:  # orientation has changed since last use of method
                    # updates field coordiante
                    self.location_field_x += 10
                    self.location_field_y -= 10
                loc_field_x = self.location_field_x + 1  # horizontal field + 1, needed because of design flaw
                loc_field_y = self.location_field_y  # vertical field

            # updates tile's coordinate
            self.location_coord_x = 3 / 2 * field_size + loc_field_x * field_size
            self.location_coord_y = 3 / 2 * field_size + loc_field_y * field_size

    def draw(self, screen, field_size):
        """
        displays tile with black and white outline and marke as clicked/hit if neccessary

        :param screen: Surface; surfacce covering the whole game window
        :param field_size: float; size of a virtual field, depending on size of the playfield and the size of the window
        """
        # displays thick black outline
        pygame.draw.rect(screen, BLACK, (self.location_coord_x, self.location_coord_y, field_size, field_size), 3)
        pygame.draw.rect(screen, WHITE,  # dispalys thinner white outline so that board is seen on all backgrounds
                         (self.location_coord_x, self.location_coord_y, field_size, field_size), 1)

        if self.clicked_on:  # tile is marked and thus waiting for confiramtion
            pygame.draw.rect(screen, BLACK,  # dispalays tile black
                             (self.location_coord_x, self.location_coord_y, field_size, field_size), 0)

        if self.hit_on:  # tile was hit
            color = GREY
            # dispalys grey cross on top of tile
            pygame.draw.line(screen, color, (self.location_coord_x + field_size,
                                             self.location_coord_y),
                             (self.location_coord_x, self.location_coord_y + field_size), 5)
            pygame.draw.line(screen, color, (self.location_coord_x, self.location_coord_y),
                             (self.location_coord_x + field_size, self.location_coord_y + field_size), 5)

    def become_hit_player(self, resource_path, sound_volume, language):
        """
        hits tile
        :param resource_path: Func; returns the resource path to a relative path
        :param sound_volume: float; volume of sounds
        """
        if self.hit_on:  # tile was hit previously
            self.clicked_on = False  # unclicks field, should not be required in any case

        elif self.clicked_on:  # tile is curretly marked and waiting for confirmation
            self.clicked_on = False  # unclicks field, thus erasing black mark
            self.hit_on = True  # hits field, thus displaying it with grey cross from now on
            # plays sound of something hitting the water
            try:
                new_channel = pygame.mixer.Channel(0)  # sets a channel
                sound = pygame.mixer.Sound(resource_path("assets/sounds/nothit.wav"))  # gets sound
            except FileNotFoundError:
                chat.add_missing_message("nothit.wav", resource_path("assets/sounds/"), language)
            else:
                sound.set_volume(sound_volume)
                new_channel.play(sound)

        else:  # tile has been newly clicked
            self.clicked_on = True  # clicks the field to mark it black and allow confirmation

    def become_hit_enemy(self):
        """
        hits tile
        """
        self.hit_on = True  # hits field, thus displaying it with a greey cross from now on
        self.clicked_on = True  # clicks field to mark it as the last hit field by the enemy


class PlayfieldWriting(writing.Writing):
    """
    writing on boards' sides

    allows player to distinguish between tiles more easily and enables communication about certain tiles
    """

    def __init__(self, content, font, color, top_left_corner, field_coord_top_left, own_field, orientation=None):
        """
        initializes the writing
        :param content: str; displayed text
        :param font: SysFont; font of the writing
        :param color: tuple(int, int, int); color in RGB
        :param top_left_corner: list[int, int]; writing's top left corner
        :param field_coord_top_left: list[int, int]; writing's top left corner as a field coordinate
        :param own_field: bool; own field or not
        :param orientation: str; width or height depending on the size and appearance of the window
        """
        super().__init__(content, font, color, top_left_corner)  # initializes the writing
        self.field_coord_top_left = field_coord_top_left
        self.own_field = own_field
        self.orientation = orientation

    def refresh_loc_coords(self, field_size, orientation):
        """
        refreshes the writing's location and font
        :param field_size: float; size of a virtual field, depending on size of the playfield and the size of the window
        :param orientation: str; width or height depending on the size and appearance of the window
        """
        if self.own_field:  # checks on who's board the writing is
            if orientation != self.orientation:  # checks, if the orientation changed
                self.orientation = orientation  # refreshes the writing's orientation

                if orientation == "width":  # game window is bigger in horizontal direction
                    # updates field coordinates
                    self.field_coord_top_left[0] += 11
                    self.field_coord_top_left[1] -= 11
                else:  # game window is bigger in vertical direction
                    # updates field coordinates
                    self.field_coord_top_left[0] -= 11
                    self.field_coord_top_left[1] += 11

        for i in range(2):
            # refreshes the writing's location
            self.top_left_corner[i] = self.field_coord_top_left[i] * field_size + field_size

        font_size = int(field_size * 1.3)  # calculates the new size of the writing
        self.font = pygame.font.SysFont(None, font_size)  # refreshes the font


# -------
# creates boards, their tiles and writings on boards' sides
def _create_big_fields(field_size, field_count_x, field_count_y, orienation):
    """
    creates both boards into global list big_fields

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param field_count_x: int; quantity of tiles on one board in horizontal direction
    :param field_count_y: int; quantity of tiles on one board in vertical direction
    :param orienation: str; width/height, depending on what is bigger
    """
    global big_fields  # creates list later containing both boards
    big_fields = [0, 0]
    size_x = field_count_x * field_size  # sets size in horizontal direction
    size_y = field_count_y * field_size  # sets size in vertical direction

    location_top_left = [3 / 2 * field_size, 3 / 2 * field_size]  # sets top left corner
    # creates enemy's board
    big_fields[0] = BigField(size_x, size_y, location_top_left, field_count_x, field_count_y)

    if orienation == "height":  # game window is bigger in vertical direction
        location_top_left = [3 / 2 * field_size, 25 / 2 * field_size]  # sets top left corner
    else:  # gae window is bigger in horizontal direction
        location_top_left = [25 / 2 * field_size, 3 / 2 * field_size]  # sets top left corner
    # creates player's board
    big_fields[1] = BigField(size_x, size_y, location_top_left, field_count_x, field_count_y)


def _create_small_fields(field_size, orienation):
    """
    creates boards' tiles into global list small_fields

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orienation: str; width/height, depending on what is bigger
    """
    global small_fields  # creates lsit later containing all tiles
    small_fields = []
    for x in range(2):  # goes through number of boards
        small_fields.append([])
        for i in range(big_fields[x].field_count_x):  # goes through number of tiles in horizontal direction default=10
            small_fields[x].append([])
            for j in range(big_fields[x].field_count_y):  # goes through number of tiles in vertical direction default10
                small_fields[x][i].append(0)
                # sets field coordinates
                location_field_y = j
                location_field_x = i
                if x == 0:  # tile is on enemy's board
                    # creates tile
                    small_fields[x][i][j] = SmallField(x, False, False, False,
                                                       field_size * (3 / 2 + location_field_x), location_field_x,
                                                       location_field_y, field_size * (3 / 2 + location_field_y))
                else:  # tile is on player's board
                    if orienation == "height":  # game window is bigger in vertical direction
                        # creates tile
                        small_fields[x][i][j] = SmallField(x, False, False, False,
                                                           field_size * (3 / 2 + location_field_x), location_field_x,
                                                           location_field_y + 10,
                                                           field_size * (25 / 2 + location_field_y))
                    else:  # agme window is bigger in horizontal direction
                        # creates tile
                        small_fields[x][i][j] = SmallField(x, False, False, False,
                                                           field_size * (25 / 2 + location_field_x),
                                                           location_field_x + 10,
                                                           location_field_y, field_size * (3 / 2 + location_field_y))


def _create_writings(field_size):
    """
    creates the writings on the side of the boards into global list playfield_writings

    :param field_size: float; size of a virtual field, depending on size of the playfield and the size of the window
    """
    global playfield_writings
    playfield_writings = []  # creates a list that later holds the writings

    color = (255, 255, 255)  # sets the color to lime green
    font_size = int(field_size * 1.3)  # calculates the writing's size
    font = pygame.font.SysFont(None, font_size)  # sets the writing's font

    for i in range(4):  # there are 4 different "lines" of writings, two of which consist solely of letters
        # sets starting coordinates for those lines
        field_coord_x = [0, 0, 11, 22]
        field_coord_y = [0, 0, 0, 0]

        for j in range(big_fields[0].field_count_x):
            if i < 2:  # writing next to enemy's board is created
                own_field = False
            else:  # writing next to player's board is created
                own_field = True

            if i % 2 == 1:  # numbers are created
                content = str(j + 1)  # sets the content to the next number
                field_coord_y[i] += 1  # changes the y field coord
            else:  # letters are created
                content = alphabet[j]  # sets the content to the next letter
                field_coord_x[i] += 1  # changes the x field coord

            field_coord_top_left = [field_coord_x[i], field_coord_y[i]]  # sets the next field coordinate

            # calculates the writing's location
            top_left_corner = [0, 0]
            for ij in range(2):
                top_left_corner[ij] = field_coord_top_left[ij] * field_size + field_size

            # adds the writing to the list of writings
            playfield_writings.append(PlayfieldWriting(content, font, color, top_left_corner, field_coord_top_left,
                                                       own_field, "width"))


def __init__playfield(load, language, orienation, field_size, field_count_x, field_count_y, resource_path):
    """
    creates boards and their tiles as well as writing on boards' side

    when game is loaded, loads boards and their tiles instead

    :param load: bool; game is loaded insted of being newly created
    :param language: str; language all texts are currently displayed in
    :param orienation: str; width/height, depending on what is bigger
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param field_count_x: int; quantity of tiles on one board in horizontal direction
    :param field_count_y: int; quantity of tiles on one board in vertical direction
    :param resource_path: Func; returns the resource path to a relative path
    """
    if load:  # saved game is loaded
        global big_fields
        global small_fields
        try:
            big_fields = save.load('lis', 'playfield', 1, resource_path)  # loads both boards
        except FileNotFoundError:
            chat.add_missing_message("playfield1.lis", resource_path("saves/"), language)
            return True
        try:
            small_fields = save.load('lis', 'playfield', 2, resource_path)  # loads boards' tiles
        except FileNotFoundError:
            chat.add_missing_message("playfield2.lis", resource_path("saves/"), language)
            return True
    else:  # new game is created
        _create_big_fields(field_size, field_count_x, field_count_y, orienation)  # creates both boards
        _create_small_fields(field_size, orienation)  # creates boards' tiles
    _create_writings(field_size)  # creates writings on the side of the boards


# -------
# updates boards' coordinates on the game window
def refresh_loc_small_fields(field_size, orientation):
    """
    refreshes the tiles' coordinates, used when changes to game window are made
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    """
    for z in range(2):
        for i in range(big_fields[z].field_count_x):
            for j in range(big_fields[z].field_count_y):  # goes through every tile
                small_fields[z][i][j].change_loc_coords(field_size, orientation)  # updates its coordinates


def refresh_loc_big_fields(field_size, orientation):
    """
    refreshes the boards' coordinates, used when changes to game window are made
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    """
    for i in range(2):  # goes through both boards
        if i == 0:  # board is the enemy's
            own_field = False
        else:  # board is the player's
            own_field = True
        big_fields[i].change_loc_coords(field_size, orientation, own_field)  # upates board's coordinates


def refresh_loc_writings(field_size, orientation):
    """
    refreshes the writings' coordinates, used when changes to game window are made
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    """
    for writing_local in playfield_writings:  # goes through every writing
        writing_local.refresh_loc_coords(field_size, orientation)  # refreshes writing's coordinates


# -------
# displays boards
def draw_playfield(screen, field_size, zustand):
    """
    displays both boards and nubers and letters used to make the player be able to tell tiles apart
    :param screen: Surface; surface covering the whole game window
    :param field_size: float; size of a virtual fieldthat is determined by the size of the window that inhabits the GUI
    :param zustand: str; start/ingame/settings, used to determine loop the game is in currently
    """
    if zustand == "ingame":  # boards are displayed
        for big_field in big_fields:  # goes through boards
            big_field.draw(screen)  # displays it

        for z in range(2):
            for i in range(big_fields[z].field_count_x):
                for j in range(big_fields[z].field_count_y):  # goes htrough every tile
                    small_fields[z][i][j].draw(screen, field_size)  # displays it

        for writing_local in playfield_writings:  # goes through every writing
            writing_local.draw(screen, True)  # dispalys it


# ------
# updates boards' values
def hit_small_field(player, field_coord_x, field_coord_y, resource_path, sound_volume, language, old_field_coord_x=-1,
                    old_field_coord_y=-1):
    """
    hits a small field by marking it with an x and playing a sound while also displaying,
     whether a ship is on that field or not

    :param player: int; opposite of the player currently playing
    :param field_coord_x: int; x coordiante of the small field that is hit
    :param field_coord_y: int; y coordiante of the small field that is hit
    :param resource_path: Func; creates the resource path to a relative path
    :param sound_volume: float; 0 - 1, volume of sounds
    :param language: str; language all texts are currently displayed in
    :param old_field_coord_x: int; x coordiante of the small field that was hit before
    :param old_field_coord_y: int; y coordiante of the small field that was hit before
    """
    if player == 1:  # checks which player is currently playing
        # hits the field as a player
        small_fields[1 - player][field_coord_x][field_coord_y].become_hit_player(resource_path, sound_volume, language)
    else:
        # unclicks the previously hit field
        small_fields[1 - player][old_field_coord_x][old_field_coord_y].clicked_on = False
        # hits the field as an enemy
        small_fields[1 - player][field_coord_x][field_coord_y].become_hit_enemy()


def unclick(coord):
    """
    reverts a click on the plyfield, used for the enemies clicks
     and to revert players clicks when not click is not confirmed
    :param coord: list[int, int]; coordinate of the field that is going to be unclicked
    """
    xcoord, ycoord = coord  # coordinate of field that is unclicked
    small_fields[0][xcoord][ycoord].clicked_on = False  # unclicks that field


# -------
# returns board and values
def get_big_fields():
    """
    :return: list[BigField, BigField]; list wih both boards
    """
    return big_fields


def get_small_fields():
    """
    :return: list[SmallField, SmallField, ...]; list with all tiles on the boards
    """
    return small_fields


def get_small_fieldcounts():
    """
    :return: list[int, int]; quantity of tiles on one board
    """
    return big_fields[0].field_count_x, big_fields[0].field_count_y


# ------
# saves game
def save_playfield(resource_path, language):
    """
    saves the playfield, used to continue games after closing the program

    :param resource_path: Func; returns the resource path to a relative path
    :param language: str; language all texts are currently dispalyed in
    """
    try:
        save.save(big_fields, 'lis', 'playfield', 1, resource_path)  # saves board
    except FileNotFoundError:
        chat.add_missing_message("", resource_path("saves/"), language, False)
    else:
        save.save(small_fields, 'lis', 'playfield', 2, resource_path)  # saves tiles on the board
