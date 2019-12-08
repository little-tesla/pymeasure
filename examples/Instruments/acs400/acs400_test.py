"""
This example demonstrates how to use the HBS ACS400 with the Ethernet
option. This should work as well with the Serial or GPIB option.

Run the program by changing to the directory containing this file and calling:

python3 acs400_test.py

"""

import random
import tempfile
from time import sleep

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from pymeasure.instruments.hbs import ACS400
from pymeasure.adapters import TelnetAdapter

import binascii


if __name__ == "__main__":

    log.info("Setting up source")
    source = ACS400(TelnetAdapter("10.23.68.217", 6000))

    print(source.id)
    #print(source.options)

    print("Errors")
    print(source.check_errors())
