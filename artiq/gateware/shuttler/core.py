from migen import *
from migen.genlib.io import DDROutput
from misoc.interconnect.csr import *

class Parallel_Interface(Module, AutoCSR):
    def __init__(self, din_pads, bit_width = 14):
        # To be removed: dac_din[number of channel][Data A or Data B][bit]
        self.din = [ [Signal(bit_width) for _ in range(2)] for _ in range(len(din_pads))]
        
        # To be removed: dclk_en should be enabled when the clock should be ready
        self.dclk_en = CSRStorage(len(din_pads))

        for i, din in enumerate(din_pads):
            # To be removed: AD917 Clock Frequency 125MHz
            self.specials += DDROutput(1, 0, din.dclkio, ClockSignal())
            for bit in range(bit_width):
                self.specials += DDROutput(self.din[i][0][bit], self.din[i][1][bit], din.data[bit], ClockSignal())
            


class Shuttler(Module, AutoCSR):
    def __init__(self, dac_din_pads):
        self.submodules.dac_din_interface = Parallel_Interface(dac_din_pads)

        # binary: reset = 0b0101010101010101
        self.din_data_test = CSRStorage(14, reset=0x55)
        # Channel 0I
        self.comb += self.dac_din_interface.din[0][0].eq(self.din_data_test.storage)
        # Channel 0Q
        self.comb += self.dac_din_interface.din[0][1].eq(self.din_data_test.storage)
