import pygame
from writing import Writing

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
LIGHTGREY = (100, 100, 100)
ORANGE = (200, 100, 50)
TRANS = (1, 1, 1)


class Slider:
    def change_loc(self, field_size):
        self.coord_x = field_size * 1.5 + field_size * self.field_coord_x
        self.coord_y = field_size * 1.5 + field_size * self.field_coord_y
        self.surf = pygame.surface.Surface((field_size * 11, field_size * 2))
        self.font = pygame.font.SysFont(None, int(field_size))

    def __init__(self, name, val, maxi, mini, field_pos, field_size):
        self.name = name
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.field_coord_x = field_pos[0]  # x-location on screen
        self.field_coord_y = field_pos[1]
        self.coord_x, self.coord_y = 0, 0
        self.change_loc(field_size)
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.active = True

    def draw(self, screen, field_size):
        """
        Combination of static and dynamic graphics in a copy of the basic slide surface
        """
        # Static graphics - slider background #
        self.surf.fill(YELLOW)
        pygame.draw.rect(self.surf, GREY, [0, 0, field_size * 11, field_size * 2], 3)
        pygame.draw.rect(self.surf, ORANGE, [field_size * 1.5, field_size / 5, field_size * 8, field_size * 0.8], 0)
        pygame.draw.rect(self.surf, WHITE, [field_size * 1.5, field_size * 1.2, field_size * 8, field_size * 0.4], 0)

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((int(field_size * 0.4), int(field_size * 0.4)))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (int(field_size * 0.2), int(field_size * 0.2)), 10, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (int(field_size * 0.2), int(field_size * 0.2)), 8, 0)
        # dynamic
        center_pos = (self.coord_x + int((self.val-self.mini)/(self.maxi-self.mini) * field_size * 8), field_size * 1.4)
        self.button_rect = self.button_surf.get_rect(center=center_pos)
        self.surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.coord_x, self.coord_y)  # move of button box to correct screen position
        self.txt_surf = self.font.render(self.name, 1, BLUE)
        self.txt_rect = self.txt_surf.get_rect(center=(field_size * 5.5, field_size * 0.6))
        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes
        # screen
        screen.blit(self.surf, (self.coord_x, self.coord_y))

    def move(self, field_size):
        """
        The dynamic part; reacts to movement of the slider button.
        """
        self.val = (pygame.mouse.get_pos()[0] - self.coord_x - self.coord_x) / (field_size * 8) *\
                   (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


def _get_field_pos():
    number_of_sliders = 2
    start_cord = [0, 3]
    for i in range(number_of_sliders):
        start_cord[1] = 3 * (i + 1)
        yield start_cord


def create_slider(field_size, sound_volume, music_volume):
    global slides
    field_positions = _get_field_pos()
    field_pos = next(field_positions)
    music = Slider("Music", music_volume, 1.0, 0.0, field_pos, field_size)
    field_pos = next(field_positions)
    sfx = Slider("SFX", sound_volume, 1.0, 0.0, field_pos, field_size)
    slides = [music, sfx]


def draw_slides(screen, field_size):
    for slider in slides:
        if slider.active:
            slider.draw(screen, field_size)


def refresh_loc_sliders(field_size):
    for slider in slides:
        slider.change_loc(field_size)


def refresh_slides(task_number):
    if task_number == 7:
        for slider in slides:
            slider.active = True
    else:
        for slider in slides:
            slider.active = False


def get_sliders():
    return slides
