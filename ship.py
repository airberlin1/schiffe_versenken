# import fixed
import random as rd
import pygame
from playfield import hit_small_field
# TODO Modul sortieren
RED = (255, 0, 0)


class Ship:
    """Schiff, mit Laenge und Zustand"""

    def __init__(self, length, status, color, identification_number, player):
        # Klasse bzw. Objekte der Klasse initialisieren
        self.length = length
        self.status = status
        self.color = color
        self.identification_number = identification_number
        self.player = player

    def get_color(self):
        # gibt die Farbe des Schiffes zurueck
        return self.color

    def print_attributes(self):
        # die Eigenschaften des Schiffes ausgeben
        print("Length: " + str(self.length))
        print("Status: " + str(self.status))
        print("Color: " + str(self.color))

    def draw(self, screen, field_size, orientation, small_field_count_x, small_field_count_y):
        poslist = self.list_pos()
        for pos in poslist:
            if pos[2] == 1:
                color = RED
                draw_ship = True
            else:
                color = self.color
                if self.player == 0:
                    draw_ship = True
                else:
                    draw_ship = False
            if draw_ship:
                if self.player == 0:
                    if orientation == "width":
                        x_coord = pos[0] * field_size + 2.5 * field_size + small_field_count_x * field_size
                        y_coord = pos[1] * field_size + 1.5 * field_size
                    else:
                        x_coord = pos[0] * field_size + 1.5 * field_size
                        y_coord = pos[1] * field_size + 2.5 * field_size + small_field_count_y * field_size
                else:
                    x_coord = pos[0] * field_size + 1.5 * field_size
                    y_coord = pos[1] * field_size + 1.5 * field_size
                pygame.draw.rect(screen, color,
                                 (x_coord, y_coord, field_size, field_size), 0)


class Kreuzer5(Ship):
    """Schiff mit der Laenge 5"""

    def __init__(self, pos1, pos2, pos3, pos4, pos5, identification_number, player):
        Ship.__init__(self, 5, "safe", (0, 255, 0), identification_number, player)
        # Klasse bzw. Objekte der Klasse initialisieren
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.pos4 = pos4
        self.pos5 = pos5

    def print_positions(self):
        # die Positionen des Schiffes ausgeben
        print("Pos1: " + str(self.pos1))
        print("Pos2: " + str(self.pos2))
        print("Pos3: " + str(self.pos3))
        print("Pos4: " + str(self.pos4))
        print("Pos5: " + str(self.pos5))

    def list_pos(self):
        # die Positionen des Schiffes als Liste zurueckgeben
        return [self.pos1, self.pos2, self.pos3, self.pos4, self.pos5]

    def change_pos(self, poslist):
        # setzt alle Positionen aus einer Liste heraus neu
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]
        self.pos4 = poslist[3]
        self.pos5 = poslist[4]


class ContainerShip4(Ship):
    """Schiff mit der Laenge 4"""

    def __init__(self, pos1, pos2, pos3, pos4, identification_number, player):
        Ship.__init__(self, 4, "safe", (255, rd.randint(150, 255), 0), identification_number, player)
        # Klasse bzw. Objekte der Klasse initialisieren
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.pos4 = pos4

    def print_positions(self):
        # die Positionen des Schiffes ausgeben
        print("Pos1: " + str(self.pos1))
        print("Pos2: " + str(self.pos2))
        print("Pos3: " + str(self.pos3))
        print("Pos4: " + str(self.pos4))
        return

    def list_pos(self):
        # die Positionen des Schiffes als Liste zurueckgeben
        return [self.pos1, self.pos2, self.pos3, self.pos4]

    def change_pos(self, poslist):
        # setzt alle Positionen aus einer Liste heraus neu
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]
        self.pos4 = poslist[3]
        return


class ShipShip3(Ship):
    """Schiff mit der Laenge 3"""

    def __init__(self, pos1, pos2, pos3, identification_number, player):
        Ship.__init__(self, 3, "safe", (rd.randint(150, 255), 125, 0), identification_number, player)
        # Klasse bzw. Objekte der Klasse initialisieren
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3

    def print_positions(self):
        # die Positionen des Schiffes ausgeben
        print("Pos1: " + str(self.pos1))
        print("Pos2: " + str(self.pos2))
        print("Pos3: " + str(self.pos3))
        return

    def list_pos(self):
        # die Positionen des Schiffes als Liste zurueckgeben
        return [self.pos1, self.pos2, self.pos3]

    def change_pos(self, poslist):
        # setzt alle Positionen aus einer Liste heraus neu
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        self.pos3 = poslist[2]
        return


class FisherShip2(Ship):
    """Schiff mit der Laenge 2"""

    def __init__(self, pos1, pos2, identification_number, player):
        Ship.__init__(self, 2, "safe", (128, rd.randint(0, 128), 128), identification_number, player)
        # Klasse bzw. Objekte der Klasse initialisieren
        self.pos1 = pos1
        self.pos2 = pos2

    def print_positions(self):
        # die Positionen des Schiffes ausgeben
        print("Pos1: " + str(self.pos1))
        print("Pos2: " + str(self.pos2))
        return

    def list_pos(self):
        # die Positionen des Schiffes als Liste zurueckgeben
        return [self.pos1, self.pos2]

    def change_pos(self, poslist):
        # setzt alle Positionen aus einer Liste heraus neu
        self.pos1 = poslist[0]
        self.pos2 = poslist[1]
        return


