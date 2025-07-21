from numpy import int32, int64

from artiq.language.core import *
from artiq.language.types import *
from artiq.coredevice.rtio import rtio_output, rtio_input_data
from artiq.coredevice import spi2 as spi
from artiq.language.units import ms, us, ns

from artiq.coredevice.dac34h84 import DAC34H84
from artiq.coredevice.trf372017 import TRF372017

PHASER_BOARD_ID = 19
PHASER_HW_REV_VARIANT = 1 << 4


PHASER_GW_BASE = 1
PHASER_GW_MIQRO = 2

PHASER_ADDR_BOARD_ID                = 0x00
PHASER_ADDR_HW_REV                  = 0x01
PHASER_ADDR_GW_REV                  = 0x02
PHASER_ADDR_CFG                     = 0x03
PHASER_ADDR_STA                     = 0x04
PHASER_ADDR_CRC_ERR                 = 0x05
PHASER_ADDR_FAN_PWM                 = 0x06
PHASER_ADDR_DUC_STB                 = 0x07
PHASER_ADDR_ADC_CFG                 = 0x08
PHASER_ADDR_SYNC_DLY                = 0x09

PHASER_ADDR_DUC0_CFG                = 0x0a
PHASER_ADDR_DUC0_F                  = 0x0b
PHASER_ADDR_DUC0_P                  = 0x0c
PHASER_ADDR_DAC0_DATA               = 0x0d
PHASER_ADDR_DAC0_TEST               = 0x0e
PHASER_ADDR_DUC1_CFG                = 0x0f

PHASER_ADDR_DUC1_F                  = 0x10
PHASER_ADDR_DUC1_P                  = 0x11
PHASER_ADDR_DUC_OFFSET              = PHASER_ADDR_DUC1_CFG - PHASER_ADDR_DUC0_CFG

PHASER_ADDR_DAC1_DATA               = 0x12
PHASER_ADDR_DAC1_TEST               = 0x13


PHASER_ADDR_SERVO_CFG0                  = 0x14
PHASER_ADDR_CH0_OSCILLATOR_BASE         = 0x15
PHASER_ADDR_CH0_OSCILLATOR_AMPLITUDE0   = 0x15
PHASER_ADDR_CH0_OSCILLATOR_FREQUENCY0   = 0x16
PHASER_ADDR_CH0_OSCILLATOR_AMPLITUDE1   = 0x17
PHASER_ADDR_CH0_OSCILLATOR_FREQUENCY1   = 0x18
PHASER_ADDR_CH0_OSCILLATOR_AMPLITUDE2   = 0x19
PHASER_ADDR_CH0_OSCILLATOR_FREQUENCY2   = 0x1A
PHASER_ADDR_CH0_OSCILLATOR_AMPLITUDE3   = 0x1B
PHASER_ADDR_CH0_OSCILLATOR_FREQUENCY3   = 0x1C
PHASER_ADDR_CH0_OSCILLATOR_AMPLITUDE4   = 0x1D
PHASER_ADDR_CH0_OSCILLATOR_FREQUENCY4   = 0x1E

PHASER_ADDR_SERVO_CFG1                  = 0x1F

PHASER_ADDR_CH1_OSCILLATOR_BASE         = 0x20
PHASER_ADDR_CH1_OSCILLATOR_AMPLITUDE0   = 0x20
PHASER_ADDR_CH1_OSCILLATOR_FREQUENCY0   = 0x21
PHASER_ADDR_CH1_OSCILLATOR_AMPLITUDE1   = 0x22
PHASER_ADDR_CH1_OSCILLATOR_FREQUENCY1   = 0x23
PHASER_ADDR_CH1_OSCILLATOR_AMPLITUDE2   = 0x24
PHASER_ADDR_CH1_OSCILLATOR_FREQUENCY2   = 0x25
PHASER_ADDR_CH1_OSCILLATOR_AMPLITUDE3   = 0x26
PHASER_ADDR_CH1_OSCILLATOR_FREQUENCY3   = 0x27
PHASER_ADDR_CH1_OSCILLATOR_AMPLITUDE4   = 0x28
PHASER_ADDR_CH1_OSCILLATOR_FREQUENCY4   = 0x29

PHASER_ADDR_SERVO_DATA_BASE         = 0x2A
PHASER_ADDR_CH0_PROFILE0_DATA0      = 0x2A
PHASER_ADDR_CH0_PROFILE0_DATA1      = 0x2B
PHASER_ADDR_CH0_PROFILE0_DATA2      = 0x2C
PHASER_ADDR_CH0_PROFILE0_DATA3      = 0x2D
PHASER_ADDR_CH0_PROFILE1_DATA0      = 0x2E
PHASER_ADDR_CH0_PROFILE1_DATA1      = 0x2F
PHASER_ADDR_CH0_PROFILE1_DATA2      = 0x30
PHASER_ADDR_CH0_PROFILE1_DATA3      = 0x31
PHASER_ADDR_CH0_PROFILE2_DATA0      = 0x32
PHASER_ADDR_CH0_PROFILE2_DATA1      = 0x33
PHASER_ADDR_CH0_PROFILE2_DATA2      = 0x34
PHASER_ADDR_CH0_PROFILE2_DATA3      = 0x35
PHASER_ADDR_CH0_PROFILE3_DATA0      = 0x36
PHASER_ADDR_CH0_PROFILE3_DATA1      = 0x37
PHASER_ADDR_CH0_PROFILE3_DATA2      = 0x38
PHASER_ADDR_CH0_PROFILE3_DATA3      = 0x39

PHASER_ADDR_CH1_PROFILE0_DATA0      = 0x3A
PHASER_ADDR_CH1_PROFILE0_DATA1      = 0x3B
PHASER_ADDR_CH1_PROFILE0_DATA2      = 0x3C
PHASER_ADDR_CH1_PROFILE0_DATA3      = 0x3D
PHASER_ADDR_CH1_PROFILE1_DATA0      = 0x3E
PHASER_ADDR_CH1_PROFILE1_DATA1      = 0x3F
PHASER_ADDR_CH1_PROFILE1_DATA2      = 0x40
PHASER_ADDR_CH1_PROFILE1_DATA3      = 0x41
PHASER_ADDR_CH1_PROFILE2_DATA0      = 0x42
PHASER_ADDR_CH1_PROFILE2_DATA1      = 0x43
PHASER_ADDR_CH1_PROFILE2_DATA2      = 0x44
PHASER_ADDR_CH1_PROFILE2_DATA3      = 0x45
PHASER_ADDR_CH1_PROFILE3_DATA0      = 0x46
PHASER_ADDR_CH1_PROFILE3_DATA1      = 0x47
PHASER_ADDR_CH1_PROFILE3_DATA2      = 0x48
PHASER_ADDR_CH1_PROFILE3_DATA3      = 0x49

