from math import *
current_gates_number = 0  # counter of gates in use


def bool_portable(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class Gate:
    def __init__(self, gname: str, inum: int, onum: int, selnum=0, *inpvs):
        assert (len(inpvs) == inum or not inpvs), all(bool_portable(x) for x in inpvs)
        global current_gates_number
        self._gate_name = gname
        self._input_number = inum            # number of input channels in the gate
        self._output_number = onum           # number of output channels in the gate
        self._select_lines_number = selnum   # number of selectors in the gate
        if not inpvs:
            self._input_values = [None for _ in range(self._input_number)]  # None is analogue of "X" state
        else:
            self._input_values = [bool(i) for i in inpvs]
        self._select_values = []                                              # todo! does it make any sense?
        self._out_connections_list = [{} for _ in range(self._output_number)]  # list of (_output_number) dicts with
        # connected gate as key and its input channel as value
        self._in_connections_list = [None for _ in range(self._input_number)]  # list of (_input_number) connected
        # Gates, where index is (input channel number - 1)
        self._output_values = [None for _ in range(self._output_number)]
        current_gates_number += 1

    def func(self, sel=None):
        assert None not in self._input_values, "Function error: one input is either disconnected or invalid"
        return self.__return_value(self._output_values)

    def connect(self, other, self_channel_number=None, other_channel_number=None):
        if self_channel_number is None:
            self_channel_number = self._output_number - 1
        else:
            self_channel_number -= 1
        connected = False
        if other_channel_number is None:
            for i in range(len(other._input_values)):
                if other._input_values[i] is None:
                    other._input_values[i] = self.func()[self_channel_number]
                    self._out_connections_list[self_channel_number][other] = i + 1
                    other._in_connections_list[i] = self
                    connected = True
                    break

        else:
            other_channel_number -= 1
            other._input_values[other_channel_number] = self.func()[0]
            self._out_connections_list[self_channel_number][other] = other_channel_number + 1
            other._in_connections_list[other_channel_number] = self
            connected = True

        if not connected:
            raise RuntimeError("Connection failed: all channels are in use and no particular channel was specified")
        # return connected

    def disconnect(self, other):
        assert other in [j for sub in self._out_connections_list for j in sub], \
            "Disconnection error: this gates were not connected"

        # Old version:
        # for channel in range(len(other._in_connections_list)):
        #     if other._in_connections_list[channel] is self:
        #         other._in_connections_list[channel] = None
        #         other._input_values[channel] = None

        # todo! write it more beautiful
        for channel in range(len(self._out_connections_list)):
            for gate in self._out_connections_list[channel]:
                if gate is other:
                    other._in_connections_list[self._out_connections_list[channel][gate] - 1] = None
                    other._input_values[self._out_connections_list[channel][gate] - 1] = None
                    self._out_connections_list[channel] = {}

    def change_signal(self, value):  # doesn't work with DMS
        assert isinstance(value, bool)
        self._output_values = [bool(value)]
        for _ in range(len(self._out_connections_list)):
            if not len(self._out_connections_list[0]):
                return
            connected_gate, num = list(self._out_connections_list[0].keys())[0], \
                                  list(self._out_connections_list[0].values())[0]
            self.disconnect(connected_gate)
            self.connect(connected_gate, None, num)
            connected_gate.change_signal(connected_gate.func()[0])

    def __return_value(self, values):
        assert all(isinstance(x, bool) for x in self._output_values), "Output error: invalid output values"
        for output_channel in range(self._output_number):
            for pair in self._out_connections_list[output_channel]:
                pair._input_values[pair._in_connections_list.index(self)] = values[output_channel]
        return values  # fixme! it should look more beautiful

    def get_info(self):
        ret = f"Gate name is '{self._gate_name}'\n"\
              f"Number of inputs: {self._input_number}, number of outputs: {self._output_number}\n\n"\
              f"This gate is in-connected to:\n"
        for channel in range(len(self._in_connections_list)):
            ret += "\tChannel "+str(channel+1)+": "
            if isinstance(self._in_connections_list[channel], Gate):
                ret += self._in_connections_list[channel].gate_name + "\n"
            else:
                ret += "unconnected\n"
        ret += "This gate out-connects to:\n"
        for channel in range(len(self._out_connections_list)):
            ret += "\tChannel "+str(channel+1)+": "
            for gate in self._out_connections_list[channel]:
                ret += f"\t\t{gate._gate_name} to its in-channel {self._out_connections_list[channel][gate]}\n"
            else:
                ret += "unconnected\n"
        ret += f"\nInput values are: {self._input_values}\n"
        ret += f"Output values now are {self._output_values}\n"
        return ret


class OR(Gate):
    def __init__(self, gname="OR" + str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] or self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] or self._input_values[1]]
        return super(OR, self).func()


