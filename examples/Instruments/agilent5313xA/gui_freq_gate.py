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

    DATA_COLUMNS = ['Iteration', 'Frequency']

    def startup(self):
        log.info("Setting up counter")
        self.meter = Agilent5313xA(VXI11Adapter("10.23.68.217", name="gpib0,26"))
        self.meter.reset()

        # Setup instrument
        self.meter.measure_freq = 1
        self.meter.arming_time(self.gate)

    def execute(self):
        log.info("Starting to log data")

        for i in range(self.iterations):
            self.meter.measure_start()
            data = {
                'Iteration': i,
                'Frequency': self.meter.fetch_frequency
            }
            log.debug("Produced numbers: %s" % data)
            self.emit('results', data)
            self.emit('progress', 100*i/self.iterations)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=TestProcedure,
            inputs=['iterations', 'gate'],
            displays=['iterations', 'gate',],
            x_axis='Iteration',
            y_axis='Frequency'
        )
        self.setWindowTitle('Frequency Logging')

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