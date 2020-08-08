"""slider module containing two functioning slider objects controlling volume"""
import pygame
from writing import Writing

# ------
# colors used for sliders
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
TRANS = (1, 1, 1)


# ------
# class Slider
class Slider:

    def change_loc(self, field_size):
        """
        updates sliders coordinates and locations
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        # calculates top left corner
        self.coord_x = field_size * 1.5 + field_size * self.field_coord_x
        self.coord_y = field_size * 1.5 + field_size * self.field_coord_y
        # updates slider surface
        self.surf = pygame.surface.Surface((field_size * 11, field_size * 2))
        # resizes font of name
        self.font = pygame.font.SysFont(None, int(field_size))

    def __init__(self, name, val, maxi, mini, field_pos, field_size):
        """
        :param name: str; name displayed on top of slider
        :param val: float; start value
        :param maxi: float; maximum value at slider position right
        :param mini: float; minimum value at slider position left
        :param field_pos: list[int, int]; sliders top left position as field coordinate
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        self.name = name
        self.val = val
        self.maxi = maxi
        self.mini = mini
        self.field_coord_x = field_pos[0]
        self.field_coord_y = field_pos[1]
        self.coord_x, self.coord_y = 0, 0
        self.change_loc(field_size)
        self.hit = False  # slider is not clicked
        self.active = True  # slider is displayed

    def draw(self, screen, field_size):
        """
        Combination of static and dynamic graphics in a copy of the basic slide surface
        :param screen: Surf; surfacec that covers the whole game window
        :param field_size: float; size of a virtual field
         that is determined by the size of the window that inhabits the GUI
        """
        # Static graphics - slider background, only changed due to window resizing
        self.surf.fill(YELLOW)  # fills slider yellow
        pygame.draw.rect(self.surf, GREY, [0, 0, field_size * 11, field_size * 2], 3)  # outlines slider in grey
        # draws orange rectangle later containing name
        pygame.draw.rect(self.surf, ORANGE, [field_size * 1.5, field_size / 5, field_size * 8, field_size * 0.8], 0)
        # draws white rectangle later containing sliding circle
        pygame.draw.rect(self.surf, WHITE, [field_size * 1.5, field_size * 1.2, field_size * 8, field_size * 0.4], 0)

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((int(field_size * 0.4), int(field_size * 0.4)))
        # makes button surface transparent
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        # displays black oulined orange cicrle as sliding circle
        pygame.draw.circle(self.button_surf, BLACK, (int(field_size * 0.2), int(field_size * 0.2)), 10, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (int(field_size * 0.2), int(field_size * 0.2)), 8, 0)
        # displays circle at the correct location
        center_pos = (self.coord_x + int((self.val-self.mini)/(self.maxi-self.mini) * field_size * 8), field_size * 1.4)
        self.button_rect = self.button_surf.get_rect(center=center_pos)
        self.surf.blit(self.button_surf, self.button_rect)
        # moves the clickable button to the same location
        self.button_rect.move_ip(self.coord_x, self.coord_y)
        # displays name oon top of button
        self.txt_surf = self.font.render(self.name, 1, BLUE)
        self.txt_rect = self.txt_surf.get_rect(center=(field_size * 5.5, field_size * 0.6))
        self.surf.blit(self.txt_surf, self.txt_rect)
        # dispalys all of this on game window
        screen.blit(self.surf, (self.coord_x, self.coord_y))

    def move(self, field_size):
        """
        reacts to movement of the slider button, updates sliders value
        """
        # recalculates value
        self.val = (pygame.mouse.get_pos()[0] - self.coord_x - self.coord_x) / (field_size * 8) *\
                   (self.maxi - self.mini) + self.mini
        # if value is out of range, it is set to boarder
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


# ------
# slider creation
def _get_field_pos():
    """
    generator to pass correct field positions to sliders
    :return: generator; list[int, int], list[int, int]; sliders top left field positions
    """
    number_of_sliders = 2  # music and sfx
    start_coord = [0, 3]  # music slider's field posisiton
    for i in range(number_of_sliders):
        start_coord[1] = 3 * (i + 1)  # calculates field position
        yield start_coord  # yields position


def create_slider(field_size, sound_volume, music_volume):
    """
    creates sliders, currently one to control music's volume and one to control sounds' volumes
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    :param sound_volume: float, 0 - 1, volume the sound i scurrently playing in
    :param music_volume: float; 0 - 1, volume the music is currently playing in
    """
    global slides
    field_positions = _get_field_pos()  # generates field positions for sliders
    field_pos = next(field_positions)  # gets field position for music slider
    # creates music slider
    music = Slider(name="Music", val=music_volume, mini=0.0, maxi=1.0, field_pos=field_pos, field_size=field_size)
    field_pos = next(field_positions)  # gets field position for sound slider
    # creates sound slider
    sfx = Slider(name="SFX", val=sound_volume, mini=0.0, maxi=1.0, field_pos=field_pos, field_size=field_size)
    slides = [music, sfx]  # puts both sliders into global list


# ------
# displaying slider
def draw_slides(screen, field_size):
    """
    displays sliders in the game window
    :param screen: Surface; surface that covers the whole window
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    for slider in slides:  # geos through every slider
        if slider.active:  # slider is displayed
            slider.draw(screen, field_size)  # displays slider


# ------
# updating sliders' values
def refresh_loc_sliders(field_size):
    """
    updates sliders' locations
    :param field_size: float; size of a virtual field that is determined by the size of the window that inhabits the GUI
    """
    for slider in slides:  # goes through every slider
        slider.change_loc(field_size)  # updates its coordinates


def refresh_slides(task_number):
    """
    updates whether sliders are displayed
    :param task_number: int; number of currently ongoing task
    """
    if task_number == 7:  # volume settings are currently dispalyed
        for slider in slides:
            slider.active = True  # sliders are dispalyed
    else:
        for slider in slides:
            slider.active = False  # sliders are not displayed


# ------
# return sliders
def get_sliders():
    """
    :return: list[Slider, Slider]; list containing all sliders
    """
    return slides
