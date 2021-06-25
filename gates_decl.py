from gate_interface import *


class OR(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] or self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] or self._input_values[1]]
        return super(OR, self).func()


class XOR(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] != self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] != self._input_values[1]]
        return super(XOR, self).func()


class AND(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] and self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] and self._input_values[1]]
        return super(AND, self).func()


class NOT(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 1, 1, *inpvs)
        self._output_values = [not self._input_values[0]]

    def func(self, sel=None):
        self._output_values = [not self._input_values[0]]
        return super(NOT, self).func()


class NOR(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 2, 1, *inpvs)
        self._output_values = [not (self._input_values[0] or self._input_values[1])]

    def func(self, sel=None):
        self._output_values = [not (self._input_values[0] or self._input_values[1])]
        return super(NOR, self).func()


class NAND(GateInterface):
    def __init__(self, coord, filename, name, *inpvs):
        super().__init__(coord, filename, name, 2, 1, *inpvs)
        self._output_values = [not (self._input_values[0] and self._input_values[1])]

    def func(self, sel=None):
        self._output_values = [not (self._input_values[0] and self._input_values[1])]
        return super(NAND, self).func()


class SND(GateInterface):
    def __init__(self, coord, filename, name, value=False):
        assert isinstance(value, bool)
        super().__init__(coord, filename, name, 0, 1)
        self._output_values = [bool(value)]

    def change_image(self):
        if self._output_values[0] == 0:
            self.image = pg.image.load("./gates/SND.png").convert_alpha()
        else:
            self.image = pg.image.load("./gates/SND_ON.png").convert_alpha()

    def __str__(self):
        return "SND"


class RCV(GateInterface):
    def __init__(self, coord, filename, name, value=None):
        assert value is None or isinstance(value, bool)
        super().__init__(coord, filename, name, 1, 0)
        self._input_values = [value]

    def func(self, sel=None):
        return self._input_values

    def change_signal(self, value):
        self._input_values = [value]
        self.change_image()

    def change_image(self):
        if self._input_values[0] == 0:
            self.image = pg.image.load("./gates/RCV.png").convert_alpha()
        else:
            self.image = pg.image.load("./gates/RCV_ON.png").convert_alpha()
