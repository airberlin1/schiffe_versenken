from writing import Writing
from translation import get_dict
from pygame.font import SysFont


class Chat:
    """Chat containing 6 line objects"""

    def __init__(self, field_size, orientation):
        """
        creates chat's lines, sets chat's coordiantes
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        :param orientation: str; width/height, what is bigger
        """
        line_list = []  # creates a list
        for i in range(6):
            line_list.append(Line(field_size, i, orientation))  # fills the list with lines
        self.lines = line_list
        self.refresh_loc(field_size, orientation)  # sets coordinates on the screen

    def refresh_loc(self, field_size, orientation):
        """
        sets/updates chat's coordinates
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        :param orientation: str; width/height, what is bigger
        """
        for line in self.lines:  # goes through every line
            line.refresh_loc(field_size, orientation)  # updates line's coordinates
        self.location = [field_size * 22, field_size * 0.5]  # updates chat's loaction
        # updates chat's size
        self.width = field_size * 6
        self.heigth = field_size * 4

    def draw(self, screen):
        """
        displays chat on the game window
        :param screen: Surf; surface that covers the whole window
        """
        for line in self.lines:  # goes through every line
            line.draw(screen)  # dsiplays taht line

    def delete_oldest_message(self):
        """
        deletes the oldest message to create space for new ones
        """
        for i in range(-1, -7, -1):  # goes backwards through the lines
            if self.lines[i].writing.content:  # gets the last displayed line
                self.lines[i].content = None  # erases it
                return  # breaks the loop so that no more lines are erased

    def add_message(self, message, color):
        """
        adds a message to the chat from the top

        moving all other messages one line down, potentially erasing the oldest one
        :param message: str; new message that is shown in the chat
        :param color: tup(int, int, int); color the message si shown in
        """
        number = 6  # prevents number from being unassigned
        # calculates number of occupied lines - 1
        for line in self.lines:
            if not line.writing.content:
                number = line.number
                break
        if number == 6:  # all lines are occupied
            self.delete_oldest_message()  # deletes the oldest message
            number = 5
        for i in range(0, 0 - number, -1):  # goes backwards through every occupied line
            # moves messages one line to the bottom
            self.lines[number + i].writing.content = self.lines[number + i - 1].writing.content
            self.lines[number + i].writing.color = self.lines[number + i - 1].writing.color
        # updates first line with new message
        self.lines[0].writing.content, self.lines[0].writing.color = message, color


class Line:
    """
    one line of Chat using writing.Writing to display itself
    """
    def __init__(self, field_size, line_number, orientation):
        """
        creates Line and its writing
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        :param line_number: int; 0 - 5, number to sort line
        :param orientation: str; width/height, what is bigger
        """
        # sets size
        self.width = field_size * 6
        self.height = field_size * 4 / 6
        # sets location
        x_coord = 24 if orientation == "width" else 12
        location = [field_size * x_coord, field_size * 0.5 + field_size * 4 / 6 * line_number]
        self.number = line_number
        # creates writing with default values
        content = None
        color = (125, 125, 125)
        font = SysFont(None, int(field_size * 4 / 6))
        self.writing = Writing(content, font, color, location)

    def refresh_loc(self, field_size, orientation):
        """
        refreshes line's size and writing's coordinates

        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        :param orientation: str; width/height, what is bigger
        """
        # updates size
        self.width = field_size * 6
        self.height = field_size * 4 / 6
        # updates writing's coordiantes
        x_coord = 24 if orientation == "width" else 12
        self.writing.top_left_corner = [field_size * x_coord, field_size * 0.5 + field_size * 4 / 6 * self.number]
        self.writing.font = SysFont(None, int(field_size * 4 / 6))

    def draw(self, screen):
        """
        displays line on the game window
        :param screen: Surf; surface that covers the whole window
        """
        if self.writing.content:  # line has a dsipalying meesage
            self.writing.draw(screen)  # line's writing is displayed


def __init__chat(field_size, orientation):
    """
    initializes chat

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, what is bigger
    """
    global chat
    chat = Chat(field_size, orientation)


def draw_chat(screen, zustand):
    """
    shows the chat on the game window

    :param screen: Surf; surface that covers the whole window
    :param zustand: start/settings/ingame; which loop is currently running
    """
    if zustand == "ingame":  # chat should be seen
        chat.draw(screen)


def refresh_loc(field_size, orientation):
    """
    updates chat's location

    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param orientation: str; width/height, what is bigger
    """
    chat.refresh_loc(field_size, orientation)


def add_message(message, color):
    """
    adds a message to be displayed in the chat
    :param message: str; new message that is shown in the chat
    :param color: tup(int, int, int); color the message si shown in
    """
    chat.add_message(message, color)


def delete_oldest():
    """
    deletes the oldest message currently displayed in the chat
    """
    chat.delete_oldest_message()


def add_missing_message(file, path, language, file_not_here=True):
    """
    adds file is missing message to chat

    :param file: str; file that is missing
    :param path: str; missing file's directory
    :param language: str; language all texts are currently displayed in
    :param file_not_here: bool; file is missing, not directory
    """
    chat.add_message("   " + path, (50, 50, 0))  # displays path
    # displays translated missing message
    dictionary = get_dict(language, "message")
    if file_not_here:
        chat_message = dictionary["System"] + dictionary["missing"] + file + "' in "
    else:
        chat_message = dictionary["System"] + dictionary["missingdir"]
    chat.add_message(chat_message, (50, 50, 0))