def _set_rand_pos():
    """
    setzt jedes Schiff auf eine zufaellige Postion im Spielfeld
    :return: nothing
    """
    # TODO Variablennamen
    # geht alle Schiffe durch
    for y in range(2):
        for x in range(10):
            testing = 0
            while testing == 0:
                testing = 1
                # bekommt deren Ausrichtung und setzt pos1 auf ein zufaelliges Feld
                dire = _get_rand_pos(y, x, ship[y][x].length)
                positionsr = ship[y][x].list_pos()
                lengthr = ship[y][x].length
                # ueberprueft die Laenge und dann die Richtung und legt damit pos2 bis ggf. pos5 fest, die jeweils um
                # 1 von der vorherigen pos Abweichen
                for i in range(2):
                    for j in range(lengthr):
                        if dire == 1:
                            eeb = -i * j
                        elif dire == 2:
                            eeb = j - (i * j)
                        elif dire == 3:
                            eeb = i * j
                        elif dire == 4:
                            eeb = -(j - (i * j))
                        if j > 0:
                            positionsr[j][i] = positionsr[0][i] + eeb
                ship[y][x].change_pos(positionsr)
                positionsd = ship[y][x].list_pos()
                length = ship[y][x].length
                for h in range(length):
                    if ship_check[y][int(positionsd[h][0])][int(positionsd[h][1])] == 1:
                        testing = 0
            positions = ship[y][x].list_pos()
            length = ship[y][x].length
            for h in range(length):
                ship_check[y][positions[h][0]][positions[h][1]] = 1


def __init__ship():
    """initialisiert die Methode Schiff"""
    set_ship_count(10)
    __init__shipcheck()
    return


def __init__shipcheck():
    """erstellt eine ueberpruefende Liste, die dafuer sorgt, dass biem Erstellen der Schiffe keine Ueberschneidungen
    entstehen"""
    global ship_check
    ship_check = []
    for t in range(2):
        ship_check.append([])
        for x in range(10):
            ship_check[t].append([])
            for y in range(10):
                ship_check[t][x].append(0)


def set_ships():
    """
    erstellt die Schiffe, sodass ship[0] die eigenen und ship[1] die generischen Schiffe enthaelt, nach Groesse dieser
    sortiert
    :return: nothing
    """
    global ship
    ship = []
    for i in range(2):
        # zwei Listen erstellen, in denen spaeter die Schiffe sind
        ship.append([])
        for j in range(10):
            ship[i].append(0)
        # fuer jeden Spieler zehn Schiffe mit verschiedenen Laengen erstellen, die noch nicht zerstoert sind
        for j in range(4):
            ship[i][j] = FisherShip2([-1, -1, 3], [-1, -1, 3], identification_number=j + 1, player=i)
        for j in range(3):
            d = j + 4
            ship[i][d] = ShipShip3([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], identification_number=d + 1, player=i)
        ship[i][7] = ContainerShip4([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                                    identification_number=8, player=i)
        ship[i][8] = ContainerShip4([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                                    identification_number=9, player=i)
        ship[i][9] = Kreuzer5([-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3], [-1, -1, 3],
                              identification_number=10, player=i)
    # alle Schiffe auf zufaellige Positionen setzen
    _set_rand_pos()
    return


def check_ship_status(end):
    """
    :return: nothing
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
            end(1 - f)
    return


def _get_rand_pos(y, x, length):
    """
    erstellt eine zufaellige Position fuer das Schiff und und dessen Ausrichtung
    :param y: Spieler, dem das Schiff gehoert, benutzt in ship[y]
    :param x: Nummer des Schiffes, benutzt in ship[][x]
    :param length: Laenge des Schiffes
    :return: Ausrichtung des Schiffes
    die Position wird bereits direkt als erste position des Schiffes eingetragen
    """
    global ship
    # zufaellige Startposition setzen
    ship[y][x].pos1 = [rd.randint(0, 9), rd.randint(0, 9), 3]
    while True:
        # zufaellige Richtung setzen und ueberpruefen, ob das Schiff komplett auf dem Spielfeld ist,
        # wenn nicht, wird es wiederholt
        direction = rd.randint(1, 4)
        if direction == 1:
            if 0 <= ship[y][x].pos1[1] - length <= 9:
                return direction
        elif direction == 2:
            if 0 <= ship[y][x].pos1[0] + length <= 9:
                return direction
        elif direction == 3:
            if 0 <= ship[y][x].pos1[1] + length <= 9:
                return direction
        elif direction == 4:
            if 0 <= ship[y][x].pos1[0] - length <= 9:
                return direction


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


def hit_something(xcoord, ycoord, player, old_xcoord=-1, old_ycoord=-1):
    """trifft ein Schiff, dass sich an dem Ort (xcoord, ycoord) befindet"""
    player = 1 - player
    for i in range(ship_count):
        if check_ship_pos(ship[player][i], (xcoord, ycoord))[0]:
            # aendert den dritten Wert der Position des Schiffteiles, das getroffen wurde,
            # sodass es als zerstört erkannt wird
            hit_small_field(player, xcoord, ycoord, old_xcoord, old_ycoord)
            ship_part_number = check_ship_pos(ship[player][i], (xcoord, ycoord))[2]
            positions_local = ship[player][i].list_pos()
            positions_local[ship_part_number][2] = 1
            ship[player][i].change_pos(positions_local)
            return
    hit_small_field(player, xcoord, ycoord, old_xcoord, old_ycoord)


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


def set_ship_count(count):
    # setzt die Anzahl der Schiffe
    global ship_count
    ship_count = count
    return


def get_ship_positions():
    ship_coordinates = []
    for x in ship[0]:
        ship_coordinates += x.list_pos()
    return ship_coordinates
