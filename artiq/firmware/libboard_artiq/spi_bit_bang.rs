


// Half Duplex SPI Bit Bang Soft Core
// MSB First
// SPI Mode 0
// Data width: 8 Bit

mod imp {
    use board_misoc::csr;
    use board_misoc::clock;

    const NO_SPI: &'static str = "No I2C support on this platform";

    fn half_period() { clock::spin_us(100)}
    fn quad_period() { clock::spin_us(50)}
    // option if not half duplex
    //fn mosi_bit() -> u8 (1 << 3)
    fn miso_bit() -> u8 { 1 << 2 }
    fn sclk_bit() -> u8 { 1 << 1 }
    fn cs_n_bit() -> u8 { 1 << 0 }

    fn miso_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & miso_bit() != 0
        }
    }
    
    fn sclk_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & sclk_bit() != 0
        }
    }

    fn cs_n_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & cs_n_bit() != 0
        }
    }

    fn miso_oe(oe: bool) {
        unsafe {
            let reg = csr::spi_bit_bang::oe_read();
            let reg = if oe { reg | miso_bit() } else { reg & !miso_bit() };
            csr::spi_bit_bang::oe_write(reg)
        }
    }


    fn miso_o(o: bool) {
        unsafe {
            println!("Set miso_o to {}", o);
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | miso_bit() } else { reg & !miso_bit() };
            println!("reg o {}", reg);
            csr::spi_bit_bang::out_write(reg)
        }
    }

    fn sclk_oe(oe: bool) {
        unsafe {
            let reg = csr::spi_bit_bang::oe_read();
            let reg = if oe { reg | sclk_bit() } else { reg & !sclk_bit() };
            csr::spi_bit_bang::oe_write(reg)
        }
    }

    fn sclk_o(o: bool) {
        unsafe {
            println!("Set sclk to {}", o);
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | sclk_bit() } else { reg & !sclk_bit() };
            println!("reg o {}", reg);
            csr::spi_bit_bang::out_write(reg)
        }
    }

    fn cs_n_oe(oe: bool) {
        unsafe {
            let reg = csr::spi_bit_bang::oe_read();
            let reg = if oe { reg | cs_n_bit() } else { reg & !cs_n_bit() };
            csr::spi_bit_bang::oe_write(reg)
        }
    }

    fn cs_n_o(o: bool) {
        unsafe {
            println!("Set cs_n to {}", o);
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | cs_n_bit() } else { reg & !cs_n_bit() };
            println!("reg o {}", reg);
            csr::spi_bit_bang::out_write(reg)
        }
    }

    fn test(){

    }

    fn start() -> Result<(), &'static str>{
        println!("SPI Start");

        miso_oe(true);
        sclk_oe(true);
        cs_n_oe(true);
        cs_n_o(false);

        half_period();
        half_period();

        cs_n_o(true);

        half_period();
        half_period();

        cs_n_o(false);

        Ok(())
    }

    fn end()-> Result<(), &'static str>{
        miso_o(false);
        miso_oe(false);
        cs_n_o(true);

        println!("SPI End");

        Ok(())
    }

    pub fn init() -> Result<(), &'static str> {
        if csr::CONFIG_SPI_BIT_BANG_HALF_DUPLEX == 1{
            return Err("Only SPI Half Duplex Mode is supported");
        }
        
        miso_oe(false);
        sclk_oe(true);
        cs_n_oe(true);
        
        miso_o(false);
        sclk_o(true);
        cs_n_o(true);

        // Check the I2C bus is ready
        half_period();
        half_period();
        
        Ok(())
    }

    pub fn write(reg_addr: u8, data: u8)-> Result<(), &'static str>{
        start();
        
        for bit in (0..8).rev() {
            miso_o(reg_addr & (1 << bit) == 0);
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        for bit in (0..8).rev() {
            miso_o(data & (1 << bit) == 0);
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        end();

        Ok(())
    }

    pub fn read(reg_addr: u8) -> u8 {
    //pub fn read(reg_addr: u8) -> Result<u8, &'static str> {

        println!("reg_addr {}", reg_addr);

        start();

        unsafe{
            let reg = csr::spi_bit_bang::oe_read();
            println!("oe value befiore read {}:", reg);
        }
        
        println!("instruction byte");
        for bit in (0..8).rev() {
            miso_o(!(reg_addr & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        let mut data: u8 = 0;
        quad_period();
        miso_oe(false);
        quad_period();
        sclk_o(false);

        println!("read data byte");
        for bit in (0..8).rev() {
            half_period();
            sclk_o(true);
            if miso_i() { data |= 1 << bit }
            half_period();
            sclk_o(false);
        }

        end();

        return data;

        //return Ok(data);
    }

}

/* 
mod imp {
    const NO_SPI_BIT_BANG: &'static str = "No SPI BIT BANG support on this platform";
    pub fn init() -> Result<(), &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn write(_reg_addr: u8, _data: u8) -> Result<bool, &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn read(_reg_addr: u8) -> Result<u8, &'static str> { Err(NO_SPI_BIT_BANG) }
}
*/

pub use self::imp::*;