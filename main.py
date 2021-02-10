from gates import *


# just testing, nothing useful here
or1 = OR("test")
in1 = bool(int(input()))
in2 = False
in3 = True

snd1 = SND(in1)
snd2 = SND(in2)
snd3 = SND(in3)

snd1.connect(or1)
snd2.connect(or1)
print(or1.in_connections_list)
print(or1.func())

snd3.connect(or1)
print(or1.in_connections_list)
print(or1.func())

snd3.connect(or1, other_channel_number=1)
print(or1.in_connections_list)
print(or1.func())


##########################################
# Trying to assemble first simple scheme #
##########################################
a = SND(True)
b = SND(False)
c = SND(True)
d = SND(False)
or1 = OR("or1")
a.connect(or1)
b.connect(or1)
not1 = NOT("not1")
or1.connect(not1)
not2 = NOT("not2")
c.connect(not2)
nand1 = NAND("nand1")
not1.connect(nand1)
not2.connect(nand1)
xor1 = XOR("xor1")
nand1.connect(xor1)
d.connect(xor1)
print(xor1.func())
