"""
This example demonstrates how to use the Agilent 5313xA with a VXI11Adapter.
It performs multiple configurations on Channel 1 and finally it reads the
frequency and prints it out. THerefore it requires that a singal source is 
connected to to Channel 1 as well.

Run the program by changing to the directory containing this file and calling:

python3 5313xA_test.py

"""

import random
import tempfile
from time import sleep

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from pymeasure.instruments.hp import HP66312A
from pymeasure.adapters import VXI11Adapter

import binascii


if __name__ == "__main__":

    log.info("Setting up counter")
    meter = HP66312A(VXI11Adapter("10.23.68.217", name="gpib0,4"))

    print(meter.id)
    meter.reset()

    log.info("Test Source")

    print("Set 5V")
    meter.sour_voltage = 5.0
    sleep(0.5)
    print(meter.sour_voltage)

    print("Set 0.5A")
    meter.sour_current = 0.5
    sleep(0.5)
    print(meter.sour_current)

    print("Output On/Off")
    meter.output = True
    sleep(0.5)
    print(meter.output)
    meter.output = False
    print(meter.output)
    sleep(0.5)
    meter.output = True

    print("Measure Current / Voltage")
    """
    Try different mesurements.
    """

    for pos in range(5):
        print("Udc: ", meter.meas_voltage_dc)
        print("Idc: ", meter.meas_current_dc)
        sleep(0.2)

    print("Errors")
    print(meter.check_errors())
