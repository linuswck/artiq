use spi;
use board_misoc::{csr, clock};

const IRCML_REG : u8 = 0x05;
const QRCML_REG : u8 = 0x08;

const CLKMODE_REG : u8 = 0x14;

fn clk_enable(en: bool){
    unsafe{
        if en {
            csr::dac_interface::clk_en_write(0xff);
        }
        else {
            csr::dac_interface::clk_en_write(0x00);
        }
    }
}

fn hard_reset(){
    unsafe {
        // Min Pulse Width: 50ns
        csr::dac_rst::out_write(0);
        clock::spin_us(1);
        csr::dac_rst::out_write(1);
        clock::spin_us(1);
        csr::dac_rst::out_write(0);
    }
}

fn spi_setup(dac_sel: u8){
    unsafe{
        while csr::converter_spi::idle_read() == 0 {}
        csr::converter_spi::offline_write(0);
        csr::converter_spi::end_write(0);
        csr::converter_spi::cs_polarity_write(dac_sel << 1);
        csr::converter_spi::clk_polarity_write(0);
        csr::converter_spi::clk_phase_write(0);
        csr::converter_spi::lsb_first_write(0);
        csr::converter_spi::half_duplex_write(0);
        // To be refractored here
        csr::converter_spi::length_write(8 - 1);
        // To be refractored here
        csr::converter_spi::div_write(64 - 2);
        csr::converter_spi::cs_write(0b0001);
    }
}

fn write(dac_sel: u8, reg: u8, val: u8) -> Result<(), ()> {
    spi_setup(dac_sel);
    spi::write(0, ((reg as u32) << 24).into())?;
    unsafe{
        while csr::converter_spi::writable_read() == 0 {}
        csr::converter_spi::end_write(1);
    }
    spi::write(0, ((val as u32) << 24).into())?;
    
    Ok(())
}

fn read(dac_sel: u8, reg: u8) -> Result<u8, ()> {
    spi_setup(dac_sel);
    spi::write(0, (((reg | 1 << 7)as u32) << 24).into())?;
    unsafe{
        while csr::converter_spi::writable_read() == 0 {}
        csr::converter_spi::end_write(1);
        csr::converter_spi::half_duplex_write(1);
    }
    spi::write(0, 0)?;

    Ok(spi::read(0)? as u8)
}

pub fn init() -> Result<(), &'static str> {
    debug!("DAC CLK Enabled");
    clk_enable(true);

    debug!("DAC Hard Reset");
    hard_reset();
    
    for channel in 0..8 {
        let reg = read(channel, 0x1F).unwrap();
        if reg != 0x0A {
            debug!("DAC AD9117 Channel {} is not found. hw_rev reg: {:02x}", channel, reg);
            return Err("Device revision of AD9117 does not match.");
        }
        let reg = read(channel, CLKMODE_REG).unwrap();
        info!("CLKMDOE reg: {:02x}", reg);
        if reg >> 4 & 1 != 0 {
            debug!("DAC AD9117 Channel {} fails to retime. CLKMDOE reg: {:02x}", channel, reg);
            return Err("DAC AD9117 retiming failure");
        }

        // ToDo: Determine the init value of other registers

        // Enable internal common mode resistor of both channels
        debug!("IRCML_REG reesistor enabled");
        write(channel, IRCML_REG, 1 << 7);
        
        debug!("QRCML_REG reesistor enabled");
        write(channel, QRCML_REG, 1 << 7);

        unsafe{
            csr::dac_interface::ready_write(1);
        }
    } 

    Ok(())
}