# Miqro profile memory select
PHASER_MIQRO_SEL_PROFILE = 1 << 14

PHASER_SEL_DAC = 1 << 0
PHASER_SEL_TRF0 = 1 << 1
PHASER_SEL_TRF1 = 1 << 2
PHASER_SEL_ATT0 = 1 << 3
PHASER_SEL_ATT1 = 1 << 4

PHASER_STA_DAC_ALARM = 1 << 0
PHASER_STA_TRF0_LD = 1 << 1
PHASER_STA_TRF1_LD = 1 << 2
PHASER_STA_TERM0 = 1 << 3
PHASER_STA_TERM1 = 1 << 4
PHASER_STA_SPI_IDLE = 1 << 5

PHASER_DAC_SEL_DUC = 0
PHASER_DAC_SEL_TEST = 1

PHASER_HW_REV_VARIANT = 1 << 4


SERVO_COEFF_WIDTH = 16
SERVO_DATA_WIDTH = 16
SERVO_COEFF_SHIFT = 14
SERVO_T_CYCLE = (32+12+192+24+4)*ns  # Must match gateware ADC parameters

### For frequency turning
##### Center frequency is set in the up converter
class PhaserOscillator:
    """Phaser IQ channel oscillator (NCO/DDS).

    .. note:: Latencies between oscillators within a channel and between
        oscillator parameters (amplitude and phase/frequency) are deterministic
        (with respect to the 25 MS/s sample clock) but not matched.
    """
    kernel_invariants = {"target_base", "base_offset"}

    # pass from config
    # channel <-Config object , PHASER_ADDR_CH0_OSCILLATOR_BASE, sub channel offset
    def __init__(self, target_base, base_offset, idx):
        self.target_base = target_base # RTIO Channel
        self.base_offset = base_offset + 2 * idx

    # rtio_output(self.target_base | self.target_board_id | self.target_read, 0)

    @kernel
    def set_frequency_mu(self, ftw):
        """Set Phaser MultiDDS frequency tuning word.

        :param ftw: Frequency tuning word (32-bit)
        """
        rtio_output(self.target_base | (self.base_offset + 1), ftw)
        ## Calculate Delay
        delay(1*us)

    @kernel
    def set_frequency(self, frequency):
        """Set Phaser MultiDDS frequency.

        :param frequency: Frequency in Hz (passband from -10 MHz to 10 MHz,
            wrapping around at +- 12.5 MHz)
        """
        ftw = int32(round(frequency*((1 << 30)/(6.25*MHz))))
        self.set_frequency_mu(ftw)



    @kernel
    def set_amplitude_phase_mu(self, asf=0x7fff, pow=0, clr=0):
        """Set Phaser MultiDDS amplitude, phase offset and accumulator clear.

        :param asf: Amplitude (15-bit)
        :param pow: Phase offset word (16-bit)
        :param clr: Clear the phase accumulator (persistent)
        """

        # This should be config
        data = (asf & 0x7fff) | ((clr & 1) << 15) | (pow << 16)
        rtio_output(self.target_base | self.base_offset, data)
        ## Calculate Delay
        delay(1*us)


    @kernel
    def set_amplitude_phase(self, amplitude, phase=0., clr=0):
        """Set Phaser MultiDDS amplitude and phase.

        :param amplitude: Amplitude in units of full scale
        :param phase: Phase in turns
        :param clr: Clear the phase accumulator (persistent)
        """
        asf = int32(round(amplitude*0x7fff))
        if asf < 0 or asf > 0x7fff:
            raise ValueError("amplitude out of bounds")
        pow = int32(round(phase*(1 << 16)))
        self.set_amplitude_phase_mu(asf, pow, clr)


