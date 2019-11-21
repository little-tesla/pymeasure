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
    meter.display_menu_off = 1

    print("Input impedance")
    meter.input_imp_set(1, 0)
    print(meter.input_imp_get(1))
    meter.input_imp_set(1, 50)
    print(meter.input_imp_get(1))

    print("Input filter")
    meter.input_filt_set(1, True)
    print(meter.input_filt_get(1))
    meter.input_filt_set(1, False)
    print(meter.input_filt_get(1))

    print("Input coupling")
    meter.input_coupling_set(1, "DC")
    print(meter.input_coupling_get(1))
    meter.input_coupling_set(1, "AC")
    print(meter.input_coupling_get(1))

    print("Input attenuator")
    meter.input_att_set(1, 10)
    print(meter.input_att_get(1))
    meter.input_att_set(1, 1)
    print(meter.input_att_get(1))

    print("Input combined settings")
    print("1 50 AC")
    meter.input_configure(1, 1, 50, "AC")
    print(meter.input_att_get(1), meter.input_imp_get(1), meter.input_coupling_get(1))
    print("10 50 AC")
    meter.input_configure(1, 10, 50, "AC")
    print(meter.input_att_get(1), meter.input_imp_get(1), meter.input_coupling_get(1))
    print("1 1M AC")
    meter.input_configure(1, 1, 0, "AC")
    print(meter.input_att_get(1), meter.input_imp_get(1), meter.input_coupling_get(1))
    print("1 50 DC")
    meter.input_configure(1, 1, 50, "DC")
    print(meter.input_att_get(1), meter.input_imp_get(1), meter.input_coupling_get(1))
    print("1 50 AC")
    meter.input_configure(1, 1, 50, "AC")
    print(meter.input_att_get(1), meter.input_imp_get(1), meter.input_coupling_get(1))

    print("Format Data")
    meter.format_data("ASCII")

    print("Hcopy disable")
    meter.hcopy_off = 1

    print("Measure Frequency")
    """
    This seto f commands sets up the counter to transfer data at the fastest
    possible rate. Note that the arming mode is AUTO. This mode provides
    the least resolution of all the arming modes.
    """
    meter.arming_auto()
    meter.measure_freq()
    meter.trigger_level_set(0)
    meter.reference = "INT"
    meter.cal_interpolator_auto = False
    meter.display = False
    meter.hcopy_off = 1
    meter.postproc_disable()
    meter.trigger_set_fetc()
    meter.continous_mode()
    """
    This number must be within 10% of the Ch 1 input frequency.
    Using this greatly increases throughput, but is not
    recommended for signals that change by more than 10%
    """
    temp_f = meter.fetch_frequency
    meter.freq_exp_set(temp_f)
    for pos in range(5):
        print("Freq: ", meter.fetch_frequency)


    print("Errors")
    print(meter.check_errors())
