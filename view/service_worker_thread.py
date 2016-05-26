from PyQt4.QtCore import QThread, SIGNAL


class ServiceThread(QThread):
    def __init__(self, function_map):
        QThread.__init__(self)
        self._function_map= function_map

    def __del__(self):
        self.wait()

    def set_reference_path(self, reference_path):
        self._reference_path=reference_path
    def run(self):
        print "Ejecutando Hilo"
        if self._function_map is not None:
            self._process_worker()


    def _process_worker(self):
        for key, values in self._function_map.iteritems():
            if key == "PARSING_DIRECTORY":
                values(self._reference_path)
            else:
                values()
            self.emit(SIGNAL('setTextInVerboseLabel(QString)'), key)
