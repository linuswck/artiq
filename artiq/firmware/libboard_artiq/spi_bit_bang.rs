// SPI Bit Bang Configuration:
// 3 wire Half Duplex
// MSB First
// SPI Mode 0
// Data width: 8 Bit

mod imp {
    use board_misoc::csr;
    use board_misoc::clock;

    const NO_SPI: &'static str = "No I2C support on this platform";

    fn half_period() { clock::spin_us(100)}
    fn quad_period() { clock::spin_us(50)}
    fn mosi_bit() -> u8 { 1 << 2 }
    fn sclk_bit() -> u8 { 1 << 1 }
    fn cs_n_bit() -> u8 { 1 << 0 }

    fn mosi_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & mosi_bit() != 0
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

    fn mosi_oe(oe: bool) {
        unsafe {
            let reg = csr::spi_bit_bang::oe_read();
            let reg = if oe { reg | mosi_bit() } else { reg & !mosi_bit() };
            csr::spi_bit_bang::oe_write(reg)
        }
    }


    fn mosi_o(o: bool) {
        unsafe {
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | mosi_bit() } else { reg & !mosi_bit() };
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
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | sclk_bit() } else { reg & !sclk_bit() };
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
            let reg = csr::spi_bit_bang::out_read();
            let reg = if o  { reg | cs_n_bit() } else { reg & !cs_n_bit() };
            csr::spi_bit_bang::out_write(reg)
        }
    }

    fn start(){
        mosi_oe(true);
        sclk_oe(true);
        cs_n_oe(true);

        mosi_o(false);
        sclk_o(false);
        cs_n_o(true);

        half_period();
        half_period();

        cs_n_o(false);
    }

    fn end(){
        mosi_oe(false);
        sclk_oe(false);
        cs_n_oe(true);

        mosi_o(false);
        sclk_o(false);
        cs_n_o(true);
    }

    pub fn init() -> Result<(), &'static str> {
        if csr::CONFIG_SPI_BIT_BANG_HALF_DUPLEX != 1{
            return Err("Only SPI Half Duplex Mode is supported");
        }
        
        mosi_oe(false);
        sclk_oe(false);
        cs_n_oe(true);

        mosi_o(false);
        sclk_o(false);
        cs_n_o(true);

        // To-do: Add logic to check if the spi line does not get stuck
        // Test if the line works as expected
        // Test 1: push and read the 
        

        half_period();
        half_period();
        
        Ok(())
    }

    pub fn write(reg_addr: u8, data: u8)-> Result<(), &'static str>{
        start();
        
        for bit in (0..8).rev() {
            mosi_o(!(reg_addr & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        for bit in (0..8).rev() {
            mosi_o(!(data & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        end();

        Ok(())
    }

    pub fn read(reg_addr: u8) -> Result<u8, &'static str> {
        start();

        for bit in (0..8).rev() {
            mosi_o(!(reg_addr & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        let mut data: u8 = 0;
        quad_period();
        mosi_oe(false);
        quad_period();
        sclk_o(false);

        for bit in (0..8).rev() {
            half_period();
            sclk_o(true);
            if mosi_i() { data |= 1 << bit }
            half_period();
            sclk_o(false);
        }

        end();

        Ok(data)
    }
}

pub use self::imp::*;