# Instantiate after DAC object is declared in Phaser Class
class PhaserChannel:

    kernel_invariants = {"config", "phaser", "index", "trf_mmap"}
    def __init__(self, phaser, config, index, trf):
        self.phaser = phaser
        self.config = config
        self.index = index
        self.trf_mmap = TRF372017(trf).get_mmap()

        osc_base_offset = PHASER_ADDR_CH0_OSCILLATOR_BASE if index==0 else PHASER_ADDR_CH1_OSCILLATOR_BASE
        self.oscillator = [PhaserOscillator(config.target_base, osc_base_offset, osc) for osc in range(5)]

    @kernel
    def get_dac_data(self) -> TInt32:
        """Get a sample of the current DAC data.

        The data is split accross multiple registers and thus the data
        is only valid if constant.

        :return: DAC data as 32-bit IQ. I/DACA/DACC in the 16 LSB,
            Q/DACB/DACD in the 16 MSB
        """
        return self.config.read(PHASER_ADDR_DAC0_DATA + (PHASER_ADDR_DUC_OFFSET * self.index))

    @kernel
    def set_dac_test(self, data: TInt32):
        """Set the DAC test data.

        :param data: 32-bit IQ test data, I/DACA/DACC in the 16 LSB,
            Q/DACB/DACD in the 16 MSB
        """
        self.config.write(PHASER_ADDR_DAC0_TEST + (PHASER_ADDR_DUC_OFFSET * self.index), data)

    @kernel
    def set_duc_cfg(self, clr=0, clr_once=0, select=0):
        """Set the digital upconverter (DUC) and interpolator configuration.

        :param clr: Keep the phase accumulator cleared (persistent)
        :param clr_once: Clear the phase accumulator for one cycle
        :param select: Select the data to send to the DAC (0: DUC data, 1: test
            data, other values: reserved)
        """
        self.config.write(PHASER_ADDR_DUC0_CFG + (PHASER_ADDR_DUC_OFFSET * self.index),
                           ((clr & 1) << 0) | ((clr_once & 1) << 1) |
                           ((select & 3) << 2))

    @kernel
    def set_duc_frequency_mu(self, ftw):
        """Set the DUC frequency.

        :param ftw: DUC frequency tuning word (32-bit)
        """
        self.config.write32(PHASER_ADDR_DUC0_F + (self.index << 4), ftw)

    @kernel
    def set_duc_frequency(self, frequency):
        """Set the DUC frequency in SI units.

        :param frequency: DUC frequency in Hz (passband from -200 MHz to
            200 MHz, wrapping around at +- 250 MHz)
        """
        ftw = int32(round(frequency*((1 << 30)/(125*MHz))))
        self.set_duc_frequency_mu(ftw)

    @kernel
    def set_duc_phase_mu(self, pow):
        """Set the DUC phase offset.

        :param pow: DUC phase offset word (16-bit)
        """
        addr = PHASER_ADDR_DUC0_P + (self.index << 4)
        self.config.write(addr, pow)
        # self.config.write(addr + 1, )

    @kernel
    def set_duc_phase(self, phase):
        """Set the DUC phase in SI units.

        :param phase: DUC phase in turns
        """
        pow = int32(round(phase*(1 << 16)))
        self.set_duc_phase_mu(pow)


    @kernel
    def set_nco_frequency_mu(self, ftw):
        """Set the NCO frequency.

        This method stages the new NCO frequency, but does not apply it.

        Use of the DAC-NCO requires the DAC mixer and NCO to be enabled. These
        can be configured via the ``dac`` configuration dictionary (see 
        :class:`Phaser`).

        :param ftw: NCO frequency tuning word (32-bit)
        """
        self.phaser.dac_write(0x15 + (self.index << 1), ftw >> 16)
        self.phaser.dac_write(0x14 + (self.index << 1), ftw)

    @kernel
    def set_nco_frequency(self, frequency):
        """Set the NCO frequency in SI units.

        This method stages the new NCO frequency, but does not apply it.

        Use of the DAC-NCO requires the DAC mixer and NCO to be enabled. These
        can be configured via the ``dac`` configuration dictionary (see
        :class:`Phaser`).

        :param frequency: NCO frequency in Hz (passband from -400 MHz
            to 400 MHz, wrapping around at +- 500 MHz)
        """
        ftw = int32(round(frequency*((1 << 30)/(250*MHz))))
        self.set_nco_frequency_mu(ftw)

    @kernel
    def set_nco_phase_mu(self, pow):
        """Set the NCO phase offset.

        By default, the new NCO phase applies on completion of the SPI
        transfer. This also causes a staged NCO frequency to be applied.
        Different triggers for applying NCO settings may be configured through
        the ``syncsel_mixerxx`` fields in the ``dac`` configuration dictionary (see
        :class:`Phaser`).

        Use of the DAC-NCO requires the DAC mixer and NCO to be enabled. These
        can be configured via the ``dac`` configuration dictionary.

        :param pow: NCO phase offset word (16-bit)
        """
        self.phaser.dac_write(0x12 + self.index, pow)

    @kernel
    def set_nco_phase(self, phase):
        """Set the NCO phase in SI units.

        By default, the new NCO phase applies on completion of the SPI
        transfer. This also causes a staged NCO frequency to be applied.
        Different triggers for applying NCO settings may be configured through
        the ``syncsel_mixerxx`` fields in the ``dac`` configuration dictionary (see
        :class:`Phaser`).

        Use of the DAC-NCO requires the DAC mixer and NCO to be enabled. These
        can be configured via the ``dac`` configuration dictionary.

        :param phase: NCO phase in turns
        """
        pow = int32(round(phase*(1 << 16)))
        self.set_nco_phase_mu(pow)

    @kernel
    def set_att_mu(self, data):
        """Set channel attenuation.

        :param data: Attenuator data in machine units (8-bit)
        """
        t_xfer = self.phaser.core.seconds_to_mu((8 + 1)*ATT_SPI_DIV*8*ns)
        # DAC_SPI_CONFIG

        self.phaser.att[self.index].bus.set_config_mu(ATT_SPI_CONFIG, 8, ATT_SPI_DIV, CS_ATT)
        self.phaser.att[self.index].bus.write(data << 24)
        # self.phaser.att[self.index].bus.write(data & 0xFF)
        delay_mu(t_xfer)

    # @kernel
    # def read_spi_att_mu(self):
    #     data = self.phaser.att[self.index].bus.read_write_data()
    #     delay(20*us)
    #     return data
        
        

    @kernel
    def set_att(self, att):
        """Set channel attenuation in SI units.

        :param att: Attenuation in dB
        """
        # 2 lsb are inactive, resulting in 8 LSB per dB
        data = 0xff - int32(round(att*8))
        if data < 0 or data > 0xff:
            raise ValueError("attenuation out of bounds")
        self.set_att_mu(data)

    @kernel
    def get_att_mu(self) -> TInt32:
        """Read current attenuation.

        The current attenuation value is read without side effects.

        :return: Current attenuation in machine units
        """
        t_xfer = self.phaser.core.seconds_to_mu((8 + 1)*ATT_SPI_DIV*8*ns)
        self.phaser.att[self.index].bus.set_config_mu(ATT_SPI_CONFIG | 1 * spi.SPI_INPUT | 0 * spi.SPI_END, 8, ATT_SPI_DIV, CS_ATT)
        self.phaser.att[self.index].bus.write(0)
        # Don't know if it is needed
        delay_mu(t_xfer)
        data = self.phaser.att[self.index].bus.read()

        delay(20*us)  # slack
        self.phaser.att[self.index].bus.set_config_mu(ATT_SPI_CONFIG | 1 * spi.SPI_END, 8, ATT_SPI_DIV, CS_ATT)
        self.phaser.att[self.index].bus.write(data)

        # Don't know if it is needed
        delay_mu(t_xfer)
        return data



    ###### Multiple 8 bit reg
    @kernel
    def trf_write(self, data, readback=False):
        self.phaser.trf[self.index].bus.set_config_mu(TRF_SPI_CONFIG, 32, TRF_SPI_DIV, CS_ATT)
        self.phaser.trf[self.index].bus.write(data)
        delay(20*us)  # slack

    


    # @kernel
    # def trf_write(self, data, readback=False):
    #     """Write 32 bits to quadrature upconverter register.

    #     :param data: Register data (32-bit) containing encoded address
    #     :param readback: Whether to return the read back MISO data
    #     """
    #     div = 34  # 50 ns min period
    #     t_xfer = self.phaser.core.seconds_to_mu((8 + 1)*div*4*ns)
    #     read = 0
    #     end = 0
    #     clk_phase = 0
    #     if readback:
    #         clk_phase = 1
    #     for i in range(4):
    #         if i == 0 or i == 3:
    #             if i == 3:
    #                 end = 1
    #             self.phaser.trf[self.index].set_config_mu(TRF_SPI_CONFIG | clk_phase * spi.SPI_CLK_PHASE, 8, div, CS_ATT)


    #             self.phaser.spi_cfg(select=PHASER_SEL_TRF0 << self.index,
    #                                 div=div, lsb_first=1, clk_phase=clk_phase,
    #                                 end=end)
    #         self.phaser.spi_write(data)
    #         data >>= 8
    #         delay_mu(t_xfer)
    #         if readback:
    #             read >>= 8
    #             read |= self.phaser.spi_read() << 24
    #             delay(20*us)  # slack
    #     return read

    @kernel
    def trf_read(self, addr, cnt_mux_sel=0) -> TInt32:
        """Quadrature upconverter register read.

        :param addr: Register address to read (0 to 7)
        :param cnt_mux_sel: Report VCO counter min or max frequency
        :return: Register data (32-bit)
        """
        # raise NotImplementedError
        self.trf_write(0x80000008 | (addr << 28) | (cnt_mux_sel << 27))
        delay(20*us)  # slack

        # single clk pulse with ~LE to start readback
        self.phaser.trf[self.index].bus.set_config_mu(TRF_SPI_CONFIG, 1, TRF_SPI_DIV, CS_ATT)
        self.phaser.trf[self.index].bus.write(0)

        # Don't know the value yet
        delay((1 + 1)*34*4*ns)


        self.phaser.trf[self.index].bus.set_config_mu(TRF_SPI_CONFIG | spi.SPI_INPUT, 32, TRF_SPI_DIV, CS_ATT)
        self.phaser.trf[self.index].bus.write(0x00000008 | (cnt_mux_sel << 27))

        delay((1 + 1)*34*4*ns)
        return self.phaser.trf[self.index].bus.read()

    @kernel
    def cal_trf_vco(self):
        """Start calibration of the upconverter (hardware variant) VCO.

        TRF outputs should be disabled during VCO calibration.
        """
        self.trf_write(self.trf_mmap[1] | (1 << 31))

    @kernel
    def en_trf_out(self, rf=1, lo=0):
        """Enable the rf/lo outputs of the upconverter (hardware variant).

        :param rf: 1 to enable RF output, 0 to disable
        :param lo: 1 to enable LO output, 0 to disable
        """
        data = self.trf_read(0xc)
        delay(0.1 * ms)
        # set RF and LO output bits
        data = data | (1 << 12) | (1 << 13) | (1 << 14)
        # clear to enable output
        if rf == 1:
            data = data ^ (1 << 14)
        if lo == 1:
            data = data ^ ((1 << 12) | (1 << 13))
        self.trf_write(data)

    ##########
    @kernel
    def set_servo(self, profile=0, enable=0, hold=0):
        """Set the servo configuration.

        :param enable: 1 to enable servo, 0 to disable servo (default). If disabled,
            the servo is bypassed and hold is enforced since the control loop is broken.
        :param hold: 1 to hold the servo IIR filter output constant, 0 for normal operation.
        :param profile: Profile index to select for channel. (0 to 3)
        """
        if (profile < 0) or (profile > 3):
            raise ValueError("invalid profile index")
        addr = PHASER_ADDR_SERVO_CFG0 + 11 * self.index
        # enforce hold if the servo is disabled
        data = (profile << 2) | (((hold | ~enable) & 1) << 1) | (enable & 1)
        self.config.write(addr, data)

    @kernel
    def set_iir_mu(self, profile, b0, b1, a1, offset):
        """Load a servo profile consiting of the three filter coefficients and an output offset.

        Avoid setting the IIR parameters of the currently active profile.

        The recurrence relation is (all data signed and MSB aligned):

        .. math::
            a_0 y_n = a_1 y_{n - 1} + b_0 x_n + b_1 x_{n - 1} + o

        Where:

            * :math:`y_n` and :math:`y_{n-1}` are the current and previous
              filter outputs, clipped to :math:`[0, 1[`.
            * :math:`x_n` and :math:`x_{n-1}` are the current and previous
              filter inputs in :math:`[-1, 1[`.
            * :math:`o` is the offset
            * :math:`a_0` is the normalization factor :math:`2^{14}`
            * :math:`a_1` is the feedback gain
            * :math:`b_0` and :math:`b_1` are the feedforward gains for the two
              delays

        See also :meth:`PhaserChannel.set_iir`.

        :param profile: Profile to set (0 to 3)
        :param b0: b0 filter coefficient (16-bit signed)
        :param b1: b1 filter coefficient (16-bit signed)
        :param a1: a1 filter coefficient (16-bit signed)
        :param offset: Output offset (16-bit signed)
        """
        if (profile < 0) or (profile > 3):
            raise ValueError("invalid profile index")
   
        # 32 byte-sized data registers per channel and 8 (2 bytes * (3 coefficients + 1 offset)) registers per profile
        addr = PHASER_ADDR_SERVO_DATA_BASE + (4 * profile) + (self.index * 16)
        for data in [b0, b1, a1, offset]:
            self.config.write(addr, data)
            addr += 1

    @kernel
    def set_iir(self, profile, kp, ki=0., g=0., x_offset=0., y_offset=0.):
        """Set servo profile IIR coefficients.

        Avoid setting the IIR parameters of the currently active profile.

        Gains are given in units of output full per scale per input full scale.

        .. note:: Due to inherent constraints of the fixed point datatypes and IIR
            filters, the ``x_offset`` (setpoint) resolution depends on the selected
            gains. Low ``ki`` gains will lead to a low ``x_offset`` resolution.

        The transfer function is (up to time discretization and
        coefficient quantization errors):

        .. math::
            H(s) = k_p + \\frac{k_i}{s + \\frac{k_i}{g}}

        Where:
            * :math:`s = \\sigma + i\\omega` is the complex frequency
            * :math:`k_p` is the proportional gain
            * :math:`k_i` is the integrator gain
            * :math:`g` is the integrator gain limit

        :param profile: Profile number (0-3)
        :param kp: Proportional gain. This is usually negative (closed
            loop, positive ADC voltage, positive setpoint). When 0, this
            implements a pure I controller.
        :param ki: Integrator gain (rad/s). Equivalent to the gain at 1 Hz.
            When 0 (the default) this implements a pure P controller.
            Same sign as ``kp``.
        :param g: Integrator gain limit (1). When 0 (the default) the
            integrator gain limit is infinite. Same sign as ``ki``.
        :param x_offset: IIR input offset. Used as the negative
            setpoint when stabilizing to a desired input setpoint. Will
            be converted to an equivalent output offset and added to ``y_offset``.
        :param y_offset: IIR output offset.
        """
        NORM = 1 << SERVO_COEFF_SHIFT
        COEFF_MAX = 1 << SERVO_COEFF_WIDTH - 1
        DATA_MAX = 1 << SERVO_DATA_WIDTH - 1

        kp *= NORM
        if ki == 0.:
            # pure P
            a1 = 0
            b1 = 0
            b0 = int(round(kp))
        else:
            # I or PI
            ki *= NORM*SERVO_T_CYCLE/2.
            if g == 0.:
                c = 1.
                a1 = NORM
            else:
                c = 1./(1. + ki/(g*NORM))
                a1 = int(round((2.*c - 1.)*NORM))
            b0 = int(round(kp + ki*c))
            b1 = int(round(kp + (ki - 2.*kp)*c))
            if b1 == -b0:
                raise ValueError("low integrator gain and/or gain limit")

        if (b0 >= COEFF_MAX or b0 < -COEFF_MAX or
                b1 >= COEFF_MAX or b1 < -COEFF_MAX):
            raise ValueError("high gains")

        forward_gain = (b0 + b1) * (1 << SERVO_DATA_WIDTH - 1 - SERVO_COEFF_SHIFT)
        effective_offset = int(round(DATA_MAX * y_offset + forward_gain * x_offset))

        self.set_iir_mu(profile, b0, b1, a1, effective_offset)





