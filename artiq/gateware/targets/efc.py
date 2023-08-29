#!/usr/bin/env python3

import argparse

from migen import *
from migen.build.generic_platform import *

from misoc.cores import gpio, spi2
from misoc.targets.efc import BaseSoC
from misoc.integration.builder import builder_args, builder_argdict

from artiq.gateware.amp import AMPSoC
from artiq.gateware import rtio
from artiq.gateware.rtio.xilinx_clocking import fix_serdes_timing_path
from artiq.gateware.rtio.phy import ttl_simple
from artiq.gateware.drtio.transceiver import eem_serdes
from artiq.gateware.drtio.rx_synchronizer import NoRXSynchronizer
from artiq.gateware.drtio import *
from artiq.build_soc import *

# To be refractored
from artiq.gateware.shuttler.core import Shuttler
from misoc.interconnect.csr import *

class Satellite(BaseSoC, AMPSoC):
    mem_map = {
        "rtio":          0x20000000,
        "drtioaux":      0x50000000,
        "mailbox":       0x70000000
    }
    mem_map.update(BaseSoC.mem_map)

    def __init__(self, gateware_identifier_str=None, **kwargs):
        BaseSoC.__init__(self,
                 cpu_type="vexriscv",
                 cpu_bus_width=64,
                 sdram_controller_type="minicon",
                 l2_size=128*1024,
                 clk_freq=125e6,
                 **kwargs)
        AMPSoC.__init__(self)
        add_identifier(self, gateware_identifier_str=gateware_identifier_str)

        platform = self.platform

        drtio_eem_io = [
            ("drtio_tx", 0,
                Subsignal("p", Pins("eem0:d0_cc_p eem0:d1_p eem0:d2_p eem0:d3_p")),
                Subsignal("n", Pins("eem0:d0_cc_n eem0:d1_n eem0:d2_n eem0:d3_n")),
                IOStandard("LVDS_25"),
            ),
            ("drtio_rx", 0,
                Subsignal("p", Pins("eem0:d4_p eem0:d5_p eem0:d6_p eem0:d7_p")),
                Subsignal("n", Pins("eem0:d4_n eem0:d5_n eem0:d6_n eem0:d7_n")),
                IOStandard("LVDS_25"), Misc("DIFF_TERM=TRUE"),
            ),
        ]

        platform.add_extension(drtio_eem_io)
        data_pads = [
            (platform.request("drtio_rx"), platform.request("drtio_tx"))
        ]

        # Disable SERVMOD, hardwire it to ground to enable EEM 0
        servmod = self.platform.request("servmod")
        self.comb += servmod.eq(0)

        self.submodules.eem_transceiver = eem_serdes.EEMSerdes(self.platform, data_pads)
        self.csr_devices.append("eem_transceiver")
        self.config["HAS_DRTIO_EEM"] = None
        self.config["EEM_DRTIO_COUNT"] = 1

        self.submodules.rtio_tsc = rtio.TSC(glbl_fine_ts_width=3)

        cdr = ClockDomainsRenamer({"rtio_rx": "sys"})
        core = cdr(DRTIOSatellite(
            self.rtio_tsc, self.eem_transceiver.channels[0],
            NoRXSynchronizer()))
        self.submodules.drtiosat = core
        self.csr_devices.append("drtiosat")

        self.submodules.drtioaux0 = cdr(DRTIOAuxController(
            core.link_layer, self.cpu_dw))
        self.csr_devices.append("drtioaux0")

        memory_address = self.mem_map["drtioaux"]
        self.add_wb_slave(memory_address, 0x800, self.drtioaux0.bus)
        self.add_memory_region("drtioaux0_mem", memory_address | self.shadow_base, 0x800)

        self.config["HAS_DRTIO"] = None
        self.add_csr_group("drtioaux", ["drtioaux0"])
        self.add_memory_group("drtioaux_mem", ["drtioaux0_mem"])

        i2c = self.platform.request("fpga_i2c")
        self.submodules.i2c = gpio.GPIOTristate([i2c.scl, i2c.sda])
        self.csr_devices.append("i2c")
        self.config["I2C_BUS_COUNT"] = 1

        # Enable I2C
        i2c_reset = self.platform.request("i2c_mux_rst_n")
        self.comb += i2c_reset.eq(1)

        fix_serdes_timing_path(platform)

        self.config["DRTIO_ROLE"] = "satellite"
        self.config["RTIO_FREQUENCY"] = "125.0"

        shuttler_io = [            
            ('dac_spi', 0,
                Subsignal('clk', Pins('fmc0:HB16_N')),
                Subsignal('mosi', Pins('fmc0:HB06_CC_N')),
                Subsignal('cs_n', Pins('fmc0:LA31_N fmc0:LA31_P fmc0:HB19_P fmc0:LA30_P')),
                IOStandard("LVCMOS18")),
            ('dac_rst', 0, Pins('fmc0:HB16_P'), IOStandard("LVCMOS18")),
            ('dac_din', 0,
                Subsignal('data', Pins('fmc0:HA06_N fmc0:HA06_P fmc0:HA07_N fmc0:HA02_N fmc0:HA07_P fmc0:HA02_P fmc0:HA03_N fmc0:HA03_P fmc0:HA04_N fmc0:HA04_P fmc0:HA05_N fmc0:HA05_P fmc0:HA00_CC_N fmc0:HA01_CC_N')),
                Subsignal('dclkio', Pins('fmc0:HA00_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 1,
                Subsignal('data', Pins('fmc0:LA09_P fmc0:LA09_N fmc0:LA07_N fmc0:LA08_N fmc0:LA07_P fmc0:LA08_P fmc0:LA05_N fmc0:LA04_N fmc0:LA05_P fmc0:LA06_N fmc0:LA04_P fmc0:LA03_N fmc0:LA03_P fmc0:LA06_P')),
                Subsignal('dclkio', Pins('fmc0:LA00_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 2,
                Subsignal('data', Pins('fmc0:HA14_N fmc0:HA14_P fmc0:HA12_N fmc0:HA12_P fmc0:HA13_N fmc0:HA10_N fmc0:HA10_P fmc0:HA11_N fmc0:HA11_P fmc0:HA13_P fmc0:HA08_N fmc0:HA08_P fmc0:HA09_N fmc0:HA09_P')),
                Subsignal('dclkio', Pins('fmc0:HA01_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 3,
                Subsignal('data', Pins('fmc0:LA14_N fmc0:LA15_N fmc0:LA16_N fmc0:LA15_P fmc0:LA14_P fmc0:LA13_N fmc0:LA16_P fmc0:LA13_P fmc0:LA11_N fmc0:LA12_N fmc0:LA11_P fmc0:LA12_P fmc0:LA10_N fmc0:LA10_P')),
                Subsignal('dclkio', Pins('fmc0:LA01_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 4,
                Subsignal('data', Pins('fmc0:HA22_N fmc0:HA19_N fmc0:HA22_P fmc0:HA21_N fmc0:HA21_P fmc0:HA19_P fmc0:HA18_CC_N fmc0:HA20_N fmc0:HA20_P fmc0:HA18_CC_P fmc0:HA15_N fmc0:HA15_P fmc0:HA16_N fmc0:HA16_P')),
                Subsignal('dclkio', Pins('fmc0:HA17_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 5,
                Subsignal('data', Pins('fmc0:LA24_N fmc0:LA25_N fmc0:LA24_P fmc0:LA25_P fmc0:LA21_N fmc0:LA21_P fmc0:LA22_N fmc0:LA22_P fmc0:LA23_N fmc0:LA23_P fmc0:LA19_N fmc0:LA19_P fmc0:LA20_N fmc0:LA20_P')),
                Subsignal('dclkio', Pins('fmc0:LA17_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 6,
                Subsignal('data', Pins('fmc0:HB08_N fmc0:HB08_P fmc0:HB07_N fmc0:HB07_P fmc0:HB04_N fmc0:HB04_P fmc0:HB01_N fmc0:HB05_N fmc0:HB01_P fmc0:HB05_P fmc0:HB02_N fmc0:HB02_P fmc0:HB03_N fmc0:HB03_P')),
                Subsignal('dclkio', Pins('fmc0:HB00_CC_P')),
                IOStandard('LVCMOS18')),
            ('dac_din', 7,
                Subsignal('data', Pins('fmc0:HB13_N fmc0:HB12_N fmc0:HB13_P fmc0:HB12_P fmc0:HB15_N fmc0:HB15_P fmc0:HB11_N fmc0:HB09_N fmc0:HB09_P fmc0:HB14_N fmc0:HB14_P fmc0:HB10_N fmc0:HB10_P fmc0:HB11_P')),
                Subsignal('dclkio', Pins('fmc0:HB06_CC_P')),
                IOStandard('LVCMOS18')),
            ('mmcx_osc_sel_n', 0, Pins('fmc0:HB17_CC_N'), IOStandard('LVCMOS18')),
            ('ref_clk_sel', 0, Pins('fmc0:LA32_N'), IOStandard('LVCMOS18')),
        ]

        platform.add_extension(shuttler_io)

        self.submodules.converter_spi = spi2.SPIMaster(spi2.SPIInterface(self.platform.request("dac_spi", 0)))
        self.csr_devices.append("converter_spi")
        self.config["HAS_CONVERTER_SPI"] = None

        self.submodules.dac_rst = gpio.GPIOOut(self.platform.request("dac_rst"))
        self.csr_devices.append("dac_rst")

        self.submodules.mmcx_osc_sel_n = gpio.GPIOOut(self.platform.request("mmcx_osc_sel_n"))
        self.csr_devices.append("mmcx_osc_sel_n")

        self.submodules.ref_clk_sel = gpio.GPIOOut(self.platform.request("ref_clk_sel"))
        self.csr_devices.append("ref_clk_sel")

        dac_din_ios = []
        dac_din_ios += [ platform.request("dac_din", i) for i in range(8) ]
        self.submodules.shuttler = Shuttler(dac_din_ios)
        self.csr_devices.append("shuttler")

        self.rtio_channels = [] 

        for i in range(2):
            phy = ttl_simple.Output(self.virtual_leds.get(i))
            self.submodules += phy
            self.rtio_channels.append(rtio.Channel.from_phy(phy))

        self.config["HAS_RTIO_LOG"] = None
        self.config["RTIO_LOG_CHANNEL"] = len(self.rtio_channels)
        self.rtio_channels.append(rtio.LogChannel())

        self.add_rtio(self.rtio_channels)

    def add_rtio(self, rtio_channels, sed_lanes=8):
        # Only add MonInj core if there is anything to monitor
        if any([len(c.probes) for c in rtio_channels]):
            self.submodules.rtio_moninj = rtio.MonInj(rtio_channels)
            self.csr_devices.append("rtio_moninj")

        # satellite (master-controlled) RTIO
        self.submodules.local_io = SyncRTIO(self.rtio_tsc, rtio_channels, lane_count=sed_lanes)
        self.comb += self.drtiosat.async_errors.eq(self.local_io.async_errors)

        # subkernel RTIO
        self.submodules.rtio = rtio.KernelInitiator(self.rtio_tsc)
        self.register_kernel_cpu_csrdevice("rtio")

        self.submodules.rtio_dma = rtio.DMA(self.get_native_sdram_if(), self.cpu_dw)
        self.csr_devices.append("rtio_dma")
        self.submodules.cri_con = rtio.CRIInterconnectShared(
            [self.drtiosat.cri, self.rtio_dma.cri],
            [self.local_io.cri],
            enable_routing=True)
        self.csr_devices.append("cri_con")
        self.submodules.routing_table = rtio.RoutingTableAccess(self.cri_con)
        self.csr_devices.append("routing_table")

        self.submodules.rtio_analyzer = rtio.Analyzer(self.rtio_tsc, self.local_io.cri,
                                                self.get_native_sdram_if(), cpu_dw=self.cpu_dw)
        self.csr_devices.append("rtio_analyzer")


def main():
    parser = argparse.ArgumentParser(
        description="ARTIQ device binary builder for EEM FMC Carrier systems")
    builder_args(parser)
    parser.set_defaults(output_dir="artiq_efc")
    parser.add_argument("-V", "--variant", default="shuttler")
    parser.add_argument("--gateware-identifier-str", default=None,
                        help="Override ROM identifier")
    args = parser.parse_args()

    argdict = dict()
    argdict["gateware_identifier_str"] = args.gateware_identifier_str

    soc = Satellite(**argdict)
    build_artiq_soc(soc, builder_argdict(args))


if __name__ == "__main__":
    main()
