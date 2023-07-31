// SPI Config Support for AD911X Series DAC
use board_misoc::{csr};
use spi_bit_bang;

struct Registers{
    version: u8
}

pub struct AD9117 {
    ch_sel: u8,
    registers: Registers,
}

//Write select logic csr here
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

        spi_bit_bang::init();

        let hw_rev = spi_bit_bang::read(read_instruction_byte(0x1F));

        println!("hw_rev: {}", hw_rev);

        if (hw_rev != 0x0A){
            //println!("Wrong hw_rev Number. Expected: 0x0A");
            //prtinln!(hw_rev);
            return Err("Wrong hw_rev Number. Expected: 0x0A");
        }

        return Ok(ad9117);
    }
}