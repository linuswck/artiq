// SPI Bit Bang Configuration:
//   Mode 0 (SPI_CLK_POLARITY = 0, SPI_CLK_PHASE = 0)
//   3 Wire Half Duplex Communication
//   MSB First
//   Data width: 8 Bit
#[cfg(has_spi_bit_bang)]
mod imp {
    use board_misoc::{csr, clock};

    fn half_period() { clock::spin_us(100)}
    fn mosi_bit() -> u8 { 1 << 2 }
    fn sclk_bit() -> u8 { 1 << 1 }
    fn cs_n_bit() -> u8 { 1 << 0 }

    fn mosi_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & mosi_bit() != 0
        }
    }

    fn mosi_oe_i() -> bool {
        unsafe {
            return csr::spi_bit_bang::oe_read() & mosi_bit() != 0
        }
    }

    
    fn sclk_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & sclk_bit() != 0
        }
    }

    fn sclk_oe_i() -> bool {
        unsafe {
            return csr::spi_bit_bang::oe_read() & sclk_bit() != 0
        }
    }

    fn cs_n_i() -> bool {
        unsafe {
            csr::spi_bit_bang::in_read() & cs_n_bit() != 0
        }
    }

    fn cs_n_oe_i() -> bool {
        unsafe {
            return csr::spi_bit_bang::oe_read() & cs_n_bit() != 0
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

    pub fn start() -> Result<(), &'static str> {
        // precondition: OE for CS_N, SCLK and MOSI high
        // precondition: CS_N high | SCLK and MOSI low
        if !cs_n_oe_i(){
            return Err("OE for CS_N is not set to high")
        }

        if !cs_n_i(){
            return Err("CS_N is stuck low");
        }

        if !sclk_oe_i(){
            return Err("OE for CS_N is not set to high");
        }

        if sclk_i(){
            return Err("SCLK is stuck high");
        }
        
        if !mosi_oe_i(){
            return Err("OE for MOSI is not set to high");
        }        

        if mosi_i(){
            return Err("MOSI is stuck high");
        }

        cs_n_o(false);

        half_period();
        half_period();
        // postcondition: OE for CS_N, SCLK, MOSI high
        // postcondition: CS_N, SCLK and MOSI low
        Ok(())
    }

    pub fn end() -> Result<(), &'static str> {
        // precondition: OE for CS_N, SCLK high | MOSI don't care
        // precondition: CS_N and SCLK low | MOSI don't care
        cs_n_o(true);
        mosi_o(false);
        
        // Drive MOSI after deassertion of CS_N to avoid
        //  bus contention with slave device after read
        mosi_oe(true);

        if !cs_n_i(){
            return Err("CS_N is stuck low");
        }

        if sclk_i(){
            return Err("SCLK is stuck high");
        }
        
        if mosi_i(){
            return Err("MOSI is stuck high");
        }
        // postcondition: OE for CS_N, SCLK high | MOSI low
        // postcondition: CS_N high | SCLK and MOSI low

        Ok(())
    }

    pub fn init() -> Result<(), &'static str> {
        // Check if CS_N, SCLK and MOSI can be driven high and low.
        cs_n_oe(true);
        cs_n_o(false);
        if cs_n_i(){ 
            return Err("CS_N cannot be driven high"); 
        }

        cs_n_o(true);
        if !cs_n_i(){ 
            return Err("CS_N cannot be driven low"); 
        }

        sclk_oe(true);
        sclk_o(true);
        if !sclk_i(){ 
            return Err("SCLK cannot be driven low"); 
        }

        sclk_o(false);
        if sclk_i(){ 
            return Err("SCLK cannot be driven high"); 
        }

        mosi_oe(true);
        mosi_o(true);
        if !mosi_i(){ 
            return Err("MOSI cannot be driven low"); 
        }

        mosi_o(false);
        if mosi_i(){
            return Err("MOSI cannot be driven high"); 
        }
        // postcondition: OE for CS_N, SCLK and MOSI high
        // postcondition: CS_N high | SCLK and MOSI low.

        Ok(())
    }

    pub fn write(reg_addr: u8, data: u8)-> Result<(), &'static str>{
        // precondition: OE for CS_N, SCLK and MOSI high
        // precondition: CS_N, SCLK and MOSI low
        
        // MSB first
        for bit in (0..8).rev() {
            mosi_o(!(reg_addr & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        // MSB first
        for bit in (0..8).rev() {
            mosi_o(!(data & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }
        half_period();
        sclk_o(false);
        // post condition: OE for CS_N, SCLK and MOSI high
        // post condition: CS_N low and SCLK low | MOSI don't care

        Ok(())
    }

    pub fn read(reg_addr: u8) -> Result<u8, &'static str> {
        // precondition: OE for CS_N, SCLK and MOSI high
        // precondition: CS_N, SCLK and MOSI low

        let mut data: u8 = 0;

        // MSB first
        for bit in (0..8).rev() {
            mosi_o(!(reg_addr & (1 << bit) == 0));
            half_period();
            sclk_o(false);
            half_period();
            sclk_o(true);
        }

        // Release MOSI for slave device to shift data out
        mosi_oe(false);
        sclk_o(false);

        // MSB first
        for bit in (0..8).rev() {
            half_period();
            sclk_o(true);
            if mosi_i() { data |= 1 << bit }
            half_period();
            sclk_o(false);
        }
        // postcondition: OE for CS_N and SCLK high | MOSI low
        // postcondition: CS_N and SCLK low | MOSI don't care

        Ok(data)
    }
}

#[cfg(not(has_spi_bit_bang))]
mod imp {
    const NO_SPI_BIT_BANG: &'static str = "No SPI Bit Bang supports on this platform";
    pub fn init() -> Result<(), &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn start() -> Result<(), &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn end() -> Result<(), &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn write(reg_addr: u8, data: u8)-> Result<(), &'static str> { Err(NO_SPI_BIT_BANG) }
    pub fn read(reg_addr: u8) -> Result<u8, &'static str> { Err(NO_SPI_BIT_BANG) }
}

pub use self::imp::*;