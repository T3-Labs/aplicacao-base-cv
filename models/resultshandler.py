from PyQt5.QtCore import QThread
from PyQt5 import QtCore


class ResultsHandler(QThread):
    
    sendFrame = QtCore.pyqtSignal(object)
    sendValuesToView = QtCore.pyqtSignal(object)
    sendValuesToDataIter = QtCore.pyqtSignal(object)

    def __init__(self, resultsQueue):
        super().__init__()
        self.resultsQueue = resultsQueue
    
    def run(self):
        while not self.isInterruptionRequested():
            frame, obj_count, measurement = self.resultsQueue.cat()
            self.sendFrame.emit(frame)
            self.sendValuesToView.emit([obj_count, measurement])
            data = self.make_payload(obj_count, measurement)
            self.sendValuesToDataIter.emit(data)

    @staticmethod
    def make_payload(objects: int, measurement: float):
        data = dict()
        data["line"] = 1
        data["parts_quantity"] = objects
        data["area_production"] = measurement
        data["line_stops"] = False
        data["stops_quantity"] = []
        return data


    def __del__(self):
        try: 
            self.sendFrame.disconnect()
            self.sendValuesToView.disconnect()
        except Exception as e:
            print(f"Warning: {e}")
            pass

        self.requestInterruption()
        self.wait()
