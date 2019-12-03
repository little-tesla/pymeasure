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

class Agilent34401A(Instrument):
    """
    Represent the HP/Agilent/Keysight 34401A and related multimeters.

    Implemented measurements: voltage_dc, voltage_ac, current_dc, current_ac, resistance, resistance_4w
    """

    #############
    #  Mappings #
    #############
    ONOFF = ["ON", "OFF"]
    ONOFF_MAPPING = {True: 'ON', False: 'OFF', 1: 'ON', 0: 'OFF'}

    ##################
    #  Configuration #
    ##################
    
    display = Instrument.setting(
        "DISP:ENABLE %s", "Instrument display (ON/OFF)",
        validator=strict_discrete_set,
        map_values=True,
        values=ONOFF_MAPPING
    )

    id = Instrument.measurement(
        "*IDN?", """ Reads the instrument identification """
    )
    
    #only the most simple functions are implemented
    voltage_dc = Instrument.measurement("MEAS:VOLT:DC? DEF,DEF", "DC voltage, in Volts")
    
    voltage_ac = Instrument.measurement("MEAS:VOLT:AC? DEF,DEF", "AC voltage, in Volts")
    
    current_dc = Instrument.measurement("MEAS:CURR:DC? DEF,DEF", "DC current, in Amps")
    
    current_ac = Instrument.measurement("MEAS:CURR:AC? DEF,DEF", "AC current, in Amps")
    
    resistance = Instrument.measurement("MEAS:RES? DEF,DEF", "Resistance, in Ohms")
    
    resistance_4w = Instrument.measurement("MEAS:FRES? DEF,DEF", "Four-wires (remote sensing) resistance, in Ohms")
    
    def __init__(self, adapter, delay=0.02, **kwargs):
        super(Agilent34401A, self).__init__(
            adapter, "HP/Agilent/Keysight 34401A Multimeter", **kwargs
        )

    def display_text(self, text):
        """ Write string on display """
        self.write("DISP:TEXT '%s'" % text)

    def display_textClear(self):
        """ Clear sting from display """
        self.write("DISP:TEXT:CLE")
