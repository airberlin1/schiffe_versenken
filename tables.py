"""tabels module controlling the table that shows remaining ships"""

# imports used classes
from writing import Writing  # used to dsiplay text
from pygame.font import SysFont  # used to render text
from pygame.surface import Surface  # used to display table

# ------
# dictionarys helping to transalte text in table
title_dict_german = {  # into german
    "Remaining Ships": "Restliche Schiffe",
    "Enemy": "Gegner",
    "Player": "Spieler",
    "Ship": "Schiff",
    "Ships": "Schiffe",
    "4": "4",
    "3": "3",
    "2": "2",
    "1": "1",
    "0": "0"
}
title_dict_latin = {  # into latin
    "Remaining Ships": "Navis Reliquae",
    "Enemy": "Lusor",
    "Player": "Hostis",
    "Ship": "Navis",
    "Ships": "Naves",
    "4": "IV",
    "3": "III",
    "2": "II",
    "1": "I",
    "0": "Nulla"
}


# ------
# table as object
class TableSpot:
    """
    one single table cell dispalying itself as its writing
    """
    def __init__(self, content, column_number, row_number):
        """
        :param content: str; cells content displayed as text
        :param column_number: int; x coord in the table this spot is in
        :param row_number: int; y coord in the table this spot is in
        """
        self.column = column_number
        self.row = row_number
        if not column_number:  # gets content for first column that does not change
            content = get_content_left_column(row_number)
        self.writing = Writing(content, None, (0, 255, 100), None)  # initializes its writing

    def refresh_loc(self,  field_size):
        """
        refreshes spot's coordiantes on the table surface
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        self.writing.font = SysFont(None, int(field_size * 4 / 7))  # resizes font
        # calculates writing's center
        self.writing.top_left_corner = [field_size * (3 / 2 + self.column * 3), field_size * (5 / 2 + self.row)]
        # calcualtes writing's size, currently not used further
        self.size = [field_size * 3, field_size * 3]

    def draw(self, table_surf, language, ships):
        """
        displays its writing on the table surface and thus on the game window
        :param table_surf: Surface; surface the table is shown on
        :param language: str; language the program's texts are currently displayed in
        :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
        """
        if self.column:  # content is dynamic
            self.get_content(language, ships)  # updates content
        self.writing.draw(table_surf, True)  # displays itself as writing

    def get_content(self, language, ships):
        """
        updates content depending on language and remaining ships
        :param language: str; language the program's texts are currently displayed in
        :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
        """
        self.writing.content = get_content_spot(self.column, self.row, ships, language)


class Column:
    """
    one column with a title as Writing containing several TableSpot objects
    """
    def __init__(self, number_of_rows, title, column_number):
        """
        :param number_of_rows: int; number of rows column contains
        :param title: str; title of column, displayed bigger than TableSpot writings on top of column
        :param column_number: int; x coord in the table the column is in
        """
        self.title = title
        self.number = column_number
        self.writing = Writing(title, None, (0, 100, 0), None)  # initializes its writing
        spot_list = []  # creates a list later containing all spots in this column
        for i in range(number_of_rows):
            spot_list.append(TableSpot("test", column_number, i))  # adds TableSpot
        self.spots = spot_list

    def refresh_loc(self, field_size):
        """
        refreshes column's coordiantes on the table surface
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        self.writing.font = SysFont(None, int(field_size))  # resizes font
        # calculates titles's center
        self.writing.top_left_corner = [field_size * 3 / 2 + field_size * self.number * 3, field_size * 3 / 2]
        for spot in self.spots:  # goes through every spot in this column
            spot.refresh_loc(field_size)  # refreshes its coordiantes

    def draw(self, language, table_surf, ships):
        """
        displays its title and all spots in this column on the table surface
        :param language: str; language the program's texts are currently displayed in
        :param table_surf: Surface; surface the table is shown on
        :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
        """
        self.writing.content = translate_title(language, self.title)  # transaltes title if neccessary
        self.writing.draw(table_surf, True)  # dsipalys the title as writing
        for spot in self.spots:  # goes through every spot in this column
            spot.draw(table_surf, language, ships)  # displays its content as writing


