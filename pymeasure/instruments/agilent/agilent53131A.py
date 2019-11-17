#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2019 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from pymeasure.instruments import Instrument


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Agilent53131A(Instrument):
    """
    Represent the HP/Agilent/Keysight 53131A and related counter.

    Implemented measurements: Frequency
    """

    id = Instrument.measurement(
        "*IDN?", """ Reads the instrument identification """
    )

    opt = Instrument.measurement(
        "*OPT?", """ Reads the installed options """
    )

    read = Instrument.measurement(":READ?", "Frequency, in Hertz")
    
    def __init__(self, adapter, delay=0.02, **kwargs):
        super(Agilent53131A, self).__init__(
            adapter, "HP/Agilent/Keysight 53131A Counter", **kwargs
        )

    def reset(self):
        """ Resets the instrument state. """
        self.write("*RST;*CLS;*SRE 0;*ESE 0;:STAT:PRES;")

    def disp_control(self, enable):
        """ Enable or disable diplay. """
        if enable:
            flag = "ON"
        else:
            flag = "OFF"
        self.write("DISP:ENABLE {0}".format(flag))

    def disp_menu_off(self):
        """ Clear active menu items. """
        self.write(":DISP:MENU OFF")

    def measure_freq_simple(self, freq, resolution, channel):
        """ Configure measure frequency on channel. NOT TESTED"""
        if 0 < channel <= 3:
            self.write(":MEASURE:FREQ? {0}Hz {1}, (@{2})".format(freq, resolution, channel))

    def configure_freq(self, channel):
        """ Configure measure frequency on channel. NOT TESTED"""
        if 0 < channel <= 3:
            self.write(":CONF:FREQ (@{0})".format(channel))

    def measure_freq(self, channel):
        """ Measure frequency on channel. NOT TESTED"""
        if 0 < channel <= 3:
            self.write("FREQ {0}".format(channel))

    def freq_exp_set(self, frequency):
        """ Set expected frequency. NOT TESTED"""
        self.write(":FREQ:EXP1 {0}".format(frequency))

    def measure_t_interval(self):
        """ Time Interval from CH1 to CH2. NOT TESTED"""
        self.write("MEAS:TINT? (@1),(@2)")

    def measure_freq(self):
        """ Measure frequency. NOT TESTED"""
        self.write(":FUNC 'FREQ 1'")

    def arming_auto(self):
        """ Enable the time arming mode. NOT TESTED"""
        self.write(":FREQ:ARM:STAR:SOUR IMM")
        self.write(":FREQ:ARM:STOP:SOUR TIM")

    def arming_time(self, time):
        """ Enable the time arming mode. NOT TESTED"""
        self.write(":FREQ:ARM:STAR:SOUR IMM")
        self.write(":FREQ:ARM:STOP:SOUR TIM")
        self.write((":FREQ:ARM:STOP:TIM %.1f" % time).lstrip('0'))

    def continous_mode(self):
        """ Put counter in run mode."""
        self.write(":INIT:CONT ON")

    def postproc_disable(self):
        """ Disable all post processing. """
        self.write(":CALC:MATH:STATE OFF")
        self.write(":CALC2:LIM:STATE OFF")
        self.write(":CALC3:AVER:STATE OFF")

    def hcopy_disable(self):
        """ Disable printing operation. """
        self.write(":HCOPY:CONT OFF")

    def format_data(self, dtype = "ASCII"):
        """ Set data format. """
        self.write(":FORMAT {0}".format(dtype))

    def cal_read(self):
        """ Ask for calibration data. Returned data is binary. """
        self.write(":CAL:DATA?")
        return self.adapter.read_raw()

    def cal_write(self, data):
        """ Write calibration data. Input data is binary. NOT TESTED"""
        self.adapter.write_raw(":CAL:DATA ".encode('utf-8') + data)

    def trigger_level_set(self, level):
        """ Set trigger level. NOT TESTED"""
        self.write((":EVENT1:LEVEL %.2f" % level).lstrip('0'))

    def measure_start(self):
        """ Start measurement. NOT TESTED"""
        self.write("INIT")

    def osc_set(self, source="INT"):
        """ Set reference oscillator.
            INT or EXT"""
        if source != "INT":
            source = "EXT"

        self.write(":ROSC:SOURCE {0}".format(source))

    def osc_external_no_check(self):
        """ Disable check of external osciallator source. """
        self.write(":ROSC:EXT:CHECK OFF")

    def calib_interpolator_auto(self, state):
        """ Disable automatic interpolater calibration.
        The most recent calibration values are used in the
        calculation of frequency """
        if state:
            status = "ON"
        else:
            status = "OFF"
        self.write(":DIAG:CAL:INT:AUTO {0}".format(status))

    def trigger_set_fetc(self):
        """ Define the Trigger command. This means the command FETC?
        does not need to be sent for every measurement, decreasing the
        number of bytes transferred over the bus  """
        self.write("*DDT #15FETC?")

    def fetch_freq(self):
        """ Read frequency measurement. """
        return self.ask("FETCH:FREQ?")

    def fetch_period(self):
        """ Read period measurement. NOT TESTED"""
        return self.ask("FETCH:PERIOD?")

    def input_imp_set(self, channel, impedance):
        """ Set input impedance 50OHM or 1MOHM. """
        if impedance == 50:
            imp = "50OHM"
        else:
            imp = "1MOHM"
        
        if 0 < channel <= 2:
            self.write(":INP{0}:IMP {1}".format(channel, imp))

    def input_imp_get(self, channel):
        """ Get input impedance 50OHM or 1MOHM. """
        if 0 < channel <= 3:
            return self.ask(":INP{0}:IMP?".format(channel))

    def input_filt_set(self, channel, enable):
        """ Set input filter LP 100kHz (on/off). """
        if enable:
            flag = "ON"
        else:
            flag = "OFF"

        if 0 < channel <= 2:
            self.write(":INP{0}:FILT {1}".format(channel, flag))

    def input_filt_get(self, channel):
        """ Get input filter state. """
        if 0 < channel <= 2:
            return self.ask(":INP{0}:FILT?".format(channel))

    def input_coupling_set(self, channel, coupling = "AC"):
        """ Set input coupling AC / DC. """
        if coupling != "DC":
            coupling = "AC"

        if 0 < channel <= 2:
            self.write(":INP{0}:COUP {1}".format(channel, coupling))

    def input_coupling_get(self, channel):
        """ Get input coupling. """
        if 0 < channel <= 2:
            return self.ask(":INP{0}:COUP?".format(channel))

    def input_att_set(self, channel, attenuation):
        """ Set input attenuation 1 or 10. """
        if attenuation != 10:
            attenuation = 1
        
        if 0 < channel <= 2:
            self.write(":INP{0}:ATT {1}".format(channel, attenuation))

    def input_att_get(self, channel):
        """ Get input attenuation. """
        if 0 < channel <= 2:
            return self.ask(":INP{0}:ATT?".format(channel))

    def input_configure(self, channel, attenuation, impedance = 50, coupling="AC"):
        """ Configure input. 
            Attenuation 1 or 10
            Impedance 50 or 1000000 OHM
            Coupling AC or DC """
        
        self.input_att_set(channel, attenuation)
        self.input_coupling_set(channel, coupling)
        self.input_imp_set(channel, impedance)

    def check_errors(self):
        """ Read all errors from the instrument. """

        errors = []
        while True:
            err = self.values("SYST:ERR?")
            if int(err[0]) != 0:
                errmsg = "Agilent 53131A: {0}: {1}".format(err[0], err[1])
                log.error(errmsg + '\n')
                errors.append(errmsg)
            else:
                break

        return errors
