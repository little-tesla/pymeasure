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
from pymeasure.instruments.validators import (
    strict_discrete_set,
    truncated_discrete_set,
    truncated_range,
    joined_validators,
    strict_range
)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Channel3(object):
        """The optional channel 3 supports only reading it's impedance,
        which is anyway always 50Ohm. For simplicity this is hardcoded.
        """
        impedance = 50
        
        def __init__(self, instrument, number):
            self.instrument = instrument
            self.number = number

class Channel(object):
        """This is the instrument channel representation class used for
        controlling channel 1 and 2.
        """

        #############
        #  Mappings #
        #############
        IMP_MAPPING = {50: '50', 1e6: '1M', 1000000: '1M'}
        ONOFF_MAPPING = {True: 'ON', False: 'OFF', 1: 'ON', 0: 'OFF'}

        impedance = Instrument.control(
            "IMP?","IMP %sOHM",
            """ A number property that controls the input impedance
            as 50OHM or 1MOHM. This property can be set (50, 1000000).""",
            validator=strict_discrete_set,
            map_values=True,
            values=IMP_MAPPING
        )

        lpfilter = Instrument.control(
            "FILT?","FILT %s",
            """ A bool property that controls the input 100kHz filter.
            This property can be set (True, False).""",
            validator=strict_discrete_set,
            map_values=True,
            values=ONOFF_MAPPING
        )

        coupling = Instrument.control(
            "COUP?","COUP %s",
            """ A string property that controls the input coupling.
            This property can be set (AC, DC).""",
            validator=strict_discrete_set,
            values=["AC", "DC"]
        )

        attenuation = Instrument.control(
            "ATT?","ATT %d",
            """ A number property that controls the input attenuation.
            This property can be set (1, 10).""",
            validator=strict_discrete_set,
            values=[1, 10]
        )
        
        def __init__(self, instrument, number):
            self.instrument = instrument
            self.number = number

        def values(self, command, **kwargs):
            """ Reads a set of values from the instrument through the adapter,
            passing on any key-word arguments.
            """
            return self.instrument.values(":INP%d:%s" % (
                                          self.number, command), **kwargs)
        def ask(self, command):
            self.instrument.ask(":INP%d:%s" % (self.number, command))

        def write(self, command):
            self.instrument.write(":INP%d:%s" % (self.number, command))

        def read(self):
            self.instrument.read()


class Agilent53131A(Instrument):
        """
        Represent the HP/Agilent/Keysight 53131A and related counter.

        Implemented measurements: Frequency
        """

        #############
        #  Mappings #
        #############
        ONOFF = ["ON", "OFF"]
        ONOFF_MAPPING = {True: 'ON', False: 'OFF', 1: 'ON', 0: 'OFF'}

        id = Instrument.measurement(
            "*IDN?", """ Reads the instrument identification """
        )

        options = Instrument.measurement(
            "*OPT?", """ Reads the installed options """
        )

        read_val = Instrument.measurement(":READ?", "Read current measured value.")

        fetch_frequency = Instrument.measurement("FETCH:FREQ?", "Read current frequency.")

        fetch_period = Instrument.measurement("FETCH:PERIOD?", "Read current period.")

        display = Instrument.setting(
            "DISP:ENABLE %s", "Instrument display (ON/OFF)",
            validator=strict_discrete_set,
            map_values=True,
            values=ONOFF_MAPPING
        )

        display_menu_off = Instrument.setting(
            ":DISP:MENU %s", "Clear active menu item. Set to 1 or True to initiate command",
            map_values=True,
            values={True: 'OFF'}
        )

        hcopy_off = Instrument.setting(
            ":HCOPY:CONT %s", "Disable printing operation. Set to 1 or True to initiate command",
            map_values=True,
            values={True: 'OFF'}
        )

        reference = Instrument.setting(
            ":ROSC:SOURCE %s", "Control reference oscillator. Can be set to INT / EXT",
            validator=strict_discrete_set,
            values=["INT", "EXT"]
        )

        reference_autocheck_off = Instrument.setting(
            ":ROSC:EXT:CHECK %s", "Disable check of external reference source. Set to 1 or True to initiate command",
            map_values=True,
            values={True: 'OFF'}
        )

        cal_interpolator_auto = Instrument.setting(
            ":DIAG:CAL:INT:AUTO %s", "Disable automatic interpolater calibration. The most recent calibration values are used in the calculation of frequency. Set to (ON/OFF)",
            validator=strict_discrete_set,
            map_values=True,
            values=ONOFF_MAPPING
        )
        
        def __init__(self, adapter, delay=0.02, **kwargs):
            super(Agilent53131A, self).__init__(
                adapter, "HP/Agilent/Keysight 53131A Counter", **kwargs
            )

            self.ch1 = Channel(self, 1)
            self.ch2 = Channel(self, 2)
            self.ch3 = Channel3(self, 3)

        def reset(self):
            """ Resets the instrument and clears the queue. """
            self.write("*RST;*CLS;*SRE 0;*ESE 0;:STAT:PRES;")

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

        def trigger_set_fetc(self):
            """ Define the Trigger command. This means the command FETC?
            does not need to be sent for every measurement, decreasing the
            number of bytes transferred over the bus  """
            self.write("*DDT #15FETC?")

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
