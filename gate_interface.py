from gateway import *
import pygame as pg
from gates_proto import *


class GateInterface(Gate):  # оболочка для вентилей, с помощью которой можно взаимодействовать с ними
    def __init__(self, coord, filename, name, inum, onum, selnum=0, *inpvs):
        super().__init__(name, inum, onum, selnum, *inpvs)

        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(coord[0], coord[1]))
        self.offsets = [0, 0]  # координаты курсора относительно центра объекта при клике на него
        # область взаимодействия со входами
        self.left_rect = pg.Rect(self.rect.left, self.rect.top, 20, self.rect.height)
        self.right_rect = pg.Rect(self.rect.right - 20, self.rect.top, 20, self.rect.height)  # - с выходами
        # - с селективными входами
        self.bottom_rect = pg.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        self.old_coord = self.rect.center

        self.input_pool = list()  # хранит входы вентиля
        for i in range(inum):  # располагаем область взаимодействия каждого входа
            rect = pg.Rect(self.left_rect.left, self.left_rect.top, self.left_rect.width, self.left_rect.height // inum)
            rect.move_ip(0, i * self.left_rect.height // inum)
            self.input_pool.append(Gateway(self.name, i, rect))

        self.output_pool = list()  # хранит выходы вентиля
        for i in range(onum):  # ...
            rect = pg.Rect(self.right_rect.left, self.right_rect.top,
                           self.right_rect.width, self.right_rect.height // onum)
            rect.move_ip(0, i * self.right_rect.height // onum)
            self.output_pool.append(Gateway(self.name, i, rect))

        self.selector_pool = list()  # хранит входы мультиплексора/декодера
        for i in range(selnum):  # ...
            rect = pg.Rect(self.bottom_rect.left, self.bottom_rect.top,
                           self.bottom_rect.width // selnum, self.bottom_rect.height)
            rect.move_ip(i * self.bottom_rect.width // selnum, 0)
            self.selector_pool.append(Gateway(self.name, i, rect))

    def update_offsets(self, coord):
        self.offsets = [self.rect.center[0] - coord[0], self.rect.center[1] - coord[1]]

    def move(self, coord):  # перемещаем область объекта и области входов
        self.rect.move_ip(coord[0] + self.offsets[0] - self.rect.center[0],
                          coord[1] + self.offsets[1] - self.rect.center[1])

        self.left_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        self.right_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        self.bottom_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        for element in [*self.input_pool, *self.output_pool, *self.selector_pool]:
            element.rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])

        self.old_coord = self.rect.center

    def where_to_click(self, coord):  # определяем в какую область объекта попал курсор
        if self.left_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.input_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "input", gateway
        elif self.right_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.output_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "output", gateway
        elif self.bottom_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.selector_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "input", gateway
        return self.name, None

    def return_all_gateways(self):
        return [*self.input_pool, *self.output_pool, *self.selector_pool]

    def del_self(self):
        for gateway in self.return_all_gateways():
            try:
                gateway.wire.del_self()
            except:
                pass
