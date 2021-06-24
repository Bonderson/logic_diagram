from gates import *

try:
    # # just testing, nothing useful here
    # # or1 = OR("test")
    # # in1 = bool(int(input()))
    # # in2 = False
    # # in3 = True
    # #
    # # snd1 = SND(in1)
    # # snd2 = SND(in2)
    # # snd3 = SND(in3)
    # #
    # # snd1.connect(or1)
    # # snd2.connect(or1)
    # # print(or1.__in_connections_list)
    # # print(or1.func())
    # #
    # # snd3.connect(or1)
    # # print(or1.__in_connections_list)
    # # print(or1.func())
    # #
    # # snd3.connect(or1, other_channel_number=1)
    # # print(or1.__in_connections_list)
    # # print(or1.func())
    #
    # ##########################################
    # # Trying to assemble first simple scheme #
    # ##########################################
    # a = SND(True)
    # b = SND(False)
    # c = SND(True)
    # d = SND(False)
    # or1 = OR("or1")
    # a.connect(or1)
    # b.connect(or1)
    # not1 = NOT("not1")
    # or1.connect(not1)
    # not2 = NOT("not2")
    # c.connect(not2)
    # nand1 = NAND("nand1")
    # not1.connect(nand1)
    # not2.connect(nand1)
    # xor1 = XOR("xor1")
    # nand1.connect(xor1)
    # d.connect(xor1)
    # y = RCV(gname="Y")
    # xor1.connect(y)
    # print(y.func())
    #
    # #############################################
    # # It worked! Let's try to break it down now #
    # #############################################
    #
    # # y.connect(y) - good, raised error
    # e = SND(False)
    #
    # a.disconnect(or1)
    # e.connect(or1)
    # print(or1.func())  # perfect! disconnection successful
    #
    # e.disconnect(or1)
    # # print(or1.func()) - good, raised error
    # # e.disconnect(or1)  - good, didn't disconnect twice
    #
    # ##########################################################
    # # Trying to embed a multiplexer into the previous scheme #
    # ##########################################################
    # a = SND(True)
    # b = SND(False)
    # c = SND(True)
    # d = SND(False)
    # or1 = OR("or1")
    # a.connect(or1)
    # b.connect(or1)
    # not1 = NOT("not1")
    # or1.connect(not1)
    # not2 = NOT("not2")
    # c.connect(not2)
    # nand1 = NAND("nand1")
    # not1.connect(nand1)
    # not2.connect(nand1)
    # xor1 = XOR("xor1")
    # nand1.connect(xor1)
    # d.connect(xor1)
    # y = BUF(gname="Y")
    # xor1.connect(y)
    # mux1 = MUX("mux1", 4)
    # y.connect(mux1)
    # y.connect(mux1)
    # y.connect(mux1)
    # e.connect(mux1)
    # print(mux1.func([0, 0]))
    # print()
    # print(mux1.get_info())

    #########################
    # Testing demultiplexer #
    #########################
    a = SND(True)
    b = SND(True)
    c = SND(False)
    # d = SND(False)
    # # 1010
    # dms1 = DMS("dms1", 4)
    # a.connect(dms1)
    # b.connect(dms1)
    # c.connect(dms1)
    # d.connect(dms1)
    # print(dms1.func())  # success!

    #####################################
    # Testing changing of signal of SND #
    #####################################
    and_t = AND("and_t")
    or_t = OR("or_t")
    a.connect(and_t)
    b.connect(and_t)
    and_t.connect(or_t)
    c.connect(or_t)
    print(or_t.func())
    a.change_signal(False)
    print(or_t.func())


except Exception as exception:
    print(exception)
    print("Error caught. Terminating")
