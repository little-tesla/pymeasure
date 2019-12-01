"""
This example demonstrates how to make a simple command line interface, and uses
a random number generator to simulate data so that it does not require
an instrument to use.

Run the program by changing to the directory containing this file and calling:

python script.py

"""

import random
import tempfile
from time import sleep

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from pymeasure.instruments.agilent import Agilent53131A
from pymeasure.adapters import VXI11Adapter

import binascii


if __name__ == "__main__":

    log.info("Setting up counter")
    meter = Agilent53131A(VXI11Adapter("10.23.68.217", name="gpib0,26"))

    print(meter.id)
    print(meter.options)
    print(binascii.hexlify(bytearray(meter.cal_read())))
    # b'233235360000080000000800000006c8000006cf000008420000083100000a060000093b00000674000005e700000663000006e1000007f70001326c0a'

    meter.reset()
    print("Display Off/On")
    meter.display_control = False
    sleep(1)
    meter.display_control = True
    sleep(1)

    print("Menu off")
    meter.display_menu_off = True

    print("Input impedance")
    meter.ch1.impedance = 1e6
    print(meter.ch1.impedance)
    sleep(0.5)
    meter.ch1.impedance = 50
    print(meter.ch1.impedance)

    print("Input filter")
    meter.ch1.lpfilter = True
    print(meter.ch1.lpfilter)
    sleep(0.5)
    meter.ch1.lpfilter = False
    print(meter.ch1.lpfilter)

    print("Input filter freq")
    print(meter.ch1.lpfilter_freq)

    print("Input coupling")
    meter.ch1.coupling = "DC"
    print(meter.ch1.coupling)
    sleep(0.5)
    meter.ch1.coupling = "AC"
    print(meter.ch1.coupling)

    print("Input attenuator")
    meter.ch1.attenuation = 10
    print(meter.ch1.attenuation)
    sleep(0.5)
    meter.ch1.attenuation = 1
    print(meter.ch1.attenuation)

    print("Format Data")
    meter.format = "ASCII"

    print("Hcopy disable")
    meter.hcopy = False

    if 0:
        print("Measure Frequency fastest")
        """
        This set of commands sets up the counter to transfer data at the fastest
        possible rate. Note that the arming mode is AUTO. This mode provides
        the least resolution of all the arming modes.
        """
        meter.reset()
        meter.arming_auto()
        meter.measure_freq = 1
        meter.trigger_level_set(0)
        meter.reference = "INT"
        meter.cal_interpolator_auto = False
        meter.display = False
        meter.hcopy = False
        meter.postproc_disable()
        meter.trigger_set_fetc()
        meter.cont_measurements = True
        """
        This number must be within 10% of the Ch 1 input frequency.
        Using this greatly increases throughput, but is not
        recommended for signals that change by more than 10%
        """
        temp_f = meter.fetch_frequency
        meter.freq_exp_set(temp_f)
        for pos in range(5):
            print("Freq: ", meter.fetch_frequency)

    print("Measure Frequency gated")
    """
    This set of commands sets up the counter to make freqeuncy measurements
    on channel 1, using a 1 second gate time.
    """
    meter.reset()
    meter.measure_freq = 1
    meter.arming_time(0.5)

    for pos in range(5):
        meter.measure_start()
        print("Freq: ", meter.fetch_frequency)

    print("Errors")
    print(meter.check_errors())
