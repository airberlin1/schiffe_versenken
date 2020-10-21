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
        self.selected = False

    def draw(self, surface, centered=False):
        """
        places the writing visible on the GUI
        :param surface: Surface; surface the writing is shown on
        :param centered: bool; show writing with top left corner as center, used in tables.Table
        """
        if self.selected:
            used_color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])
        else:
            used_color = self.color
        # shows the writing
        if centered:
            # displays the writing centered with top left corner as center
            rect = self.font.render(self.content, True, used_color,
                                    self.background).get_rect(center=self.top_left_corner)
            surface.blit(self.font.render(self.content, True, used_color, self.background), rect)
        else:
            # displays the writing with top left corner as top left corner
            surface.blit(self.font.render(self.content, True, used_color, self.background), self.top_left_corner)