class Table:
    """
    table with a title containing several columns and rows, only columns as objects
    """
    def __init__(self, title, number_of_columns, number_of_rows, column_titles, field_size):
        """
        :param title: str; tables title, dsipalyed on top of the table
        :param number_of_columns: int; number of columns in the table
        :param number_of_rows: int; number of rows in the table
        :param column_titles: list[str, ...]; list containg all columns' titles
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        self.title = title
        font = SysFont(None, int(field_size * 3 / 2))  # sets font
        self.writing = Writing(title, font, (0, 100, 0), (field_size, field_size / 5))  # initializes title as writing
        self.fake_size = [number_of_columns, number_of_rows]  # sets size in rows and colums
        column_list = []  # creates a lsit later containg every column inhabiting the table
        for i in range(number_of_columns):
            column_list.append(Column(number_of_rows, column_titles[i], i))  # creates a column
        self.columns = column_list
        self.refresh_loc(field_size)  # initializes coordiantes and locations

    def refresh_loc(self, field_size):
        """
        updates coordinates on teh table surface
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        # gets surface with fitting size
        self.surf = Surface((self.fake_size[0] * 3 * field_size, self.fake_size[1] * 3 * field_size))
        self.location = [field_size * 25, field_size * 5]  # updates location on the game window
        self.writing.font = SysFont(None, int(field_size * 3 / 2))  # resizes title's font
        # calculates title's center
        self.writing.top_left_corner = [field_size * self.columns.__len__() * 3 / 2, field_size * 3 / 4]
        for column in self.columns:  # goes through every column
            column.refresh_loc(field_size)  # updates its locations

    def draw_outline(self, table_surf):
        """
        does nothing, use to draw outline?
        :param table_surf: Surface; surface the table is shown on
        """
        pass

    def draw(self, language, screen, ships):
        """
        dsiplays table on table surface and table surface on the game window
        :param language: str; language the program's texts are currently displayed in
        :param screen: Surface; surface that covers the whole window
        :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
        """
        table_surf = self.surf.copy()  # gets a new surface to prevent overlaying writings
        table_surf.set_colorkey((0, 0, 0))  # sets a colorkey to make table surface transparent apart from its content
        self.writing.content = translate_title(language, self.title)  # translates title if neccessary
        self.writing.draw(table_surf, True)  # displays its title
        self.draw_outline(table_surf)  # does nothing, potentially display an outline here?
        for column in self.columns:  # goes through every column
            column.draw(language, table_surf, ships)  # displays it
        screen.blit(table_surf, self.location)  # displays table surface on game window


# ------
# creation of tables, as of now only for remaining ships
def create_remainings_table(field_size):
    """
    creates table displaying remaining ships
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    global remainings
    remainings = Table(title="Remaining Ships", number_of_columns=3, number_of_rows=4,
                       column_titles=("Ship", "Player", "Enemy"), field_size=field_size)


# ------
# contents for table spots
def get_content_left_column(row_number):
    """
    returns content dor table spots in the left column, these don't change
    :param row_number: int; row the table spot is in
    :return: str; ship name together with number of tiles it covers
    """
    left_column_contents = ["FisherShip(2)", "ShipShip(3)", "ContainerShip(4)", "CruiseShip(5)"]
    return left_column_contents[row_number]


def get_content_spot(column, row, ships, language):
    """
    gets content for table spot that is not in the left column
    :param column: int; column the spot is in
    :param row: int; row the spot is in
    :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
    :param language: str; language the program's texts are currently displayed in
    :return: str; translated content of table spot
    """
    names = ["FisherShip", "ShipShip", "ContainerShip", "CruiseShip"]  # names of ships
    name = names[row]  # gets name of ship in taht row
    count = 0  # starts to count number of remaining ships of that ship type
    for ship in ships[column - 1]:  # goes through ships of correct player
        if not ship.is_destroyed() and name == ship.name:  # ship is remaining
            count += 1
    # gets singular/plural used for ship
    ship_saying = "Ship" if count == 1 else "Ships"
    if language == "latin" and not count:
        ship_saying = "Ship"
    # translates these terms and returns updated string
    return translate_title(language, str(count)) + " " + translate_title(language, ship_saying)


# ------
# translation
def translate_title(language, title):
    """
    translates title or content into english/german/latin
    :param language: str; language the program's texts are currently displayed in
    :param title: str; title or content that is translated
    :return: str; translated title or content
    """
    if language == "german":  # checks language
        translated_title = title_dict_german[title]  # translates title to german
    elif language == "latin":
        translated_title = title_dict_latin[title]  # translates title to latin
    else:
        translated_title = title  # does not change the title because it is english by default
    return translated_title  # returns translated title


# ------
# updating locations
def refresh_loc(field_size):
    """
    uodates tables coordinates
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    remainings.refresh_loc(field_size)


# ------
# displaying tables
def draw_tables(language, screen, ships):
    """
    displays all tables on the game window, currently only the one showing remaining ships
    :param language: str; language the program's texts are currently displayed in
    :param screen: Surface; surface that covers the whole window
    :param ships: list[list[Ship, ..], list]; list containing all ships that are on the board
    """
    remainings.draw(language, screen, ships)  # displays remaining ships table
