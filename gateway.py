class Gateway:  # блок входа/выхода, куда входит или откуда исходит провод
    def __init__(self, name, i, rect, wire=None):
        self.name = name
        self.index = i
        self.wire = wire
        self.rect = rect

    def change_wire(self, wire=None):
        self.wire = wire