class Config:
    """Phaser configuration registers interface.

    3 types of register
    1. Writable and Readable
    2. Readonly
    3. Strobe



    """
    kernel_invariants = {
        "core", "channel", "target_base", "target_read",
        "target_board_id", "target_cfg", "target_fan_pwm"
    }

    def __init__(self, dmgr, channel, core_device="core"):
        self.core = dmgr.get(core_device)
        self.channel = channel
        self.target_base   = channel << 8
        self.target_read   = 1 << 6
        self.target_board_id = 0 # READONLY
        self.target_cfg = 3
        self.target_fan_pwm = 6 # 8 bit max


        # self.target_gain   = 0 * (1 << 4)
        # self.target_offset = 1 * (1 << 4)
        # self.target_clr    = 1 * (1 << 5)

    @kernel
    def write(self, addr, data):
        rtio_output(self.target_base | addr, data)
        delay(20*us)  # slack

        ###### Maybe adding a calculated delay here is neccesary


        # return 
    @kernel
    def read(self, addr):
        rtio_output(self.target_base | addr | self.target_read, 0)
        delay(20*us)  # slack
        return rtio_input_data(self.channel)

    @kernel
    def get_board_id(self):
        """Return the pre-DAC gain value of a Shuttler Core channel.

        :param channel: The Shuttler Core channel.
        :return: Pre-DAC gain value. See :meth:`set_gain`.
        """
        rtio_output(self.target_base | self.target_board_id |
            self.target_read, 0)
        return rtio_input_data(self.channel)

    @kernel
    def get_fan_pwm(self):
        """
        """
        rtio_output(self.target_base | self.target_fan_pwm |
            self.target_read, 0)
        return rtio_input_data(self.channel)

    @kernel
    def set_fan_pwm(self, duty_cycle):
        """
        """
        rtio_output(self.target_base | self.target_fan_pwm, int(2**8 * duty_cycle))

    @kernel
    def deassert_dac_resetb(self):
        # Set reset pin to HIGH to deassert reset of dac chip
        # rtio_output(self.target_base | self.target_cfg |
        #     self.target_read, 0)
        # cfg = rtio_input_data(self.channel)

        # delay_mu(int64(self.core.ref_multiplier))
        # delay_mu(int64(self.core.ref_multiplier))
        # delay_mu(int64(self.core.ref_multiplier))
        rtio_output(self.target_base | self.target_cfg, 0 | 0b00000010)


    # @kernel
    # def deassert_dac_resetb(self):
    #     # Set reset pin to HIGH to deassert reset of dac chip
    #     # rtio_output(self.target_base | self.target_cfg |
    #     #     self.target_read, 0)
    #     # cfg = rtio_input_data(self.channel)

    #     # delay_mu(int64(self.core.ref_multiplier))
    #     # delay_mu(int64(self.core.ref_multiplier))
    #     # delay_mu(int64(self.core.ref_multiplier))
    #     rtio_output(self.target_base | self.target_cfg, 0 | 0b00000010)
    


    @kernel
    def set_cfg(self, clk_sel=0, dac_resetb=1, dac_sleep=0, dac_txena=1,
                trf0_ps=0, trf1_ps=0, att0_rstn=1, att1_rstn=1):
        """Set the configuration register.

        Each flag is a single bit (0 or 1).

        :param clk_sel: Select the external SMA clock input
        :param dac_resetb: Active low DAC reset pin
        :param dac_sleep: DAC sleep pin
        :param dac_txena: Enable DAC transmission pin
        :param trf0_ps: Quadrature upconverter 0 power save
        :param trf1_ps: Quadrature upconverter 1 power save
        :param att0_rstn: Active low attenuator 0 reset
        :param att1_rstn: Active low attenuator 1 reset
        """
        rtio_output(self.target_base | PHASER_ADDR_CFG,
                    ((clk_sel & 1) << 0) | ((dac_resetb & 1) << 1) |
                    ((dac_sleep & 1) << 2) | ((dac_txena & 1) << 3) |
                    ((trf0_ps & 1) << 4) | ((trf1_ps & 1) << 5) |
                    ((att0_rstn & 1) << 6) | ((att1_rstn & 1) << 7))

    @kernel
    def set_sync_dly(self, dly):
        """Set SYNC delay.

        :param dly: DAC SYNC delay setting (0 to 7)
        """
        if dly < 0 or dly > 7:
            raise ValueError("SYNC delay out of bounds")
        rtio_output(self.target_base | PHASER_ADDR_SYNC_DLY, dly)

    @kernel
    def duc_stb(self):
        """Strobe the DUC configuration register update.

        Transfer staging to active registers.
        This affects both DUC channels.
        """
        self.write(PHASER_ADDR_DUC_STB, 1)

    @kernel
    def duc_stb_high(self):
        """Strobe the DUC configuration register update.

        Transfer staging to active registers.
        This affects both DUC channels.
        """
        self.write(PHASER_ADDR_DUC_STB, 1)
    
    @kernel
    def duc_stb_low(self):
        """Strobe the DUC configuration register update.

        Transfer staging to active registers.
        This affects both DUC channels.
        """
        self.write(PHASER_ADDR_DUC_STB, 1)

    @kernel
    def get_sta(self):
        """Get the status register value.

        Bit flags are:

        * :const:`PHASER_STA_DAC_ALARM`: DAC alarm pin
        * :const:`PHASER_STA_TRF0_LD`: Quadrature upconverter 0 lock detect
        * :const:`PHASER_STA_TRF1_LD`: Quadrature upconverter 1 lock detect
        * :const:`PHASER_STA_TERM0`: ADC channel 0 termination indicator
        * :const:`PHASER_STA_TERM1`: ADC channel 1 termination indicator
        * :const:`PHASER_STA_SPI_IDLE`: SPI machine is idle and data registers can be read/written

        :return: Status register
        """
        return self.read(PHASER_ADDR_STA)




