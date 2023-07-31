class TXSerdes(Module):
    def __init__(self):
        self.txdata = [ Signal(5) for _ in range(4) ]
        self.ser_out = [ Signal() for _ in range(4) ]
        self.t_out = [ Signal() for _ in range(4) ]

        # TX SERDES
        for i in range(4):
            self.specials += Instance("OSERDESE2",
                p_DATA_RATE_OQ="SDR", p_DATA_RATE_TQ="BUF",
                p_DATA_WIDTH=5, p_TRISTATE_WIDTH=1,
                p_INIT_OQ=0b00000,
                o_OQ=self.ser_out[i],
                o_TQ=self.t_out[i],
                i_RST=ResetSignal("eem_sys"),
                i_CLK=ClockSignal("eem_sys5x"),
                i_CLKDIV=ClockSignal("eem_sys"),
                i_D1=self.txdata[i][0],
                i_D2=self.txdata[i][1],
                i_D3=self.txdata[i][2],
                i_D4=self.txdata[i][3],
                i_D5=self.txdata[i][4],
                i_TCE=1, i_OCE=1,
                i_T1=0)