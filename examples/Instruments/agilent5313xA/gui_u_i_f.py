"""
This example demonstrates how to make a graphical interface by using
the Agilent 5313xA Frequency counter from which it reads the frequency
with configurable gate time which defines the resolution.
It uses a VXI11Adapter for communication.

Run the program by changing to the directory containing this file and calling:

python3 gui_freq_gate.py

"""

import sys
import random
import tempfile
from time import sleep
import pyqtgraph as pg

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from pymeasure.instruments.hp import HP66312A
from pymeasure.instruments.agilent import Agilent34401A
from pymeasure.instruments.agilent import Agilent5313xA
from pymeasure.adapters import VXI11Adapter
from pymeasure.log import console_log
from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter
from pymeasure.experiment import Results
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow


class TestProcedure(Procedure):

    iterations = IntegerParameter('Loop Iterations', default=100)
    gate = FloatParameter('Gate Time', units='s', default=0.2)
    source_voltage = FloatParameter('Source Voltage', units='V', default=0.0)
    source_current = FloatParameter('Source Current', units='A', default=0.0)

    DATA_COLUMNS = ['Iteration', 'Frequency', 'Usour', 'Isour', 'Umeas']

    def startup(self):
        log.info("Setting up instruments")
        self.fmeter = Agilent5313xA(VXI11Adapter("10.23.68.217", name="gpib0,26"))
        self.fmeter.reset()
        self.Umeter = Agilent34401A(VXI11Adapter("10.23.68.217", name="gpib0,22"))
        self.Umeter.reset()
        self.source = HP66312A(VXI11Adapter("10.23.68.217", name="gpib0,4"))
        self.source.reset()

        # Setup instruments
        self.fmeter.measure_freq = 1
        self.fmeter.arming_time(self.gate)

        self.source.sour_voltage = self.source_voltage
        self.source.sour_current = self.source_current
        self.source.output = True

    def execute(self):
        log.info("Starting to log data")

        for i in range(self.iterations):
            self.fmeter.measure_start()
            data = {
                'Iteration': i,
                'Frequency': self.fmeter.fetch_frequency,
                'Usour': self.source.meas_voltage_dc,
                'Isour': self.source.meas_current_dc,
                'Umeas': self.Umeter.voltage_dc
            }
            log.debug("Produced numbers: %s" % data)
            self.emit('results', data)
            self.emit('progress', 100*i/self.iterations)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        self.source.output = False
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=TestProcedure,
            inputs=['iterations', 'gate', 'source_voltage', 'source_current'],
            displays=['iterations', 'gate', 'source_voltage', 'source_current',],
            x_axis='Iteration',
            y_axis='Frequency'
        )
        self.setWindowTitle('OCXO Test Bench')

    def queue(self):
        filename = tempfile.mktemp()

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())