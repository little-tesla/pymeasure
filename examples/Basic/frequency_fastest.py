"""
This example demonstrates how to make a graphical interface, and uses
a Frequency counter to from which it reads the data.

Run the program by changing to the directory containing this file and calling:

python frequency.py

"""

import sys
import random
import tempfile
from time import sleep
import pyqtgraph as pg

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from pymeasure.instruments.agilent import Agilent53131A
from pymeasure.adapters import VXI11Adapter
from pymeasure.log import console_log
from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter
from pymeasure.experiment import Results
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow


class TestProcedure(Procedure):

    iterations = IntegerParameter('Loop Iterations', default=100)
    delay = FloatParameter('Delay Time', units='s', default=0.2)

    DATA_COLUMNS = ['Iteration', 'Frequency']

    def startup(self):
        log.info("Setting up counter")
        self.meter = Agilent53131A(VXI11Adapter("10.23.68.217", name="gpib0,26"))
        self.meter.reset()

    def execute(self):
        log.info("Starting to log data")

        # Setup instrument
        self.meter.arming_auto()
        self.meter.measure_freq()
        self.meter.trigger_level_set(0)
        self.meter.reference = "INT"
        self.meter.cal_interpolator_auto = False
        self.meter.display = True
        self.meter.hcopy_off = 1
        self.meter.postproc_disable()
        self.meter.trigger_set_fetc()
        self.meter.continous_mode()
        """
        This number must be within 10% of the Ch 1 input frequency.
        Using this greatly increases throughput, but is not
        recommended for signals that change by more than 10%
        """
        temp_f = self.meter.fetch_freq()
        self.meter.freq_exp_set(temp_f)

        for i in range(self.iterations):
            data = {
                'Iteration': i,
                'Frequency': self.meter.fetch_frequency
            }
            log.debug("Produced numbers: %s" % data)
            self.emit('results', data)
            self.emit('progress', 100*i/self.iterations)
            sleep(self.delay)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=TestProcedure,
            inputs=['iterations', 'delay'],
            displays=['iterations', 'delay',],
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