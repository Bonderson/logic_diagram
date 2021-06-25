from field import *


class Interaction:
    def __init__(self, lscreen, rscreen):
        self.lscreen = lscreen
        self.rscreen = rscreen

    def create_object_in_lscreen(self):
        if self.rscreen.thrown_element is not None:
            self.lscreen.create_object(self.rscreen.thrown_element)


class Display:
    def __init__(self, width, height):
        self.m_screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Logic_scheme")
        self.l_screen = Field(width - width // 4, height)
        self.r_screen = GatesList(width // 4, height)
        self.interaction_space = Interaction(self.l_screen, self.r_screen)
        self.mini_rect = pg.Rect(width - width // 4 - 2, 0, 4, height)  # полоса разделяющая две части экрана
        self.redraw()

    def redraw(self):
        self.m_screen.fill((0, 0, 0))
        self.m_screen.blit(*self.l_screen.scale())
        self.m_screen.blit(self.r_screen.surface, self.r_screen.rect)
        pg.draw.rect(self.m_screen, [0, 0, 0], self.mini_rect)
