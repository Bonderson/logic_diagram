current_gates_number = 0


class Gate:
    def __init__(self, gname: str, inum: int, onum: int, *inpvs):
        global current_gates_number
        assert (len(inpvs) == inum or not inpvs), all(isinstance(x, bool) for x in inpvs)
        self.gate_name = gname
        self.input_number = inum
        self.output_number = onum
        if not inpvs:
            self.input_values = [None for _ in range(self.input_number)]  # None is analogue of "X" state
        else:
            self.input_values = [bool(i) for i in inpvs]
        current_gates_number += 1
        self.out_connections_list = [{} for _ in range(self.output_number)]
        self.in_connections_list = [None for _ in range(self.input_number)]
        self.output_value = None

    def func(self):
        assert None not in self.input_values, "Function error: one input is either disconnected or invalid"
        return self.return_value(self.output_value)

    def connect(self, other, self_channel_number=None, other_channel_number=None):
        if self_channel_number is None:
            self_channel_number = self.output_number-1
        else:
            self_channel_number -= 1
        connected = False
        if other_channel_number is None:
            for i in range(len(other.input_values)):
                if other.input_values[i] is None:
                    other.input_values[i] = self.func()
                    self.out_connections_list[self_channel_number][other] = i + 1
                    other.in_connections_list[i] = self
                    connected = True
                    break

        else:
            other_channel_number -= 1
            other.input_values[other_channel_number] = self.func()
            self.out_connections_list[self_channel_number][other] = other_channel_number + 1
            other.in_connections_list[other_channel_number] = self
            connected = True

        if not connected:
            raise RuntimeError("Connection failed: both channels are in use and no particular channel was specified")
        # return connected

    def disconnect(self, other):
        assert other in [j for sub in self.out_connections_list for j in sub], \
            "Disconnection error: this gates were not connected"

        # Old version:
        # for channel in range(len(other.in_connections_list)):
        #     if other.in_connections_list[channel] is self:
        #         other.in_connections_list[channel] = None
        #         other.input_values[channel] = None

        # todo! write it more beautiful
        for channel in range(len(self.out_connections_list)):
            for gate in self.out_connections_list[channel]:
                if gate is other:
                    other.in_connections_list[self.out_connections_list[channel][gate]-1] = None
                    other.input_values[self.out_connections_list[channel][gate]-1] = None
                    self.out_connections_list[channel] = {}

    def return_value(self, value, output_channel=None):
        assert type(self.output_value) is bool, \
            "Output error: invalid output value"
        if output_channel is None:
            output_channel = self.output_number-1
        else:
            output_channel -= 1
        for pair in self.out_connections_list[output_channel]:
            pair.input_values[pair.in_connections_list.index(self)] = value
        return value

    def get_info(self):
        ret = f"Gate name is '{self.gate_name}'\n"\
              f"Number of inputs: {self.input_number}, number of outputs: {self.output_number}\n\n"\
              f"This gate is in-connected to:\n"
        for channel in range(len(self.in_connections_list)):
            ret += "\tChannel "+str(channel+1)+": "
            if type(self.in_connections_list[channel]) == Gate:
                ret += self.in_connections_list[channel].gate_name + "\n"
            else:
                ret += "unconnected\n"
        ret += "This gate out-connects to:\n"
        for channel in range(len(self.out_connections_list)):
            ret += "\tChannel "+str(channel+1)+": \n"
            for gate in self.out_connections_list[channel]:
                ret += f"\t\t{gate.gate_name} to its in-channel {self.out_connections_list[channel][gate]}\n"
            else:
                ret += "unconnected\n"
        ret += f"\nInput values are: {self.input_values}"
        ret += f"Output value now is {self.output_value}\n"
        return ret


class OR(Gate):
    def __init__(self, gname="OR" + str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self.output_value = self.input_values[0] or self.input_values[1]

    def func(self):
        self.output_value = self.input_values[0] or self.input_values[1]
        return super(OR, self).func()


class XOR(Gate):
    def __init__(self, gname="XOR"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self.output_value = self.input_values[0] != self.input_values[1]

    def func(self):
        self.output_value = self.input_values[0] != self.input_values[1]
        return super(XOR, self).func()


class AND(Gate):
    def __init__(self, gname="AND"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self.output_value = self.input_values[0] and self.input_values[1]

    def func(self):
        self.output_value = self.input_values[0] and self.input_values[1]
        return super(AND, self).func()


class NOT(Gate):
    def __init__(self, gname="NOT"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 1, 1, *inpvs)
        self.output_value = not self.input_values[0]

    def func(self):
        self.output_value = not self.input_values[0]
        return super(NOT, self).func()


class NOR(Gate):
    def __init__(self, gname="NOR"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self.output_value = not(self.input_values[0] or self.input_values[1])

    def func(self):
        self.output_value = not(self.input_values[0] or self.input_values[1])
        return super(NOR, self).func()


class NAND(Gate):
    def __init__(self, gname="NAND"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 2, 1, *inpvs)
        self.output_value = not (self.input_values[0] and self.input_values[1])

    def func(self):
        self.output_value = not (self.input_values[0] and self.input_values[1])
        return super(NAND, self).func()


class BUF(Gate):
    def __init__(self, gname="BUF"+str(current_gates_number + 1), *inpvs):
        super().__init__(gname, 1, 1, *inpvs)
        self.output_value = self.input_values[0]

    def func(self):
        self.output_value = self.input_values[0]
        return super(BUF, self).func()


class SND(Gate):
    def __init__(self, value=False, gname="SND" + str(current_gates_number + 1)):
        assert isinstance(value, bool)
        super().__init__(gname, 0, 1)
        self.output_value = bool(value)


class RCV(Gate):
    def __init__(self, value=None, gname="RCV" + str(current_gates_number + 1)):
        assert value is None or isinstance(value, bool)
        super().__init__(gname, 1, 0)
        self.input_values = [value]

    def func(self):
        return self.input_values[0]
