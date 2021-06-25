import time
from UI import *
from gates_decl import *
count_of_wires = 0


class GatesList:
    def __init__(self, width, height):
        self.thrown_element = None  # элемент, который будет создан в lscreen
        self.time_name = [0, -1]  # для двойного клика
        self.surface = pg.surface.Surface((width, height))
        self.rect = self.surface.get_rect(center=(width * 3 + width // 2, height // 2))
        self.surface.fill((255, 255, 255))
        self.gates_pool = list([AND((0, 0), "./gates/AND.png", "AND"),
                                NAND((0, 0), "./gates/NAND.png", "NAND"),
                                OR((0, 0), "./gates/OR.png", "OR"),
                                NOR((0, 0), "./gates/NOR.png", "NOR"),
                                XOR((0, 0), "./gates/XOR.png", "XOR"),
                                NOT((0, 0), "./gates/NOT.png", "NOT"),
                                SND((0, 0), "./gates/SND.png", "SND"),
                                RCV((0, 0), "./gates/RCV.png", "RCV")])
        self.font = pg.font.SysFont(None, 20)
        self.gates_names = [self.font.render(element.name, True, (0, 0, 0)) for element in self.gates_pool]
        sum_heights = 5
        for element in self.gates_pool:  # располагаем объекты друг под другом
            element.rect.inflate_ip(0, 15)
            element.rect.move_ip(width // 2, element.rect.height * 0.5 + sum_heights + 5)
            sum_heights += element.rect.height + 10
        self.redraw()

    def redraw(self):
        self.surface.fill((255, 255, 255))
        for element, name in zip(self.gates_pool, self.gates_names):
            self.surface.blit(element.image, element.rect)
            self.surface.blit(name, name.get_rect(center=(element.rect.center[0],
                                                          element.rect.center[1] + element.rect.height * 0.5 - 5)))

    def click_lmouse(self, coord):
        self.redraw()
        coord = [self.rect.width // 2, coord[1]]
        self.thrown_element = None
        for element in self.gates_pool:
            if element.rect.collidepoint((coord[0], coord[1])):
                if abs(self.time_name[0] - time.time()) < 0.5 and self.time_name[1] == element.name:
                    self.thrown_element = element
                    break
                else:
                    self.time_name[0] = time.time()
                    self.time_name[1] = element.name
                    color_rect = pg.Rect(0, element.rect.top, self.rect.width, element.rect.height)
                    color_surface = pg.surface.Surface((color_rect.width, color_rect.height))
                    color_surface.fill((200, 200, 200))
                    color_surface.set_alpha(128)
                    self.surface.blit(color_surface, color_rect)
                    break
