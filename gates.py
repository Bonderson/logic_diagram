num = 0


class Gate:
    def __init__(self, gname: str, inum: int, onum: int):
        global num
        self.gate_name = gname
        self.input_number = inum
        self.output_number = onum
        num += 1

    def func(self, *args: bool):
        pass


class OR(Gate):
    def __init__(self, gname="OR"+str(num+1)):
        self.gate_name = gname
        self.input_number = 2
        self.output_number = 1
        num += 1

    def func(self, i1: bool, i2: bool):
        return i1 or i2


class XOR(Gate):
    def __init__(self, gname="XOR"+str(num+1)):
        self.gate_name = gname
        self.input_number = 2
        self.output_number = 1
        num += 1

    def func(self, i1: bool, i2: bool):
        return i1 != i2


class AND(Gate):
    def __init__(self, gname="AND"+str(num+1)):
        self.gate_name = gname
        self.input_number = 2
        self.output_number = 1
        num += 1

    def func(self, i1: bool, i2: bool):
        return i1 and i2


class NOT(Gate):
    def __init__(self, gname="NOT"+str(num+1)):
        self.gate_name = gname
        self.input_number = 1
        self.output_number = 1
        num += 1

    def func(self, i1: bool):
        return not i1


class NOR(Gate):
    def __init__(self, gname="NOR"+str(num+1)):
        self.gate_name = gname
        self.input_number = 2
        self.output_number = 1
        num += 1

    def func(self, i1: bool, i2: bool):
        return not(i1 or i2)


class NAND(Gate):
    def __init__(self, gname="NAND"+str(num+1)):
        self.gate_name = gname
        self.input_number = 2
        self.output_number = 1
        num += 1

    def func(self, i1: bool, i2: bool):
        return not(i1 and i2)


class BUF(Gate):
    def __init__(self, gname="BUF"+str(num+1)):
        self.gate_name = gname
        self.input_number = 1
        self.output_number = 1
        num += 1

    def func(self, i1: bool):
        return i1