class XOR(Gate):
    def __init__(self, gname="XOR"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] != self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] != self._input_values[1]]
        return super(XOR, self).func()


class AND(Gate):
    def __init__(self, gname="AND"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self._output_values = [self._input_values[0] and self._input_values[1]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0] and self._input_values[1]]
        return super(AND, self).func()


class NOT(Gate):
    def __init__(self, gname="NOT"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 1, 1, *inpvs)
        self._output_values = [not self._input_values[0]]

    def func(self, sel=None):
        self._output_values = [not self._input_values[0]]
        return super(NOT, self).func()


class NOR(Gate):
    def __init__(self, gname="NOR"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self._output_values = [not(self._input_values[0] or self._input_values[1])]

    def func(self, sel=None):
        self._output_values = [not(self._input_values[0] or self._input_values[1])]
        return super(NOR, self).func()


class NAND(Gate):
    def __init__(self, gname="NAND"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self._output_values = [not (self._input_values[0] and self._input_values[1])]

    def func(self, sel=None):
        self._output_values = [not (self._input_values[0] and self._input_values[1])]
        return super(NAND, self).func()


class BUF(Gate):
    def __init__(self, gname="BUF"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 1, 1, *inpvs)
        self._output_values = [self._input_values[0]]

    def func(self, sel=None):
        self._output_values = [self._input_values[0]]
        return super(BUF, self).func()


class SND(Gate):
    def __init__(self, value=False, gname="SND" + str(current_gates_number + 1)):
        assert isinstance(value, bool)
        super().__init__(gname, 0, 1)
        self._output_values = [bool(value)]


class RCV(Gate):
    def __init__(self, value=None, gname="RCV" + str(current_gates_number + 1)):
        assert value is None or isinstance(value, bool)
        super().__init__(gname, 1, 0)
        self.input_values = [value]

    def func(self, sel=None):
        return self.input_values[0]


class MUX(Gate):
    def __init__(self, gname="MUX" + str(current_gates_number + 1), inum=2, selnum=0, *inpvs):
        if selnum == 0:
            selnum = ceil(log2(inum))
        super().__init__(gname, inum, 1, selnum, *inpvs)
        self.select_values = [0 for _ in range(0, selnum)]  # fixme! Does it make any sense?
        self._output_values = [None]

    def func(self, sel=None):
        if sel is None:
            self._output_values = [None]
        else:
            assert isinstance(sel, list), "MUX process failed: Selection signal is invalid"
            assert len(sel) == self._select_lines_number, "MUX process failed: Selection signal is invalid"
            sel = int(''.join([str(int(i)) for i in sel]), 2)
            self._output_values = [self._input_values[sel]]
        return super(MUX, self).func()


class DMS(Gate):  # Decoder
    def __init__(self, gname="DMS" + str(current_gates_number + 1), inum=2, selnum=0, *inpvs):
        onum = 2 ** inum
        super().__init__(gname, inum, onum, selnum, *inpvs)
        self._output_values = [None for _ in range(self._output_number)]

    def func(self, sel=None):
        assert all(isinstance(x, bool) for x in self._input_values), "DMS Process failed: wrong input"
        sel = int(''.join([str(int(i)) for i in self._input_values]), 2)
        self._output_values = [False if i != sel else True for i in range(self._output_number)]
        return super(DMS, self).func()
