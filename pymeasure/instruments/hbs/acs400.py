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
    strict_discrete_set
)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class ACS400(Instrument):
    """ Represents the HBS Electronik GmbH ACS400 power source.
    """
    
    #############
    #  Mappings #
    #############
    ONOFF = ["ON", "OFF"]
    ONOFF_MAPPING = {True: 'ON', False: 'OFF', 1: 'ON', 0: 'OFF'}

    ##################
    #  Configuration #
    ##################

    id = Instrument.measurement(
        "*IDN?", """ Reads the instrument identification """
    )

    voltage_dc = Instrument.measurement("MEAS:VOLT:DC? DEF,DEF", "DC voltage, in Volts")
    
    voltage_ac = Instrument.measurement("MEAS:VOLT:AC? DEF,DEF", "AC voltage, in Volts")
    
    current_dc = Instrument.measurement("MEAS:CURR:DC? DEF,DEF", "DC current, in Amps")
    
    current_ac = Instrument.measurement("MEAS:CURR:AC? DEF,DEF", "AC current, in Amps")
    
    resistance = Instrument.measurement("MEAS:RES? DEF,DEF", "Resistance, in Ohms")
    
    resistance_4w = Instrument.measurement("MEAS:FRES? DEF,DEF", "Four-wires (remote sensing) resistance, in Ohms")

    def __init__(self, resourceName, **kwargs):
        super(ACS400, self).__init__(
            resourceName,
            "HBS ACS400",
            **kwargs
        )

    def display_text(self, text):
        """ Write string on display """
        self.write("DISP:TEXT '%s'" % text)

    def display_text_clear(self):
        """ Clear string from display """
        self.write("DISP:TEXT:CLE")

    def reset(self):
        """ Resets the instrument and clears the queue. """
        self.write("*RST;*CLS;*SRE 0;*ESE 0;:STAT:PRES;")

    def check_errors(self):
        """ Read all errors from the instrument. """

        errors = []
        while True:
            err = self.values("SYST:ERR?")
            if int(err[0]) != 0:
                errmsg = "Agilent 34401A: {0}: {1}".format(err[0], err[1])
                log.error(errmsg + '\n')
                errors.append(errmsg)
            else:
                break

        return errors

