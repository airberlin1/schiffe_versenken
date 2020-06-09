# module that displays the writing
class Writing:
    """Writing and the possibilty to bring it on screen"""

    def __init__(self, content, font, color, top_left_corner, background=None):
        """
        initializes the writing
        :param content: str; displayed text
        :param font: SysFont; font of the writing
        :param color: tuple(int, int, int); color in RGB
        :param top_left_corner: list[int, int]; writing's top left corner
        :param field_coord_top_left: list[int, int]; writing's top left corner as a field coordinate
        :param background: tuple(int, int, int); Hintergrundfarbe der Schrift
        """
        self.content = content
        self.font = font
        self.color = color
        self.top_left_corner = top_left_corner
        self.background = background

    def draw(self, screen):
        """
        places the writing visible on the GUI
        :param screen: Surface; surface of the GUI
        :return: nothing
        """
        # shows the writing
        screen.blit(self.font.render(self.content, True, self.color, self.background), self.top_left_corner)