### CLK_PHASE = 0 | CLK_POLARITY = 0 | HALF_DUPLEX = 0 | OFFLINE = 0 

#### For write event, 24 bit = 8 bit Address +  16 bit data
DAC_SPI_CONFIG = (0*spi.SPI_OFFLINE | 1*spi.SPI_END |


                    0*spi.SPI_INPUT | 0*spi.SPI_CS_POLARITY |
                    0*spi.SPI_CLK_POLARITY | 0*spi.SPI_CLK_PHASE |
                    0*spi.SPI_LSB_FIRST | 0*spi.SPI_HALF_DUPLEX)

# SPI clock write and read dividers
DAC_SPI_DIV = 16 # Max: SCLK Frequency = 10 MHz
CS_DAC = 1 << 0


### END = 0
ATT_SPI_CONFIG = (0*spi.SPI_OFFLINE | 1*spi.SPI_END |
                    0*spi.SPI_INPUT | 0*spi.SPI_CS_POLARITY |
                    0*spi.SPI_CLK_POLARITY | 0*spi.SPI_CLK_PHASE |
                    0*spi.SPI_LSB_FIRST | 0*spi.SPI_HALF_DUPLEX)
ATT_SPI_DIV = 68 + 20
CS_ATT = 1 << 0

# Default LSB_FIRST
TRF_SPI_CONFIG = (0*spi.SPI_OFFLINE | 1*spi.SPI_END |
                    0*spi.SPI_INPUT | 0*spi.SPI_CS_POLARITY |
                    0*spi.SPI_CLK_POLARITY | 0*spi.SPI_CLK_PHASE |
                    1*spi.SPI_LSB_FIRST | 0*spi.SPI_HALF_DUPLEX)
