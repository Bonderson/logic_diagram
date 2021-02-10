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
