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

class HP66312A(Instrument):
    """ Represents the HP 66312A instrument.
    """

    id = Instrument.measurement(
        "*IDN?", """ Reads the instrument identification """
    )

    meas_voltage_dc = Instrument.measurement("MEAS:VOLT?", "DC voltage, in Volts")
    meas_voltage_high = Instrument.measurement("MEAS:VOLT:HIGH?", "DC voltage high, in Volts")
    meas_voltage_low = Instrument.measurement("MEAS:VOLT:LOW?", "DC voltage low, in Volts")
    meas_voltage_max = Instrument.measurement("MEAS:VOLT:MAX?", "DC voltage max, in Volts")
    meas_voltage_min = Instrument.measurement("MEAS:VOLT:MIN?", "DC voltage min, in Volts")
    
    meas_voltage_acdc = Instrument.measurement("MEAS:VOLT:ACDC?", "DC+ACrms voltage, in Volts")
    
    meas_current_dc = Instrument.measurement("MEAS:CURR?", "DC current, in Amps")
    meas_current_high = Instrument.measurement("MEAS:CURR:HIGH?", "DC current, in Amps")
    meas_current_low = Instrument.measurement("MEAS:CURR:LOW?", "DC current, in Amps")
    meas_current_max = Instrument.measurement("MEAS:CURR:MAX?", "DC current, in Amps")
    meas_current_min = Instrument.measurement("MEAS:CURR:MIN?", "DC current, in Amps")
    
    meas_current_acdc = Instrument.measurement("MEAS:CURR:ACDC?", "DC+ACrms current, in Amps")

    output = Instrument.control(
        "OUTP?","OUTP %d",
        """ Instrument output.
        This property can be set (True, False).""",
        validator=strict_discrete_set,
        cast=bool,
        values=[True, False]
    )

    sour_voltage = Instrument.control(
        "SOUR:VOLT?","SOUR:VOLT %e",
        """ A floating point property that controls the output voltage
        in V. This property can be set.""",
        validator=strict_range,
        values=[0.0, 20.475]
    )

    sour_current = Instrument.control(
        "SOUR:CURR?","SOUR:CURR %e",
        """ A floating point property that controls the output current
        in A. This property can be set.""",
        validator=strict_range,
        values=[0.0, 2.0475]
    )

    def __init__(self, resourceName, **kwargs):
        super(HP66312A, self).__init__(
            resourceName,
            "HP 66312A",
            **kwargs
        )

    def reset(self):
        """ Resets the instrument and clears the queue. """
        self.write("*RST;*CLS;*SRE 0;*ESE 0;:STAT:PRES;")

    def check_errors(self):
        """ Read all errors from the instrument. """

        errors = []
        while True:
            err = self.values("SYST:ERR?")
            if int(err[0]) != 0:
                errmsg = "HP 66312A: {0}: {1}".format(err[0], err[1])
                log.error(errmsg + '\n')
                errors.append(errmsg)
            else:
                break

        return errors

