// SPI Config Support for AD911X Series DAC
use board_misoc::{csr};
use spi_bit_bang;

struct Registers{
    version: u8,
    pwr_down: u8,
    data_ctrl: u8,
    i_dac_gain: u8,
    irset: u8,
    ircml: u8,
    q_dac_gain: u8,
    qrset: u8,
    qrcml: u8,
    aux_dac_i: u8,
    aux_ctrl_i: u8,
    aux_dac_q: u8,
    aux_ctrl_q: u8,
    

}

pub struct AD9117 {
    ch_sel: u8,
    registers: Registers,
}

fn write_instruction_byte(reg_addr: u8) -> u8{
    return 0b0001_1111 & reg_addr;
}

fn read_instruction_byte(reg_addr: u8) -> u8{
    return 0b1000_0000 | reg_addr & 0b1001_1111;
}

impl AD9117 {
    // Bit[6:5] Number of byte transferred = 1
    // Bit7: Write Operation
    pub fn new()-> Result<Self, &'static str> {
        let mut ad9117 = AD9117{
            ch_sel: 0,
            registers: Registers{
                version:0x1F,
            }
        };

        spi_bit_bang::init().expect("SPI Bit Bang Core Init Failure");

        /* 
        let hw_rev = spi_bit_bang::read(read_instruction_byte(0x1F));

        if (hw_rev? != 0x0A){
            #[cfg(feature = "log")]
            log::info!(
                "AD9117 has hw rev number of {:#02x} instead of 0x0A", hw_rev
            );
        }
        #[cfg(feature = "log")]
        log::info!(
            "AD9117 has hw rev number of {:#02x}", hw_rev
        );
        */

        return Ok(ad9117);
    }
}