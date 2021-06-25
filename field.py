import time
from gates_list import *
from wire import *


class Field:
    def __init__(self, width, height):
        self.scale_val = 100
        self.scale_speed = 10
        self.scale_edges = [50, 150]  # speed должен быть кратен разности val и edges[0] для адекватной работы
        k = (self.scale_val - self.scale_edges[0]) / self.scale_speed  # коэффициент масштабирования полотна
        self.surface = pg.surface.Surface((width // k * k * 2, height // k * k * 2))
        self.surface.fill((255, 255, 255))
        self.pool_objects = [list(), list()]  # 0 - вентили, 1 - провода
        self.rect = self.surface.get_rect(center=(width // k * k // 2, height // k * k // 2))
        # хранит время последнего клика правой кнопки мыши и имя объекта(нужно для двойного клика)
        self.time_name = [0, -1]
        self.moveobj = None  # хранит передвигаемый объект
        self.old_coord = [0, 0]
        self.generic_SNDs_list = dict()  # лист фиктивных входов, на которые подаётся 0

    def redraw(self):
        self.update_wire_states()
        self.surface.fill((255, 255, 255))
        for element in self.pool_objects[0]:
            self.surface.blit(element.image, element.rect)

        for element in self.pool_objects[1]:
            try:
                self.draw_wire(element.input.rect.center, element.output.rect.center, element.color)
            except:
                pass

    def update_wire_states(self):
        for gate in self.pool_objects[0]:
            for gateway in gate.output_pool:
                if gateway.wire is not None:
                    if gateway.wire.state != gate.output_values()[gateway.index]:
                        gateway.wire.change_state()

    def draw_wire(self, inp, outp, color):
        pg.draw.line(self.surface, color, inp, [outp[0] // 2 + inp[0] // 2, inp[1]], 1)
        pg.draw.line(self.surface, color, [outp[0] // 2 + inp[0] // 2, inp[1]], [outp[0] // 2 + inp[0] // 2, outp[1]],
                     1)
        pg.draw.line(self.surface, color, [outp[0] // 2 + inp[0] // 2, outp[1]], outp, 1)

    def scale_const(self, k):
        new_scale = self.scale_val + self.scale_speed * k
        if self.scale_edges[0] <= new_scale <= self.scale_edges[1] and self.moveobj is None:
            self.scale_val = new_scale
            self.moveobj = self.rect
            self.old_coord = list(self.rect.center)
            self.move_obj(self.rect.center)
            self.moveobj = None

    def scale(self):
        sc_surf = pg.transform.smoothscale(self.surface,
                                           (self.rect.width * self.scale_val // 100,
                                            self.rect.height * self.scale_val // 100))
        sc_rect = sc_surf.get_rect(center=self.rect.center)
        return sc_surf, sc_rect

    def transform_c(self, x, y):  # преобразование координат из системы дисплея в систему поверхности класса Field с
        # учётом масштаба
        n_x = self.rect.left + (x - self.rect.center[0]) * 100 // self.scale_val + self.rect.width // 2
        n_y = self.rect.top + (y - self.rect.center[1]) * 100 // self.scale_val + self.rect.height // 2
        return n_x, n_y

    def move_obj(self, coord):
        coord = self.transform_c(*coord)
        if self.moveobj.__str__() == "wire":
            self.redraw()
            if self.moveobj.output is None:
                self.draw_wire(self.moveobj.input.rect.center,
                               (coord[0] - self.rect.left, coord[1] - self.rect.top), [0, 0, 0])
            else:
                self.draw_wire(self.moveobj.output.rect.center,
                               (coord[0] - self.rect.left, coord[1] - self.rect.top), [0, 0, 0])

        elif self.moveobj == self.rect:
            self.rect.move_ip(coord[0] - self.old_coord[0],
                              coord[1] - self.old_coord[1])
            # не даём вентилю выйти за пределы l_screen
            if self.rect.center[0] - self.rect.width * self.scale_val // 100 // 2 > 0:
                self.rect.move_ip(-(self.rect.center[0] - self.rect.width * self.scale_val // 100 // 2), 0)
            elif self.rect.center[0] + self.rect.width * self.scale_val // 100 // 2 < self.rect.width // 2:
                self.rect.move_ip(self.rect.width // 2 -
                                  (self.rect.center[0] + self.rect.width * self.scale_val // 100 // 2), 0)
            if self.rect.center[1] + self.rect.height * self.scale_val // 100 // 2 < self.rect.height // 2:
                self.rect.move_ip(0, self.rect.height // 2 -
                                  (self.rect.center[1] + self.rect.height * self.scale_val // 100 // 2))
            elif self.rect.center[1] - self.rect.height * self.scale_val // 100 // 2 > 0:
                self.rect.move_ip(0, -(self.rect.center[1] - self.rect.height * self.scale_val // 100 // 2))
            self.old_coord = coord
            self.redraw()
        else:  # двигаем поверхность Field
            if coord[0] - self.rect.left <= self.rect.width:
                self.moveobj.move((coord[0] - self.rect.left, coord[1] - self.rect.top))
            else:  # не даем выйти поверхности за пределы
                self.moveobj.move((self.rect.width - 10, coord[1] - self.rect.top))
            self.redraw()

    def click_lmouse(self, coord):
        coord = self.transform_c(*coord)
        for element in self.pool_objects[0][::-1]:
            if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                if part == "input" or part == "output":
                    if gateway.wire is None:
                        global count_of_wires
                        if part == "input":
                            gateway.change_wire(Wire(f"wire{count_of_wires}", None, gateway))
                        else:
                            gateway.change_wire(Wire(f"wire{count_of_wires}", gateway, None))
                            count_of_wires += 1
                        self.moveobj = gateway.wire
                        self.draw_wire(gateway.rect.center,
                                       (coord[0] - self.rect.left, coord[1] - self.rect.top), [0, 0, 0])
                    else:
                        self.moveobj = gateway.wire
                        if part == "input":
                            for el in self.pool_objects[0][::-1]:
                                if el.name == self.moveobj.input.name:
                                    el.disconnect(element)
                                    name_snd = element.name + "." + str(gateway.index)
                                    self.generic_SNDs_list[name_snd] = SND((0, 0), "./gates/SND.png", "")
                                    self.generic_SNDs_list[name_snd].connect(element, 1, gateway.index + 1)
                                    break
                            self.moveobj.change_output()
                            self.redraw()
                            self.draw_wire(self.moveobj.input.rect.center,
                                           (coord[0] - self.rect.left, coord[1] - self.rect.top), [0, 0, 0])
                        else:
                            for el in self.pool_objects[0][::-1]:
                                if el.name == self.moveobj.output.name:
                                    element.disconnect(el)
                                    name_snd = el.name + "." + str(self.moveobj.output.index)
                                    self.generic_SNDs_list[name_snd] = SND((0, 0), "./gates/SND.png", "")
                                    self.generic_SNDs_list[name_snd].connect(el, 1, self.moveobj.output.index + 1)
                                    break
                            self.moveobj.change_input()
                            self.redraw()
                            self.draw_wire((coord[0] - self.rect.left, coord[1] - self.rect.top),
                                           self.moveobj.output.rect.center, [0, 0, 0])
                        gateway.change_wire()
                        self.pool_objects[1].remove(self.moveobj)
                    break

                else:
                    if element.__str__() == "SND":
                        self.time_name[0] = time.time()
                    self.moveobj = element
                    self.moveobj.update_offsets((coord[0] - self.rect.left, coord[1] - self.rect.top))
                    self.pool_objects[0].remove(element)
                    self.pool_objects[0].append(element)
                    self.redraw()
                    break
        if self.moveobj is None:
            self.moveobj = self.rect
            self.old_coord = [coord[0], coord[1]]

    def lbutton_up(self, coord):  # прекращаем перемещение объекта
        coord = self.transform_c(*coord)
        if self.moveobj.__str__() == "wire":
            for element in self.pool_objects[0][::-1]:
                if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                    part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                    which_connect = self.moveobj.output or self.moveobj.input
                    if (part == "input" or part == "output") and gateway.wire is None:
                        if part == "input" and self.moveobj.output is None \
                                and gateway.name != self.moveobj.input.name:
                            self.moveobj.change_output(gateway)
                            gateway.change_wire(self.moveobj)
                            self.pool_objects[1].append(gateway.wire)
                            for el in self.pool_objects[0][::-1]:
                                if el.name == which_connect.name:
                                    name_snd = element.name + "." + str(gateway.index)
                                    self.generic_SNDs_list[name_snd].disconnect(element)
                                    self.generic_SNDs_list.pop(name_snd)
                                    el.connect(element, self.moveobj.input.index + 1, gateway.index + 1)
                                    break
                        elif part == "output" and self.moveobj.input is None \
                                and gateway.name != self.moveobj.output.name:
                            self.moveobj.change_input(gateway)
                            gateway.change_wire(self.moveobj)
                            self.pool_objects[1].append(gateway.wire)
                            for el in self.pool_objects[0][::-1]:
                                if el.name == which_connect.name:
                                    name_snd = el.name + "." + str(self.moveobj.output.index)
                                    self.generic_SNDs_list[name_snd].disconnect(el)
                                    self.generic_SNDs_list.pop(name_snd)
                                    element.connect(el, gateway.index + 1, self.moveobj.output.index + 1)
                                    break
                        break
            if self.moveobj.output is None or self.moveobj.input is None:
                self.moveobj.del_self()
            self.redraw()
        if self.moveobj.__str__() == "SND":
            if time.time() - self.time_name[0] < 0.1:
                self.moveobj.change_signal()
                self.moveobj.change_image()
                self.redraw()
        self.time_name[0] = 0
        self.moveobj = None

    def click_rmouse(self, coord):
        self.del_object(coord)

    def create_object(self, obj):
        coord = self.transform_c(self.rect.width // 4, self.rect.height // 4)
        self.pool_objects[0].append(obj.__class__((coord[0] - self.rect.left, coord[1] - self.rect.top),
                                                  "./gates/" + obj.name + ".png", obj.name + str(current_gates_number)))
        for i in range(self.pool_objects[0][-1].input_number()):
            name_snd = self.pool_objects[0][-1].name + "." + str(i)
            self.generic_SNDs_list[name_snd] = SND((0, 0), "./gates/SND.png", "")
            self.generic_SNDs_list[name_snd].connect(self.pool_objects[0][-1], 1, i + 1)

        self.surface.blit(self.pool_objects[0][-1].image, self.pool_objects[0][-1].rect)

    def del_object(self, coord):
        coord = self.transform_c(*coord)
        for element in self.pool_objects[0][::-1]:
            if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                if part == "input" or part == "output":
                    if gateway.wire is not None:
                        element = gateway.wire
                if abs(self.time_name[0] - time.time()) < 0.5 and self.time_name[1] == element.name:
                    if element.__str__() == "wire":
                        gate1 = None
                        gate2 = None
                        i = 0
                        while gate1 is None or gate2 is None:
                            if self.pool_objects[0][i].name == element.input.name:
                                gate1 = self.pool_objects[0][i]
                            elif self.pool_objects[0][i].name == element.output.name:
                                gate2 = self.pool_objects[0][i]
                            i += 1
                        gate1.disconnect(gate2)
                        name_snd = gate2.name + "." + str(element.output.index)
                        self.generic_SNDs_list[name_snd] = SND((0, 0), "./gates/SND.png", "")
                        self.generic_SNDs_list[name_snd].connect(gate2, 1, element.output.index + 1)
                        element.del_self()
                        self.pool_objects[1].remove(element)
                    else:
                        for i in range(element.input_number()):
                            for gate in self.pool_objects[0]:
                                if element.input_pool[i].wire and gate.name == element.input_pool[i].wire.input.name:
                                    gate.disconnect(element)
                                    break

                        for i in range(element.output_number()):
                            for gate in self.pool_objects[0]:
                                if element.output_pool[i].wire and gate.name == element.output_pool[i].wire.output.name:
                                    element.disconnect(gate)
                                    name_snd = str(gate.name) + "." + str(element.output_pool[i].wire.output.index)
                                    self.generic_SNDs_list[name_snd] = SND((0, 0), "./gates/SND.png", "")
                                    self.generic_SNDs_list[name_snd].connect(gate, 1,
                                                                             element.output_pool[
                                                                                 i].wire.output.index + 1)

                        for gateway in element.return_all_gateways():
                            try:
                                self.pool_objects[1].remove(gateway.wire)
                            except:
                                pass
                        element.del_self()
                        self.pool_objects[0].remove(element)
                    self.time_name[0] = 0
                    self.redraw()
                    break
                else:
                    self.time_name[0] = time.time()
                    self.time_name[1] = element.name
                    break