TRF_SPI_DIV = 68



class DAC:
    """
    """
    kernel_invariants = {"core", "bus", "channel"}

    def __init__(self, dmgr, spi_device, core_device="core"):
        self.core = dmgr.get(core_device)
        self.bus = dmgr.get(spi_device)
        self.channel = [] # Store PhaserChannel Class


    @kernel
    def init(self):
        # PLACEHOLDER
        """Initialize SPI device.

        Configures the SPI bus to 24 bits, write-only, simultaneous relay
        switches and LED control.
        """

        self.write(0x02, 0x0080)

    @kernel
    def write(self, addr: TInt32, data: TInt32, div=DAC_SPI_DIV):
        """Write to 16-bit register.

        :param addr: Register address.
        :param data: Data to be written.
        """
        self.bus.set_config_mu(
            DAC_SPI_CONFIG, 24, div, CS_DAC)
        self.bus.write(addr << 24 | (data & 0xffff) << 8)

    @kernel
    def read(self, addr: TInt32, div=DAC_SPI_DIV) -> TInt32:
        """Read from 16-bit register.

        :param addr: Register address.
        :return: Read-back register content.
        """
        self.bus.set_config_mu(
            DAC_SPI_CONFIG | spi.SPI_INPUT,
            24, div, CS_DAC)
        self.bus.write((addr | 0x80) << 24)
        return self.bus.read() & 0xffff

    @kernel
    def get_temperature(self) -> TInt32:
        """Read the DAC die temperature.

        :return: DAC temperature in degree Celsius
        """
        return self.read(0x06, div=128) >> 8

    @kernel
    def sync(self):
        """Trigger DAC synchronisation for both output channels.

        The DAC ``sif_sync`` is de-asserted, then asserted. The synchronisation is
        triggered on assertion.

        By default, the fine-mixer (NCO) and QMC are synchronised. This
        includes applying the latest register settings.

        The synchronisation sources may be configured through the ``syncsel_x``
        fields in the ``dac`` configuration dictionary (see :class:`Phaser`).

        .. note:: Synchronising the NCO clears the phase-accumulator.
        """
        config1f = self.read(0x1f)
        delay(.4*ms)
        self.write(0x1f, config1f & ~int32(1 << 1))
        self.write(0x1f, config1f | (1 << 1))

    @kernel
    def set_cmix(self, fs_8_step):
        """Set the DAC coarse mixer frequency for both channels.

        Use of the coarse mixer requires the DAC mixer to be enabled. The mixer
        can be configured via the ``dac`` configuration dictionary (see
        :class:`Phaser`).

        The selected coarse mixer frequency becomes active without explicit
        synchronisation.

        :param fs_8_step: coarse mixer frequency shift in 125 MHz steps. This
            should be an integer between -3 and 4 (inclusive).
        """
        # values recommended in data-sheet
        #         0       1       2       3       4       -3      -2      -1
        vals = [0b0000, 0b1000, 0b0100, 0b1100, 0b0010, 0b1010, 0b0001, 0b1110]
        cmix = vals[fs_8_step%8]
        config0d = self.read(0x0d)
        delay(.1*ms)
        self.write(0x0d, (config0d & ~(0b1111 << 12)) | (cmix << 12))

    @kernel
    def get_alarms(self):
        """Read the DAC alarm flags.

        :return: DAC alarm flags (see datasheet for bit meaning)
        """
        return self.read(0x05)

    @kernel
    def clear_alarms(self):
        """Clear DAC alarm flags."""
        self.write(0x05, 0x0000)

    @kernel
    def iotest(self, pattern) -> TInt32:
        """Performs a DAC IO test according to the datasheet.

        :param pattern: List of four int32s containing the pattern
        :return: Bit error mask (16-bit)
        """
        if len(pattern) != 4:
            raise ValueError("pattern length out of bounds")
        for addr in range(len(pattern)):
            self.write(0x25 + addr, pattern[addr])
            # repeat the pattern twice
            self.write(0x29 + addr, pattern[addr])
        delay(.1*ms)


        #### This need porting

        for ch in range(2):
            channel = self.channel[ch]
            channel.set_duc_cfg(select=1)  # test
            # NEW DELAY
            delay(20*us)

            data = pattern[2*ch] | (pattern[2*ch + 1] << 16)
            channel.set_dac_test(data)
            # NEW DELAY
            delay(20*us)

            if channel.get_dac_data() != data:
                raise ValueError("DAC test data readback failed")
            delay(.1*ms)

        cfg = self.read(0x01)
        delay(.1*ms)
        self.write(0x01, cfg | 0x8000)  # iotest_ena
        self.write(0x04, 0x0000)  # clear iotest_result
        delay(.2*ms)  # let it rip
        # no need to go through the alarm register,
        # just read the error mask
        # self.clear_alarms()
        alarms = self.get_alarms()
        delay(.1*ms)  # slack
        if alarms & 0x0080:  # alarm_from_iotest
            errors = self.read(0x04)
            delay(.1*ms)  # slack
        else:
            errors = 0
        self.write(0x01, cfg)  # clear config
        self.write(0x04, 0x0000)  # clear iotest_result
        return errors

    @kernel
    def tune_fifo_offset(self):
        """Scan through ``fifo_offset`` and configure midpoint setting.

        :return: Optimal ``fifo_offset`` setting with maximum margin to write
            pointer.
        """
        # expect two or three error free offsets:
        #
        # read offset 01234567
        # write pointer  w
        # distance    32101234
        # error free  x     xx
        config9 = self.read(0x09)
        delay(.1*ms)
        good = 0
        for o in range(8):
            # set new fifo_offset
            self.write(0x09, (config9 & 0x1fff) | (o << 13))
            self.clear_alarms()
            delay(.1*ms)   # run
            alarms = self.get_alarms()
            delay(.1*ms)  # slack
            if (alarms >> 11) & 0x7 == 0:  # any fifo alarm
                good |= 1 << o
        # if there are good offsets accross the wrap around
        # offset for computations
        if good & 0x81 == 0x81:
            good = ((good << 4) & 0xf0) | (good >> 4)
            offset = 4
        else:
            offset = 0
        # calculate mean
        sum = 0
        count = 0
        for o in range(8):
            if good & (1 << o):
                sum += o
                count += 1
        if count == 0:
            raise ValueError("no good fifo offset")
        best = ((sum // count) + offset) % 8
        self.write(0x09, (config9 & 0x1fff) | (best << 13))
        return best

class TRF:
    kernel_invariants = {"core", "bus"}

    def __init__(self, dmgr, spi_device, core_device="core"):
        self.core = dmgr.get(core_device)
        self.bus = dmgr.get(spi_device)

class ATT:
    kernel_invariants = {"core", "bus"}

    def __init__(self, dmgr, spi_device, core_device="core"):
        self.core = dmgr.get(core_device)
        self.bus = dmgr.get(spi_device)

    # @kernel
    # def write(self, data: TInt32, div=ATT_SPI_DIV):
    #     """Set channel attenuation.

    #     :param data: Attenuator data in machine units (8-bit)
    #     """
    #     self.bus.set_config_mu(
    #         ATT_SPI_CONFIG, 8, div, CS_ATT)
    #     self.bus.write(data)

    # @kernel
    # def read(self, addr: TInt32, div=ATT_SPI_DIV) -> TInt32:
    #     """Read from 16-bit register.

    #     :param addr: Register address.
    #     :return: Read-back register content.
    #     """
    #     self.bus.set_config_mu(
    #         ATT_SPI_CONFIG | spi.SPI_INPUT,
    #         24, div, CS_ATT)
    #     self.bus.write((addr | 0x80) << 24)
    #     return self.bus.read() & 0xffff

class Phaser:
    kernel_invariants = {"core", "config", "dac"}

    # def __init__(self, dmgr, config, dac, trf0, att0, trf1, att1,
    def __init__(self, dmgr, config, dac, trf0, att0, trf1, att1,
                #FIXME tune_fifo_offset should be True
                miso_delay=1, tune_fifo_offset=False,
                dac_settings=None, trf0_settings=None, trf1_settings=None,
                clk_sel=0, sync_dly=0, gw_rev=PHASER_GW_BASE,
                core_device="core"):
        # No Chennel Base. 

        self.core = dmgr.get(core_device)
        self.config = dmgr.get(config)
        self.dac = dmgr.get(dac)

        # NOT EXISTED IN BASE Variant 
        self.att = [dmgr.get(att0), dmgr.get(att1)]
        self.trf = [dmgr.get(trf0), dmgr.get(trf1)]

        # self.trf0 = dmgr.get(trf0)
        # self.att0 = dmgr.get(att0)
        # self.trf1 = dmgr.get(trf1)
        # self.att1 = dmgr.get(att1)

        # TODO: auto-align miso-delay in phy
        self.miso_delay = miso_delay
        # frame duration in mu (10 words, 8 clock cycles each 4 ns)
        # self.core.seconds_to_mu(10*8*4*ns)  # unfortunately this returns 319
        assert self.core.ref_period == 1*ns
        self.t_frame = 10*8*4
        self.frame_tstamp = int64(0)
        self.clk_sel = clk_sel
        self.tune_fifo_offset = tune_fifo_offset
        self.sync_dly = sync_dly
        self.gw_rev = gw_rev  # verified in init()

        self.dac_mmap = DAC34H84(dac_settings).get_mmap()

        self.channel = [PhaserChannel(self, self.config, ch, trf)
                        for ch, trf in enumerate([trf0_settings, trf1_settings])]
        self.dac.channel = self.channel
        

    @kernel
    def init(self, debug=False):
        """Initialize the board.

        Verifies board and chip presence, resets components, performs
        communication and configuration tests and establishes initial
        conditions.
        """
        board_id = self.config.read(PHASER_ADDR_BOARD_ID)
        if board_id != PHASER_BOARD_ID:
            raise ValueError("invalid board id")
        delay(.1*ms)  # slack

        hw_rev = self.config.read(PHASER_ADDR_HW_REV)
        delay(.1*ms)  # slack
        is_baseband = hw_rev & PHASER_HW_REV_VARIANT

        gw_rev = self.config.read(PHASER_ADDR_GW_REV)
        if debug:
            print("gw_rev:", self.gw_rev)
            self.core.break_realtime()
        assert gw_rev == self.gw_rev
        delay(.1*ms)  # slack


        ### Phaser DRTIO does not use fastlink
        # allow a few errors during startup and alignment since boot
        # if self.get_crc_err() > 20:
        #     raise ValueError("large number of frame CRC errors")
        # delay(.1*ms)  # slack

        # determine the origin for frame-aligned timestamps
        # self.measure_frame_timestamp()
        # if self.frame_tstamp < 0:
        #     raise ValueError("frame timestamp measurement timed out")
        # delay(.1*ms)

        # reset

        self.config.set_cfg(dac_resetb=0, dac_sleep=1, dac_txena=0,
                     trf0_ps=1, trf1_ps=1,
                     att0_rstn=0, att1_rstn=0)
        delay(25*ns)  # Min DAC pulse width

        
        # Not implemented yet
        # self.set_leds(0x00)

        # No fan pwm connection
        # self.set_fan_mu(0)
        
        # bring dac out of reset, keep tx off
        self.config.set_cfg(clk_sel=self.clk_sel, dac_txena=0,
                     trf0_ps=1, trf1_ps=1,
                     att0_rstn=0, att1_rstn=0)
        delay(.1*ms)  # slack

        # crossing dac_clk (reference) edges with sync_dly
        # changes the optimal fifo_offset by 4
        self.config.set_sync_dly(self.sync_dly)
        # NEW DELAY
        delay(20*us)
        

        # 4 wire SPI, sif4_enable
        self.dac.write(0x02, 0x0080)
        ver_number = self.dac.read(0x7f)

        self.core.break_realtime()
        if self.dac.read(0x7f) != 0x5409:
            raise ValueError("DAC version readback invalid")
        delay(.1*ms)
        if self.dac.read(0x00) != 0x049c:
            raise ValueError("DAC config0 reset readback invalid")
        delay(.1*ms)

        t = self.dac.get_temperature()
        delay(.1*ms)
        if t < 10 or t > 90:
            raise ValueError("DAC temperature out of bounds")

        for data in self.dac_mmap:
            self.dac.write(data >> 16, data)
            delay(120*us)
        self.dac.sync()
        delay(40*us)

        # pll_ndivsync_ena disable
        config18 = self.dac.read(0x18)
        delay(.1*ms)
        self.dac.write(0x18, config18 & ~0x0800)





        
        patterns = [
            [0xf05a, 0x05af, 0x5af0, 0xaf05],  # test channel/iq/byte/nibble
            [0x7a7a, 0xb6b6, 0xeaea, 0x4545],  # datasheet pattern a
            [0x1a1a, 0x1616, 0xaaaa, 0xc6c6],  # datasheet pattern b
        ]
        # A data delay of 2*50 ps heuristically and reproducibly matches
        # FPGA+board+DAC skews. There is plenty of margin (>= 250 ps
        # either side) and no need to tune at runtime.
        # Parity provides another level of safety.
        for i in range(len(patterns)):
            delay(.5*ms)
            errors = self.dac.iotest(patterns[i])
            if errors:
                raise ValueError("DAC iotest failure")


        #################### TO BE CONTINUED

        delay(2*ms)  # let it settle
        lvolt = self.dac.read(0x18) & 7
        delay(.1*ms)
        if lvolt < 2 or lvolt > 5:
            raise ValueError("DAC PLL lock failed, check clocking")

        if self.tune_fifo_offset:
            fifo_offset = self.dac.tune_fifo_offset()
            if debug:
                print("fifo_offset:", fifo_offset)
                self.core.break_realtime()

        # self.dac.write(0x20, 0x0000)  # stop fifo sync
        # alarm = self.get_sta() & 1
        # delay(.1*ms)
        self.dac.clear_alarms()
        delay(2*ms)  # let it run a bit
        alarms = self.dac.get_alarms()
        delay(.1*ms)  # slack
        if alarms & ~0x0040:  # ignore PLL alarms (see DS)
            if debug:
                print("alarms:", alarms)
                self.core.break_realtime()
                # ignore alarms
            else:
                raise ValueError("DAC alarm")

        # avoid malformed output for: mixer_ena=1, nco_ena=0 after power up
        self.dac.write(self.dac_mmap[2] >> 16, self.dac_mmap[2] | (1 << 4))
        delay(40*us)
        self.dac.sync()
        delay(100*us)
        self.dac.write(self.dac_mmap[2] >> 16, self.dac_mmap[2])
        delay(40*us)
        self.dac.sync()
        delay(100*us)

        # power up trfs, release att reset
        self.config.set_cfg(clk_sel=self.clk_sel, dac_txena=0)
        # NEW DELAY
        delay(20*us)

        for ch in range(2):
            channel = self.channel[ch]
            # test attenuator write and readback
            channel.set_att_mu(0x5a)
            # channel.set_att_mu(0xFFFFFFFF)

            # test = channel.read_spi_att_mu()
            # print(test)
            # self.core.break_realtime()

            if channel.get_att_mu() != 0x5a:
                raise ValueError("attenuator test failed")
            delay(.1*ms)
            channel.set_att_mu(0x00)  # maximum attenuation

            channel.set_servo(profile=0, enable=0, hold=1)

            if self.gw_rev == PHASER_GW_BASE:
                # test oscillators and DUC
                for i in range(len(channel.oscillator)):
                    oscillator = channel.oscillator[i]
                    asf = 0
                    if i == 0:
                        asf = 0x7fff
                    # 6pi/4 phase
                    oscillator.set_amplitude_phase_mu(asf=asf, pow=0xc000, clr=1)
                    delay(1*us)
                # 3pi/4
                channel.set_duc_phase_mu(0x6000)
                delay(1*us)
                channel.set_duc_cfg(select=0, clr=1)
                delay(1*us)
                self.config.duc_stb()

                # self.config.duc_stb_high()
                # delay(.1*ms)  # settle link, pipeline and impulse response

                # self.config.duc_stb_low()
                # delay(.1*ms)  # settle link, pipeline and impulse response
                data = channel.get_dac_data()
                delay(1*us)
                channel.oscillator[0].set_amplitude_phase_mu(asf=0, pow=0xc000,
                                                            clr=1)
                delay(.1*ms)
                sqrt2 = 0x5a81  # 0x7fff/sqrt(2)
                data_i = data & 0xffff
                data_q = (data >> 16) & 0xffff
                # allow ripple
                if (data_i < sqrt2 - 30 or data_i > sqrt2 or
                        abs(data_i - data_q) > 2):
                    print("ch", ch, "data_i:", data_i, " | data_q:" , data_q, "sqrt2:", sqrt2)
                    raise ValueError("DUC+oscillator phase/amplitude test failed")

            if self.gw_rev == PHASER_GW_MIQRO:
                raise ValueError("MIQRO is not supported")
                # channel.miqro.reset()

            if is_baseband:
                continue

            if channel.trf_read(0) & 0x7f != 0x68:
                raise ValueError("TRF identification failed")
            delay(.1*ms)

            delay(.2*ms)
            for data in channel.trf_mmap:
                channel.trf_write(data)
            channel.cal_trf_vco()

            delay(2*ms)  # lock
            if not (self.config.get_sta() & (PHASER_STA_TRF0_LD << ch)):
                raise ValueError("TRF lock failure")
            delay(.1*ms)
            if channel.trf_read(0) & 0x1000:
                raise ValueError("TRF R_SAT_ERR")
            delay(.1*ms)
            channel.en_trf_out()

        # enable dac tx
        self.config.set_cfg(clk_sel=self.clk_sel)
    