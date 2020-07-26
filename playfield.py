# commented, partly german
# module with the playfield, it's output on the GUI and it's coordinates

# ------
# imports pygame, that is used to build a GUI, and the writing for it being able to displayed on the GUI
import pygame
import writing

# ------
# sets tuples with used colors and the alphabet in alphabetic order to be displayed on top of the playfield
RED = (255, 0, 0)
GREY = (170, 170, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", " I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


# ------
# classes "BigField", "SmallField" and "PlayfieldWriting"
class BigField:
    """
    Spielfeld, standardmaeßig 10x10, welches beide Spieler, sowohl der Spieler als auch der Computergegner haben
    """

    def __init__(self, size_x, size_y, location_top_left, field_count_x=10, field_count_y=10):
        """
        initialisiert das jeweilige Spielfeld und setzt dessen Werte
        :param size_x: int; die Groesse des Spielfelds in die Breite
        :param size_y: int; die Groesse des Spielfelds in die Hoehe
        :param location_top_left: list[int, int]; die Koordinaten der linken oberen Ecke des Spielfelds
        :param field_count_x: int; die Anzahl der Felder innerhalb des Spielfelds in die Breite
        :param field_count_y: int; die Anzahl der Felder innerhalb des Spielfelds in die Hoehe
        """
        self.size_x = size_x
        self.size_y = size_y
        self.field_count_x = field_count_x
        self.field_count_y = field_count_y
        self.location_top_left = location_top_left

    def change_loc_coords(self, field_size, orienation, own_field):
        """
        aendert die Koordinaten des Spielfeldes
        :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
        :param orienation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
        :param own_field: bool; gibt an, ob es sich um das eigene oder das gegnerische Spielfeld handelt
        :return: nothing
        """
        # aendert die Groesse des Spielfelds
        self.size_y = self.field_count_y * field_size
        self.size_x = self.field_count_x * field_size
        # aendert die Koordinaten der oberen linken Ecke, ueberprueft dafuer zuerst, von welchem Spielfeld dies
        # geaendert wird und ggf. die Oberflaechenausrichtung
        if not own_field:
            self.location_top_left = [field_size * 3 / 2, field_size * 3 / 2]
        else:
            if orienation == "height":
                self.location_top_left = [field_size * 3 / 2, field_size * 25 / 2]
            else:
                self.location_top_left = [field_size * 25 / 2, field_size * 3 / 2]

    def draw(self, screen):
        """
        gibt das grosse Feld auf dem Bildschirm aus, als dicke schwarze Umrandung,
        mit einer etwas duenneren, weissen Umrandung,
        die zusammen einen Kontrast zu nahezu jedem Hintergrund zur Folge haben
        :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
        :return: nothing
        """
        pygame.draw.rect(screen, BLACK,  # zeichnet die dicke, schwarze Umrandung
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 5)
        pygame.draw.rect(screen, WHITE,  # zeichnet die duennere, weisse Umrandung
                         (self.location_top_left[0], self.location_top_left[1], self.size_x, self.size_y), 3)


class SmallField:
    """
    kleines feld, auf dem entweder ein Schiff ist oder auch nicht, und das entweder getroffen wurde oder auch nicht
    """

    def __init__(self, big_field, ship_on, hit_on, clicked_on, location_coord_x, location_field_x, location_field_y,
                 location_coord_y, ship_number=-1):
        """
        initialisiert das jeweilige kleine Feld
        :param big_field: int; die Nummer des Spielfeldes, zu dem das kleine Feld gehoert,
                          wobei 1 das eigene und 0 das gegnerische Spielfeld darstellt
        :param ship_on: bool; gibt an, ob sich ein Schiff auf diesem Feld befindet
        :param hit_on: bool; gibt an, ob dieses Feld bereits beschossen wurde
        :param clicked_on: bool; Feld angeklickt
        :param location_coord_x: int; die x-Koordintae der oberen linken Ecke des Feldes
        :param location_field_x: int; die Nummer des Feldes in der Breite, auf dem sich das Feld befindet
        :param location_field_y: int; die Nummer des Feldes in der Hoehe, auf dem sich das Feld befindet
        :param location_coord_y: int; die y-Koordintae der oberen linken Ecke des Feldes
        :param ship_number: die Nummer des Schiffes, das sich auf dem Feld befindet, falls eines vorhanden ist
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

    def change_loc_coords(self, field_size, orienation):
        """
        aendert die Koordinaten des Feldes
        :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
        :param orienation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
        :return: nothing
        """
        if self.big_field == 0:  # ueberpruft, in welchem Spielfeld sich das Feld befindet
            # setzt die Koordinaten neu
            self.location_coord_x = 3 / 2 * field_size + self.location_field_x * field_size
            self.location_coord_y = 3 / 2 * field_size + self.location_field_y * field_size
        else:
            if orienation == "height":  # ueberprueft den Bildschirmzustand
                if self.location_field_x > 9:  # ueberprueft, ob sich der Bildschirmzustand veraendert hat
                    self.location_field_x -= 10  # setzt das Feld in die Breite neu
                    self.location_field_y += 10  # setzt das Feld in die Hoehe neu
                loc_field_x = self.location_field_x  # setzt eine Variable auf die Nummer des Feldes in die Breite
                # setzt eine Variable auf die Nummer des Feldes in die Hoehe + 1, da hier ein Feld uebersprungen wird
                loc_field_y = self.location_field_y + 1
            else:
                if self.location_field_y > 9:  # ueberprueft, ob sich der Bildschirmzustand veraendert hat
                    self.location_field_x += 10  # setzt das Feld in die Breite neu
                    self.location_field_y -= 10  # setzt das Feld in die Hoehe neu
                # setzt eine Variable auf die Nummer des Feldes in die Breite + 1, da hier ein Feld uebersprungen wird
                loc_field_x = self.location_field_x + 1
                loc_field_y = self.location_field_y  # setzt eine Variable auf die Nummer des Feldes in die Hoehe
            # setzt die Koordinaten des Feldes neu
            self.location_coord_x = 3 / 2 * field_size + loc_field_x * field_size
            self.location_coord_y = 3 / 2 * field_size + loc_field_y * field_size

    def draw(self, screen, field_size):
        """
        gibt das kleine Feld auf dem Bildschirm aus, als dicke schwarze Umrandung,
        mit einer etwas duenneren, weissen Umrandung,
        die zusammen einen Kontrast zu nahezu jedem Hintergrund zur Folge haben
        :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
        :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
        :return: nothing
        """
        # zeichnet die dicke, schwarze Umrandung
        pygame.draw.rect(screen, BLACK, (self.location_coord_x, self.location_coord_y, field_size, field_size), 3)
        pygame.draw.rect(screen, WHITE,  # zeichnet die duennere, weisse Umrandung
                         (self.location_coord_x, self.location_coord_y, field_size, field_size), 1)

        if self.clicked_on:  # ueberprueft, ob das Feld
            pygame.draw.rect(screen, BLACK,  # zeigt das Feld schwarz
                             (self.location_coord_x, self.location_coord_y, field_size, field_size), 0)

        if self.hit_on:  # ueberprueft, ob das Feld bereits getroffen wurde
            color = GREY  # setzt due Farbe auf Grau
            # zeichnet ein  graues Kreuz ueber das Feld
            pygame.draw.line(screen, color, (self.location_coord_x + field_size,
                                             self.location_coord_y),
                             (self.location_coord_x, self.location_coord_y + field_size), 5)
            pygame.draw.line(screen, color, (self.location_coord_x, self.location_coord_y),
                             (self.location_coord_x + field_size, self.location_coord_y + field_size), 5)

    def become_hit_player(self, resource_path, sound_volume):
        """
        das kleine Feld wird getroffen
        :param resource_path: Func; returns the resource path to a relative path
        :param sound_volume: float; volume of sounds
        """
        if self.hit_on:  # ueberprueft, ob das Feld bereits zuvor getroffen wurde
            self.clicked_on = False  # entklickt das Feld

        elif self.clicked_on:
            self.clicked_on = False  # entklickt das Feld
            self.hit_on = True  # setzt das Feld als getroffen
            new_channel = pygame.mixer.Channel(0)
            sound = pygame.mixer.Sound(resource_path("assets/sounds/nothit.wav"))
            sound.set_volume(sound_volume)
            new_channel.play(sound)

        else:
            self.clicked_on = True  # klickt das Feld an
        print(self.location_field_x, self.location_field_y)
        print(self.clicked_on, self.hit_on)

    def become_hit_enemy(self):
        """
        das kleine Feld wird getroffen
        """
        self.hit_on = True  # trifft das Feld
        self.clicked_on = True  # klickt das Feld an


class PlayfieldWriting(writing.Writing):
    """Schrift am Rand des Spielelds"""

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
        :param field_size: int; size of a virtual field, depending on size of the playfield and the size of the window
        :param orientation: str; width or height depending on the size and appearance of the window
        :return: nothing
        """
        if self.own_field:  # checks, on who's playfield the writing is
            if orientation != self.orientation:  # checks, if the orientation changed
                self.orientation = orientation  # refreshes the writing's orientation

                if orientation == "width":  # checks the orientation
                    # refreshes the field_coords
                    self.field_coord_top_left[0] += 11
                    self.field_coord_top_left[1] -= 11
                else:
                    # refreshes the field_coords
                    self.field_coord_top_left[0] -= 11
                    self.field_coord_top_left[1] += 11

        for i in range(2):
            # refreshes the writing's location
            self.top_left_corner[i] = self.field_coord_top_left[i] * field_size + field_size * (0.7 - 0.1 * i)

        font_size = int(field_size * 1.3)  # calculates the new size of the writing
        self.font = pygame.font.SysFont(None, font_size)  # refreshes the font


# -------
# erstellt die Spielfelder
def _create_big_fields(field_size, field_count_x, field_count_y, orienation):
    """
    erstellt die beiden Spielfelder
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param field_count_x: int; die Anzahl der Felder eines Spielfeldes in horizontale Richtung
    :param field_count_y: int; die Anzahl der Felder eines Spielfeldes in vertikale Richtung
    :param orienation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    :return: nothing
    """
    global big_fields  # erstellt eine leere Liste, in der sich spaeter die beiden Spielfelder befinden
    big_fields = [0, 0]
    # legt Werte fuer die Spielfelder fest
    location_top_left = [3 / 2 * field_size, 3 / 2 * field_size]  # ermittelt die obere linke Ecke
    size_x = field_count_x * field_size  # ermittelt die Groesse des Feldes in horizontaler Richtung
    size_y = field_count_y * field_size  # ermittelt die Groesse des Feldes in vertikaler Richtung
    # erstellt das erste und gegnerische Spielfeld
    big_fields[0] = BigField(size_x, size_y, location_top_left, field_count_x, field_count_y)
    # ueberprueft den Bildschirmzustand und setzt danach die Ecke links oben neu
    if orienation == "height":
        location_top_left = [3 / 2 * field_size, 25 / 2 * field_size]
    else:
        location_top_left = [25 / 2 * field_size, 3 / 2 * field_size]
    # erstellt das zweite und eigene Spielfeld
    big_fields[1] = BigField(size_x, size_y, location_top_left, field_count_x, field_count_y)


def _create_small_fields(field_size, orienation):
    """
    erstellt die kleinen Felder, die sich in den Spielfeldern befinden
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param orienation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    :return: nothing
    """
    global small_fields  # erstellt eine leere Liste, in der sich spaeter alle kleinen Felder befinden
    small_fields = []
    for x in range(2):
        # erstellt zwei Listen in der Liste, um zwischen den beiden Spielfeldern zu unterscheiden
        small_fields.append([])
        for i in range(big_fields[x].field_count_x):
            # erstellt weitere Listen, die mit Nullen gefuellt sind, bei ansonsten normalen Einstellungen 10 x 10
            small_fields[x].append([])
            for j in range(big_fields[x].field_count_y):
                small_fields[x][i].append(0)
                # setzt die Koordinaten innerhalb des Spielfeldes auf den Erstellungsort innerhalb der Listen
                location_field_y = j
                location_field_x = i
                if x == 0:  # ueberprueft, in welchem Spielfeld sich das Feld befindet
                    # erstellt die Felder in dem ersten und gegnerischen Feld
                    small_fields[x][i][j] = SmallField(x, False, False, False,
                                                       field_size * (3 / 2 + location_field_x), location_field_x,
                                                       location_field_y, field_size * (3 / 2 + location_field_y))
                else:
                    if orienation == "height":  # ueberpruft die Bildschirmausrichtung
                        # erstellt die Felder im zweiten und eigenen Spielfeld
                        small_fields[x][i][j] = SmallField(x, False, False, False,
                                                           field_size * (3 / 2 + location_field_x), location_field_x,
                                                           location_field_y + 10,
                                                           field_size * (25 / 2 + location_field_y))
                    else:
                        # erstellt die Felder im zweiten und eigenen Spielfeld
                        small_fields[x][i][j] = SmallField(x, False, False, False,
                                                           field_size * (25 / 2 + location_field_x),
                                                           location_field_x + 10,
                                                           location_field_y, field_size * (3 / 2 + location_field_y))


def _create_writings(field_size):
    """
    creates the writings on the side of the game
    :param field_size: int; size of a virtual field, depending on size of the playfield and the size of the window
    :return: nothing
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
            if i < 2:  # checks, whether the writing next to the player's field is created
                own_field = False
            else:
                own_field = True

            if i % 2 == 1:  # checks, whether letters or numbers are created
                content = str(j + 1)  # sets the content to the next number
                field_coord_y[i] += 1  # changes the y field coord
            else:
                content = alphabet[j]  # sets the content to the next letter
                field_coord_x[i] += 1  # changes the x field coord

            field_coord_top_left = [field_coord_x[i], field_coord_y[i]]  # sets the next field coordinate

            if i == 1 and j == 9:  # checks, if the ten next to the enemy's playfield is created
                field_coord_top_left[0] -= 0.3  # sets it a small amount to the left

            # calculates the writing's location
            top_left_corner = [0, 0]
            for ij in range(2):
                top_left_corner[ij] = field_coord_top_left[ij] * field_size + field_size * (0.7 - 0.15 * ij)

            # adds the writing to the list of writings
            playfield_writings.append(PlayfieldWriting(content, font, color, top_left_corner, field_coord_top_left,
                                                       own_field, "width"))


def __init__playfield(orienation, field_size, field_count_x, field_count_y):
    """
    erstellt das gesamte Spielfeld mit den beiden Spielfeldern und den darin vorhandenen kleine Feldern,
    sowie die Knoepfe auf der Oberflaeche
    :param orienation: str; gibt an, ob der Bildschirm eine größere Ausbreitung in die Breite oder in die Hoehe hat
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param field_count_x: int; die Anzahl der Felder eines Spielfeldes in horizontale Richtung
    :param field_count_y: int; die Anzahl der Felder eines Spielfeldes in vertikale Richtung
    :return: nothing
    """
    _create_big_fields(field_size, field_count_x, field_count_y, orienation)  # erstellt die beiden Spielfelder
    _create_small_fields(field_size, orienation)  # erstellt die kleinen Felder in den Spielfeldern
    _create_writings(field_size)  # creates the writing on the side of the big fields


# -------
# erneuert die Koordinaten der Spielfelder und andere Attribute
def refresh_loc_small_fields(field_size, orientation):
    """
    setzt die Koordinaten der kleinen Felder neu, noetig wenn die Oberflaeche veraendert wird
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :return: nothing
    """
    # geht durch alle kleinen Spielfelder durch
    for z in range(2):
        for i in range(big_fields[z].field_count_x):
            for j in range(big_fields[z].field_count_y):
                small_fields[z][i][j].change_loc_coords(field_size, orientation)  # aendert die Koordinaten des Felds


def refresh_loc_big_fields(field_size, orientation):
    """
    setzt die Koordinaten der Spielfelder neu, noetig wenn die Oberflaeche veraendert wird
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    """
    for i in range(2):
        if i == 0:  # Ueberprueft die Nummer des Spielfeldes, wobei 0 das gegnerische und 1 das eigene ist
            # setzt eine Variable, die angibt, ob das eigene Feld bearbeitet wird, auf 'False',
            # wenn das gegnerische Feld bearbeitet wird
            own_field = False
        else:
            # setzt eine Variable, die angibt, ob das eigene Feld bearbeitet wird, auf 'True',
            # wenn das eigene Feld bearbeitet wird
            own_field = True
        big_fields[i].change_loc_coords(field_size, orientation, own_field)  # aendert die Koordinaten des Spielfelds


def refresh_loc_writings(field_size, orientation):
    """
    refreshes the coordinates of the writings
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, depending on what is bigger
    :return: nothing
    """
    for writing_local in playfield_writings:  # goes through every writing
        writing_local.refresh_loc_coords(field_size, orientation)  # refreshes the coordiantes of the writing


def unclick(coord):
    """
    reverts a click on the plyfield, used for the enemies clicks
    :param coord: list[int, int]; coordiante of the field, that is going to be unclicked
    :return: nothing
    """
    xcoord, ycoord = coord  # unpyks the coordinate of the field, that is going to be unclicked
    small_fields[0][xcoord][ycoord].clicked_on = False  # unclicks that field


# -------
# gibt die Spielfelder aus
def draw_playfield(screen, field_size, zustand):
    """
    gibt die Spielfelder aus
    :param screen: Surface; die Oberflaeche, auf der alles zu sehen ist
    :param field_size: int; die Groeße eines virtuellen Feld,
                           abhaengig von der Spielfeldgroesse und der Groesse des Bildschirms
    :param zustand: str; gibt an, ob das Spiel bereits gespielt wird, oder sich noch am Start befindet
    :return: nothing
    """
    # ueberprueft, ob das Spiel bereits gespielt wird, und damit auch, ob das Spielfeld angezeigt werden soll
    if zustand == "ingame":
        for big_field in big_fields:  # geht die beiden Spielfelder durch
            big_field.draw(screen)  # zeichnet das jeweilige Spielfeld
        # geht durch alle kleinen Spielfelder durch
        for z in range(2):
            for i in range(big_fields[z].field_count_x):
                for j in range(big_fields[z].field_count_y):
                    small_fields[z][i][j].draw(screen, field_size)  # zeichnet das jeweilige kleine Feld
        for writing_local in playfield_writings:
            writing_local.draw(screen)


def hit_small_field(player, field_coord_x, field_coord_y, resource_path, sound_volume, old_field_coord_x=-1,
                    old_field_coord_y=-1):
    """
    hits a small field by marking it with an x and playing a sound while also displaying,
     whether a ship is on that field or not

    :param player: int; opposite of the player currently playing
    :param field_coord_x: int; x coordiante of the small field that is hit
    :param field_coord_y: int; y coordiante of the small field that is hit
    :param resource_path: Func; creates the resource path to a relative path
    :param sound_volume: float; 0 - 1, volume of sounds
    :param old_field_coord_x: int; x coordiante of the small field that was hit before
    :param old_field_coord_y: int; y coordiante of the small field that was hit before
    """
    if player == 1:  # checks which player is currently playing
        # hits the field as a player
        small_fields[1 - player][field_coord_x][field_coord_y].become_hit_player(resource_path, sound_volume)
    else:
        # unclicks the previously hit field
        small_fields[1 - player][old_field_coord_x][old_field_coord_y].clicked_on = False
        # hits the field as an enemy
        small_fields[1 - player][field_coord_x][field_coord_y].become_hit_enemy()


# -------
# gibt die Felder zurueck
def get_big_fields():
    """
    gibt die Spielfelder zurueck
    :return: list[BigField, BigField]; Liste mit den beiden grossen Felder
    """
    return big_fields  # gibt die Spielfelder zurueck


def get_small_fields():
    """
    gibt die kleinen Felder zurueck
    :return: list[SmallField, SmallField, ...]; Liste mit kleinen Felder
    """
    return small_fields


def get_small_fieldcounts():
    """
    gibt die Anzahl der kleinen Felder eines Spielfelds zurueck
    :return: list[int, int]; Anzahl der kleinen Felder eines Spielfelds
    """
    return big_fields[0].field_count_x, big_fields[0].field_count_y
