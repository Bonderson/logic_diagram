class Wire:
    def __init__(self, name, inp, outp):
        self.name = name
        self.input = inp
        self.output = outp
        self.state = 0
        self.color = [0, 0, 0]

    def __str__(self):
        return "wire"

    def change_input(self, inp=None):
        self.input = inp

    def change_output(self, outp=None):
        self.output = outp

    def change_state(self):
        self.state = abs(self.state - 1)
        self.color[1] = 255 * self.state
        self.color[2] = 255 * self.state

    def del_self(self):
        try:
            self.input.change_wire()
        except:
            pass
        try:
            self.output.change_wire()
        except:
            pass
