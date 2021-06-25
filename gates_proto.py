current_gates_number = 0  # counter of gates in use (вентили в правой части экрана тоже учитываются при подсчёте)


class Gate:
    @staticmethod
    def bool_portable(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __init__(self, gname: str, inum: int, onum: int, selnum=0, *inpvs):
        assert (len(inpvs) == inum or not inpvs), all(self.bool_portable(x) for x in inpvs)
        global current_gates_number
        self.name = gname
        self._input_number = inum  # number of input channels in the gate
        self.input_number = lambda: self._input_number
        self._output_number = onum  # number of output channels in the gate
        self.output_number = lambda: self._output_number
        self._select_lines_number = selnum  # number of selectors in the gate
        self.select_lines_number = lambda: self._select_lines_number
        if not inpvs:
            self._input_values = [None for _ in range(self.input_number())]  # None is analogue of "X" state
        else:
            self._input_values = [bool(i) for i in inpvs]
        self.input_values = lambda: self._input_values
        self._select_values = []
        self.select_values = lambda: self._select_values
        self._out_connections_list = [{} for _ in range(self.output_number())]  # list of (_output_number) dicts with
        self.out_connections_list = lambda: self._out_connections_list
        # connected gate as key and its input channel as value
        self._in_connections_list = [None for _ in range(self.input_number())]  # list of (_input_number) connected
        self.in_connections_list = lambda: self._in_connections_list
        # Gates, where index is (input channel number - 1)
        self._output_values = [None for _ in range(self.output_number())]
        self.output_values = lambda: self._output_values
        current_gates_number += 1

    def func(self, sel=None):
        assert None not in self._input_values, "Function error: one input is either disconnected or invalid"
        return self._return_value(self._output_values)

    def connect(self, other, self_channel_number=None, other_channel_number=None):
        if self_channel_number is None:
            self_channel_number = self._output_number - 1
        else:
            self_channel_number -= 1
        connected = False
        if other_channel_number is None:
            for i in range(len(other.input_values())):
                if other.input_values()[i] is None:
                    other.input_values()[i] = self.func()[self_channel_number]
                    self.out_connections_list()[self_channel_number][other] = i + 1
                    other.in_connections_list()[i] = self
                    connected = True
                    break

        else:
            other_channel_number -= 1
            other.input_values()[other_channel_number] = self.func()[0]
            self._out_connections_list[self_channel_number][other] = other_channel_number + 1
            other.in_connections_list()[other_channel_number] = self
            connected = True

        if not connected:
            raise RuntimeError("Connection failed: all channels are in use and no particular channel was specified")
        # return connected

    def disconnect(self, other):
        assert other in [j for sub in self._out_connections_list for j in sub], \
            "Disconnection error: this gates were not connected"

        for channel in range(len(self._out_connections_list)):
            for gate in self._out_connections_list[channel]:
                if gate is other:
                    other.in_connections_list()[self._out_connections_list[channel][gate] - 1] = None
                    other.input_values()[self._out_connections_list[channel][gate] - 1] = None
                    self._out_connections_list[channel] = {}

    def change_signal(self, value=None):  # doesn't work with DMS
        if value is None:
            value = bool(abs(self._output_values[0] - 1))
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

    def _return_value(self, values):
        assert all(isinstance(x, bool) for x in self._output_values), "Output error: invalid output values"
        for output_channel in range(self._output_number):
            for pair in self._out_connections_list[output_channel]:
                pair.input_values()[pair.in_connections_list().index(self)] = values[output_channel]
        return values

    def get_info(self):
        ret = f"Gate name is '{self.name}'\n" \
              f"Number of inputs: {self._input_number}, number of outputs: {self._output_number}\n\n" \
              f"This gate is in-connected to:\n"
        for channel in range(len(self._in_connections_list)):
            ret += "\tChannel " + str(channel + 1) + ": "
            if isinstance(self._in_connections_list[channel], Gate):
                ret += self._in_connections_list[channel].name + "\n"
            else:
                ret += "unconnected\n"
        ret += "This gate out-connects to:\n"
        for channel in range(len(self._out_connections_list)):
            ret += "\tChannel " + str(channel + 1) + ": "
            for gate in self._out_connections_list[channel]:
                ret += f"\t\t{gate.name} to its in-channel {self._out_connections_list[channel][gate]}\n"
            else:
                ret += "unconnected\n"
        ret += f"\nInput values are: {self._input_values}\n"
        ret += f"Output values now are {self._output_values}\n"
        return ret
